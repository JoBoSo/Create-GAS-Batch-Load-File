Obtaining Input Data
- Data is sourced from the Coast and Interior Appraisal Manuals (CAM and IAM) on the BC Government Website
    - Coast: https://www2.gov.bc.ca/gov/content/industry/forestry/competitive-forest-industry/timber-pricing/coast-timber-pricing/coast-appraisal-manual-and-amendments
    - Interior: https://www2.gov.bc.ca/gov/content/industry/forestry/competitive-forest-industry/timber-pricing/interior-timber-pricing/interior-appraisal-manual

Preparing Input Data
- The PDFs can be converted to word docs and the required data tables can then be copied and pasted in the Input_CSVs folder
    - CAM_7_3.xlsx contains Table 7-3: Average Sawlog Rates for Salvaged Timber ($/m3) in the CAM
    - IAM_6_4.xlsx contains Table 6-4: Coniferous Average Sawlog Stumpage Rates for Salvage of Damaged Timber in $/m3 in the IAM
    - IAM_6_4a.xlsx contains IAM Table 6-4a: Coniferous Average Sawlog Stumpage Rates for Salvage of Fire Damaged Timber in $/m3 in the IAM
    - IAM_6_5.xlsx contains IAM Table 6-5: Coniferous Average Sawlog Stumpage Rates for Salvage of Post- Harvest Material in $/m3 in the IAM

Producing the GAS Batch Load File
- Assuming the table format remains consistent with previous versions, create_batch_load_csv.py can be run to produce the batch load file
  for the General Appraisal System (GAS).

Application Links:
GAS: https://www2.gov.bc.ca/gov/content/industry/forestry/competitive-forest-industry/timber-pricing/general-appraisal-system
