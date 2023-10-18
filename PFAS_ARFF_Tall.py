# This script is used for taking the "all results flat file" PFAS sampling data and turning it into a "tall" feature class.
# "Tall" means that each analyte tested at an address in a sampling round has its own row in the spreadsheet. See "PFAS_ARFF_Wide" for re-shaping the data.

# This script assumes you've already geocoded the unique Sampled_Address_Clean values for the site, put them in the master PFAS address layer, attributed them
# with the appropriate site name (see "site" variable below), and field-calculated address IDs (copy the object ID). The master PFAS address layer is here:
# []

# Data should not just be "fed" to this script and considered good to go. There could be issues in the sampling data that need to be addressed.
# There could be address matching issues. There could be additional matrix or analysis method values that need to be standardized.

# Add to this script if/when you do find things that need to be added so that the script can be made more robust.

# Last updated 10/11/2023

import pandas as pd # Used for working with Excel

# Things to definitely change per site and user

# Site summary workbook location (this script assumes your gdb and site summary workbook are in the same folder)
location = r"C:\Users\JohnsonN35\Local_Work\PFAS_Script"

# Site summary workbook file name (in Windows, click on the file and press F2 to select the file name text)
name = "Grayling-GAAF_SiteSummary_Copy"

# Geodatabase name (this script assumes your gdb and site summary workbook are in the same folder)
gdb = "PFAS.gdb"

# Name of the site; used later on to definition query the address layer
site = "'Grayling GAAF'" # Make sure the site listed here is the same one you used when attributing the address layer's "site" field
site_ = "Grayling_GAAF"

# Definition query for the sampling results (used later on in script)
# We only want unknown/pre-filter samples, we only want the rows that correspond to PFAS analytes (& not gen chem), and...
# SPECIFIC TO GRAYLING, we don't want results for the monitoring wells, which all start with "GAAF"
samplesDQ = '("Sample_PrePost" = \'PRE\' Or "Sample_PrePost" = \'Unknown\') And "Analyte_Group" = \'PFAS\' And "Sampled_Address_Clean" NOT LIKE \'GAAF%\''
# samplesDQ = '("Sample_PrePost" = \'PRE\' Or "Sample_PrePost" = \'Unknown\') And "Analyte_Group" = \'PFAS\''

# Definition query for the address points
addrDQ = '"Site" = \'Grayling GAAF\''

# Read in the "all results flat file" table of the site summary workbook, get rid of no-data rows at top of sheet, and re-export as single-sheet workbook
# https://pandas.pydata.org/pandas-docs/version/1.2/reference/api/pandas.read_excel.html

ext = ".xlsx"
sheet = "AllResultsFlatFile"
headerRow = 0 # Specific row (0-indexed) that contains the headers; accounts for the rows you skip
skipRows = 3 # Number of rows to skip

ff = pd.read_excel(location + "/" + name + ext, sheet_name = sheet, header = headerRow, skiprows = skipRows)

outName = name.replace("-","_") + "_AllResultsFlatFile" # Having a hyphen in the site name will be a problem later, so replace it
ff.to_excel(location + "/" + outName + ext, sheet_name = "AllResultsFlatFile")

# Create a new table where the "all results flat file" data will eventually go

arcpy.management.CreateTable(location + "/" + gdb, outName)

