from osgeo import gdal, ogr
import geopandas as gpd
import pandas as pd
import fiona 

path = r"C:\PANALESIS\Vers0_christian\COB_psAbs_output.gpkg"

layers = fiona.listlayers(path)

#Connaitre les polygones qui dépassent les limites des bornes longitudes [-180,180] :
for layer in layers:
    gdf = gpd.read_file(path, layer=layer)

    print("Couche :",layer)
    print(gdf.head())
     # Vérifier les géométries
    for idx, geom in enumerate(gdf.geometry):

        # Bornes (-180 à +180) : minx, miny, maxx, maxy
        minx, miny, maxx, maxy = geom.bounds

        # Hors limites
        if minx < -180 or maxx > 180:
            print("Polygone dépasse les limites longitudes")
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
        
#Tout est ok pour les latitudes 

#Avec shapely test longitudes sur les sommets des multipolygons pour identifier les sommets hors limite:

from shapely.geometry import MultiPolygon

for layer in layers:
    gdf = gpd.read_file(path, layer=layer)
    for poly in geom.geoms:
        for x, y in poly.exterior.coords:
             if x < -180 or x > 180:
                print("Couche :",layer, "Longitude invalide :", x)


#Correction des géométries et export :

from shapely.ops import transform
import numpy as np

#fonction pour clip dans l'interval :

def clip_lon_lat(x, y):
    if abs(x) > 180 or abs(x) < -180:
        x = np.clip(x, -180, 180)
    if abs(y) > 90 or abs(y) < -90:
        y = np.clip(y, -90, 90)
    return (x, y)

#appliquer à toutes les couches et export : 


output_directory = r"C:\PANALESIS\Vers0_christian\COB_psAbs_output_bounds_clean.gpkg"



for layer in layers:
    
    gdf = gpd.read_file(path, layer=layer)

    gdf["geometry"] = gdf["geometry"].apply(lambda geom: transform(clip_lon_lat, geom))
    gdf.to_file(output_directory, layer=layer, driver="GPKG")
    
print("export done")

#Verification géométrie sur le nouveau gpkg corrigé : 

for layer in layers:
    path = r"C:\PANALESIS\Vers0_christian\COB_psAbs_output_bounds_clean.gpkg"
    gdf = gpd.read_file(path, layer=layer)

    print("Couche :",layer)
    print(gdf.head())
     # Vérifier les géométries
    for idx, geom in enumerate(gdf.geometry):

        # Bornes (-180 à +180) : minx, miny, maxx, maxy
        minx, miny, maxx, maxy = geom.bounds

        # Hors limites
        if minx < -180 or maxx > 180:
            print("Polygone dépasse les limites longitudes")
            print("minx=", minx, "maxx=",maxx)