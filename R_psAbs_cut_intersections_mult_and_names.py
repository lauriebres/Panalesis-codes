from osgeo import gdal, ogr
import geopandas as gpd
import fiona
import pandas as pd
import os
from pathlib import Path
from shapely import make_valid
import fiona
from shapely.geometry import shape
from shapely import MultiLineString
 
gpkg_plate = r"C:\PANALESIS\outputs\Plates_ps_Abs_valid.gpkg" 
gpkg_line = r"C:\PANALESIS\outputs\R_psAbs_names_filled_single_int.gpkg"
gpkg_line_output = r"C:\PANALESIS\outputs\R_psAbs_cut_intersection.gpkg"

layer_Plate = fiona.listlayers("C:\PANALESIS\outputs\Plates_ps_Abs_valid.gpkg")
layer_line = fiona.listlayers("C:\PANALESIS\outputs\R_psAbs_names_filled_single_int.gpkg")

# correspondance entre le nom des couches des gpkg:
corres_layers = {'Plate_000' : 'R_psAbs_000',
    'Plate_006' : 'R_psAbs_006',
    'Plate_011' : 'R_psAbs_011',
    'Plate_015' : 'R_psAbs_015',
    'Plate_020' : 'R_psAbs_020',
    'Plate_033' : 'R_psAbs_033',
    'Plate_040' : 'R_psAbs_040',
    'Plate_048' : 'R_psAbs_048',
    'Plate_056' : 'R_psAbs_056',
    'Plate_068' : 'R_psAbs_068',
    'Plate_084' : 'R_psAbs_084',
    'Plate_094' : 'R_psAbs_094',
    'Plate_100' : 'R_psAbs_100',
    'Plate_113' : 'R_psAbs_113',
    'Plate_120' : 'R_psAbs_120',
    'Plate_133' : 'R_psAbs_133',
    'Plate_140' : 'R_psAbs_140',
    'Plate_154' : 'R_psAbs_154',
    'Plate_165' : 'R_psAbs_165',
    'Plate_180' : 'R_psAbs_180',
    'Plate_200' : 'R_psAbs_200',
    'Plate_210' : 'R_psAbs_210',
    'Plate_220' : 'R_psAbs_220',
    'Plate_230' : 'R_psAbs_230',
    'Plate_240' : 'R_psAbs_240',
    'Plate_250' : 'R_psAbs_250',
    'Plate_270' : 'R_psAbs_270',
    'Plate_290' : 'R_psAbs_290', 
    'Plate_300' : 'R_psAbs_300',
    'Plate_315' : 'R_psAbs_315',
    'Plate_330' : 'R_psAbs_331',
    'Plate_350' : 'R_psAbs_350',
    'Plate_370' : 'R_psAbs_370',
    'Plate_383' : 'R_psAbs_383',
    'Plate_393' : 'R_psAbs_393',
    'Plate_408' : 'R_psAbs_408',
    'Plate_420' : 'R_psAbs_420',
    'Plate_444' : 'R_psAbs_444',
    'Plate_463' : 'R_psAbs_463',
    'Plate_475' : 'R_psAbs_475',
    'Plate_489' : 'R_psAbs_489',
    'Plate_500' : 'R_psAbs_500',
    'Plate_518' : 'R_psAbs_518',
    'Plate_535' : 'R_psAbs_535',
    'Plate_545' : 'R_psAbs_545',
    'Plate_560' : 'R_psAbs_560',
    'Plate_580' : 'R_psAbs_580',
    'Plate_600' : 'R_psAbs_600' }

# Reverse mapping: R_psAbs -> plate
corres_layers_rev = {v: k for k, v in corres_layers.items()}

# pour le rapport :
report =[]
report_out = r"C:\PANALESIS\Report\report_ZDEM_cuting_R_psAbs.txt"
modified_fid_geom = []
report_fid_out= r"C:\PANALESIS\Report\report_line_cut_fid.txt"



