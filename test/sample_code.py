import xenarix as xen
import xenarix.results as xen_r

# default repository is sub-directory of your_working_directory
# ( [your_working_directory]/repository )
# xen.set_repository('c:\repository')

scenSetID = 'set1'
scenID = 'scen1'
resultID = 'res1'

xen.test_generate(scenSetID, scenID, resultID)

# get result from current repository
result = xen_r.ResultObj(scenSetID, scenID, resultID)

multipath = result.get_multipath(scen_count=0) # select using scen_count
#modelpath = result.get_modelpath(model_count=0) #