# Create the fields for the table
arcpy.management.AddFields(outName, "\
Site TEXT Site 255 # #;\
Site_Name TEXT Site_Name 255 # #;\
Site_Subarea TEXT Site_Subarea 255 # #;\
Data_File_Name TEXT Data_File_Name 255 # #;\
Report_File_Name TEXT Report_File_Name 255 # #;\
Lab_Name TEXT Lab_Name 255 # #;\
Lab_Work_Order TEXT Lab_Work_Order 255 # #;\
Lab_Sample_ID TEXT Lab_Sample_ID 255 # #;\
Field_Sample_ID TEXT Field_Sample_ID 255 # #;\
Field_Location_Code TEXT Field_Location_Code 255 # #;\
Sampled_Address_Clean TEXT Sampled_Address_Clean 255 # #;\
Sampling_Round TEXT Sampling_Round 255 # #;\
Sample_PrePost TEXT Sample_PrePost 255 # #;\
Duplicate TEXT Duplicate 255 # #;\
Collect_Date DATE Collect_Date # # #;\
Collected_By TEXT Collected_By 255 # #;\
Matrix TEXT Matrix 255 # #;\
Matrix_Stdz TEXT Matrix_Stdz 255 # #;\
Analyte_Group TEXT Analyte_Group 255 # #;\
Analysis_Method TEXT Analysis_Method 255 # #;\
Analysis_Method_Stdz TEXT Analysis_Method_Stdz 255 # #;\
Analyte_Abbrev TEXT Analyte_Abbrev 255 # #;\
Result TEXT Result 255 # #;\
Result_Num DOUBLE Result_Num # # #;\
Result_Unit TEXT Result_Unit 255 # #;\
Result_Unit_Stdz TEXT Result_Unit_Stdz 255 # #;\
Result_Qualifier TEXT Result_Qualifier 255 # #;\
Detect_Flag TEXT Detect_Flag 255 # #;\
RDL DOUBLE RDL # # #;\
LOQ DOUBLE LOQ # # #;\
Analyte_NDE TEXT Analyte_NDE 255 # #;\
Sample_NDE TEXT Sample_NDE 255 # #;\
Sample_TotalPFAS DOUBLE Sample_TotalPFAS # # #;\
DEH_Comment TEXT DEH_Comment 255 # #;\
Address_NDE TEXT Address_NDE 255 # #;\
Current_AltWaterRec TEXT Current_AltWaterRec 255 # #;\
")

# Append the "all results flat file" data to the table

# These are just the fields that Stuart indicated we MIGHT want; not all of these translate to the wide table
field_mapping = '\
Site "Site" true true false 255 Text 0 0,First,#;\
Site_Name "Site_Name" true true false 255 Text 0 0,First,#,inputs,Site_Name,0,255;\
Site_Subarea "Site_Subarea" true true false 255 Text 0 0,First,#,inputs,Site_Subarea,0,255;\
Data_File_Name "Data_File_Name" true true false 255 Text 0 0,First,#,inputs,Data_File_Name,0,255;\
Report_File_Name "Report_File_Name" true true false 255 Text 0 0,First,#,inputs,Report_File_Name,0,255;\
Lab_Name "Lab_Name" true true false 255 Text 0 0,First,#,inputs,Lab_Name,0,255;\
Lab_Work_Order "Lab_Work_Order" true true false 255 Text 0 0,First,#,inputs,Lab_Work_Order,0,255;\
Lab_Sample_ID "Lab_Sample_ID" true true false 255 Text 0 0,First,#,inputs,Lab_Sample_ID,0,255;\
Field_Sample_ID "Field_Sample_ID" true true false 255 Text 0 0,First,#,inputs,Field_Sample_ID,0,255;\
Field_Location_Code "Field_Location_Code" true true false 255 Text 0 0,First,#,inputs,Field_Location_Code,0,255;\
Sampled_Address_Clean "Sampled_Address_Clean" true true false 255 Text 0 0,First,#,inputs,Sampled_Address_Clean,0,255;\
Sampling_Round "Sampling_Round" true true false 255 Text 0 0,First,#,inputs,Sampling_Round,0,255;\
Sample_PrePost "Sample_PrePost" true true false 255 Text 0 0,First,#,inputs,Sample_PrePost,0,255;\
Duplicate "Duplicate" true true false 255 Text 0 0,First,#,inputs,Duplicate,0,255;\
Collect_Date "Collect_Date" true true false 8 Date 0 0,First,#,inputs,Collect_Date,-1,-1;\
Collected_By "Collected_By" true true false 255 Text 0 0,First,#,inputs,Collected_By,0,255;\
Matrix "Matrix" true true false 255 Text 0 0,First,#,inputs,Matrix,0,255;\
Analyte_Group "Analyte_Group" true true false 255 Text 0 0,First,#,inputs,Analyte_Group,0,255;\
Analysis_Method "Analysis_Method" true true false 255 Text 0 0,First,#,inputs,Analysis_Method,0,255;\
Analyte_Abbrev "Analyte_Abbrev" true true false 255 Text 0 0,First,#,inputs,Analyte_Abbrev,0,255;\
Result "Result" true true false 255 Text 0 0,First,#,inputs,Result,0,255;\
Result_Num "Result_Num" true true false 8 Double 0 0,First,#,inputs,Result_Num,-1,-1;\
Result_Unit "Result_Unit" true true false 255 Text 0 0,First,#,inputs,Result_Unit,0,255;\
Result_Qualifier "Result_Qualifier" true true false 255 Text 0 0,First,#,inputs,Result_Qualifier,0,255;\
Detect_Flag "Detect_Flag" true true false 255 Text 0 0,First,#,inputs,Detect_Flag,0,255;\
RDL "RDL" true true false 8 Double 0 0,First,#,inputs,RDL,-1,-1;\
LOQ "LOQ" true true false 8 Double 0 0,First,#,inputs,LOQ,0,255;\
Analyte_NDE "Analyte_NDE" true true false 255 Text 0 0,First,#,inputs,Analyte_NDE,0,255;\
Sample_NDE "Sample_NDE" true true false 255 Text 0 0,First,#,inputs,Sample_NDE,0,255;\
Sample_TotalPFAS "Sample_TotalPFAS" true true false 8 Double 0 0,First,#,inputs,Sample_TotalPFAS,-1,-1;\
DEH_Comment "DEH_Comment" true true false 255 Text 0 0,First,#,inputs,DEH_Comment,0,255;\
Address_NDE "Address_NDE" true true false 255 Text 0 0,First,#,inputs,Address_NDE,0,255;\
Current_AltWaterRec "Current_AltWaterRec" true true false 255 Text 0 0,First,#,inputs,Current_AltWaterRec,0,255'

