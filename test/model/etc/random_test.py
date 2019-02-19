# coding=utf-8
import xenarix as xen
import xenarix.results as xen_r
import xenarix.viewer as xen_v

def get_test_model(process_name):
    model = xen.RandomProcessModel(process_name)

    return model


def do_test():
    scenSet = xen.ScenarioSet('set1')
    model = get_test_model('rnd_model')
    scen1 = xen.Scenario('scen1', 'testResult')
    scen1.add_model(model)

    scen1.general.scenario_num = 1000
    scen1.general.maxyear = 5
    scen1.general.frequency = xen.TimeGridFrequency.Day
    #print scen1.dump()
    scenSet.add_scenario(scen1)
    scenSet.generate_test()

    xen_v.plot_all(scenSet)
