import xenarix as xen
import xenarix.results as xen_r

#import model_generate as mg

scenSetID='set1'
scenID='scen1'
resultID='res1'

# mg.generate(scenSetID=scenSetID,
#             scenID=scenID,
#             resultID=resultID)

result = xen_r.ResultObj(scenSetID, scenID, resultID)

multipath = result.get_multipath(scen_count=0)
modelpath = result.get_modelpath(model_count=0)

calculated_result = []

print(result.names)

# print (multipath)
# print (modelpath)

# for t in result.timegrid:
    # print(multipath[:,t[0]])
    # calculated_result.append([])

# for t in result.timegrid:
#     print(modelpath[:, t[0]])