inputs = location + "/" + outName + ext + "/" + sheet + "$"
target = outName

arcpy.management.Append(inputs, target, "NO_TEST", field_mapping)

# Access the map and layers/tables within it

aprx = arcpy.mp.ArcGISProject("CURRENT")
m = aprx.listMaps("Map3")[0]
addresses = m.listLayers("PFAS_Addresses")[0]
samples = m.listTables(target)[0]

# Improve the sampling data

# Input the "main" site name (the site name field has so many different values; need an overarching name to associate with the data)
arcpy.management.CalculateField(samples, "Site", site)

# Need to capitalize the address values (the flat file can contain multiple values for the same address in rare circumstances)
arcpy.management.CalculateField(samples, "Sampled_Address_Clean", "!Sampled_Address_Clean!.upper()")

# Definition query the addresses and sampling results with the queries we set up earlier

addresses.definitionQuery = addrDQ
samples.definitionQuery = samplesDQ

# Join the address data to the sampling data

arcpy.management.JoinField(samples, "Sampled_Address_Clean", addresses, "Address", "displayx;displayy;AddressID")

# Select by Attributes for features that have a null joined address ID; no records returned is good here!
arcpy.management.SelectLayerByAttribute(samples, "NEW_SELECTION", "AddressID IS NULL")

# Create an XY event layer (only after confirming that no desired addresses are without coordinates)

xyEvent = target + "_XYEvent"
gcs = '\
GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],\
UNIT["Degree",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision'

arcpy.management.MakeXYEventLayer(samples, "displayx", "displayy", xyEvent, gcs)

samplesXY = m.listLayers(xyEvent)[0]

samplesXY.definitionQuery = samplesDQ # Make XY Event Layer doesn't seem to honor definition queries, so re-set this before creating a feature class next

# Create a feature class from the XY events layer

samplesFC = xyEvent + "_FC"

