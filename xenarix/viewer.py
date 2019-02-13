# coding=utf-8
import xenarix as xen
import results as xen_r
import matplotlib.pyplot as plt


def plot_all(res):
    if not isinstance(res, xen_r.ResultObj):
        raise Exception('ResultObj type is needed')

    for i, m in enumerate(res.models.values()):
        plt.figure(i+1)
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




