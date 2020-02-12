# This is step 2 to create mxd file of the archaeological Barcin Hoyuk project to be used in ArcMap 10.3

import os
import arcpy
from arcpy import env

print
"BEFORE CONTINUING PLEASE DELETE:"
print
""
print
"1. 'locus_list.txt' which is stored in the TEMPLATE folder : e.g. C:\Dropbox\Barcin_Hoyuk\AIS_Barcin_Hoyuk_DB_GIS\TEMPLATE\lists\locus_list.txt "
print
""

# Create list of all locus.shp BEGIN

org_GIS = raw_input("Path to GIS folder: e.g. c:\Dropbox\...\AIS_Barcin_Hoyuk\AIS\GIS\ (Note \ at the end of path!): ")
template_fld = raw_input("Path to Template folder: e.g. c:\Dropbox\...\AIS_Barcin_Hoyuk_DB_GIS\TEMPLATE\: ")
output_fld = raw_input(
    "Path to Output folder which has been specified executing BH_Create_Output_layers_add_locus_field.py : e.g. C:\Dropbox\...\AIS_Barcin_Hoyuk_DB_GIS\OUTPUT\: ")
os.system("dir " + org_GIS + "*_locus.shp /s/d >" + template_fld + "lists\locus_list_2.txt")

file2 = open("" + template_fld + "lists\locus_list_2.txt", "r")
lines = file2.readlines()
file2.close()

file3 = open("" + template_fld + "lists\locus_list_2.txt", "w")

for line in lines:
    if "TEMP" not in line:
        file3.write(line)

file3.close()

file4 = open("" + template_fld + "lists\locus_list_2.txt", "r")
lines = file4.readlines()
file4.close()

file5 = open("" + template_fld + "lists\locus_list_2.txt", "w")

for line in lines:
    if ".shp" in line:
        file5.write(line)

file5.close()

# Create list of all locus.shp END

# get the map document
mxd = arcpy.mapping.MapDocument("" + template_fld + "Barcin_GIS_Template.mxd")
# get the data frame
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]

# create a new layer and add layer
locus_diss = arcpy.mapping.Layer("" + template_fld + "layer_files\BH_locus_diss.lyr")
locus_diss.visible = True
arcpy.mapping.AddLayer(df, locus_diss, "TOP")

locus = arcpy.mapping.Layer("" + template_fld + "layer_files\BH_locus.lyr")
locus.visible = True
arcpy.mapping.AddLayer(df, locus, "TOP")

locus_points = arcpy.mapping.Layer("" + template_fld + "layer_files\BH_locus_points.lyr")
locus_points.visible = True
arcpy.mapping.AddLayer(df, locus_points, "TOP")

heights = arcpy.mapping.Layer("" + template_fld + "layer_files\BH_heights.lyr")
heights.visible = False
arcpy.mapping.AddLayer(df, heights, "TOP")

annotation = arcpy.mapping.Layer("" + template_fld + "layer_files\BH_annotation.lyr")
annotation.visible = False
arcpy.mapping.AddLayer(df, annotation, "TOP")

finds_samples = arcpy.mapping.Layer("" + template_fld + "layer_files\BH_finds_samples.lyr")
finds_samples.visible = False
arcpy.mapping.AddLayer(df, finds_samples, "TOP")

graphic = arcpy.mapping.Layer("" + template_fld + "layer_files\BH_graphic.lyr")
graphic.visible = False
arcpy.mapping.AddLayer(df, graphic, "TOP")

height_differences = arcpy.mapping.Layer("" + template_fld + "layer_files\BH_height_differences.lyr")
height_differences.visible = False
arcpy.mapping.AddLayer(df, height_differences, "TOP")

unclear_limits = arcpy.mapping.Layer("" + template_fld + "layer_files\BH_unclear_limits.lyr")
unclear_limits.visible = False
arcpy.mapping.AddLayer(df, unclear_limits, "TOP")