arcpy.conversion.FeatureClassToFeatureClass(samplesXY, location + "/" + gdb, samplesFC, '', '\
Site "Site" true true false 255 Text 0 0,First,#,samplesXY,Site,0,255;\
Site_Name "Site_Name" true true false 255 Text 0 0,First,#,samplesXY,Site_Name,0,255;\
Site_Subarea "Site_Subarea" true true false 255 Text 0 0,First,#,samplesXY,Site_Subarea,0,255;\
Data_File_Name "Data_File_Name" true true false 255 Text 0 0,First,#,samplesXY,Data_File_Name,0,255;\
Report_File_Name "Report_File_Name" true true false 255 Text 0 0,First,#,samplesXY,Report_File_Name,0,255;\
Lab_Name "Lab_Name" true true false 255 Text 0 0,First,#,samplesXY,Lab_Name,0,255;\
Lab_Work_Order "Lab_Work_Order" true true false 255 Text 0 0,First,#,samplesXY,Lab_Work_Order,0,255;\
Lab_Sample_ID "Lab_Sample_ID" true true false 255 Text 0 0,First,#,samplesXY,Lab_Sample_ID,0,255;\
Field_Sample_ID "Field_Sample_ID" true true false 255 Text 0 0,First,#,samplesXY,Field_Sample_ID,0,255;\
Field_Location_Code "Field_Location_Code" true true false 255 Text 0 0,First,#,samplesXY,Field_Location_Code,0,255;\
Sampled_Address_Clean "Sampled_Address_Clean" true true false 255 Text 0 0,First,#,samplesXY,Sampled_Address_Clean,0,255;\
Sampling_Round "Sampling_Round" true true false 255 Text 0 0,First,#,samplesXY,Sampling_Round,0,255;\
Sample_PrePost "Sample_PrePost" true true false 255 Text 0 0,First,#,samplesXY,Sample_PrePost,0,255;\
Duplicate "Duplicate" true true false 255 Text 0 0,First,#,samplesXY,Duplicate,0,255;\
Collect_Date "Collect_Date" true true false 8 Date 0 0,First,#,samplesXY,Collect_Date,-1,-1;\
Collected_By "Collected_By" true true false 255 Text 0 0,First,#,samplesXY,Collected_By,0,255;\
Matrix "Matrix" true true false 255 Text 0 0,First,#,samplesXY,Matrix,0,255;\
Matrix_Stdz "Matrix_Stdz" true true false 255 Text 0 0,First,#,samplesXY,Matrix_Stdz,0,255;\
Analyte_Group "Analyte_Group" true true false 255 Text 0 0,First,#,samplesXY,Analyte_Group,0,255;\
Analysis_Method "Analysis_Method" true true false 255 Text 0 0,First,#,samplesXY,Analysis_Method,0,255;\
Analysis_Method_Stdz "Analysis_Method_Stdz" true true false 255 Text 0 0,First,#,samplesXY,Analysis_Method_Stdz,0,255;\
Analyte_Abbrev "Analyte_Abbrev" true true false 255 Text 0 0,First,#,samplesXY,Analyte_Abbrev,0,255;\
Result "Result" true true false 255 Text 0 0,First,#,samplesXY,Result,0,255;\
Result_Num "Result_Num" true true false 8 Double 0 0,First,#,samplesXY,Result_Num,-1,-1;\
Result_Unit "Result_Unit" true true false 255 Text 0 0,First,#,samplesXY,Result_Unit,0,255;\
Result_Unit_Stdz "Result_Unit_Stdz" true true false 255 Text 0 0,First,#,samplesXY,Result_Unit_Stdz,0,255;\
Result_Qualifier "Result_Qualifier" true true false 255 Text 0 0,First,#,samplesXY,Result_Qualifier,0,255;\
Detect_Flag "Detect_Flag" true true false 255 Text 0 0,First,#,samplesXY,Detect_Flag,0,255;\
RDL "RDL" true true false 8 Double 0 0,First,#,samplesXY,RDL,-1,-1;\
LOQ "LOQ" true true false 8 Double 0 0,First,#,samplesXY,LOQ,-1,-1;\
Analyte_NDE "Analyte_NDE" true true false 255 Text 0 0,First,#,samplesXY,Analyte_NDE,0,255;\
Sample_NDE "Sample_NDE" true true false 255 Text 0 0,First,#,samplesXY,Sample_NDE,0,255;\
Sample_TotalPFAS "Sample_TotalPFAS" true true false 8 Double 0 0,First,#,samplesXY,Sample_TotalPFAS,-1,-1;\
DEH_Comment "DEH_Comment" true true false 255 Text 0 0,First,#,samplesXY,DEH_Comment,0,255;\
Address_NDE "Address_NDE" true true false 255 Text 0 0,First,#,samplesXY,Address_NDE,0,255;\
Current_AltWaterRec "Current_AltWaterRec" true true false 255 Text 0 0,First,#,samplesXY,Current_AltWaterRec,0,255;\
AddressID "AddressID" true true false 10 Text 0 0,First,#,samplesXY,AddressID,0,10')

# Remove definition queries

samples.definitionQuery = None
samplesXY.definitionQuery = None
addresses.definitionQuery = None

# Field-calculate the standardized analysis method, result units, and matrix

