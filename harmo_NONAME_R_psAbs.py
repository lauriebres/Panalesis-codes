#Enlever les NONAME du champs PLATE de R_psAbs :

from osgeo import gdal, ogr
import geopandas as gpd
import fiona
import pandas as pd
import os
from pathlib import Path

#Pour afficher tous les différents noms des plaques dans le champ "PlateName" :

path = r"C:\PANALESIS\outputs\R_psAbs_names_maj_harmo.gpkg"
layers = fiona.listlayers(path)
field = "PLATE"
values = set()

for layer in fiona.listlayers(path):
    gdf = gpd.read_file(path, layer=layer)
    if field in gdf.columns:
        values.update(gdf[field].dropna().unique())

print(len(values), "nombre de noms différents :") #pour obtenir le nombre de noms différents trouvées dans tous les âges

for v in sorted(values):
    print(v)
 
#identifier dans quelles couches sont les valeurs "NONAME" :

for layer in fiona.listlayers(path):
    gdf = gpd.read_file(path, layer=layer)
    if field in gdf.columns:
            noname = (gdf[field] == "NONAME").sum()
            
            if noname > 0:
                print(layer, noname, "NONAME") 
                
# Enlever les valeurs "NONAME" du gpkg : 

output = r"C:\PANALESIS\outputs\R_psAbs_names_maj_harmo_clean.gpkg"

for layer in fiona.listlayers(path):
    gdf = gpd.read_file(path, layer=layer)
    if field in gdf.columns:
        mask = (gdf[field] == "NONAME")
        gdf = gdf[~mask]
        gdf.to_file(output, layer = layer, driver ="GPKG")
        
print("export done")

# Verification :

path = r"C:\PANALESIS\outputs\R_psAbs_names_maj_harmo_clean.gpkg"
layers = fiona.listlayers(path)
field = "PLATE"
for layer in fiona.listlayers(path):
    gdf = gpd.read_file(path, layer=layer)
    if field in gdf.columns:
            noname = (gdf[field] == "NONAME").sum()
            
            if noname > 0:
                print(layer, noname, "NONAME")
            else :
                print(layer, "pas de valeur NONAME")
