from osgeo import gdal, ogr
import geopandas as gpd
import pandas as pd
import fiona 

path = r"C:\PANALESIS\outputs\Plates_psAbs_output_geom_clean.gpkg"
layers = fiona.listlayers(path)
print(len(layers))

#Plates que des multipolygons

#Connaitre les multipolygones qui dépassent les limites des bornes longitudes [-180,180] :

for layer in layers:
    gdf = gpd.read_file(path, layer=layer)
    
     # Vérifier les géométries
    for fid, geom in enumerate(gdf.geometry):

        # Bornes (-180 à +180) : minx, miny, maxx, maxy
        minx, miny, maxx, maxy = geom.bounds

        # Hors limites
        if minx < -180 or maxx > 180:
            print(layer, ": Polygone dépasse les limites longitudes")
            print(layer, "FID:", fid, "minx=", minx, "maxx=",maxx)
        

#Connaitre les multipolygones qui dépassent les limites des bornes latitudes [-90, 90] :

for layer in layers:
    gdf = gpd.read_file(path, layer=layer)
     # Vérifier les géométries
    for fid, geom in enumerate(gdf.geometry):

        # Bornes (-90 à +90) : minx, miny, maxx, maxy
        minx, miny, maxx, maxy = geom.bounds

        # Hors limites
        if miny < -90 or maxy > 90:
            print(layer, ":Polygone dépasse les limites latitudes")
            print(layer, "FID:", fid, "miny=", miny, "maxy=",maxy)

        

#Avec shapely test longitudes sur les sommets des multipolygons pour identifier les sommets hors limite:
for layer in layers:
    gdf = gpd.read_file(path, layer=layer)
    print(gdf.crs)

from shapely.geometry import MultiPolygon

for layer in layers:
    gdf = gpd.read_file(path, layer=layer)
    for geom in gdf.geometry :
        for poly in geom.geoms:
            for x, y in poly.exterior.coords:
                if x < -180 or x > 180:
                    print("layer :",layer, "Longitude invalide :", x)
                    print(type(x))
                if y < -90 or y > 90:
                        print("layer :",layer, "Latitude invalide :", y)
                        print(type(y))
                    
                        

from shapely.ops import transform
import numpy as np

output_directory = r"C:\PANALESIS\outputs\Plates_psAbs_output_bounds_clean.gpkg"

#fonction pour clip dans l'interval :

def clip_lon_lat(x, y):
    if abs(x) > 180 or abs(x) < -180:
        x = np.clip(x, -180, 180)
    if abs(y) > 90 or abs(y) < -90:
        y = np.clip(y, -90, 90)
    return (x, y)


for layer in layers:
    
    gdf = gpd.read_file(path, layer=layer)
    original_geom = gdf.geometry.copy() #copie des géométries originales pour comparaison 
    gdf["geometry"] = gdf["geometry"].apply(lambda geom: transform(clip_lon_lat, geom)) # application du clip
    modified = gdf.geometry.ne(original_geom)
    nbre_modified = modified.sum()
    print("layer:", layer, "nombre de géométrie modifées :", nbre_modified)
    gdf.to_file(output_directory, layer=layer, driver="GPKG")
    
print("export done")

#Verification géométrie sur le nouveau gpkg corrigé : 

from shapely.geometry import MultiPolygon

path = r"C:\PANALESIS\outputs\Plates_psAbs_output_bounds_clean.gpkg"
layers = fiona.listlayers(path)

for layer in layers:
    gdf = gpd.read_file(path, layer=layer)
    for geom in gdf.geometry :
        for poly in geom.geoms:
            for x, y in poly.exterior.coords:
                if x < -180 or x > 180:
                    print(layer, "Longitude invalide :", x)
                
                if y < -90 or y > 90:
                    print(layer, "Latitude invalide :", y)
                    
print("Géométries OK")