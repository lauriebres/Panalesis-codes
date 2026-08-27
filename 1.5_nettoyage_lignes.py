# Librairies :

from osgeo import gdal, ogr
import geopandas as gpd
import fiona
import pandas as pd
import os
from shapely import MultiLineString
from pyproj import Geod

#Données :

path =  r"C:\PANALESIS\outputs\R_psAbs_points_length.gpkg"
layers = fiona.listlayers(path)
output = r"C:\PANALESIS\outputs\R_psAbs_names_maj_harmo_clean_points.gpkg"

# pour le rapport :
report = []

# Focntion afin de compter le nombre de points présents dans les différentes features : 

def count_points(geom):
    if geom is None:
        return 0

    if geom.geom_type == "LineString":
        return len(geom.coords)
    
    elif geom.geom_type == "MultiLineString":
        return sum(len(line.coords) for line in geom.geoms)

# Selectionner les lignes composées de < de 3 points :

for layer in fiona.listlayers(path):
    gdf = gpd.read_file(path, layer=layer)
    gdf["nbre_points"] = gdf.geometry.apply(count_points)
    points = (gdf["nbre_points"] < 3).sum()

    print(layer, points, "géométries avec strictement moins de 3 points")
    
# Calculer les longueurs géodésique en mètres et kilomètres des lignes : 

geod = Geod(ellps="WGS84")    #pour convertir degrès en mètres

def longueur_geodesique(geom):
    
    return geod.geometry_length(geom)

# Ajouter les nouvelles colonnes au gdf : 

for layer in fiona.listlayers(path):
    gdf = gpd.read_file(path, layer=layer)
    gdf["nbre_points"] = gdf.geometry.apply(count_points)
    gdf["length_m"]= gdf.geometry.apply(longueur_geodesique) #length convertie en mètres
    gdf["length_km"]=gdf["length_m"]/1000

    
# Enlever les géométries avec strictement moins de 3 points et dont la longueur est < 1000 mètres :

output = r"C:\PANALESIS\outputs\R_psAbs_names_maj_harmo_clean_points.gpkg"
from pyproj import Geod

for layer in fiona.listlayers(path):
    gdf = gpd.read_file(path, layer=layer)
    gdf["nbre_points"] = gdf.geometry.apply(count_points)
    points = (gdf["nbre_points"] < 3)
    length = (gdf["length_m"] < 1000)
    conditions = points & length
   
    # Sauvgarde infos avant suppression :
    if conditions.any() :
        for fid, row in gdf[conditions].iterrows():
            report.append({"layer" : layer, "fid" : fid+1, "Plate Name" : row["PLATE"], "nombre de points": row["nbre_points"], "longueur": row["length_m"], "TYPE": row["TYPE"]})
    # Conserver que les géométries > 3 points et > 1000 m de long
    gdf = gdf[conditions]

        
print("export done")

# Rapport txt des lignes supprimées :

report_out = r"C:\PANALESIS\Report\report_features_erased_R_psAbs_1000m.txt"
pd.DataFrame(report).to_csv(report_out,index=False,encoding="utf-8")
print("report done")