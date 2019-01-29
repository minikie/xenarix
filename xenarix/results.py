# coding=utf-8
import numpy as np
import pandas as pd
import os
import xenarix as xen

def build_result_data_info2(set_name, scen_name, result_name):
    result_info_file_path = xen.xen_result_dir() + '/' + set_name + '/' + scen_name + '/' + result_name

    return build_result_data_info(result_info_file_path)


def build_result_data_info(result_info_file_path):
    if not os.path.exists(result_info_file_path):
        raise Exception("result info load error. file not exist.")

    result_data_info = pd.read_csv(result_info_file_path + '/' + xen.resultinfo_filename, delimiter='|')

    return result_data_info


# file load numpy wrapping
class ReulstModel:
    def __init__(self, result_data_info_row):
        # REF_DT
        # RESULT_ID
        # RESULT_NM
        # SCENARIO_ID
        # SHOCK_NAME
        # SHOCK_SEQ
        # REF_INDEX_CD
        # MODEL_TYPE
        # CALCULATION
        # ORIGIN_CURRENCY
        # TARGET_CURRENCY
        # OUTPUT
        # CALC_TYPE
        # SCENARIO_NUM
        # T_COUNT
        # STEP_PER_YEAR
        # GEN_START_TIME
        # GEN_END_TIME
        # GEN_TYPE
        # STATUS_MESSAGE
        # STATUS
        # DESCRIPTION
        # FILEPATH

        self.filepath = result_data_info_row['FILEPATH']
        self.scenario_num = result_data_info_row['SCENARIO_NUM']
        self.t_count = result_data_info_row['T_COUNT']
        self.calc_type = result_data_info_row['CALCULATION']

        self.info = result_data_info_row
        if self.calc_type == 'DEBUGPRINT':
            scenario_num = 1
        self.data = self.arr = np.memmap(self.filepath, np.double, mode='r', shape=(self.scenario_num, self.t_count))


class ResultObj:
    def __init__(self, set_name, scen_name, result_name):
        self.set_name = set_name
        self.scen_name = scen_name
        self.result_name = result_name
        self.models = []

        self.initialize()

    def initialize(self):
        self.result_data_info = build_result_data_info2(self.set_name, self.scen_name, self.result_name)

        for index, row in self.result_data_info.iterrows():
            self.models.append(ReulstModel(row))


    def load(self, start_pos=None, end_pos=None):
        if start_pos is None:
            start_pos = 1

        scenario_num = self.result_data_info['SCENARIO_NUM'][0]

        if end_pos is None:
            end_pos = scenario_num

        if self.calc_type == 'DEBUGPRINT':
            scenario_num = 1

        t_count = self.result_data_info['T_COUNT'][0]
        self.arr = np.memmap(self.file_full_path, np.double, mode='r', shape=(scenario_num, t_count))[start_pos-1:end_pos].tolist()
        return self.arr

    def averave(self, start_pos=None, end_pos=None):
        if self.arr is None:
            self.load(start_pos, end_pos)

        return np.average(self.arr, axis=0)


def xeResultLoad(result_obj, start_pos, end_pos):
    result_obj.load(start_pos, end_pos)
    return result_obj.arr


def resultModel_list(set_name, scen_name, result_name):
    result_dir = xen.xen_result_dir() + '/' + set_name + '/' + scen_name + '/' + result_name

    result_data_info = build_result_data_info(result_dir + '/' + xen.resultinfo_filename)
    result_arr = dict()
    # for model_name, shock_nm, calculation, filepath, calc_type in zip(result_data_info['REF_INDEX_CD'], result_data_info['SHOCK_NAME'], result_data_info['CALCULATION'], result_data_info['FILEPATH'], result_data_info['CALC_TYPE']):
    #     result_arr[str(model_name) + '_' + str(shock_nm) + '_' + str(calculation)] = ResultObj(filepath, calc_type)
    for index, row in result_data_info.iterrows():
        result_arr[str(row['REF_INDEX_CD']) + '_' + str(row['SHOCK_NAME']) + '_' + str(row['CALCULATION'])] = ReulstModel(row)

    return result_arr


def result_list():
    res = []
    scen_set_items = os.listdir(xen.xen_result_dir())

    for scen_set in scen_set_items:
        scen_id_items = os.listdir(xen.xen_result_dir() + "\\" + scen_set)
        for scen_id in scen_id_items:
            result_id_items = os.listdir(xen.xen_result_dir() + "\\" + scen_set + "\\" + scen_id)
            for result_id in result_id_items:
                #res.append([scen_set, scen_id, result_id, ResultObj(scen_set, scen_id, result_id)])
                res.append(ResultObj(scen_set, scen_id, result_id))

    return res


# def xeResultFile(file_full_path):
#     result_obj = ResultObj(file_full_path)
#     return result_obj


def xeResultAggregate(result_obj_list, scen_num):
    arr = []

    for obj in result_obj_list:
        obj.load(scen_num,scen_num)
        arr.append(obj.arr[0])

    return np.array(arr)

