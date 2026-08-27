# Librairies :

import geopandas as gpd
import numpy as np
import fiona
import os
from osgeo import gdal
import rasterio
from rasterio.transform import from_origin
from rasterio.mask import mask
import tempfile
from scipy.spatial import cKDTree

# Données :

gpkg_points = r"C:\PANALESIS\Rot_plates\grille_rect.gpkg"
gpkg_plates = r"C:\PANALESIS\Rot_plates\Outputs\PlatesxxxpreRotyyy_geom_valid_harmo.gpkg"
age_gap = 20000000  # Age gap entre les deux reconstructions successives en an 
layer_plates = "Plates600preRot580" # Reconstruction traitée 
output_folder = r"C:\PANALESIS\Rot_plates\Cartes_outputs\Plates600preRot580\pts"
output_folder_raster = r"C:\PANALESIS\Rot_plates\Cartes_outputs\Plates600preRot580\raster"
output_folder_raster_clip = r"C:\PANALESIS\Rot_plates\Cartes_outputs\Plates600preRot580\rasterclip"

# Lecture :

points = gpd.read_file(gpkg_points)
plates = gpd.read_file(gpkg_plates, layer=layer_plates)

#Liste des noms des plaques pour la reconstructions :

plate_names = plates["PlateName"]
print(len(plate_names), "Noms de plaques trouvés")

# Boucle sur les différentes plaques de la reconstruction :

for idx, row in plates.iterrows() :
    plate_name = row["PlateName"]
    # Extraire les paramètres de rotation
    eu_long = row["EuLong"]
    eu_lat = row["EuLat"]
    eu_ang = row["EuAng"]
    geom= row.geometry
    print("traitement de la plaque : ", plate_name)
    
    # Application du Buffer
    buffer = geom.buffer(3)
    pts_selectionnes= points[points.within(buffer)]
    gdf= pts_selectionnes
    
    # Transformation des coordonnées du pôle Euler en radians :

    lon = np.radians(gdf.geometry.x)
    lat = np.radians(gdf.geometry.y)

    # Transformation en coordonnées carthésiennes : 
    
    Xcart = np.cos(lon) * np.cos(lat)
    Ycart = np.sin(lon) * np.cos(lat)
    Zcart = np.sin(lat)
    gdf["Xcart"] = Xcart
    gdf["Ycart"] = Ycart
    gdf["Zcart"] = Zcart
          
    # Extraire l'axe de rotation (EuLong et EuLat) et l'angle de rotation (EuAng) :
    
    print("EuLong :", eu_long)
    print("EuLat : ", eu_lat)
    print("EuAng :", eu_ang)
    
    # Axe de rotation longitude et latitude en radians :

    eu_long_rad = np.radians(eu_long)
    eu_lat_rad = np.radians(eu_lat)
    
    # Calcul axe x , axe y et axe z :

    axeX = np.cos(eu_long_rad) * np.cos(eu_lat_rad)
    axeY = np.sin(eu_long_rad) * np.cos(eu_lat_rad)
    axeZ = np.sin(eu_lat_rad)
    gdf["axeX"] = axeX
    gdf["axeY"] = axeY
    gdf["axeZ"] = axeZ
    
    # checker que les formules produisent bien un vecteur de norme 1, car si les equations sont justes, l'axe de rotation devrait être un vecteur unitaire
    
    print("vecteur norme 1:",np.sqrt(axeX**2 + axeY**2 + axeZ**2))
    
    # Calcul points x,y,z pivotés :

    omega = np.radians(eu_ang)
    print("angle Euler radians", omega) # angle d'euler en radians 

    XpivCart= ((np.cos(omega)+(1-np.cos(omega))*(axeX*axeX))*Xcart)+(((1-np.cos(omega))*axeX*axeY-axeZ*np.sin(omega))*Ycart)+(((1-np.cos(omega))*axeX*axeZ+axeY*np.sin(omega))*Zcart) 
    YpivCart = (((1-np.cos(omega))*axeX*axeY+axeZ*np.sin(omega))*Xcart)+((np.cos(omega)+(1-np.cos(omega))*(axeY*axeY))*Ycart)+(((1-np.cos(omega))*axeY*axeZ-axeX*np.sin(omega))*Zcart)        
    ZpivCart = (((1-np.cos(omega))*axeX*axeZ-axeY*np.sin(omega))*Xcart)+(((1-np.cos(omega))*axeY*axeZ+axeX*np.sin(omega))*Ycart)+((np.cos(omega)+(1-np.cos(omega))*(axeZ*axeZ))*Zcart)
    gdf["XpivCart"]= XpivCart
    gdf["YpivCart"]= YpivCart
    gdf["ZpivCart"]= ZpivCart
    
    # Différence position initiale et pivotée (vecteur deplacement):

    deltaX = XpivCart-Xcart
    deltaY = YpivCart-Ycart
    deltaZ = ZpivCart-Zcart

    gdf["deltaX"] = deltaX
    gdf["deltaY"] = deltaY
    gdf["deltaZ"] = deltaZ

    # Norme du vecteur deplacement :

    vect_dep_norm = np.sqrt((deltaX**2)+(deltaY**2)+(deltaZ**2))
    gdf["vect_dep_norm"] = np.sqrt((deltaX**2)+(deltaY**2)+(deltaZ**2))
    
    # Calcul distance de deplacement :

    R= 6371000.69 #rayon Terre Excel(moyenne)
    distance_m = 2*R*np.arcsin(vect_dep_norm/2)
    distance_cm = distance_m*100
    gdf["distance_dep_m"] = distance_m
    gdf["distance_dep_cm"] = distance_cm

    #Calcul vitesse de deplacement :

    t = age_gap
    gdf["vitesse_cm_an"] = distance_cm/t
    
    # Création du fichier résultant :
    
    plate_folder = os.path.join(output_folder, f"{plate_name}") # Création d'un fichier pour chaque plaque 
    os.makedirs(plate_folder, exist_ok=True)
    output= os.path.join(plate_folder, f"points_buffer_{plate_name}_{idx}.gpkg")
    
    # Export des points selectionnes dans le buffer :
    
    gdf.to_file(output, driver ="GPKG")
    print("export pts selectionnes done")
    
    # Création du raster :
    
    # Pour grid rectangulaire de 2.5 et reso raster 0.1 : 
    
    reso = 0.1

    # limites du raster:
    
    xmin = gdf["X"].min()
    xmax = gdf["X"].max()

    ymin = gdf["Y"].min()
    ymax = gdf["Y"].max()

    # nombre de colonnes et de lignes : 
    
    cols = int(round((xmax - xmin) / reso)) + 1
    rows = int(round((ymax - ymin) / reso)) + 1
    
    # Création des coordonnées du centre de chaque pixel :
    
    x_coords = xmin + np.arange(cols) * reso
    y_coords = ymax - np.arange(rows) * reso

    # Création d'une grille 2D contenant les coordonnées :
    
    xx, yy = np.meshgrid(x_coords, y_coords)
    
    # Transformation de la grille raster en liste de coordonnées :
    
    raster_points = np.column_stack([xx.ravel(),yy.ravel()])
    
    # Coordonnées des points pour lesquels la vitesse a été calculée :
    
    points_coords = np.column_stack([gdf["X"].values,gdf["Y"].values])
    
    # Création de l'arbre spatial pour appliquer la méthode nearest neighbor :
    tree = cKDTree(points_coords)
    
    # Recherche du point le plus proche pour chaque pixel :
    distances, indices = tree.query(raster_points)

    # Extraction de la vitesse associée au point le plus proche :
    vitesses = gdf["vitesse_cm_an"].values[indices]

    # Transformation en tableau raster :
    raster = vitesses.reshape(rows, cols).astype(np.float32)
        
    # GeoTIFF :
    transform = from_origin(xmin,ymax,reso,reso) #pour georéférencer l e raster
    
    #Export raster :
    #nom du fichier de sortie :
    output= os.path.join(output_folder_raster, f"raster_buff_{plate_name}_{idx}.tif")
    
    with rasterio.open(output,"w",driver="GTiff",height=rows,width=cols,count=1,dtype="float32",crs=gdf.crs,transform=transform,nodata=-9999) as dst:

        dst.write(raster, 1)
    
    print("Raster créé")
    
    # Clip du raster selon le contour de la plaque :
    
    plate_gdf = gpd.GeoDataFrame({"PlateName": [plate_name]}, geometry=[geom],crs=plates.crs)
    
    #création d'un fichier temporaire pour la cutline GDAL :
    
    plate_path = os.path.join(output_folder_raster_clip, f"temp_{plate_name}_{idx}.gpkg")
    plate_gdf.to_file(plate_path, layer="multipolygon", driver="GPKG")
    
    # Chemin pour le raster clipé :
    output_clip =  os.path.join(output_folder_raster_clip,f"raster_clip_{plate_name}_{idx}.tif")
    
    # Clip avec GDAL :
    
    gdal.Warp(output_clip,output,cutlineDSName=plate_path,cutlineLayer="multipolygon",cropToCutline=True,dstNodata=-9999,warpOptions=["CUTLINE_ALL_TOUCHED=TRUE"])  # Pour ne pas perdre les pixels situés exactement sur la limite de plaque
    print("Raster clipé :", plate_name)
    # Suppression du fichier temporaire
    os.remove(plate_path)
    
