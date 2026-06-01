from osgeo import gdal, ogr
import geopandas as gpd
import fiona
import pandas as pd

# 1. Ouvrir la gdb: 
data = ogr.Open(r"C:\PANALESIS\PANv0\R_psAbs.gdb")

# 2. Layers 
#Combien on a de couches
layer_count = data.GetLayerCount()
print(layer_count)

#Get les diff ages et index et nom des couches de la gdb 
for i in range(layer_count):
    layer = data.GetLayerByIndex(i)
    print(i, layer.GetName())
    
#Si on prend que la couche R_psAbs_006 p.ex. 
layer006 = data.GetLayer(1)
print(layer006.GetName())
#Connaitre le nombre de features dans la couche 006 :
print("Name", layer.GetName())
print("Features", layer.GetFeatureCount())

#Appliqué à toutes les couches de la gdb :

for i in range (layer_count) :
    layer = data.GetLayerByIndex(i)
    print(i, "Name :", layer.GetName(), "Features:", layer.GetFeatureCount())

#3. Exporter les features de la couche 006 vers un GeoPackage

#Definir input et output path : 
input_directory = r"C:\PANALESIS\PANv0\R_psAbs.gdb"
output_directory = r"C:\PANALESIS\R_psAbs_output006.gpkg"

#Selectionner la couche 006
inputl006 = ogr.Open(input_directory)
layer006_input = inputl006.GetLayer(1)

#Spécifier qu'on veut GeoPackage et créer un file pour stocker la couche.gpkg
driver = ogr.GetDriverByName("GPKG")
output006 = driver.CreateDataSource(output_directory)
print(output006)

#Copier la couche dans le gpkg
layer006_output = output006.CopyLayer(layer006_input, layer006_input.GetName())

#4. Appliquer same thing pour toutes les couches (GeoPackage) :

input_directory = r"C:\PANALESIS\PANv0\R_psAbs.gdb"
output_directory = r"C:\PANALESIS\R_psAbs_output.gpkg"
input = ogr.Open(input_directory)
driver = ogr.GetDriverByName("GPKG")
output = driver.CreateDataSource(output_directory)
print(output)

for i in range (input.GetLayerCount()) :
    layers_input = data.GetLayerByIndex(i)
    output.CopyLayer(layers_input, layers_input.GetName())


#5. Exporter les features de la couche 006 vers un GeoJSON :
#Definir input et output path : 
input_directory = r"C:\PANALESIS\PANv0\R_psAbs.gdb"
output_directory = r"C:\PANALESIS\R_psAbs_output006.geojson"

#Selectionner la couche 006
inputl006 = ogr.Open(input_directory)
layer006_input = inputl006.GetLayer(1)

#Spécifier qu'on veut GeoJSON et créer un file pour stocker la couche.geojson
driver = ogr.GetDriverByName("GEOJSON")
output006 = driver.CreateDataSource(output_directory)
print(output006)

#Copier la couche dans le gpkg
layer006_output = output006.CopyLayer(layer006_input, layer006_input.GetName())

#6. Appliquer same thing pour toutes les couches (GeoJSON) : 

input_directory = r"C:\PANALESIS\PANv0\R_psAbs.gdb"
output_directory = r"C:\PANALESIS\R_psAbs_output.geojson"
input = ogr.Open(input_directory)
driver = ogr.GetDriverByName("GEOJSON")

#créer liste avec toutes les couches 

layers = fiona.listlayers(input_directory)
all_features = []

for layer in layers:
    gdf = gpd.read_file(input_directory, layer=layer)
    
     # Ajouter le nom de la couche
    gdf["layer"] = layer
    
    all_features.append(gdf)
    
print(all_features)

# Fusion de toutes les couches
gdf_all = gpd.GeoDataFrame(pd.concat(all_features))
print(gdf_all)


# Export GeoJSON
gdf_all.to_file("output_RpsAbs.geojson", driver="GeoJSON")
print("export done")