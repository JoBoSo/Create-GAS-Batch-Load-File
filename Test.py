import unittest
import numpy as np
import pandas as pd

class BatchLoadFileTest(unittest.TestCase):

    from create_batch_load_csv import batch_load

    batch_load_df = batch_load.df

    def test_interior_row_count(self):
        '''
        Test the expected row counts for the interior:
            - 3 distinct rate types
            - 2 distinct grades
            - 6 distinct forest zones
            - 7 distinct species in Northern zones
            - 9 distinct species in Southern zones
            - 96 rows per rate type (2 grades x 6 zones x (((3 Northern zones x 7 species) + (3 Southern zones x 9 species)) / 6 zones))
            - 288 rows total (3 rate types x 96 rows per rate type)
        '''
        interior_batch_load_df = self.batch_load_df.query("APRRAISAL_METHOD == 'I'")
        print(interior_batch_load_df)

        with self.subTest('3 distinct rate types'):
            unique_rate_types = interior_batch_load_df.RATE_TYPE.unique()
            self.assertEqual(len(unique_rate_types), 3)

        with self.subTest('2 distinct grades'):
            unique_grades = interior_batch_load_df.GRADE.unique()
            self.assertEqual(len(unique_grades), 2)

        with self.subTest('6 distinct forest zones'):
            unique_vals = interior_batch_load_df.FOREST_ZONE_CODE.unique()
            self.assertEqual(len(unique_vals), 6)

        with self.subTest('7 distinct species in Northern zones'):
            unique_vals = interior_batch_load_df.query("FOREST_ZONE_CODE == 'NC' | FOREST_ZONE_CODE == 'NE' | FOREST_ZONE_CODE == 'NW'").SPECIES.unique()
            self.assertEqual(len(unique_vals), 7)

        with self.subTest('9 distinct species in Southern zones'):
            unique_vals = interior_batch_load_df.query("FOREST_ZONE_CODE == 'SC' | FOREST_ZONE_CODE == 'SE' | FOREST_ZONE_CODE == 'SW'").SPECIES.unique()
            self.assertEqual(len(unique_vals), 9)

        with self.subTest('96 rows for rate type = SPH'):
            unique_vals = interior_batch_load_df.query("RATE_TYPE == 'SPH'").SPECIES.unique()
            self.assertEqual(len(unique_vals), 9)

        with self.subTest('96 rows for rate type = SDT'):
            unique_vals = interior_batch_load_df.query("RATE_TYPE == 'SPH'").SPECIES.unique()
            self.assertEqual(len(unique_vals), 9)

        with self.subTest('96 rows for rate type = SFD'):
            unique_vals = interior_batch_load_df.query("RATE_TYPE == 'SPH'").SPECIES.unique()
            self.assertEqual(len(unique_vals), 9)

        with self.subTest('288 rows total'):
            self.assertEqual(interior_batch_load_df.shape[0], 288)


    def test_coast_row_count(self):
        '''
        Test the expected row counts for the coast:
            - 2 distinct rate types
            - 1 distinct grade
            - 1 distinct forest zone
            - 11 distinct species
            - 11 rows per rate type (1 grade x 1 zone x 11 species)
            - 22 rows total (2 rate types x 11 rows per rate type)
        '''
        coast_batch_load_df = self.batch_load_df.query("APRRAISAL_METHOD == 'C'")
        print(coast_batch_load_df)

        with self.subTest('2 distinct rate types'):
            unique_rate_types = coast_batch_load_df.RATE_TYPE.unique()
            self.assertEqual(len(unique_rate_types), 2)

        with self.subTest('1 distinct grade'):
            unique_grades = coast_batch_load_df.GRADE.unique()
            self.assertEqual(len(unique_grades), 1)

        with self.subTest('1 distinct forest zone'):
            unique_vals = coast_batch_load_df.FOREST_ZONE_CODE.unique()
            self.assertEqual(len(unique_vals), 1)

        with self.subTest('11 distinct species'):
            unique_vals = coast_batch_load_df.SPECIES.unique()
            self.assertEqual(len(unique_vals), 11)

        with self.subTest('11 rows per rate type'):
            unique_vals = coast_batch_load_df.query("RATE_TYPE == 'SDT'").SPECIES.unique()
            self.assertEqual(len(unique_vals), 11)

        with self.subTest('11 rows per rate type'):
            unique_vals = coast_batch_load_df.query("RATE_TYPE == 'SPH'").SPECIES.unique()
            self.assertEqual(len(unique_vals), 11)

        with self.subTest('22 rows total'):
            self.assertEqual(coast_batch_load_df.shape[0], 22)


    def test_spot_checks(self):
        '''
        Some spot checks.
        '''
        with self.subTest('Coast, non-OT species, SPH'):
            actual = self.batch_load_df.query("RATE_TYPE == 'SPH' & APRRAISAL_METHOD == 'C' & SPECIES == 'BA' & FOREST_ZONE_CODE == 'ACR'").COST_ESTIMATE.values[0]
            expected = 3.91
            self.assertEqual(actual, expected)

        with self.subTest('Coast, OT species, SPH'):
            actual = self.batch_load_df.query("RATE_TYPE == 'SPH' & APRRAISAL_METHOD == 'C' & SPECIES == 'WB' & FOREST_ZONE_CODE == 'ACR'").COST_ESTIMATE.values[0]
            expected = 7.33
            self.assertEqual(actual, expected)

        with self.subTest('Coast, non-OT species, SDT'):
            actual = self.batch_load_df.query("RATE_TYPE == 'SDT' & APRRAISAL_METHOD == 'C' & SPECIES == 'BA' & FOREST_ZONE_CODE == 'ACR'").COST_ESTIMATE.values[0]
            expected = 6.25
            self.assertEqual(actual, expected)

        with self.subTest('Coast, OT species, SDT'):
            actual = self.batch_load_df.query("RATE_TYPE == 'SDT' & APRRAISAL_METHOD == 'C' & SPECIES == 'WB' & FOREST_ZONE_CODE == 'ACR'").COST_ESTIMATE.values[0]
            expected = 11.72
            self.assertEqual(actual, expected)

        with self.subTest('Interior, rate is not AVG, SDT'):
            actual = self.batch_load_df.query("RATE_TYPE == 'SDT' & APRRAISAL_METHOD == 'I' & SPECIES == 'BA' & FOREST_ZONE_CODE == 'NE' & GRADE == 1").COST_ESTIMATE.values[0]
            expected = 17.46
            self.assertEqual(actual, expected)

        with self.subTest('Interior, rate is AVG, SDT'):
            actual = self.batch_load_df.query("RATE_TYPE == 'SDT' & APRRAISAL_METHOD == 'I' & SPECIES == 'CE' & FOREST_ZONE_CODE == 'NE' & GRADE == 1").COST_ESTIMATE.values[0]
            expected = 16.21
            self.assertEqual(actual, expected)

        with self.subTest('Interior, rate is not AVG, SFD'):
            actual = self.batch_load_df.query("RATE_TYPE == 'SFD' & APRRAISAL_METHOD == 'I' & SPECIES == 'BA' & FOREST_ZONE_CODE == 'NE' & GRADE == 1").COST_ESTIMATE.values[0]
            expected = 12.23
            self.assertEqual(actual, expected)

        with self.subTest('Interior, rate is AVG, SFD'):
            actual = self.batch_load_df.query("RATE_TYPE == 'SFD' & APRRAISAL_METHOD == 'I' & SPECIES == 'CE' & FOREST_ZONE_CODE == 'NE' & GRADE == 1").COST_ESTIMATE.values[0]
            expected = 12.92
            self.assertEqual(actual, expected)

        with self.subTest('Interior, rate is not AVG, SPH'):
            actual = self.batch_load_df.query("RATE_TYPE == 'SPH' & APRRAISAL_METHOD == 'I' & SPECIES == 'BA' & FOREST_ZONE_CODE == 'NE' & GRADE == 1").COST_ESTIMATE.values[0]
            expected = 7.23
            self.assertEqual(actual, expected)

        with self.subTest('Interior, rate is AVG, SDT'):
            actual = self.batch_load_df.query("RATE_TYPE == 'SPH' & APRRAISAL_METHOD == 'I' & SPECIES == 'CE' & FOREST_ZONE_CODE == 'NE' & GRADE == 1").COST_ESTIMATE.values[0]
            expected = 13.05
            self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()