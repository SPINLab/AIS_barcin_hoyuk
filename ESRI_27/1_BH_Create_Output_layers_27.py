# This script is developed by Maurice de Kleijn SPINlab Vrije Universiteit Amsterdam for Python 2.7
# It integrates all the vectorized GIS data for the Excavation of Barcin Hoyuk into one shapefile allowing to ask queries over multiple layers.
# This script is step 1 Step 2 is to create a mxd for it 2_Make_MXD.py (to be used in ArcMap 10.3)

import os
import arcpy

print
"BEFORE CONTINUING PLEASE DELETE:"
print
""
print
"1. The previously (if present) generated OUTPUT folder: e.g. C:\Dropbox\..\AIS_Barcin_Hoyuk_DB_GIS\ "
print
"2. All .txt files in root GIS folder: e.g. C:\Dropbox\..\AIS_Barcin_Hoyuk\AIS\GIS\:"
print
"     annotation_list.txt"
print
"     finds_samples.txt"
print
"     graphic_list.txt"
print
"     height_differences_list.txt"
print
"     heights_list.txt"
print
"     list_folders_plans.txt"
print
"     locus_list.txt"
print
"     unclear_limits.txt"
print
"     underlying_level_lines.txt"
print
"     underlying_level_polygons.txt"
print
""

org_GIS = raw_input("Fill in path to GIS folder, eg C:\Dropbox\..\AIS_Barcin_Hoyuk\AIS\GIS\: ")
loc_output = raw_input("Fill in path where to create OUTPUT folder:, eg C:\Dropbox\..\AIS_Barcin_Hoyuk_DB_GIS\: ")
org_template = org_GIS + "Templates\Trench_Template\RENAME_template"
org_locus = org_GIS + "Templates\Trench_Template\RENAME_template\_locus.shp"
org_heights = org_GIS + "Templates\Trench_Template\RENAME_template\_heights.shp"
org_height_differences = org_GIS + "Templates\Trench_Template\RENAME_template\_height_differences.shp"
org_graphic = org_GIS + "Templates\Trench_Template\RENAME_template\_graphic.shp"
org_finds_samples = org_GIS + "Templates\Trench_Template\RENAME_template\_finds_samples.shp"
org_annotation = org_GIS + "Templates\Trench_Template\RENAME_template\_annotation.shp"
org_unclear_limits = org_GIS + "Templates\Trench_Template\RENAME_template\_unclear_limits.shp"
org_underlying_level_lines = org_GIS + "Templates\Trench_Template\RENAME_template\_underlying_level_lines.shp"
org_underlying_level_polygons = org_GIS + "Templates\Trench_Template\RENAME_template\_underlying_level_polygons.shp"

os.system('md ' + loc_output + 'OUTPUT')
arcpy.env.workspace = org_template
arcpy.CopyFeatures_management(org_locus, loc_output + 'OUTPUT/BH_locus.shp')
arcpy.CopyFeatures_management(org_heights, loc_output + 'OUTPUT/BH_heights.shp')
arcpy.CopyFeatures_management(org_height_differences, loc_output + 'OUTPUT/BH_height_differences.shp')
arcpy.CopyFeatures_management(org_graphic, loc_output + 'OUTPUT/BH_graphic.shp')
arcpy.CopyFeatures_management(org_finds_samples, loc_output + 'OUTPUT/BH_finds_samples.shp')
arcpy.CopyFeatures_management(org_annotation, loc_output + 'OUTPUT/BH_annotation.shp')
arcpy.CopyFeatures_management(org_unclear_limits, loc_output + 'OUTPUT/BH_unclear_limits.shp')
arcpy.CopyFeatures_management(org_underlying_level_lines, loc_output + 'OUTPUT/BH_underlying_level_lines.shp')
arcpy.CopyFeatures_management(org_underlying_level_polygons, loc_output + 'OUTPUT/BH_underlying_level_polygons.shp')

# Add filename to shapefile
# step 1 make a file list

os.system('dir ' + org_GIS + ' /s/d/b/A:D >' + org_GIS + 'list_folders_plans.txt')

file1 = open(org_GIS + 'list_folders_plans.txt', 'r')
lines = file1.readlines()
# step 2 add the filename to shapefile columnname is shpname
for line in lines:
    arcpy.env.workspace = line.rstrip('\n')
    fcs = arcpy.ListFeatureClasses()
    # print fcs
    for fc in fcs:
        arcpy.AddField_management(fc, 'shpname', 'text')
        arcpy.CalculateField_management(fc, 'shpname', '"' + fc + '"')

file1.close()

# Append all the LOCUS files to output shape
os.system("dir " + org_GIS + "*_locus.shp /s/d/b >" + org_GIS + "locus_list.txt")

file2 = open(org_GIS + "locus_list.txt", "r")
lines = file2.readlines()
file2.close()

file3 = open(org_GIS + "locus_list.txt", "w")

for line in lines:
    if "TEMP" not in line:
        file3.write(line)

file3.close()

file4 = open(org_GIS + 'locus_list.txt', 'r')
lines = file4.readlines()

for line in lines:
    arcpy.env.workspace = loc_output + 'OUTPUT'
    arcpy.Append_management([line[:-1]], loc_output + 'OUTPUT/BH_locus.shp')
    print(line)
