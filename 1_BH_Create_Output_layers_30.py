# This script is developed by Maurice de Kleijn SPINlab Vrije Universiteit Amsterdam for Python 3 and uses ArcGIS Pro´s Arcpy 3.0.2. It is an updated version of a 2.7 script that used ArcPy from Arcmap 10.3.
# It integrates all the vectorized GIS data for the Excavation of Barcin Hoyuk into one shapefile allowing to ask queries over multiple layers.

import arcpy
import os


print("BEFORE CONTINUING PLEASE DELETE:")
print("")
print("1. The previously (if present) generated OUTPUT folder: e.g. C:\Dropbox\..\AIS_Barcin_Hoyuk_DB_GIS\ ")
print("2. All .txt files in root GIS folder: e.g. C:\Dropbox\..\AIS_Barcin_Hoyuk\AIS\GIS\:")
print(" annotation_list.txt")
print(" finds_samples.txt")
print(" graphic_list.txt")
print(" height_differences_list.txt")
print(" heights_list.txt")
print(" list_folders_plans.txt")
print(" locus_list.txt")
print(" unclear_limits.txt")
print(" underlying_level_lines.txt")
print(" underlying_level_polygons.txt")
print("")

org_GIS = input("Fill in path to GIS folder, eg C:\Dropbox\..\AIS_Barcin_Hoyuk\AIS\GIS\: ")
loc_output = input("Fill in path where to create OUTPUT folder:, eg C:\Dropbox\..\AIS_Barcin_Hoyuk_DB_GIS\: ")
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
arcpy.management.CopyFeatures(org_locus, loc_output + 'OUTPUT/BH_locus.shp')
arcpy.management.CopyFeatures(org_heights, loc_output + 'OUTPUT/BH_heights.shp')
arcpy.management.CopyFeatures(org_height_differences, loc_output + 'OUTPUT/BH_height_differences.shp')
arcpy.management.CopyFeatures(org_graphic, loc_output + 'OUTPUT/BH_graphic.shp')
arcpy.management.CopyFeatures(org_finds_samples, loc_output + 'OUTPUT/BH_finds_samples.shp')
arcpy.management.CopyFeatures(org_annotation, loc_output + 'OUTPUT/BH_annotation.shp')
arcpy.management.CopyFeatures(org_unclear_limits, loc_output + 'OUTPUT/BH_unclear_limits.shp')
arcpy.management.CopyFeatures(org_underlying_level_lines, loc_output + 'OUTPUT/BH_underlying_level_lines.shp')
arcpy.management.CopyFeatures(org_underlying_level_polygons, loc_output + 'OUTPUT/BH_underlying_level_polygons.shp')

# Add filename to shapefile
# step 1 make a file list

os.system(f'dir {org_GIS} /s/d/b/A:D > {org_GIS}list_folders_plans.txt')

with open(f'{org_GIS}list_folders_plans.txt', 'r') as file1:
    lines = file1.readlines()

# step 2 add the filename to shapefile columnname is shpname
for line in lines:
    arcpy.env.workspace = line.rstrip('\n')
    fcs = arcpy.ListFeatureClasses()

    for fc in fcs:
        arcpy.AddField_management(fc, 'shpname', 'text')
        arcpy.CalculateField_management(fc, 'shpname', f'"{fc}"')

# Append all the LOCUS files to output shape
os.system(f'dir {org_GIS}*_locus.shp /s/d/b > {org_GIS}locus_list.txt')

with open(f'{org_GIS}locus_list.txt', 'r') as file2:
    lines = file2.readlines()

with open(f'{org_GIS}locus_list.txt', 'w') as file3:
    for line in lines:
        if 'TEMP' not in line:
            file3.write(line)

with open(f'{org_GIS}locus_list.txt', 'r') as file4:
    lines = file4.readlines()

for line in lines:
    arcpy.env.workspace = f'{loc_output}OUTPUT'
    arcpy.Append_management([line[:-1]], f'{loc_output}OUTPUT\BH_locus.shp')
    print(line)

arcpy.AddField_management(f'{loc_output}OUTPUT/BH_locus.shp', 'joinfld', 'text')
arcpy.management.CalculateField(f'{loc_output}OUTPUT/BH_locus.shp', 'joinfld', '!Trench! +"_"+ str(!Plan!)')

# Append all the ANNOTATION files to output shape
os.system(f'dir {org_GIS}*_annotation.shp /s/d/b > {org_GIS}annotation_list.txt')

with open(f'{org_GIS}annotation_list.txt', 'r') as file5:
    lines = file5.readlines()

