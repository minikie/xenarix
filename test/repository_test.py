import xenarix as xen
import xenarix.results as xen_r

xen.set_repository('c:\\xenarix')

res = xen_r.result_list()[0]

#tuple = res.timegrid.data.loc[0]
#print res.timegrid.data

print res.timegrid.has_date('2015-10-01')
print res.timegrid.has_t(1, error=0.01)

print res.timegrid.find_row_by_date('2015-10-11', interpolation=True)
print res.timegrid.find_row_by_t(1, interpolation=True, error=0.0001)

#print res.timegrid.data['DATE'][1] < res.timegrid.data['DATE'][0]