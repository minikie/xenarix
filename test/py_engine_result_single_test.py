# coding=euc-kr
import xenarix as xen
import xenarix.results as results

repository_dir = 'C:\\Users\\09928829\\Source\\Workspaces\\InsuranceHedgeProject\\InsruranceHedge_sln\\Project\\Scenario\\xenarixPy\\test_repository'
xen.set_repository(repository_dir)

set_name = 'setname_1'
scen_id = 'testallmodel_1'
result_id = 'testresult_1'

result = results.ResultObj(set_name, scen_id, result_id)

print(result.models[0].data)

