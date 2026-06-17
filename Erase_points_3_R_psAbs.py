from osgeo import gdal, ogr
import geopandas as gpd
import fiona
import pandas as pd
import os
from shapely import MultiLineString

path = r"C:\PANALESIS\outputs\R_psAbs_names_maj_harmo_clean.gpkg"
layers = fiona.listlayers(path)

#Checker les geom type R_psAbs:

for layer in layers:
    gdf = gpd.read_file(path, layer=layer)
    print(gdf.geom_type.unique())
    print("layer:", layer, gdf.geom_type.value_counts())
    
# On a uniquement des MiltilineString ici

# Nombre de features par couches :
for layer in fiona.listlayers(path):
    gdf = gpd.read_file(path, layer=layer)
    print("Nombre de features : ", len(gdf))

# focntion pour compter le points présents dans les diff features : 

def count_points(geom):
    if geom is None:
        return 0

    if geom.geom_type == "MultiLineString":
        return sum(len(line.coords) for line in geom.geoms)

for layer in fiona.listlayers(path):
    gdf = gpd.read_file(path, layer=layer)
    gdf["nbre_points"] = gdf.geometry.apply(count_points)
    points = (gdf["nbre_points"] < 3).sum()

    print(layer, points, "géométries avec strictement moins de 3 points")
    
#Enlever les géométries avec strictement moins de 3 points :

# Enlever les valeurs "NONAME" du gpkg : 

output = r"C:\PANALESIS\outputs\R_psAbs_names_maj_harmo_clean_points.gpkg"

for layer in fiona.listlayers(path):
    gdf = gpd.read_file(path, layer=layer)
    gdf["nbre_points"] = gdf.geometry.apply(count_points)
    points = (gdf["nbre_points"] < 3)
    gdf = gdf[~points]
    gdf.to_file(output, layer = layer, driver ="GPKG")
        
print("export done")

#Vérification :

path = r"C:\PANALESIS\outputs\R_psAbs_names_maj_harmo_clean_points.gpkg"
layers = fiona.listlayers(path)

def count_points(geom):
    if geom is None:
        return 0

    if geom.geom_type == "MultiLineString":
        return sum(len(line.coords) for line in geom.geoms)

for layer in fiona.listlayers(path):
    gdf = gpd.read_file(path, layer=layer)
    gdf["nbre_points"] = gdf.geometry.apply(count_points)
    points = (gdf["nbre_points"] < 3).sum()

    print(layer, points, "géométries avec strictement moins de 3 points")