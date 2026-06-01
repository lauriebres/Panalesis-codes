from osgeo import gdal, ogr
import geopandas as gpd
import pandas as pd
import fiona 
gdf = gpd.read_file("C:\PANALESIS\Vers0_christian\COB_psAbs_output.gpkg")
print(gdf)
layers = fiona.listlayers("C:\PANALESIS\Vers0_christian\COB_psAbs_output.gpkg")
for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\Vers0_christian\COB_psAbs_output.gpkg", layer = layer)
    print("layer :",layer)
    print(gdf)


print(gdf.columns)
print(gdf.geom_type.unique()) 

for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\Vers0_christian\COB_psAbs_output.gpkg", layer = layer)
    print(gdf.geometry)
    
    
# Identifier les géometries empty (True = empty) pour toutes les couches du gpkg

for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\Vers0_christian\COB_psAbs_output.gpkg", layer = layer)
    print(gdf.geometry.is_empty)
    
#Pas de géométrie empty pour la COB
