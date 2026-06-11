from osgeo import gdal, ogr
import geopandas as gpd
import pandas as pd
import fiona 
gdf = gpd.read_file("C:\PANALESIS\outputs\COB_psAbs_output.gpkg")
print(gdf.head)
layers = fiona.listlayers("C:\PANALESIS\outputs\COB_psAbs_output.gpkg")
for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\outputs\COB_psAbs_output.gpkg", layer = layer)
    print("layer :", layer)
    print(gdf)


print(gdf.columns)
print(gdf.geom_type.unique()) 

for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\outputs\COB_psAbs_output.gpkg", layer = layer)
    print(gdf.geometry)
    
    
# Identifier les géometries empty pour toutes les couches du gpkg

for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\outputs\COB_psAbs_output.gpkg", layer = layer)
    if gdf.geometry.is_empty.any() :
        print("layer:", layer)
        print(gdf[gdf.geometry.is_empty])
    else :
        print ("layer:", layer, "pas de géométrie vide")
    
#Pas de géométrie empty pour la COB

# Identifier si valeurs manquantes pour les géométries (NA) pour toutes les couches du gpkg :

for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\outputs\COB_psAbs_output.gpkg", layer = layer)
    if gdf.geometry.isna().any() :
        print("layer:", layer)
        print(gdf[gdf.geometry.isna()])
    else :
        print ("layer:", layer, "pas de géométrie NA")