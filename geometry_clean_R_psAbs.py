from osgeo import gdal, ogr
import geopandas as gpd
import pandas as pd
import fiona 
gdf = gpd.read_file("C:\PANALESIS\outputs\R_psAbs_output.gpkg")
print(gdf.head)
layers = fiona.listlayers("C:\PANALESIS\outputs\R_psAbs_output.gpkg")
for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\outputs\R_psAbs_output.gpkg", layer = layer)
    print(gdf.head)

print(gdf.columns)

# Identifier les géometries empty pour toutes les couches du gpkg :

for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\outputs\R_psAbs_output.gpkg", layer = layer)
    if gdf.geometry.is_empty.any() :
        print("layer:", layer)
        print(gdf[gdf.geometry.is_empty])
        
    else :
        print ("layer:", layer, "pas de géométrie vide")

# Pour connaitre le nombre de géométries vides par couche : 
for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\outputs\R_psAbs_output.gpkg", layer = layer)
    nbre_empty = gdf.geometry.is_empty.sum()
    if nbre_empty > 0 : 
        print("layer :", layer, "Nombre de géométries vides:", nbre_empty, gdf[gdf.geometry.is_empty] )
    else : 
        print("layer:", layer, "Pas de géométrie vide")
        
# Identifier si valeurs manquantes pour les géométries (NA) pour toutes les couches du gpkg :

for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\outputs\R_psAbs_output.gpkg", layer = layer)
    if gdf.geometry.isna().any() :
        print("layer:", layer)
        print(gdf[gdf.geometry.isna()])
    else :
        print ("layer:", layer, "pas de géométrie NA")
        
# Pas de géométrie NA pour R_psAbs
        
# Enlever les lignes avec géométries vides et exporter la version clean vers un nouveau gpkg :

input_gpkg = r"C:\PANALESIS\outputs\R_psAbs_output.gpkg"
output_gpkg = r"C:\PANALESIS\outputs\R_psAbs_output_geom_clean.gpkg"
driver = ogr.GetDriverByName("GPKG")
output = driver.CreateDataSource(output_gpkg)

#Garder uniquemenet les geométries non empty en utilisant fonction len (size de l'objet) :

for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\outputs\R_psAbs_output.gpkg", layer = layer)
    gdf_complete = len(gdf)
    print(gdf_complete, layer)
    gdf_clean = gdf[gdf.geometry.is_empty]
    cleaning = gdf_complete - len(gdf_clean)
    print(cleaning,layer)
    
#Exporter

for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\outputs\R_psAbs_output.gpkg", layer = layer)
    gdf_clean = gdf[~gdf.geometry.is_empty] # "~"" selectionne les geom pas vides
    gdf_clean.to_file(output_gpkg, layer=layer, driver="GPKG")
    
print("Export terminé")

# Vérification 

layers = fiona.listlayers("C:\PANALESIS\outputs\R_psAbs_output_geom_clean.gpkg")
for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\outputs\R_psAbs_output_geom_clean.gpkg", layer = layer)
    if gdf.geometry.is_empty.any() :
        print("layer:", layer)
        print(gdf[gdf.geometry.is_empty])
        
    else :
        print ("layer:", layer, "pas de géométrie vide")
    
    