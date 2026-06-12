from osgeo import gdal, ogr
import geopandas as gpd
import pandas as pd
import fiona 

#Checker les geom type :
path = r"C:\PANALESIS\outputs\Plates_psAbs_output_geom_clean.gpkg"
layers = fiona.listlayers(path)

for layer in layers:
    gdf = gpd.read_file(path, layer=layer)
    print(gdf.geom_type.unique())
    print("layer:", layer, gdf.geom_type.value_counts())
    
# Il y a que des multipolygones dans le fichier geom clean !

#Checker les geom type :
path = r"C:\PANALESIS\outputs\Plates_psAbs_output.gpkg"
layers = fiona.listlayers(path)

for layer in layers:
    gdf = gpd.read_file(path, layer=layer)
    print(gdf.geom_type.unique())
    print("layer:", layer, gdf.geom_type.value_counts())
    
#Checker les geom type COB:
path = r"C:\PANALESIS\outputs\COB_psAbs_output.gpkg"
layers = fiona.listlayers(path)

for layer in layers:
    gdf = gpd.read_file(path, layer=layer)
    print(gdf.geom_type.unique())
    print("layer:", layer, gdf.geom_type.value_counts())
    
    
#Checker les geom type R_psAbs:
path = r"C:\PANALESIS\outputs\R_psAbs_output_geom_clean.gpkg"
layers = fiona.listlayers(path)

for layer in layers:
    gdf = gpd.read_file(path, layer=layer)
    print(gdf.geom_type.unique())
    print("layer:", layer, gdf.geom_type.value_counts())

