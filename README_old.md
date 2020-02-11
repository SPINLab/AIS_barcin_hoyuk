# AIS_barcin_hoyuk
This repository contains the auxiliary scripts for updating the Archaeological Information System for the excavation activities of the site Barcin Hoyuk. 

For the archaeological project Barcin Hoyuk a database has been developed to store all the excavation data. The database contains data that has been translate from paper forms. In order to identify wether the information in the database corresponds to what has been identified in the field, the database contains links to scans of paper forms (e.g. lot forms, field drawings, daily reports etc.). Furthermore the database contains links to pictures that has been taken in the field or made afterwards of inidivual objects.

Whenever an individual researcher want to use the database they can download a copy and use it on their own machine. The pictures and scanned documents are stored on the Yoda platform and are accessible through the database.
In this document the recepies for the various update scripts are presented.

Note: In this document all fields/ collumn names in tables will be written like Table:Field

To update the links in MS Access please note that it requires a # before and after the URL string.

To create file lists of the links please look at https://github.com/SPINLab/AIS_barcin_hoyuk/blob/master/create_file_lists.py 

# UPDATE 1 for field: 
33_Locus_drawings:Drawing_url

Needs to refer to the drawing which are available in the folder \STATIC_DATA\PLANS\TrenchXXX_scanned_plans\ XXX. Since the file name is exactly the same as the prefix and is present in the field 33_Locus_drawings field:Drawing_No this field can be updated accordingly. The suffic varies from .tif, .jpg, .bmp and .png.


# UPDATE 2 for field: 
6_Drawings_fieldwork:Drawing_url

Needs to refer to the drawing which are available in the folder \STATIC_DATA\PLANS\TrenchXXX_scanned_plans\ XXX. Since the file name is exactly the same as the prefix and is present in the field 6_Drawings_fieldwork:Drawing_No this field can be updated accordingly. The suffic varies from .tif, .jpg, .bmp and .png.


# UPDATE 3 for field: 	
4_Lot: Link_to_scanned_lot_form

Needs to refer to scanned lot forms available in folder: \STATIC_DATA\LOT_FORMS\
The files in this folder are systematically names contain the Trenc, year and lot number and stored as pdf. E.g. TRENCH_YEAR_LOT e.g. L10_2011_007_lot_form.pdf

To generate 4_Lot: Link_to_scanned_lot_form  the fields  4_Lot:Trench, 4_Lot:Lot, 4_Lot:Date need to be combined. Please note that from 4_Lot:Date only the year needs to be extracted.


# UPDATE 4 for field:	
4_Lot: Link_to_daily_report

Needs to refer to scanned daily reports. For every day at the excavation every trench has, if work has been executed on that particular day, a daily report. The scanned forms are stored in:
STATIC_DATA\DAILY_REPORTS\

The files are systematically stored as TRENCH_DAY_MONTH_YEAR e.g. L10_03_08_2011_daily_report.pdf
In order to update 4_Lot: Link_to_daily_report the fields 4_Lot:Trench, 4_Lot:Date are to be used. (date need to be coverted to a string)


# UPDATE 5 for field: 
4_Lot: Link_to_scanned_daily_sketch 
Is exactly the same as update 4, however refers to daily sketches which are stored in STATIC_DATA\SKETCHES\


# UPDATE 6 for fields:

7_Pictures_fieldwork:picture_url </p>
77_pictures_fieldwork_BH:picture_url</p>
77_Pictures_fieldwork_Locus:picture_url</p>
77_Pictures_fieldwork_Nails:picture_url</p>
77_Pictures_fieldwork_Structure:picture_url</p>
77_Pictures_fieldwork_Structure:picture_url</p>
777_Pictures_fieldwork_Locus_Lot:picture_url</p>

Needs to refer to the pictures that have been taken during the fieldwork as part of the daily activities of the various Trenches. (this table thus does not provide a full list of all the pictures, but it does provide a great share of it). 
The pictures are stored in STATIC_DATA\PICTURES\</p>

The field picture_url, which is present in all tables can be generated based on 7_Pictures_fieldwork:Picture_ID since the Picture ID is the prefix of the files. (in order to make these unique we have added the Trench and Excavtion year to the file name).


# UPDATE 7:

Table 7777_BH_Pictures:</p>

In the first years of the excavation the database model was still under construction. The consuquence is that we have BH numbers for object that have been registered in a different table with different field than was done lateron. The data has been harmonized, however the pictures could not be linked in the way how it currently done.</p></p>

Wheras for Update 5 the links are generated based on what is filled in in the database. The link to the objects that have been photographed in the early stages of the excavation need to be linked based on solely the file name. The only way to know if a picture is taken from a particular object is go through the file names.</p>

7777_BH_Pictures:picture_url can be extracted from the file list of all pictures in STATIC_DATA\PICTURES\ and should only select pictures which have in the prefix BH as first 2 characters.</p>

7777_BH_Pictures:BH_Number is to be generated based on 7777_BH_Pictures:picture_url by selecting the numbers between BH and the next _ . For example PICTURES//BH03210_DSCF1585_13351555244_o.jpg become 03210. The next step in this conversion is to store it as a number creating the value of 7777_BH_Pictures:BH_Number in this example as 3210.</p> 


