# coding=euc-kr
import xenarix as xen
import xenarix.results as results

xen.set_repository('C:\\Users\\09928829\\Source\\Workspaces\\InsuranceHedgeProject\\InsruranceHedge_sln\\Project\\Scenario\\xenarixPy\\test_repository')

# scen_id = 'testallmodel_1'
# result_id = 'testresult_1'
# set_name = 'setname_1'

result_list = results.result_list()
print (result_list)
#print(result_list[0].result_data_info)

# for index, row in result_list[0].result_data_info.iterrows():
#     print(row)
#     print(row['REF_DT'])

print(result_list[0].models)

#print(result_list[0].result_data_info.columns.values)
#print(result_list[0].models[0].info)
# for model in result_list[0].models:
#     print(model.scenario_num)
#     print(model.data)