for layer_line, layer_Plate in corres_layers_rev.items():
    
    print("traitement :", layer_line)
    
    gdf_plate = gpd.read_file(gpkg_plate, layer = layer_Plate)

    gdf_line = gpd.read_file(gpkg_line, layer = layer_line)
    mask_zdem = gdf_line["PLATE"].astype(str).str.strip().str.upper().isin(["ZDEM", "Z_DEM"]) #prend en compte également si espace et maj
    zdem_lines = gdf_line[mask_zdem].copy()
    gdf_out = gdf_line.copy()

   
    new_features = []
    rows_to_remove = []
    modified_count = 0
    added_count = 0
    
    for idx_line, line_row in zdem_lines.iterrows():
    
        line_geom = line_row.geometry
        
        segments = []
        
        created_segments = 0
        
        for _, plate_row in gdf_plate.iterrows():
            
            plate_geom = plate_row.geometry
            plate_name = plate_row["PlateName"]
            
            inter = line_geom.intersection(plate_geom) #calcule la portion de ligne située à l'intérieur du polygone
           
            
            # Cas ou il n'y a pas d'intersection
            if inter.is_empty:
                continue
         
            if inter.geom_type == "LineString":
                if inter.length > 1e-8 : # Ignore les contacts ponctuels petits, changer ?
                        segments.append((inter, plate_name))
                        
            elif inter.geom_type == "MultiLineString":
                for part in inter.geoms :
                    if part.length > 1e-8 : # Ignore les contacts ponctuels petits, changer ?
                        segments.append((part, plate_name))
            
        #plaques distinctes intersectées :        
        intersected_plates = list(set(plate for _, plate in segments))
        
            
         # Cas ou la ligne coupe plusieurs polygone diff :   
        if len(intersected_plates) > 1:
            print(layer_line, "fid :" ,idx_line+1 , "plaques:", intersected_plates)
            
            nb_parts = len(segments)
            created_segments = 0
                
            for i, (part, plate_name) in enumerate(segments, start=1):
                
                row = line_row.copy()
                row.geometry = part
                # On attribue le nom de la plaque 
                row["PLATE"] = plate_name
                new_features.append(row)
                created_segments +=1
                report.append({"layer": layer_line,"fid": idx_line+1,"plate_name": plate_name,"partie": f"{i}/{nb_parts}","longueur_avant": line_geom.length,"longueur_apres": part.length,"type_modif": "Découpage"})
        
        #On supprime la ligne ZDEM originale pour garder que le ssegments: 
        
            rows_to_remove.append(idx_line)
    
            modified_count += 1
            added_count += max(0, created_segments -1)
            modified_fid_geom.append({"layer": layer_line, "fid" : idx_line+1, "nbre_segments" : created_segments, "nbres_plaques_int" : len(intersected_plates), "Plaques" : ";".join(sorted(intersected_plates))})
              
        if rows_to_remove :
            gdf_out = gdf_out.drop(index=rows_to_remove, errors="ignore")
            
        # Onajoute les nouveaux segments :
        if len(new_features) > 0 :
            new_gdf = gpd.GeoDataFrame(new_features, columns=gdf_line.columns, crs=gdf_line.crs)
            result = pd.concat([gdf_out,new_gdf], ignore_index=True)
            
            result = gpd.GeoDataFrame(result, geometry="geometry", crs=gdf_line.crs)
            
        else :
            result = gdf_out
            
        #export :
        result.to_file(gpkg_line_output, layer=layer_line, driver ="GPKG")
        
    print("Géométries découpées :", modified_count)
    print("Géométries ajoutées:" , added_count)

# rapports :

pd.DataFrame(report).to_csv(report_out,index=False,encoding="utf-8-sig")

pd.DataFrame(modified_fid_geom).to_csv(report_fid_out,index=False,encoding="utf-8-sig")
        
print("Export done")
                
                
                