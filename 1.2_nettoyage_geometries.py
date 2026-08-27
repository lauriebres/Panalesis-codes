# Librairies :

from osgeo import gdal, ogr
import geopandas as gpd
import pandas as pd
import fiona 

# Données :

path = r"C:\PANALESIS\Rot_plates\Outputs\PlatesxxxpreRotyyy_outputs.gpkg"
layers = fiona.listlayers(path)

# Identifier les géometries "empty" pour toutes les couches du gpkg :

for layer in layers :
    gdf = gpd.read_file(path, layer = layer)
    if gdf.geometry.is_empty.any() :
        print("layer:", layer)
        print(gdf[gdf.geometry.is_empty])
    else :
        print ("layer:", layer, "pas de géométrie vide")
        
# Identifier si il y a des valeurs manquantes pour les géométries (NA) pour toutes les couches du gpkg :

for layer in layers :
    gdf = gpd.read_file(path, layer = layer)
    if gdf.geometry.isna().any() :
        print("layer:", layer)
        print(gdf[gdf.geometry.isna()])
    else :
        print ("layer:", layer, "pas de géométrie NA")
        

# Export de fichier clean (fichier sans les géométries vides et NA): 

output_gpkg = r"C:\PANALESIS\Rot_plates\Outputs\PlatesxxxpreRotyyy_geom_clean.gpkg"
for layer in layers :
    gdf = gpd.read_file(path, layer = layer)
    gdf_clean = gdf[gdf.geometry.notna() &
        ~gdf.geometry.is_empty]# "~"" selectionne les geom pas vides
    gdf_clean.to_file(output_gpkg, layer=layer, driver="GPKG")
    
print("Export terminé")


# Vérification du nouveau gpkg:
    
# Identifier si valeurs manquantes pour les géométries (NA) pour toutes les couches du gpkg :

path = r"C:\PANALESIS\Rot_plates\Outputs\PlatesxxxpreRotyyy_geom_clean.gpkg"
layers = fiona.listlayers(path)

for layer in layers :
    gdf = gpd.read_file(path, layer = layer)
    if gdf.geometry.isna().any() :
        print("layer:", layer)
        print(gdf[gdf.geometry.isna()])
    else :
        print ("layer:", layer, "pas de géométrie NA")
        
# Connaitre les types de geométries sont présentes dans le gpkg: 

path = r"C:\PANALESIS\Rot_plates\Outputs\PlatesxxxpreRotyyy_geom_clean.gpkg"
layers = fiona.listlayers(path)

for layer in layers:
    gdf = gpd.read_file(path, layer=layer)
    print(gdf.geom_type.unique())
    print("layer:", layer, gdf.geom_type.value_counts())
    
