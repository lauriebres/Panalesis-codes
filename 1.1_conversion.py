# Librairies :

from osgeo import gdal, ogr
import geopandas as gpd
import pandas as pd
import fiona 

# Données : 

path = r"C:\PANALESIS\Rot_plates\PlatesxxxpreRotyyy"
layers = fiona.listlayers(path)
output_gpkg = r"C:\PANALESIS\Rot_plates\Outputs\PlatesxxxpreRotyyy_outputs.gpkg"

# Conversion GPKG :

for layer in layers :
    gdf = gpd.read_file(path, layer = layer)
    gdf.to_file(output_gpkg, layer=layer, driver="GPKG")
    
print("Export terminé")



