from osgeo import gdal, ogr
import geopandas as gpd
import pandas as pd
import fiona 
gdf = gpd.read_file("C:\PANALESIS\R_psAbs_output.gpkg")
print(gdf)
layers = fiona.listlayers("C:\PANALESIS\R_psAbs_output.gpkg")
for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\R_psAbs_output.gpkg", layer = layer)
    print(gdf)


print(gdf.columns)

# Identifier les géometries empty (True = empty) pour toutes les couches du gpkg

for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\R_psAbs_output.gpkg", layer = layer)
    print(gdf.geometry.is_empty)
   
    
#Afficher uniquement les lignes avec des geométries empty avec le nom de la couche, et leur index :

geom_empty = []
for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\R_psAbs_output.gpkg", layer = layer)
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

# Enlever les lignes avec géométries vides et exporter la version clean vers un nouveau gpkg :

input_gpkg = r"C:\PANALESIS\R_psAbs_output.gpkg"
output_gpkg = r"C:\PANALESIS\R_psAbs_output_geom_clean.gpkg"
driver = ogr.GetDriverByName("GPKG")
output = driver.CreateDataSource(output_gpkg)

#Garder uniquemenet les geométries non empty en utilisant fonction len (size de l'objet) :

for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\R_psAbs_output.gpkg", layer = layer)
    gdf_complete = len(gdf)
    print(gdf_complete, layer)
    gdf_clean = gdf[gdf.geometry.is_empty]
    cleaning = gdf_complete - len(gdf_clean)
    print(cleaning,layer)
    
#Exporter

for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\R_psAbs_output.gpkg", layer = layer)
    gdf_clean = gdf[~gdf.geometry.is_empty] # "~"" selectionne les geom pas vides
    gdf_clean.to_file(output_gpkg, layer=layer, driver="GPKG")
    
print("Export terminé")

#Verification

for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\R_psAbs_output_geom_clean.gpkg", layer = layer)
    print(gdf.geometry.is_empty)
