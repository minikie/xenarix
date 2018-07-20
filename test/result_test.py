import results as xen_result

set_name = 'debug'
scen_name = 'TESTSCENTEMPLATEID'
result_name = 'TESTRESULTID1'

print('xeResultFile')
# xeResultFile( file_full_name ) -> object
file_full_name = 'C:/xenbin/scen_results/debug/TESTSCENTEMPLATEID/TESTRESULTID1/20150902_TESTSCENTEMPLATEID_BASE_HW1F_VALUE.SCN'
result_obj = xen_result.xeResultFile(file_full_name)
print(result_obj)

print('xeResultList')
# xeResultList(set_name, scen_name, result_name) -> object array
result_obj_list = xen_result.xeResultList(set_name, scen_name, result_name)
print(result_obj_list)

print('xeReulstLoad')
# xeReulstLoad(result_obj, start_pos, end_pos) -> matrix
start_pos = 3
end_pos = 6
np_arr = xen_result.xeResultLoad(result_obj, start_pos, end_pos)
print(np_arr)

print('xeResultAggregate')
# xeResultAggregate(result_obj_list, scen_num) -> matrix
scen_num = 6
np_arr_agg = xen_result.xeResultAggregate(result_obj_list, scen_num)
print(np_arr_agg)
