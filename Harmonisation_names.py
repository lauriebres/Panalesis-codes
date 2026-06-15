from osgeo import gdal, ogr
import geopandas as gpd
import fiona
import pandas as pd
import os

path = r"C:\PANALESIS\outputs\Plates_psAbs_output_bounds_clean.gpkg"
layers = fiona.listlayers(path)
    
# Pour afficher tous les différents noms des plaques dans le champ "PlateName" :

field = "PlateName"
values = set()

for layer in fiona.listlayers(path):
    gdf = gpd.read_file(path, layer=layer)
    if field in gdf.columns:
        values.update(gdf[field].dropna().unique())

print(len(values), "nombre de noms différents :") #pour obtenir le nombre de noms différents trouvés dans tous les âges

for v in sorted(values):
    print(v)
    
    
#Pour le fichier R_psAbs
path = r"C:\PANALESIS\outputs\R_psAbs_output_bounds_clean.gpkg"
layers = fiona.listlayers(path)

for layer in layers:
    print(layer)
    
# Pour afficher tous les différents noms des plaques dans le champ "PLATE" :

field = "PLATE"
values = set()

for layer in fiona.listlayers(path):
    gdf = gpd.read_file(path, layer=layer)
    if field in gdf.columns:
        values.update(gdf[field].dropna().unique())

print(len(values), "nombre de noms différents :") #pour obtenir le nombre de noms différents trouvés dans tous les âges

for v in sorted(values):
    print(v)
    
    
# Mettre les noms en maj :

# Pour les Plates:
input_gpkg = r"C:\PANALESIS\outputs\Plates_psAbs_output_bounds_clean.gpkg"
output_gpkg = r"C:\PANALESIS\outputs\Plates_psAbs_names_maj.gpkg"

field = "PlateName"

for layer in fiona.listlayers(input_gpkg):
    gdf = gpd.read_file(input_gpkg, layer=layer)
    if field in gdf.columns:
        gdf[field] = gdf[field].astype(str).str.upper()

    gdf.to_file(
        output_gpkg,
        layer=layer,
        driver="GPKG"
    )

    print("export done")


# Pour R_PsAbs :

input_gpkg = r"C:\PANALESIS\outputs\R_psAbs_output_bounds_clean.gpkg"
output_gpkg = r"C:\PANALESIS\outputs\R_psAbs_names_maj.gpkg"

field = "PLATE"

for layer in fiona.listlayers(input_gpkg):
    gdf = gpd.read_file(input_gpkg, layer=layer)
    if field in gdf.columns:
        gdf[field] = gdf[field].astype(str).str.upper()

    gdf.to_file(
        output_gpkg,
        layer=layer,
        driver="GPKG"
    )

    print("export done")
    
# Comparer les deux nouveaux fichiers:

#Pour afficher tous les différents noms des plaques dans le champ "PlateName" :

path = r"C:\PANALESIS\outputs\Plates_psAbs_names_maj.gpkg"
layers = fiona.listlayers(path)
field = "PlateName"
values = set()

for layer in fiona.listlayers(path):
    gdf = gpd.read_file(path, layer=layer)
    if field in gdf.columns:
        values.update(gdf[field].dropna().unique())

print(len(values), "nombre de noms différents :") #pour obtenir le nombre de noms différents trouvées dans tous les âges

for v in sorted(values):
    print(v)
      
# Same pour le fichier R_psAbs :

path = r"C:\PANALESIS\outputs\R_psAbs_names_maj.gpkg"
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
      
#Comparer les noms des deux gpkg :

gpkg_a = r"C:\PANALESIS\outputs\Plates_psAbs_names_maj.gpkg" 
gpkg_b = r"C:\PANALESIS\outputs\R_psAbs_names_maj.gpkg"

field_a = "PlateName"
field_b = "PLATE"

def get_unique_values(gpkg, field):
    values = set()

    for layer in fiona.listlayers(gpkg):
        gdf = gpd.read_file(gpkg, layer=layer)

        if field in gdf.columns:
            values.update(
                gdf[field]
                .dropna()
                .astype(str)
                .str.strip()
            )

    return values

