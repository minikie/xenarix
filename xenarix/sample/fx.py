# coding=utf-8
import xenarix as xen


def gk(process_name):

    model = xen.GarmanKohlhagen(process_name)

    model.sections["X0"] = 100

    model.dom_rf_curve.tenor = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M']
    model.dom_rf_curve.value = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229]
    model.for_rf_curve.tenor = ['100Y']
    model.for_rf_curve.value = [0.005]
    model.sigma_curve.tenor = ['5Y', '100Y']
    model.sigma_curve.value = [0.3, 0.2]

    return model
