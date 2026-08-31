import geopandas as gpd
import pandas as pd
import fiona

gpkg_plate = r"C:\PANALESIS\outputs\Plates_ps_Abs_valid.gpkg"
gpkg_line = r"C:\PANALESIS\outputs\R_psAbs_names_maj_harmo_clean_points.gpkg"
layer_Plate = fiona.listlayers("C:\PANALESIS\outputs\Plates_ps_Abs_valid.gpkg")
layer_line = fiona.listlayers("C:\PANALESIS\outputs\R_psAbs_names_maj_harmo_clean_points.gpkg")
output =  r"C:\PANALESIS\outputs\R_psAbs_zdem_unique_int_filled.gpkg"

# Mapping de correspondance entre les noms des couches des deux gpkg:

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

total_zdem = 0
total_noms_attribues = 0


for layer_line, layer_plate in corres_layers_rev.items():

    print("Traitement :", layer_line)
    attributed_layer = 0

    gdf_plate = gpd.read_file(gpkg_plate, layer=layer_plate)
    gdf_line = gpd.read_file(gpkg_line, layer=layer_line)
    
    # Selectionner les lignes ZDEM et Z_DEM :
    
    mask_zdem = gdf_line["PLATE"].astype(str).str.strip().str.upper().isin(["ZDEM", "Z_DEM"]) #prend en compte également si espace et maj
    zdem_lines = gdf_line[mask_zdem].copy()
    print(layer_line)
    print("Total lignes:", len(gdf_line))
    print("ZDEM détectées:", mask_zdem.sum())

    # Identidication des intersections :
    
    for idx_line, line_row in zdem_lines.iterrows():

        line_geom = line_row.geometry

        intersected_plates = []

        for _, plate_row in gdf_plate.iterrows():
            plate_geom = plate_row.geometry

            inter = line_geom.intersection(plate_geom)

            if inter.is_empty:
                    continue

            # Si il y a intersection :
            
            if inter.length > 0 : # Ecarte les cas ou touche uniquement la plaque en un point
                intersected_plates.append(plate_row["PlateName"])

        intersected_plates = sorted(list(set(intersected_plates))) # Supprimer les doublons dans le cas où la la ligne intersecte plusieurs fois la même plaque 
        
        # Cas d'intersection avec une seule plaque :
        
        if len(intersected_plates) == 1:
            
             plate_name = intersected_plates[0]
             new_name = (f"{plate_name}")  # Nouveau nom attribué
             gdf_line.at[idx_line, "PLATE"] = new_name  # Modifcation pour l'attribut "PLATE" 
             attributed_layer +=1
             total_noms_attribues += 1
    print("total noms attribues :", attributed_layer)    
             
             
    gdf_line.to_file(output, layer=layer_line, driver="GPKG")
    print("export done")