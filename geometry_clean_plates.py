from osgeo import gdal, ogr
import geopandas as gpd
import pandas as pd
import fiona 
gdf = gpd.read_file("C:\PANALESIS\Vers0_christian\Plates_psAbs_output.gpkg")
print(gdf)
layers = fiona.listlayers("C:\PANALESIS\Vers0_christian\Plates_psAbs_output.gpkg")
for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\Vers0_christian\Plates_psAbs_output.gpkg", layer = layer)
    print("layer :", layer)
    print(gdf)


print(gdf.columns)
print(gdf.geom_type.unique()) 

for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\Vers0_christian\Plates_psAbs_output.gpkg", layer = layer)
    print(gdf.geometry)

    
# Identifier les géometries empty (True = empty) pour toutes les couches du gpkg

for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\Vers0_christian\Plates_psAbs_output.gpkg", layer = layer)
    print(gdf.geometry.is_empty)
    print(gdf.geometry.notna())
    
    
#Afficher uniquement les lignes avec des geométries empty avec le nom de la couche, et leur index :

geom_empty = []
for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\Vers0_christian\Plates_psAbs_output.gpkg", layer = layer)
    empty_rows = gdf[gdf.geometry.is_empty]
    print(gdf.geometry.is_empty.sum())
    for idx, row in empty_rows.iterrows():
        geom_empty.append({
            "layer": layer,
            "index": idx,
            "geometry": str(row.geometry)
        })
    
        
geom_empty_df = pd.DataFrame(geom_empty)
print(geom_empty_df)


#Pas de géométrie empty pour les plates




