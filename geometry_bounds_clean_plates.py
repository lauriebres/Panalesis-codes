from osgeo import gdal, ogr
import geopandas as gpd
import pandas as pd
import fiona 

path = r"C:\PANALESIS\Vers0_christian\Plates_psAbs_output.gpkg"

layers = fiona.listlayers(path)

#Connaitre les polygones qui dépassent les limites des bornes longitudes [-180,180] :
for layer in layers:
    gdf = gpd.read_file(path, layer=layer)

    print("Couche :",layer)
    print(gdf)
     # Vérifier les géométries
    for idx, geom in enumerate(gdf.geometry):

        # Bornes (-180 à +180) : minx, miny, maxx, maxy
        minx, miny, maxx, maxy = geom.bounds

        # Hors limites
        if minx < -180 or maxx > 180:
            print("FID:", idx, "Polygone dépasse les limites longitudes") #Ici, plus d'un polygone par couche donc indentification avec index
            print("minx=", minx, "maxx=",maxx)
        
#Connaitre les polygones qui dépassent les limites des bornes latitudes [-90, 90] :
for layer in layers:
    gdf = gpd.read_file(path, layer=layer)

    print("Couche :",layer)
    print(gdf.head())
     # Vérifier les géométries
    for idx, geom in enumerate(gdf.geometry):

        # Bornes (-90 à +90) : minx, miny, maxx, maxy
        minx, miny, maxx, maxy = geom.bounds

        # Hors limites
        if miny < -90 or maxy > 90:
            print("Polygone dépasse les limites latitudes")
            print("miny=", minx, "maxy=",maxx)
            
            
#Afficher uniquement les lignes avec des geométries NONE avec le nom de la couche, et leur index :
for layer in layers :
    gdf = gpd.read_file("C:\PANALESIS\Vers0_christian\Plates_psAbs_output.gpkg", layer = layer)
    none_rows = gdf[gdf.geometry.isna()]
    print("couche :", layer, id, none_rows)
    
    
output_directory = r"C:\PANALESIS\Vers0_christian\Plates_psAbs_output_bounds_clean.gpkg"



for layer in layers:
    
    gdf = gpd.read_file(path, layer=layer)

    gdf["geometry"] = gdf["geometry"].apply(lambda geom: transform(clip_lon_lat, geom))
    gdf.to_file(output_directory, layer=layer, driver="GPKG")
    
print("export done")

