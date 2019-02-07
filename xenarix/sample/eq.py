# coding=utf-8
import xenarix as xen
import numpy as np


def gbm(process_name):

    model = xen.GBM(process_name)

    model.sections["X0"] = 100

    model.rf_curve.tenor = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M']
    model.rf_curve.value = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229]
    model.div_curve.tenor = ['100Y']
    model.div_curve.value = [0.005]
    model.sigma_curve.tenor = ['5Y', '100Y']
    model.sigma_curve.value = [0.3, 0.2]

    return model


def gbmconst(process_name):

    model = xen.GBMConst(process_name)

    model.x0 = 100
    model.rf = 0.03
    model.div = 0.01
    model.sigma = 0.3

    return model


def gbmlocalvol(process_name):

    model = xen.GBMLocalVol(process_name)
    model.x0 = 100

    model.rf_curve.tenor = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M']
    model.rf_curve.value = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229]
    model.div_curve.tenor = ['100Y']
    model.div_curve.value = [0.005]

    model.sigma_surface.tenor = ['1Y', '2Y', '3Y', '4Y', '5Y', '100Y']
    model.sigma_surface.strike = (model.x0 * np.array([0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4])).tolist()

    model.sigma_surface.matrix = [[0.3, 0.29, 0.28, 0.27, 0.26, 0.26],
                                 [0.3, 0.29, 0.28, 0.27, 0.26, 0.26],
                                 [0.3, 0.29, 0.28, 0.27, 0.26, 0.26],
                                 [0.3, 0.29, 0.28, 0.27, 0.26, 0.26],
                                 [0.3, 0.29, 0.28, 0.27, 0.26, 0.26],
                                 [0.3, 0.29, 0.28, 0.27, 0.26, 0.26],
                                 [0.3, 0.29, 0.28, 0.27, 0.26, 0.26]]

    return model


def heston(process_name):
    model = xen.HESTON(process_name)

    model.sections["X0"] = 100
    model.rf_curve.tenor = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M']
    model.rf_curve.value = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229]
    model.div_curve.tenor = ['100Y']
    model.div_curve.value = [0.005]

    # parameter from http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.631.9340&rep=rep1&type=pdf
    # heston paper 1993
    model.v0 = 0.01
    model.kapa = 2
    model.long_variance = 0.01
    model.volofvol = 0.1
    model.rho = 0.0

    return model