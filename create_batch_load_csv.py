import pandas as pd
import numpy as np
import Dataframe
import easygui

# Input CSVs
cam_7_2 = pd.read_excel('Input_CSVs\CAM_7_3.xlsx', index_col=0, skiprows=[0])
iam_6_4 = pd.read_excel('Input_CSVs\IAM_6_4.xlsx', index_col=0)
iam_6_4a = pd.read_excel('Input_CSVs\IAM_6_4a.xlsx', index_col=0)
iam_6_5 = pd.read_excel('Input_CSVs\IAM_6_5.xlsx', index_col=0)


# Get user input for effective date
# Ex. 08/01/2023
effective_date = myvar = easygui.enterbox("Enter the effective date (MM/DD/YYYY): ")


##### IAM Table 6-4: Coniferous Average Sawlog Stumpage Rates for Salvage of Damaged Timber in $/m3 #####
iam_6_4 = Dataframe.Dataframe(iam_6_4)
iam_6_4.df = iam_6_4.df.drop(index = '(Fort Nelson)')
iam_6_4.forest_zone_code_col()
iam_6_4.df.set_index('FOREST_ZONE_CODE', inplace=True)
iam_6_4.fillna_with_AVG()
iam_6_4.df = iam_6_4.df.drop(columns = 'AVG')
iam_6_4.df = iam_6_4.df.stack().reset_index()
iam_6_4.df.columns = ['FOREST_ZONE_CODE','SPECIES','COST_ESTIMATE']
iam_6_4.zone_species_exclusions()
iam_6_4.grade_col()
iam_6_4.df['EFFECTIVE_DATE'] = effective_date
iam_6_4.df['PRODUCT'] = ''
iam_6_4.df['APRRAISAL_METHOD'] = 'I'
iam_6_4.df['RATE_TYPE'] = 'SDT'
iam_6_4.df = iam_6_4.df[['EFFECTIVE_DATE', 'SPECIES', 'GRADE', 'PRODUCT', 'APRRAISAL_METHOD', 'RATE_TYPE', 'FOREST_ZONE_CODE', 'COST_ESTIMATE']]
iam_6_4.sort()
# print(iam_6_4.df)


##### IAM Table 6-4a: Coniferous Average Sawlog Stumpage Rates for Salvage of Fire Damaged Timber in $/m3 #####
iam_6_4a = Dataframe.Dataframe(iam_6_4a)
iam_6_4a.df = iam_6_4a.df.drop(index = '(Fort Nelson)')
iam_6_4a.forest_zone_code_col()
iam_6_4a.df.set_index('FOREST_ZONE_CODE', inplace=True)
iam_6_4a.fillna_with_AVG()
iam_6_4a.df = iam_6_4a.df.drop(columns = 'AVG')
iam_6_4a.df = iam_6_4a.df.stack().reset_index()
iam_6_4a.df.columns = ['FOREST_ZONE_CODE','SPECIES','COST_ESTIMATE']
iam_6_4a.zone_species_exclusions()
iam_6_4a.grade_col()
iam_6_4a.df['EFFECTIVE_DATE'] = effective_date
iam_6_4a.df['PRODUCT'] = ''
iam_6_4a.df['APRRAISAL_METHOD'] = 'I'
iam_6_4a.df['RATE_TYPE'] = 'SFD'
iam_6_4a.df = iam_6_4a.df[['EFFECTIVE_DATE', 'SPECIES', 'GRADE', 'PRODUCT', 'APRRAISAL_METHOD', 'RATE_TYPE', 'FOREST_ZONE_CODE', 'COST_ESTIMATE']]
iam_6_4a.sort()
# print(iam_6_4a.df)


##### IAM Table 6-5: Coniferous Average Sawlog Stumpage Rates for Salvage of Post- Harvest Material in $/m3 #####
iam_6_5 = Dataframe.Dataframe(iam_6_5)
iam_6_5.df = iam_6_5.df.drop(index = '(Fort Nelson)')
iam_6_5.forest_zone_code_col()
iam_6_5.df.set_index('FOREST_ZONE_CODE', inplace=True)
iam_6_5.fillna_with_AVG()
iam_6_5.df = iam_6_5.df.drop(columns = 'AVG')
iam_6_5.df = iam_6_5.df.stack().reset_index()
iam_6_5.df.columns = ['FOREST_ZONE_CODE','SPECIES','COST_ESTIMATE']
iam_6_5.zone_species_exclusions()
iam_6_5.grade_col()
iam_6_5.df['EFFECTIVE_DATE'] = effective_date
iam_6_5.df['PRODUCT'] = ''
iam_6_5.df['APRRAISAL_METHOD'] = 'I'
iam_6_5.df['RATE_TYPE'] = 'SPH'
iam_6_5.df = iam_6_5.df[['EFFECTIVE_DATE', 'SPECIES', 'GRADE', 'PRODUCT', 'APRRAISAL_METHOD', 'RATE_TYPE', 'FOREST_ZONE_CODE', 'COST_ESTIMATE']]
iam_6_5.sort()
# print(iam_6_5.df)


##### CAM Table 7-3: Average Sawlog Rates for Salvaged Timber ($/m3) #####
cam_7_2 = Dataframe.Dataframe(cam_7_2)
cam_7_2.df = cam_7_2.df.stack().reset_index()
cam_7_2.df.columns = ['SOURCE_OF_SALVAGE_TIMBER','SPECIES_NAME','COST_ESTIMATE']
cam_7_2.species_code_col()
cam_7_2.make_other_species()
cam_7_2.rate_type_col()
cam_7_2.df['EFFECTIVE_DATE'] = effective_date
cam_7_2.df['PRODUCT'] = ''
cam_7_2.df['GRADE'] = ''
cam_7_2.df['APRRAISAL_METHOD'] = 'C'
cam_7_2.df['FOREST_ZONE_CODE'] = 'ACR'
cam_7_2.df = cam_7_2.df[['EFFECTIVE_DATE', 'SPECIES', 'GRADE', 'PRODUCT', 'APRRAISAL_METHOD', 'RATE_TYPE', 'FOREST_ZONE_CODE', 'COST_ESTIMATE']]
cam_7_2.sort()
# print(cam_7_2.df)


##### Create batch load CSV #####
batch_load = pd.concat([iam_6_4.df, iam_6_4a.df, iam_6_5.df, cam_7_2.df], ignore_index=True)
batch_load = Dataframe.Dataframe(batch_load)
batch_load.sort()
batch_load.df.to_csv(f'batch_load_file_{effective_date[:2]}_{effective_date[3:5]}_{effective_date[6:]}.csv', index=False, header=False)
