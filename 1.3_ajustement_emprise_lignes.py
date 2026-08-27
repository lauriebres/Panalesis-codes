# Librairies :

from osgeo import gdal, ogr
import geopandas as gpd
import pandas as pd
import fiona 

# Données :

path = r"C:\PANALESIS\outputs\R_psAbs_output_geom_clean.gpkg"
layers = fiona.listlayers(path)

# Identification des sommets en dehors du domaine : 

for layer in layers :
    gdf = gpd.read_file(path, layer =layer)
    gdf_bounds = gdf.geometry.bounds
    hors_limites = gdf[
        (gdf_bounds["minx"] < -180) |
        (gdf_bounds["maxx"] > 180) |
        (gdf_bounds["miny"] < -90) |
        (gdf_bounds["maxy"] > 90)
    ]
    
    if len(hors_limites) > 0:
        print("layer name: ", layer)
        print(hors_limites)
        
# Clip aux limites du domaine pour les géométries concernées :

from shapely.ops import transform
import numpy as np

# Fonction pour le clip aux valeurs du domaine :

def clip_lon_lat(x, y):
    if abs(x) > 180 or abs(x) < -180:
        x = np.clip(x, -180, 180)
    if abs(y) > 90 or abs(y) < -90:
        y = np.clip(y, -90, 90)
    return (x, y)


# Application du clip à toutes les couches et export du fichier avec les géométries corrigées :

output_directory = r"C:\PANALESIS\outputs\R_psAbs_output_bounds_clean.gpkg"

for layer in layers:
    gdf = gpd.read_file(path, layer=layer)
    original_geom = gdf.geometry.copy() # copie des géométries originales pour le rapport des modifications
    gdf["geometry"] = gdf["geometry"].apply(lambda geom: transform(clip_lon_lat, geom)) # application du clip
    modified = gdf.geometry.ne(original_geom)
    nbre_modified = modified.sum()
    print("layer:", layer, "nombre de géométries modifées :", nbre_modified)
    gdf.to_file(output_directory, layer=layer, driver="GPKG")
    
print("export done")


#Verification des géométries sur le nouveau gpkg corrigé : 

path = r"C:\PANALESIS\outputs\R_psAbs_output_bounds_clean.gpkg"
layers = fiona.listlayers(path)

for layer in layers :
    gdf = gpd.read_file(path, layer =layer)
    gdf_bounds = gdf.geometry.bounds
    hors_limites = gdf[
        (gdf_bounds["minx"] < -180) |
        (gdf_bounds["maxx"] > 180) |
        (gdf_bounds["miny"] < -90) |
        (gdf_bounds["maxy"] > 90)
    ]
    
    if len(hors_limites) > 0:
        print("layer name: ", layer)
        print(hors_limites)
    else: print(layer, "Pas de géométrie hors limites") 