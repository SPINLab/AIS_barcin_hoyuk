"""
Created on Mon Oct  10/10/2019

@author: Maurice de Kleijn SPINlab VU

This script creates a list files stored on the server in order to update the links to these files in the database.
"""
import os
import time

pathname = raw_input ("Give path where the static data is stored (e.g. U:\\research-barcin-hoyuk\\STATIC_DATA\\): ")

list = ['PLANS','PICTURES','LOT_FORMS','SKETCHES','DAILY_REPORTS','OBJECT_DRAWINGS']
for item in list:

	os.system ('dir '+pathname+item+'\\ /s/d/b/A-D >'+pathname+'list_'+item+'_temp1.txt')
	time.sleep(20)
	textToSearch = (pathname+item+'\\')
	textToReplace = ('#https://vu-data.irodspoc-sara.surf-hosted.nl//research-barcin-hoyuk//STATIC_DATA//'+item+'//')
	fileToSearch  = (pathname+'list_'+item+'_temp1.txt')
	fileToStore1  = (pathname+'list_'+item+'_temp2.txt')

	os.system ('copy NUL >'+fileToStore1)

	replacements = {textToSearch:textToReplace}

	with open(fileToSearch,'r' ) as infile, open(fileToStore1, 'w') as outfile:
		for line in infile:
			for src, target in replacements.iteritems():
				line = line.replace(src, target)
			outfile.write(line)

	
	textToSearch2 = ('.tif')
	textToReplace2 = ('.tif#')
	textToSearch3 = ('.TIF')
	textToReplace3 = ('.TIF#')
	textToSearch4 = ('.jpg')
	textToReplace4 = ('.jpg#')
	textToSearch5 = ('.JPG')
	textToReplace5 = ('.JPG#')
	textToSearch6 = ('.pdf')
	textToReplace6 = ('.pdf#')
	textToSearch7 = ('.PDF')
	textToReplace7 = ('.PDF#')
	textToSearch8 = ('.bmp')
	textToReplace8 = ('.bmp#')
	
	replacements = {textToSearch2:textToReplace2,textToSearch3:textToReplace3,textToSearch4:textToReplace4,textToSearch5:textToReplace5,textToSearch6:textToReplace6,textToSearch7:textToReplace7,textToSearch8:textToReplace8}
		
	fileToStore2  = (pathname+'list_'+item+'.txt')

	os.system ('copy NUL >'+fileToStore2)
	
			
	with open(fileToStore1,'r' ) as infile, open(fileToStore2, 'w') as outfile:
		for line in infile:
			for src, target in replacements.iteritems():
				line = line.replace(src, target)
			outfile.write(line)
stop = raw_input("press enter to delete temporary files")

for item2 in list:
	os.system ('del '+pathname+'list_'+item2+'_temp1.txt')
	os.system ('del '+pathname+'list_'+item2+'_temp2.txt')