file4.close()

arcpy.AddField_management(loc_output + 'OUTPUT/BH_locus.shp', 'joinfld', 'text')
arcpy.CalculateField_management(loc_output + 'OUTPUT/BH_locus.shp', 'joinfld', '[Trench]&"_"&[Locus]')

# Append all the ANNOTATION files to output shape
os.system("dir " + org_GIS + "*_annotation.shp /s/d/b >" + org_GIS + "annotation_list.txt")

file5 = open(org_GIS + 'annotation_list.txt', 'r')
lines = file5.readlines()

for line in lines:
    arcpy.env.workspace = loc_output + 'OUTPUT'
    arcpy.Append_management([line[:-1]], loc_output + 'OUTPUT/BH_annotation.shp')
    print(line)

file5.close()

# Append all the HEIGHTS files to output shape
os.system("dir " + org_GIS + "*_heights.shp /s/d/b >" + org_GIS + "heights_list.txt")

file6 = open(org_GIS + 'heights_list.txt', 'r')
lines = file6.readlines()

for line in lines:
    arcpy.env.workspace = loc_output + 'OUTPUT'
    arcpy.Append_management([line[:-1]], loc_output + 'OUTPUT/BH_heights.shp')
    print(line)

file6.close()

# Append all the HEIGHT DIFFERENCES files to output shape
os.system("dir " + org_GIS + "*_height_differences.shp /s/d/b >" + org_GIS + "height_differences_list.txt")

file7 = open(org_GIS + 'height_differences_list.txt', 'r')
lines = file7.readlines()

for line in lines:
    arcpy.env.workspace = loc_output + 'OUTPUT'
    arcpy.Append_management([line[:-1]], loc_output + 'OUTPUT/BH_height_differences.shp')
    print(line)

file7.close()

# Append all the GRAPHIC files to output shape
os.system("dir " + org_GIS + "*_graphic.shp /s/d/b >" + org_GIS + "graphic_list.txt")

file8 = open(org_GIS + 'graphic_list.txt', 'r')
lines = file8.readlines()

for line in lines:
    arcpy.env.workspace = loc_output + 'OUTPUT'
    arcpy.Append_management([line[:-1]], loc_output + 'OUTPUT/BH_graphic.shp')
    print(line)

file8.close()

# Append all the FIND SAMPLES files to output shape
os.system("dir " + org_GIS + "*_finds_samples.shp /s/d/b >" + org_GIS + "finds_samples.txt")

file9 = open(org_GIS + 'finds_samples.txt', 'r')
lines = file9.readlines()

for line in lines:
    arcpy.env.workspace = loc_output + 'OUTPUT'
    arcpy.Append_management([line[:-1]], loc_output + 'OUTPUT/BH_finds_samples.shp')
    print(line)

file9.close()

# Append all the UNCLEAR LIMITS files to output shape
os.system("dir " + org_GIS + "*_unclear_limits.shp /s/d/b >" + org_GIS + "unclear_limits.txt")

file10 = open(org_GIS + 'unclear_limits.txt', 'r')
lines = file10.readlines()

for line in lines:
    arcpy.env.workspace = loc_output + 'OUTPUT'
    arcpy.Append_management([line[:-1]], loc_output + 'OUTPUT/BH_unclear_limits.shp')
    print(line)

file10.close()

# Append all the "underlying_level_lines" files to output shape
os.system("dir " + org_GIS + "*_underlying_level_lines.shp /s/d/b >" + org_GIS + "underlying_level_lines.txt")

file11 = open(org_GIS + 'underlying_level_lines.txt', 'r')
lines = file11.readlines()

for line in lines:
    arcpy.env.workspace = loc_output + 'OUTPUT'
    arcpy.Append_management([line[:-1]], loc_output + 'OUTPUT/BH_underlying_level_lines.shp')
    print(line)

file11.close()

# Append all the "underlying_level_polygons" files to output shape
os.system("dir " + org_GIS + "*_underlying_level_polygons.shp /s/d/b >" + org_GIS + "underlying_level_polygons.txt")

file12 = open(org_GIS + 'underlying_level_polygons.txt', 'r')
lines = file12.readlines()

for line in lines:
    arcpy.env.workspace = loc_output + 'OUTPUT'
    arcpy.Append_management([line[:-1]], loc_output + 'OUTPUT/BH_underlying_level_polygons.shp')
    print(line)

file12.close()

# Perform dissolve and create centroids for every locus (making them unique for spatial analysis)

BH_locus = loc_output + "OUTPUT/BH_locus.shp"
BH_locus_diss = loc_output + "OUTPUT/BH_locus_diss.shp"
BH_locus_point = loc_output + "OUTPUT/BH_locus_points.shp"

# Process: Dissolve
arcpy.Dissolve_management(BH_locus, BH_locus_diss, "Trench;Locus;joinfld", "", "MULTI_PART", "DISSOLVE_LINES")

# Process: Feature To Point
arcpy.FeatureToPoint_management(BH_locus_diss, BH_locus_point, "CENTROID")

print
"The script was successful!!! Press ENTER to close"
raw_input()
