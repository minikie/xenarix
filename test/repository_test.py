import xenarix as xen
import xenarix.results as xen_r

xen.set_repository('c:\\xenarix')

res = xen_r.resultObj_list()[0]

#tuple = res.timegrid.data.loc[0]
#print res.timegrid.data

print 'has_date : 2015-10-01 - ' + str(res.timegrid.has_date('2015-10-01'))
print 'has_date : 2015-10-02 - ' + str(res.timegrid.has_date('2015-10-02'))
print res.timegrid.has_t(1, error=0.01)

t_row = res.timegrid.find_row_by_date('2020-10-11', interpolation=True)
# t_row = res.timegrid.find_row_by_t(1, interpolation=True, error=0.0001)
print t_row
print res.timegrid.pre_t_row(t_row)
print res.timegrid.next_t_row(t_row)


#print res.timegrid.data['DATE'][1] < res.timegrid.data['DATE'][0]


# Interpolation test

#for i in range(0,100):
    #print res.models['TEST_GBM_NAN_BASE'].interpolated_value(i, t_row) - res.models['TEST_GBM_NAN_BASE'].interpolated_value2(i, t_row)

print res.models['TEST_GBM_NAN_BASE'].interpolated_value(t_row, 10)
# print res.models['TEST_GBM_NAN_BASE'].interpolated_values(t_row)

print(res.models['TEST_GBM_NAN_BASE'].x0())