print ("Tous les exports done")

# MOSAIC

from osgeo import gdal
import glob
import os

input_folder = r"C:\PANALESIS\Rot_plates\Cartes_outputs\Plates600preRot580\rasterclip"
output_virt= r"C:\PANALESIS\Rot_plates\Cartes_outputs\Plates600preRot580\mosaic\mosaicPlates600preRot580.vrt"
output_tif = r"C:\PANALESIS\Rot_plates\Cartes_outputs\Plates600preRot580\mosaic\mosaicPlates600preRot580.tif"

# Importer les rasters clipés :
rasters = glob.glob(os.path.join(input_folder, "*.tif"))
print(len(rasters), "rasters trouvés")

# Création de la mosaic virtuelle :

vrt = gdal.BuildVRT(output_virt,rasters,srcNodata=-9999,VRTNodata=-9999,options=gdal.BuildVRTOptions(addAlpha=True))
vrt = None
print("VRT créé")

# Conversion en GeoTiff :

gdal.Translate(output_tif,output_virt,creationOptions=["COMPRESS=LZW"])

print("Mosaïque GeoTIFF créée")

#Pour checker les vitesses gloabales et faire une moyenne de vitesse par reconstruction : 

import rasterio
import numpy as np

with rasterio.open(output_tif) as src:

    data = src.read(1)
    # supprimer les pixels no data et NaN
    data = data[data != src.nodata]
    data = data[np.isfinite(data)]

    print("Min :", np.min(data), "cm/an")
    print("Max :", np.max(data), "cm/an")
    print("Vitesse moyenne:", np.mean(data), "cm/an")
    