samplesFC = m.listLayers(samplesFC)[0]

# -------------------ANALYSIS METHOD-------------------

# Clear selection
arcpy.management.SelectLayerByAttribute(samplesFC, "CLEAR_SELECTION", "CLEAR_SELECTION")

# Bring the messy Analysis_Method values into the standardized value field
arcpy.management.CalculateField(samplesFC, "Analysis_Method_Stdz", "!Analysis_Method!")

# EPA method 533 (not defined in EDD valid values reference manual)
arcpy.management.SelectLayerByAttribute(samplesFC, "NEW_SELECTION", "Analysis_Method = '533'")
arcpy.management.CalculateField(samplesFC, "Analysis_Method_Stdz", '"E533"')

# EPA method 537 (does NOT include modified method)
arcpy.management.SelectLayerByAttribute(samplesFC, "NEW_SELECTION", "Analysis_Method = 'EPA-537'")
arcpy.management.CalculateField(samplesFC, "Analysis_Method_Stdz", '"E537"')

# EPA method 537 modified (not defined in EDD valid values reference manual)
arcpy.management.SelectLayerByAttribute(samplesFC, "NEW_SELECTION", "Analysis_Method = 'EPA-537M'")
arcpy.management.CalculateField(samplesFC, "Analysis_Method_Stdz", '"E537M"')

# EPA method 537.1
arcpy.management.SelectLayerByAttribute(samplesFC, "NEW_SELECTION", "Analysis_Method = '537.1' Or Analysis_Method = 'EPA-537.1'")
arcpy.management.CalculateField(samplesFC, "Analysis_Method_Stdz", '"E537.1"')

# -------------------RESULT UNITS-------------------

# Clear selection
arcpy.management.SelectLayerByAttribute(samplesFC, "CLEAR_SELECTION", "CLEAR_SELECTION")

# Bring the messy Result_Unit values into the standardized value field
arcpy.management.CalculateField(samplesFC, "Result_Unit_Stdz", "!Result_Unit!")

# ng/l
arcpy.management.SelectLayerByAttribute(samplesFC, "NEW_SELECTION", "Result_Unit = 'ng/L'")
arcpy.management.CalculateField(samplesFC, "Result_Unit_Stdz", '"ng/l"')

# -------------------MATRIX-------------------

# Clear selection
arcpy.management.SelectLayerByAttribute(samplesFC, "CLEAR_SELECTION", "CLEAR_SELECTION")

# Bring the messy Matrix values into the standardized value field
arcpy.management.CalculateField(samplesFC, "Matrix_Stdz", "!Matrix!")

# Drinking water
arcpy.management.SelectLayerByAttribute(samplesFC, "NEW_SELECTION", "Matrix = 'Drinking Water' Or Matrix = 'DW' Or Matrix = 'PW' Or Matrix = 'WP'")
arcpy.management.CalculateField(samplesFC, "Matrix_Stdz", '"WP"')

# Water
arcpy.management.SelectLayerByAttribute(samplesFC, "NEW_SELECTION", "Matrix = 'Water'")
arcpy.management.CalculateField(samplesFC, "Matrix_Stdz", '"W"')

# Aqueous; unsure what this means, but if it's paired with a drinking water method, just call it WP?
arcpy.management.SelectLayerByAttribute(samplesFC, "NEW_SELECTION", "Matrix = 'Aqueous' And (Analysis_Method_Stdz = 'E533' Or Analysis_Method_Stdz = 'E537' Or Analysis_Method = 'EPA-537.1')")
arcpy.management.CalculateField(samplesFC, "Matrix_Stdz", '"WP"')

# Clear selection
arcpy.management.SelectLayerByAttribute(samplesFC, "CLEAR_SELECTION", "CLEAR_SELECTION")

# Print the unique values for the Stdz fields
methodValues = list(set(row[0] for row in arcpy.da.SearchCursor(samplesFC, "Analysis_Method_Stdz")))
unitValues = set(row[0] for row in arcpy.da.SearchCursor(samplesFC, "Result_Unit_Stdz"))
matrixValues = set(row[0] for row in arcpy.da.SearchCursor(samplesFC, "Matrix_Stdz"))

print("Method values: ", methodValues)
print("Unit values: ", unitValues)
print("Matrix values: ", matrixValues)