underlying_level_lines = arcpy.mapping.Layer("" + template_fld + "layer_files\BH_underlying_level_lines.lyr")
underlying_level_lines.visible = False
arcpy.mapping.AddLayer(df, underlying_level_lines, "TOP")

underlying_level_polygons = arcpy.mapping.Layer("" + template_fld + "layer_files\BH_underlying_level_polygons.lyr")
underlying_level_polygons.visible = False
arcpy.mapping.AddLayer(df, underlying_level_polygons, "TOP")

file6 = open("" + template_fld + "lists\locus_list_2.txt", "r")
BHlayer2 = file6.readlines()

for line in BHlayer2:
    BHLayer = line.strip('\n').rstrip().strip('_locus.shp')
    locus.definitionQuery = '"BH_locus.shpname"=' + "'" + BHLayer + "_locus.shp'"
    heights.definitionQuery = '"shpname"=' + "'" + BHLayer + "_heights.shp'"
    graphic.definitionQuery = '"shpname"=' + "'" + BHLayer + "_graphic.shp'"
    annotation.definitionQuery = '"shpname"=' + "'" + BHLayer + "_annotation.shp'"
    height_differences.definitionQuery = '"shpname"=' + "'" + BHLayer + "_height_differences.shp'"
    finds_samples.definitionQuery = '"shpname"=' + "'" + BHLayer + "_finds_samples.shp'"
    unclear_limits.definitionQuery = '"shpname"=' + "'" + BHLayer + "_unclear_limits.shp'"
    underlying_level_lines.definitionQuery = '"shpname"=' + "'" + BHLayer + "_underlying_level_lines.shp'"
    underlying_level_polygons.definitionQuery = '"shpname"=' + "'" + BHLayer + "_underlying_level_polygons.shp'"

    # Add Group layer from layer file
    insertGroupLayer = arcpy.mapping.Layer("" + template_fld + "layer_files\group1.lyr")
    arcpy.mapping.AddLayer(df, insertGroupLayer, "BOTTOM")

    # List layer group1
    targetGroupLayer = arcpy.mapping.ListLayers(mxd, "Group1", df)[0]

    layers = arcpy.mapping.ListLayers(mxd)
    for lyr in layers:
        if lyr.name == "Group1":
            lyr.name = BHLayer
            lyr.visible = False
    arcpy.RefreshTOC()

    targetGroupLayer1 = arcpy.mapping.ListLayers(mxd, BHLayer, df)[0]
    arcpy.mapping.AddLayerToGroup(df, targetGroupLayer1, heights, "BOTTOM")
    arcpy.mapping.AddLayerToGroup(df, targetGroupLayer1, graphic, "BOTTOM")
    arcpy.mapping.AddLayerToGroup(df, targetGroupLayer1, annotation, "BOTTOM")
    arcpy.mapping.AddLayerToGroup(df, targetGroupLayer1, height_differences, "BOTTOM")
    arcpy.mapping.AddLayerToGroup(df, targetGroupLayer1, finds_samples, "BOTTOM")
    arcpy.mapping.AddLayerToGroup(df, targetGroupLayer1, unclear_limits, "BOTTOM")
    arcpy.mapping.AddLayerToGroup(df, targetGroupLayer1, underlying_level_lines, "BOTTOM")
    arcpy.mapping.AddLayerToGroup(df, targetGroupLayer1, underlying_level_polygons, "BOTTOM")
    arcpy.mapping.AddLayerToGroup(df, targetGroupLayer1, locus, "BOTTOM")
    locus.visible = True
    unclear_limits.visible = False
    underlying_level_lines.visible = False
    underlying_level_polygons.visible = False
    height_differences.visible = False
    graphic.visible = False
    annotation.visible = False
    finds_samples.visible = False
    heights.visible = False
    print
    BHLayer

res_mxd = raw_input(
    "Path + name where to save the output mxd : e.g. c:\Dropbox\...\AIS_Barcin_Hoyuk_DB_GIS\BH_GIS.mxd: (DON'T FORGET .mxd) ")
mxd.saveACopy(res_mxd)

print
"The script was successful!!! Press ENTER to close"
raw_input()