values_a = get_unique_values(gpkg_a, field_a)
values_b = get_unique_values(gpkg_b, field_b)

only_a = values_a - values_b
only_b = values_b - values_a

print("Noms dans gpkg Plates :", len(values_a))
print("Noms dans gpkg R_psAbs:", len(values_b))

print("Noms présents uniquement dans gpkg Plates :")
for v in sorted(only_a):
    print(v)

print("Noms présents uniquement dans gpkg R_ps_Abs :")
for v in sorted(only_b):
    print(v)

if not only_a and not only_b:
    print("Les deux gpkg contiennent exactement les mêmes noms")
    
# Harmonisation :

gpkg_a = r"C:\PANALESIS\outputs\Plates_psAbs_names_maj.gpkg" 
gpkg_b = r"C:\PANALESIS\outputs\R_psAbs_names_maj.gpkg"
output_a = r"C:\PANALESIS\outputs\Plates_psAbs_names_maj_harmo.gpkg"
output_b = r"C:\PANALESIS\outputs\R_psAbs_names_maj_harmo.gpkg" 
plate_name_mappings_plate = {'ADMUNSEN':'AMUNDSEN',
                             'PALAU' : 'PAHAU', 
                             'SUITTENGU' : 'SUITENGU'}
plate_name_mappings_R_psAbs = {'ALTAI_QUIEUE' : 'ALTAI_QUEUE',
                               'ANT_AUST' : 'ANT_AUS', 
                               'CUB' : 'CUBA',
                               'EAST' : 'EASTER',
                               'EAST_CADOMIA' : 'E_CADOMIA',
                               'FIDJI_E' : 'FIJI_E',
                               'FIDJI_N' : 'FIJI_N',
                               'FIDJI_W' : 'FIJI_W', 
                               'GREENLAND' : 'GREEN',
                               'MADAG' : 'MAD', 
                               'NAZ' : 'NAZCA',
                               'SANAND' : 'SANANDAJ',
                               'TONGA_KER' : 'TONG_KER',
                               'YUCON' : 'YUKON'}

# Pour gpkg plate :

layers = fiona.listlayers(gpkg_a)

for layer in layers : 
    gdf = gpd.read_file(gpkg_a, layer=layer)
    field = "PlateName"
    if field in gdf.columns :
        gdf[field] = gdf[field].replace(plate_name_mappings_plate)
        gdf.to_file(output_a, layer=layer, driver="GPKG")
print ("export done")

# Pour gpkg R_psAbs:

layers = fiona.listlayers(gpkg_b)

for layer in layers : 
    gdf = gpd.read_file(gpkg_b, layer=layer)
    field = "PLATE"
    if field in gdf.columns :
        gdf[field] = gdf[field].replace(plate_name_mappings_R_psAbs)
        gdf.to_file(output_b, layer=layer, driver="GPKG")
print ("export done")

#Vérification :

gpkg_a = r"C:\PANALESIS\outputs\Plates_psAbs_names_maj_harmo.gpkg"
gpkg_b = r"C:\PANALESIS\outputs\R_psAbs_names_maj_harmo.gpkg"

field_a = "PlateName"
field_b = "PLATE"

def get_unique_values(gpkg, field):
    values = set()

    for layer in fiona.listlayers(gpkg):
        gdf = gpd.read_file(gpkg, layer=layer)

        if field in gdf.columns:
            values.update(
                gdf[field]
                .dropna()
                .astype(str)
                .str.strip()
            )

    return values

values_a = get_unique_values(gpkg_a, field_a)
values_b = get_unique_values(gpkg_b, field_b)

only_a = values_a - values_b
only_b = values_b - values_a

print("Noms dans gpkg Plates :", len(values_a))
print("Noms dans gpkg R_psAbs:", len(values_b))

print("Noms présents uniquement dans gpkg Plates :")
for v in sorted(only_a):
    print(v)

print("Noms présents uniquement dans gpkg R_ps_Abs :")
for v in sorted(only_b):
    print(v)

if not only_a and not only_b:
    print("Les deux gpkg contiennent exactement les mêmes noms")
