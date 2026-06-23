import geopandas as gpd
import pandas as pd
import fiona


gpkg_plate = r"C:\PANALESIS\outputs\Plates_ps_Abs_valid.gpkg"
gpkg_line = r"C:\PANALESIS\outputs\R_psAbs_names_maj_harmo_clean_points.gpkg"
layer_Plate = fiona.listlayers("C:\PANALESIS\outputs\Plates_ps_Abs_valid.gpkg")
layer_line = fiona.listlayers("C:\PANALESIS\outputs\R_psAbs_names_maj_harmo_clean_points.gpkg")
report_out = r"C:\PANALESIS\Report\report_ZDEM_check_intersection.txt"

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

report = []

for layer_line, layer_plate in corres_layers_rev.items():

    print("Traitement :", layer_line)

    gdf_plate = gpd.read_file(gpkg_plate, layer=layer_plate)
    gdf_line = gpd.read_file(gpkg_line, layer=layer_line)
    
    
    mask_zdem = gdf_line["PLATE"].astype(str).str.strip().str.upper().isin(["ZDEM", "Z_DEM"]) #prend en compte également si espace et maj
    zdem_lines = gdf_line[mask_zdem].copy()
    print(layer_line)
    print("Total lignes:", len(gdf_line))
    print("ZDEM détectées:", mask_zdem.sum())
    print("ZDEM filtrées:", len(zdem_lines))
    
    
    for idx_line, line_row in zdem_lines.iterrows():

        line_geom = line_row.geometry

        intersected_plates = []

        for _, plate_row in gdf_plate.iterrows():

            inter = line_geom.intersection(plate_row.geometry)

            if inter.is_empty:
                    continue

            # Ignore les contacts ponctuels petits, changer ?
            if inter.length > 1e-8:

                intersected_plates.append(plate_row["PlateName"])

        intersected_plates = sorted(list(set(intersected_plates)))
    
        report.append({"layer": layer_line,"fid": idx_line+1 ,"nb_plaques": len(intersected_plates),"plaques": "; ".join(intersected_plates)})
        

report_df = pd.DataFrame(report)

report_df.to_csv(report_out,index=False,encoding="utf-8-sig")

print("Rapport exporté")

#résumé statistique : 

report_stats_out = r"C:\PANALESIS\Report\report_ZDEM_check_intersection_stats.txt"

stats = (report_df.groupby(["layer", "nb_plaques"]).size().reset_index(name="nb_lignes"))

with open(report_stats_out, "w", encoding="utf-8") as f:

    f.write("STATISTIQUES DES INTERSECTIONS ZDEM\n")
    f.write("=" * 60 + "\n\n")

    for layer in stats["layer"].unique():

        f.write(f"COUCHE : {layer}\n")
        f.write("-" * 40 + "\n")

        layer_stats = stats[stats["layer"] == layer]

        total = layer_stats["nb_lignes"].sum()

        f.write(f"Total ZDEM : {total}\n\n")

        for _, row in layer_stats.iterrows():

            f.write(f"{row['nb_plaques']} plaque(s) : "f"{row['nb_lignes']} ligne(s)\n")

        f.write("\n")

print(stats)