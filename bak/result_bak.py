# class ResultSet:
#     def __init__(self):
#         self.set_path = ''
#         self.scen_data_ = None
#         self.result_id_list_ = []
#         self.shock_names = []
#         self.process_names = []
#         self.result_nm = None
#
#         self.result_data_info = None
#
#     def __getitem__(self, item):
#         return self.scen_data_[item]
#
#     def load_scenario(self, scen_nm, result_nm):
#         scen_path = self.set_path + '\\' + scen_nm
#
#         if result_nm == '':
#             result_path = max([os.path.join(scen_path, d) for d in os.listdir(scen_path)], key=os.path.getmtime)
#         else:
#             result_path = scen_path + '\\' +  result_nm
#
#         result_info_file_path = result_path + '\\' + 'RESULTINFO.TXT'
#
#         if not os.path.exists(result_info_file_path):
#             print ("result info load error. file not exist.")
#
#         self.result_data_info = pd.read_table(result_info_file_path, delimiter='|')
#
#         # under
#         under_group = self.result_data_info['REF_INDEX_CD'].groupby(self.result_data_info['REF_INDEX_CD'])
#         for nm in under_group.indices:
#             self.process_names.append(nm)
#
#         # shock
#         shock_group = self.result_data_info['SHOCK_NAME'].groupby(self.result_data_info['SHOCK_NAME'])
#         for nm in shock_group.indices:
#             self.shock_names.append(nm)
#
#         scenario_num = self.result_data_info['SCENARIO_NUM'][0]
#         t_count = self.result_data_info['T_COUNT'][0]
#         step_per_year = self.result_data_info['STEP_PER_YEAR'][0]
#
#         self.scen_data_ = np.ndarray((len(self.shock_names), len(self.process_names), scenario_num, t_count),
#                                      dtype=np.float)
#
#         for shk_i, shk_nm in enumerate(self.shock_names):
#             for under_i, file_info in enumerate(
#                     self.result_data_info[self.result_data_info['SHOCK_NAME'] == shk_nm]['FILEPATH']):
#                 if os.path.exists(file_info):
#                     self.scen_data_[shk_i][under_i] = np.memmap(file_info, np.float, mode='r',
#                                                                 shape=(scenario_num, t_count))
#
#                     # for i, file_info in enumerate(self.result_data_info['FILEPATH']):
#                     #     if os.path.exists(file_info):
#                     #         self.scen_data_[0][i] = np.memmap(file_info, np.float, mode='r', shape=(scenario_num, t_count))
#
#     # [shock][under_nm][calc_nm][scen_num][t]
#     # [shock][under_nm][scen_num][t]
#     # [shock][under_nm][add_calc?][scen_num][t]
#     def load(self, set_nm, result_nm=''):
#         # resultinfo file
#         self.set_nm = set_nm
#         self.set_path = xen_scen_result_dir + '\\' + set_nm
#         print  os.listdir(self.set_path)
#         # get list
#         scenario_nm_list = [ d for d in os.listdir(self.set_path) if os.path.isdir(os.path.join(self.set_path, d))]
#
#         for nm in scenario_nm_list:
#             self.load_scenario(nm, result_nm)
#
#     def export(self):
#         pass
#
#     def shocks(self):
#         pass
#
#
# def get_result_set(set_nm, result_nm=''):
#     res_set = ResultSet()
#     res_set.load(set_nm, result_nm)
#     return res_set
#
#
# if __name__ == "__main__":
#     res_set = get_result_set('newSet')
#
#     print res_set.scen_data_['']
#
#
#     print 'done.'