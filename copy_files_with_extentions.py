#This script allows you to copy all files with a certain extention to a new folder without integrating the sub folders
#Created by Maurice de Kleijn Vrije Universiteit Amsterdam Spatial Information laboratory for the datamanagement of the the archaological project Barin Hoyuk
#22062016 Python 2.7

import shutil
import os

org_GIS = raw_input("provide path to GIS folder in dropbox : eg. C:\Dropbox\Barcin_Hoyuk\AIS_Barcin_Hoyuk\AIS\GIS\\: ")
outputfolder = raw_input("provide path to output folder : eg. C:\Temp\: ")
ext = raw_input("provide extention type to be copied eg .tif or .jpg :")

os.system ('dir '+org_GIS+'*'+ext+' /s/d/b >'+org_GIS+'tempext.txt')

file1 = open(org_GIS+'tempext.txt', 'r')
lines = file1.readlines()

for line in lines:
	ln = line.rstrip('\n')
	shutil.copy (ln, outputfolder)	
file1.close()

os.system ('del '+org_GIS+'tempext.txt')

raw_input ("done!")
