# coding=utf-8
import xenarix as xen
import xenarix.results as xen_r

xen.set_repository('c:\\xenarix')
res = xen_r.ResultObj('set1','SCEN1','RES1')

timeseries = []

ts_result_model = xen_r.TimeSeriesResultModel(timeseries=timeseries, timegrid=res.timegrid)

for t_row in res.timegrid:
    ts_result_model.interpolated_value(t_row)


