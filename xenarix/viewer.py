# coding=utf-8
import xenarix as xen
import results as xen_r
import matplotlib.pyplot as plt


def plot_all_merge(res):
    if not isinstance(res, xen_r.ResultObj):
        raise Exception('ResultObj type is needed')

    for i, m in enumerate(res.models.values()):
        plt.figure(i + 1)
        plt.plot(res.timegrid.data['T'], m.average(), label=m.name)
        plt.xlabel('time (year)')
        plt.ylabel('value')
        plt.legend()

    plt.show()


def plot_all_seperate(res):
    if not isinstance(res, xen_r.ResultObj):
        raise Exception('ResultObj type is needed')

    plt.figure(1)

    for i, m in enumerate(res.models.values()):
        plt.plot(res.timegrid.data['T'], m.average(), label=m.name)

    plt.xlabel('time (year)')
    plt.ylabel('value')
    plt.legend()
    plt.show()


def plot_all(source, seperate=True):
    res = None
    if isinstance(source, xen.ScenarioSet):
        for scen in source.scenario_list:
            res = xen_r.ResultObj(source.set_name, scen.get_scen_id(), scen.get_result_id())

    elif isinstance(source, xen.Scenario):
        res = xen_r.ResultObj(source.owner_set_name, source.get_scen_id(), source.get_result_id())
    elif isinstance(source, xen_r.ResultObj):
        res = source
    else:
        raise Exception('unknown source')

    if seperate:
        plot_all_seperate(res)
    else:
        plot_all_merge(res)



