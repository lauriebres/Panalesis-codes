# Librairies:

from osgeo import gdal, ogr
import geopandas as gpd
import pandas as pd
import fiona 
import os

# Données :

path = r"C:\PANALESIS\Rot_plates\Outputs\PlatesxxxpreRotyyy_geom_clean.gpkg"
layers = fiona.listlayers(path)
output_path = r"C:\PANALESIS\Rot_plates\Outputs\PlatesxxxpreRotyyy_geom_clean_bound.gpkg"

# Identification des sommets en dehors du domaine avec shapely  : 

from shapely.geometry import MultiPolygon

for layer in layers:
    gdf = gpd.read_file(path, layer=layer)
    for geom in gdf.geometry :
        for fid, geom in enumerate(gdf.geometry):
            for poly in geom.geoms:
                for x, y in poly.exterior.coords:
                 if x < -180 or x > 180:
                    print("layer :",layer, "FID:", fid+1, "Longitude invalide :", x)
                    
                if y < -90 or y > 90:
                        print("layer :",layer, "FID:", fid+1, "Latitude invalide :", y)
                        
                                           
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

report = []

# Application du clip à toutes les couches et export du fichier avec les géométries corrigées :
for layer in layers:
    gdf = gpd.read_file(path, layer=layer)
    original_geom = gdf.geometry.copy() #copie des géométries originales pour le rapport des modifications 
    gdf["geometry"] = gdf["geometry"].apply(lambda geom: transform(clip_lon_lat, geom)) # application du clip
    modified = gdf.geometry.ne(original_geom)
    nbre_modified = modified.sum()
    print("layer:", layer, "nombre de géométries modifiées :", nbre_modified)
    
    for fid, row in gdf.loc[modified].iterrows() :
        report.append({"layer": layer, "fid": fid+1, "PlateName": row["PlateName"]})
    
    gdf.to_file(output_path, layer=layer, driver="GPKG")
print("export done")

# Créer un rapport des géométries corrigées :

output_report = r"C:\PANALESIS\Report\Rot_plate_geom_bound.txt"
report_df = pd.DataFrame(report)
print(report_df)
report_df.to_csv(output_report,index=False, sep="\t", encoding="utf-8")
print("report done")

#Verification de l'emprise des géométries sur le nouveau gpkg corrigé : 

path = output_path
layers = fiona.listlayers(path)

for layer in layers:
    gdf = gpd.read_file(path, layer=layer)
    for geom in gdf.geometry :
        for poly in geom.geoms:
            for x, y in poly.exterior.coords:
                if x < -180 or x > 180:
                    print(layer, "Longitude invalide :", x)
                
                if y < -90 or y > 90:
                    print(layer, "Latitude invalide :", y)
print("Géométries OK")