for line in lines:
    arcpy.env.workspace = f'{loc_output}OUTPUT'
    arcpy.Append_management([line[:-1]], f'{loc_output}OUTPUT/BH_annotation.shp')
    print(line)

# Append all the HEIGHTS files to output shape
os.system(f'dir {org_GIS}*_heights.shp /s/d/b > {org_GIS}heights_list.txt')

with open(f'{org_GIS}heights_list.txt', 'r') as file6:
    lines = file6.readlines()

for line in lines:
    arcpy.env.workspace = f'{loc_output}OUTPUT'
    arcpy.Append_management([line[:-1]], f'{loc_output}OUTPUT/BH_heights.shp')
    print(line) 

# Append all the HEIGHT DIFFERENCES files to output shape
os.system("dir " + org_GIS + "*_height_differences.shp /s/d/b >" + org_GIS + "height_differences_list.txt")

with open(org_GIS + 'height_differences_list.txt', 'r') as file7:
    lines = file7.readlines()

for line in lines:
    arcpy.env.workspace = loc_output + 'OUTPUT'
    arcpy.Append_management([line[:-1]], loc_output + 'OUTPUT/BH_height_differences.shp')
    print(line)

# Append all the GRAPHIC files to output shape
os.system("dir " + org_GIS + "*_graphic.shp /s/d/b >" + org_GIS + "graphic_list.txt")

with open(org_GIS + 'graphic_list.txt', 'r') as file8:
    lines = file8.readlines()

for line in lines:
    arcpy.env.workspace = loc_output + 'OUTPUT'
    arcpy.Append_management([line[:-1]], loc_output + 'OUTPUT/BH_graphic.shp')
    print(line)

# Append all the FIND SAMPLES files to output shape
os.system("dir " + org_GIS + "*_finds_samples.shp /s/d/b >" + org_GIS + "finds_samples.txt")

with open(org_GIS + 'finds_samples.txt', 'r') as file9:
    lines = file9.readlines()

for line in lines:
    arcpy.env.workspace = loc_output + 'OUTPUT'
    arcpy.Append_management([line[:-1]], loc_output + 'OUTPUT/BH_finds_samples.shp')
    print(line)

# Append all the UNCLEAR LIMITS files to output shape
os.system("dir " + org_GIS + "*_unclear_limits.shp /s/d/b >" + org_GIS + "unclear_limits.txt")

with open(org_GIS + 'unclear_limits.txt', 'r') as file10:
    lines = file10.readlines()

for line in lines:
    arcpy.env.workspace = loc_output + 'OUTPUT'
    arcpy.Append_management([line[:-1]], loc_output + 'OUTPUT/BH_unclear_limits.shp')
    print(line)

# Append all the "underlying_level_lines" files to output shape
os.system("dir " + org_GIS + "*_underlying_level_lines.shp /s/d/b >" + org_GIS + "underlying_level_lines.txt")

with open(org_GIS + 'underlying_level_lines.txt', 'r') as file11:
    lines = file11.readlines()

for line in lines:
    arcpy.env.workspace = loc_output + 'OUTPUT'
    arcpy.Append_management([line[:-1]], loc_output + 'OUTPUT/BH_underlying_level_lines.shp')
    print(line)

# Append all the "underlying_level_polygons" files to output shape
os.system("dir " + org_GIS + "*_underlying_level_polygons.shp /s/d/b >" + org_GIS + "underlying_level_polygons.txt")

with open(org_GIS + 'underlying_level_polygons.txt', 'r') as file12:
    lines = file12.readlines()

for line in lines:
    arcpy.env.workspace = loc_output + 'OUTPUT'
    arcpy.Append_management([line[:-1]], loc_output + 'OUTPUT/BH_underlying_level_polygons.shp')
    print(line)

# Perform dissolve and create centroids for every locus (making them unique for spatial analysis)
BH_locus = loc_output + "OUTPUT/BH_locus.shp"
BH_locus_diss = loc_output + "OUTPUT/BH_locus_diss.shp"
BH_locus_point = loc_output + "OUTPUT/BH_locus_points.shp"

#Process: Dissolve
arcpy.management.Dissolve(BH_locus, BH_locus_diss, ["Trench","Locus","joinfld"], None, "MULTI_PART", "DISSOLVE_LINES")

#Process: Feature To Point
arcpy.management.FeatureToPoint(BH_locus_diss, BH_locus_point, "CENTROID")

print("The script was successful!!! Press ENTER to close")
input()