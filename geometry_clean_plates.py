from osgeo import gdal, ogr
import geopandas as gpd
import pandas as pd
import fiona 
gdf = gpd.read_file("C:\PANALESIS\outputs\Plates_psAbs_output.gpkg")
print(gdf.head)
layers = fiona.listlayers("C:\PANALESIS\outputs\Plates_psAbs_output.gpkg")
for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\outputs\Plates_psAbs_output.gpkg", layer = layer)
    print("layer:", layer)
    print(gdf.head)


print(gdf.columns)
print(gdf.geom_type.unique()) 

for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\outputs\Plates_psAbs_output.gpkg", layer = layer)
    print(gdf.geometry)

# Identifier les géometries empty pour toutes les couches du gpkg

for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\outputs\Plates_psAbs_output.gpkg", layer = layer)
    if gdf.geometry.is_empty.any() :
        print("layer:", layer)
        print(gdf[gdf.geometry.is_empty])
    else :
        print ("layer:", layer, "pas de géométrie vide")
        
# Pas de géométrie empty pour les plates
        
        
# Identifier si valeurs manquantes pour les géométries (NA) pour toutes les couches du gpkg :

for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\outputs\Plates_psAbs_output.gpkg", layer = layer)
    if gdf.geometry.isna().any() :
        print("layer:", layer)
        print(gdf[gdf.geometry.isna()])
    else :
        print ("layer:", layer, "pas de géométrie NA")
        
# Une géométrie NA (age : 535)

# Export fichier clean : 
output_gpkg = r"C:\PANALESIS\outputs\Plates_psAbs_output_geom_clean.gpkg"
for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\outputs\Plates_psAbs_output.gpkg", layer = layer)
    gdf_clean = gdf[gdf.geometry.notna() &
        ~gdf.geometry.is_empty]# "~"" selectionne les geom pas vides
    gdf_clean.to_file(output_gpkg, layer=layer, driver="GPKG")
    
print("Export terminé")

# Vérification 

layers = fiona.listlayers("C:\PANALESIS\outputs\Plates_psAbs_output_geom_clean.gpkg")
for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\outputs\Plates_psAbs_output_geom_clean.gpkg", layer = layer)
    if gdf.geometry.isna().any() :
        print("layer:", layer)
        print(gdf[gdf.geometry.isna()])
    else :
        print ("layer:", layer, "pas de géométrie NA")
