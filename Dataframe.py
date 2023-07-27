import pandas as pd
import numpy as np
from copy import deepcopy

class Dataframe:
    '''
    Pandas df utilities
    '''
    
    def __init__(self, df):
        '''
        df is a pandas df
        '''
        self.df = df


    def fillna_with_AVG(self):
        '''
        fills null cells with associated average in the column called 'AVG'.
        '''
        df = self.df
        for col in df:
            df[col] = df[col].fillna(df['AVG'])


    def forest_zone_code_col(self):
        '''
        Creates a 'FOREST_ZONE_CODE' column from the 'FOREST_ZONE' column
        '''
        df = self.df

        conditions = [
            df.index == 'North Central',
            df.index == 'North East',
            df.index == 'North West',
            df.index == 'South Central',
            df.index == 'South East',
            df.index == 'South West',
        ]

        choices = [
            'NC', 'NE', 'NW', 'SC', 'SE', 'SW'
        ]

        df['FOREST_ZONE_CODE'] = np.select(conditions, choices, default=np.nan)

    
    def grade_col(self):
        '''
        Creates a column with grades 1 and 2, for which associated row values are the same.
        '''
        grade1 = deepcopy(self.df)
        grade1['GRADE'] = 1

        grade2 = deepcopy(self.df)
        grade2['GRADE'] = 2

        self.df = pd.concat([grade1, grade2], ignore_index=True)


    def sort(self):
        '''
        Sorts the df as desired for the batch load
        '''
        self.df.sort_values(by=['SPECIES', 'APRRAISAL_METHOD', 'RATE_TYPE', 'FOREST_ZONE_CODE', 'GRADE'], inplace=True, ignore_index=True)


    def zone_species_exclusions(self):
        '''
        Deleted rows for excluded zones-species combos: WH and YE in NW, NE, and NC.
        Requires df has been converted from a matrix to a table with columns FOREST_ZONE_CODE and SPECIES.
        '''
        self.df.drop(
            self.df[
                ((self.df.FOREST_ZONE_CODE == 'NW') | (self.df.FOREST_ZONE_CODE == 'NE') | (self.df.FOREST_ZONE_CODE == 'NC')) 
                & ((self.df.SPECIES == 'WH') | (self.df.SPECIES == 'YE'))
            ].index, 
            inplace=True
        )


    def species_code_col(self):
        '''
        Creates a 'SPECIES' [code] column from the 'SPECIES_NAME' column
        '''
        df = self.df

        conditions = [
            df.SPECIES_NAME == 'Balsam',
            df.SPECIES_NAME == 'Hemlock',
            df.SPECIES_NAME == 'Cedar',
            df.SPECIES_NAME == 'Cypress',
            df.SPECIES_NAME == 'Fir',
            df.SPECIES_NAME == 'Spruce',
            df.SPECIES_NAME == 'Species*',
        ]

        choices = [
            'BA', 'HE', 'CE', 'CY', 'FI', 'SP', 'OT'
        ]

        df['SPECIES'] = np.select(conditions, choices, default=np.nan)


    def make_other_species(self):
        '''
        Creates rows for other species ('LO', 'WH', 'WB', 'YE', 'LA') based on rows with SPECIES = 'OT'
        '''
        ot_rows = self.df.query("SPECIES == 'OT'")
        other_species = ['LO', 'WH', 'WB', 'YE', 'LA']
        constructed_rows = []
        for i, row in ot_rows.iterrows():
            for species in other_species:
                row = row.copy()
                row['SPECIES'] = species
                constructed_rows += [row.to_list()]

        other_species_df = pd.DataFrame(constructed_rows, columns = self.df.columns)
        self.df = pd.concat([self.df, other_species_df], ignore_index=True)
        self.df.drop(columns = 'SPECIES_NAME', inplace=True)
        self.df.drop(self.df[self.df.SPECIES == 'OT'].index, inplace=True)
        self.df.reset_index(drop=True, inplace=True)

    
    def rate_type_col(self):
        '''
        Creates a 'RATE_TYPE' column from the 'SOURCE_OF_SALVAGE_TIMBER' column
        '''
        df = self.df

        conditions = [
            df.SOURCE_OF_SALVAGE_TIMBER == 'Damaged Timber',
            df.SOURCE_OF_SALVAGE_TIMBER == 'Post-Harvest Material'
        ]

        choices = [
            'SDT', 'SPH'
        ]

        df['RATE_TYPE'] = np.select(conditions, choices, default=np.nan)

        df.drop(columns = 'SOURCE_OF_SALVAGE_TIMBER', inplace=True)

