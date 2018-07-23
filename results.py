# coding=utf-8
import numpy as np
import pandas as pd
from pathlib import Path
import os
#from xenarix import
import xenarix as xen

def build_result_data_info2(set_name, scen_name, result_name):
    result_info_file_path = xen_result_dir + '/' + set_name + '/' + scen_name + '/' + result_name + '/' + resultinfo_filename

    return build_result_data_info(result_info_file_path)


def build_result_data_info(result_info_file_path):
    if not os.path.exists(result_info_file_path):
        print ("result info load error. file not exist.")

    result_data_info = pd.read_table(result_info_file_path, delimiter='|')

    return result_data_info


class ResultObj:
    def __init__(self, file_full_path, calc_type):
        self.file_full_path = file_full_path
        self.info_load()
        self.calc_type = calc_type
        self.arr = None

    def info_load(self):
        result_info_file_path = os.path.dirname(self.file_full_path) + '/' + xen.resultinfo_filename

        self.result_data_info = build_result_data_info(result_info_file_path)
        # print self.result_data_info

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


def xeResultList(set_name, scen_name, result_name):
    result_dir = xen.xen_result_dir + '/' + set_name + '/' + scen_name + '/' + result_name

    result_data_info = build_result_data_info(result_dir + '/' + xen.resultinfo_filename)
    result_arr = dict()
    for model_name, shock_nm, calculation, filepath, calc_type in zip(result_data_info['REF_INDEX_CD'], result_data_info['SHOCK_NAME'], result_data_info['CALCULATION'], result_data_info['FILEPATH'], result_data_info['CALC_TYPE']):
        result_arr[str(model_name) + '_' + str(shock_nm) + '_' + str(calculation)] = ResultObj(filepath, calc_type)

    return result_arr


# def xeResultFile(file_full_path):
#     result_obj = ResultObj(file_full_path)
#     return result_obj


def xeResultAggregate(result_obj_list, scen_num):
    arr = []

    for obj in result_obj_list:
        obj.load(scen_num,scen_num)
        arr.append(obj.arr[0])

    return np.array(arr)

