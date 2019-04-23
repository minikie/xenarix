import xenarix as xen
import xenarix.sample as xen_s
import xenarix.results as xen_r
import unittest, sys, datetime

test_scen_set = None
test_scen = None
test_result = None # 전제조건임..

def build_test_scen_set():
    test_scen_set = xen.ScenarioSet('test_scen_set')
    scen1 = xen.Scenario('scen1', 'result1')
    scen1.add_model(xen_s.gbm('test_gbm'))
    test_scen_set.add_scenario(scen1)

    return test_scen_set


class TestGeneralInfoMethods(unittest.TestCase):

    def test_scenario_id(self):
        scen_id_in_scen = test_scen.get_scen_id() # scen obj
        scen_id_in_result_obj = test_result.scen_name # result obj
        scen_id_in_result_info_file = test_result.result_data_info['SCENARIO_ID'][0] # resultinfo file

        self.assertTrue(scen_id_in_scen.upper() ==
                        scen_id_in_result_obj.upper() ==
                        scen_id_in_result_info_file.upper())

    def test_reference_date(self):
        reference_date_in_scen = test_scen.general.reference_date
        reference_date_timegridinfo_file = test_result.timegrid[0]['DATE'].replace('-', '')

        self.assertTrue(reference_date_in_scen == reference_date_timegridinfo_file)

    def test_scenario_num(self):
        scenario_num_in_scen = test_scen.general.scenario_num # scen obj
        scenario_num_result_info_file = test_result.result_data_info['SCENARIO_NUM'][0] # resultinfo file

        self.assertTrue(scenario_num_in_scen == scenario_num_result_info_file)

    def test_delimiter(self):
        self.assertTrue(True)

    def test_maxyear(self):
        start_date_timegridinfo_file = test_result.timegrid[0]['DATE']
        end_date_timegridinfo_file = test_result.timegrid[-1]['DATE']

        start_date_obj = datetime.datetime.strptime(start_date_timegridinfo_file, '%Y-%m-%d')
        end_date_obj = datetime.datetime.strptime(end_date_timegridinfo_file, '%Y-%m-%d')
        max_year_in_scen = test_scen.general.maxyear
        total_year_in_timegridfile = end_date_obj.year - start_date_obj.year

        self.assertTrue(max_year_in_scen == total_year_in_timegridfile)

    def test_n_peryear(self):
        self.assertTrue(True)

    def test_rnd_type(self):
        self.assertTrue(True)

    def test_rnd_subtype(self):
        self.assertTrue(True)

    def test_rnd_seed(self):
        self.assertTrue(True)

    def test_rnd_skip(self):
        self.assertTrue(True)

    def test_moment_match(self):
        self.assertTrue(True)

    def test_frequency(self):
        self.assertTrue(True)

    def test_frequency_month(self):
        self.assertTrue(True)

    def test_frequency_day(self):
        self.assertTrue(True)

    def test_result_id(self):
        self.assertTrue(True)

    def test_base_currency(self):
        self.assertTrue(True)

    def test_thread_num(self):
        self.assertTrue(True)


if __name__ == '__main__':
    sys.argv.append('-v')

    test_scen_set = build_test_scen_set()
    test_scen_set.generate()
    test_scen = test_scen_set.scenario_list[0]
    test_result = test_scen_set.get_result_obj_list()[0]

    unittest.main()