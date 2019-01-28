from xenarix import results as xen_result

set_name = 'debug'
scen_name = 'TESTSCENTEMPLATEID'
result_name = 'TESTRESULTID1'

result_info = xen_result.build_result_data_info2(set_name, scen_name, result_name)
result_list = xen_result.xeResultList(set_name, scen_name, result_name )

agg_arr = xen_result.xeResultAggregate(result_list , 0)


