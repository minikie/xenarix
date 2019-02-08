import xenarix as xen
import xenarix.results as xen_r
import xenarix.test as xen_t

xen.set_repository('c:\\xenarix')

res = xen_r.resultObj_list()[0]

maturity_date = '2016-09-01'
rf = 0.03
div = 0.01
option = xen_t.VanillaEqOption(100, maturity_date)
print option.price(res.timegrid, res.models['TEST_GBMCONST_NAN_BASE'], rf)
print option.price2(res.timegrid, 100, rf, div, 0.3)