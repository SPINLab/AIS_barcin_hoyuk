#Created by Maurice de Kleijn for the datamanagement of the the archaeological project Barin Hoyuk 16042024
#The purpose of this script is to merge all the shapefiles of the individual plans into one so it can be queried more easily in QGIS. This script only uses Free and Open Sources python libraries 

#Import the required libraries
import shutil 
import pandas as pd
import glob
import os
import geopandas as gpd
from shapely.geometry import Point

#Define the variables for the locations of the GIS files
org_GIS = input("Fill in path to GIS folder, eg C:\Dropbox\..\AIS_Barcin_Hoyuk\AIS\GIS\: ")
loc_output = input("Fill in path where to create OUTPUT folder:, eg C:\Dropbox\..\AIS_Barcin_Hoyuk_DB_GIS\: ")
#Create the output folder
os.system('md ' + loc_output + 'OUTPUT')

#Step 1 add the filename of the original shapefile as a collumn so it is always clear where an object came from.
#Create a list of all the shapefiles in the folder
file_pattern = '**/*.shp'
file_list = glob.glob(os.path.join(org_GIS, file_pattern), recursive=True)
#Remove the TEMP layer from the list
file_list = [f for f in file_list if '_TEMP' not in os.path.basename(f)]
#Remove all the template files from the list
file_list = [item for item in file_list if "RENAME" not in item]

#Read the list and add the shapefile name
for file in file_list:
    # Open the shapefile with Geopandas
    gdf = gpd.read_file(file)
    # Get the filename of the shapefile without the extension
    filename = os.path.splitext(os.path.basename(file))[0]

    # Add a new column to the attribute table and populate it with the filename
    gdf['shpname'] = (filename)

    # Save the modified shapefile
    gdf.to_file(file)

#Step 2-1 create the Locus layer
#Put all the locus files from the various folders in a list 
file_pattern = '**/*_locus.shp'
file_list = glob.glob(os.path.join(org_GIS, file_pattern), recursive=True)

#Remove the TEMP locus layer from the list
file_list = [f for f in file_list if '_TEMP' not in os.path.basename(f)]
#Remove all the template files from the list
file_list = [item for item in file_list if "RENAME" not in item]

#Merge all the locus files from the list
#Read in each shapefile as a GeoDataFrame
gdfs = [gpd.read_file(shapefile) for shapefile in file_list]

#Concatenate the GeoDataFrames into one
merged_gdf = pd.concat(gdfs, ignore_index=True)

#Convert back to a GeoDataFrame
merged_gdf = gpd.GeoDataFrame(merged_gdf, crs=gdfs[0].crs, geometry='geometry')

#Save the merged shapefile
merged_gdf.to_file(loc_output+'OUTPUT\\BH_locus.shp')
shp_output = loc_output+'OUTPUT\\BH_locus.shp'

#Step 2-2 Create the joinfld in the newly created locus file
#Read in the shapefile as a geopandas GeoDataFrame
gdf = gpd.read_file(shp_output)

col1 = 'Trench'
col2 = 'Locus'

# Add the new field to the GeoDataFrame
gdf['joinfld'] = gdf.apply(lambda row: row[col1] + '_' + str(int(row[col2])), axis=1)
# Write the updated GeoDataFrame to a new shapefile
gdf.to_file(shp_output)

#Step 2-3 Create centroid point with labels of locus
# Define the paths to locus polygon shp polygon and the point shapefile to be created
poly_path = loc_output+'OUTPUT\\BH_locus.shp'
point_path = loc_output+'OUTPUT\\BH_locus_points.shp'

# Open the polygon shapefile with Geopandas
poly_gdf = gpd.read_file(poly_path)

# Calculate the centroid of each polygon
centroids = poly_gdf['geometry'].centroid

# Create a new Geopandas GeoDataFrame with the centroids as points
point_gdf = gpd.GeoDataFrame(poly_gdf.drop('geometry', axis=1), crs=poly_gdf.crs, geometry=centroids)

# Save the new point shapefile
point_gdf.to_file(point_path)

#Step 3 Create merged layers for all other files
type_list = ['annotation','heights','height_differences','graphic','finds_samples','unclear_limits','underlying_level_lines','underlying_level_lines']

for item in type_list:
    file_pattern = '**/*_'+item+'.shp'
    file_list2 = glob.glob(os.path.join(org_GIS, file_pattern), recursive=True)
    file_list2 = [item for item in file_list2 if "RENAME" not in item]
    # read in each shapefile as a GeoDataFrame
    gdfs = [gpd.read_file(shapefile) for shapefile in file_list2]
    merged_gdf = pd.concat(gdfs, ignore_index=True)
    merged_gdf = gpd.GeoDataFrame(merged_gdf, crs=gdfs[0].crs, geometry='geometry')
    merged_gdf.to_file(loc_output+'OUTPUT\\BH_'+item+'.shp')
    file_list2 =[]

print("The script was successful!!! Press ENTER to close")
input()
