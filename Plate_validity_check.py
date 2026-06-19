from osgeo import gdal, ogr
import geopandas as gpd
import fiona
import pandas as pd
import os
from shapely.geometry import shape
from shapely import make_valid
from shapely.validation import explain_validity

path = r"C:\PANALESIS\outputs\Plates_psAbs_names_maj_harmo.gpkg"
output = r"C:\PANALESIS\outputs\Plates_ps_Abs_valid.gpkg"
report_out = r"C:\PANALESIS\report_plate_validity"
layers = fiona.listlayers(path)

# Pour le bilan et rapport :

total_invalid = 0
total_fixed = 0
report = []

# Identifier les plaques avec des géométries invalides : 
 
for layer in layers :
    print("Traitement :", layer)
    gdf = gpd.read_file(path, layer=layer)
    invalid_count = 0
    new_geoms = []
   
    for fid, row in gdf.iterrows():
        geom = row.geometry

        if geom is None:

            new_geoms.append(None)
            continue

        if geom.is_valid:

            new_geoms.append(geom)
        else : 
    
            invalid_count += 1
            total_invalid += 1
            reason = explain_validity(geom)
            print("Géométries invalides :", invalid_count)
            print("Géométrie invalide:", "FID:", (fid+1), "Plate:", row["PlateName"], "Problem:" ,reason)
           
            fixed_geom = make_valid(geom)

            if fixed_geom.is_valid:
                total_fixed += 1

            report.append("layer:", layer, "FID :", fid, "Plate :", row["PlateName"], "Reason :", reason)
            new_geoms.append(fixed_geom)
 
    gdf.geometry = new_geoms
    gdf.to_file(output, layer = layer, driver = "GPKG")
print("export done")
    


print("BILAN :")
print("Géométries invalides détectées:", total_invalid)
print("Géométries réparées: ",total_fixed)

#Exporter le rapport en texte: 

pd.DataFrame(report).to_csv(report_out,index=False,encoding="utf-8")

# Verification :

path = r"C:\PANALESIS\outputs\Plates_ps_Abs_valid.gpkg"
layers = fiona.listlayers(path)

total_invalid = 0
total_fixed = 0

report = []

# Identifier les plaques avec des géométries invalides : 
 
for layer in layers :
    print("Traitement :", layer)
    gdf = gpd.read_file(path, layer=layer)
    invalid_count = 0
    new_geoms = []
   
    for fid, row in gdf.iterrows():
    
        geom = row.geometry

        if geom is None:

            new_geoms.append(None)
            continue

        if geom.is_valid:

            new_geoms.append(geom)
        else : 
    
            invalid_count += 1
            total_invalid += 1

            reason = explain_validity(geom)
            print("Géométries invalides :", invalid_count)
            print("Géométrie invalide:", "FID:", (fid+1), "Plate:", row["PlateName"], "Problem:" ,reason)
           
            fixed_geom = make_valid(geom)

            if fixed_geom.is_valid:
                total_fixed += 1

            report.append("layer:", layer, "FID :", fid, "Plate :", row["PlateName"], "Reason :", reason)

            new_geoms.append(fixed_geom)
            
print("BILAN")
print("Géométries invalides détectées :", total_invalid)
print("Géométries réparées:" , total_fixed) 