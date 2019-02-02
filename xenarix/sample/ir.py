# coding=utf-8
import xenarix as xen


def cir1f(process_name):

    model = xen.CIR1F(process_name)

    model.r0 = 0.03
    model.alpha = 0.1
    model.longterm = 0.1
    model.sigma = 0.01

    return model


def bk1f(process_name):

    model = xen.BK1F(process_name)

    model.fitting_curve.tenor = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M']
    model.fitting_curve.value = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229]
    model.alpha_curve.tenor = ['36M']
    model.alpha_curve.value = [0.1]
    model.sigma_curve.tenor = ['12M', '24M', '36M']
    model.sigma_curve.value = [0.01, 0.01, 0.01]

    model.sections["PARA_ALPHA_FIXES"] = [False]
    model.sections["PARA_SIGMA_FIXES"] = [False, False, False]

    #model.add_calc(scen.Drift())
    #model.add_calc(scen.Diffusion())
    #model.add_calc(scen.FittingTheta())
    #model.add_calc(scen.FittingAlpha())
    #model.add_calc(scen.FittingForward())
    #model.add_calc(scen.FittingSpot())
    #model.add_calc(scen.FittingDiscount())

    return model


def cir1fext(process_name):

    model = xen.CIR1FExt(process_name)

    model.fitting_curve.tenor = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M']
    model.fitting_curve.value = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229]

    model.r0 = 0.03
    model.alpha = 0.1
    model.longterm = 0.04
    model.sigma = 0.01

    return model


def g2ext(process_name):
    model = xen.G2Ext(process_name)

    model.sections["FITTING_CURVE_TENOR"] = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M', '100Y']
    model.sections["FITTING_CURVE_VALUE"] = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229, 0.0229]

    model.sections["PARA_ALPHA1_TENOR"] = ['36M']
    model.sections["PARA_SIGMA1_TENOR"] = ['12M', '24M', '36M']
    model.sections["PARA_ALPHA2_TENOR"] = ['36M']
    model.sections["PARA_SIGMA2_TENOR"] = ['12M', '24M', '36M']

    model.sections["PARA_ALPHA1_VALUE"] = [0.1]
    model.sections["PARA_SIGMA1_VALUE"] = [0.01, 0.01, 0.01]
    model.sections["PARA_ALPHA2_VALUE"] = [0.1]
    model.sections["PARA_SIGMA2_VALUE"] = [0.01, 0.01, 0.01]

    model.sections["PARA_ALPHA1_FIXES"] = [False]
    model.sections["PARA_SIGMA1_FIXES"] = [False, False, False]
    model.sections["PARA_ALPHA2_FIXES"] = [True]
    model.sections["PARA_SIGMA2_FIXES"] = [True, True, True]

    model.sections["CORR"] = 0.0

    model.add_calc(xen.XFirstFactor())
    model.add_calc(xen.YSecondFactor())
    #model.add_calc(scen.FittingTheta())
    #model.add_calc(scen.FittingAlpha())
    #model.add_calc(scen.FittingForward())
    #model.add_calc(scen.FittingSpot())
    #model.add_calc(scen.FittingDiscount())

    return model


def hw1f(process_name):

    model = xen.HullWhite1F(process_name)

    #model.fitting_curve.tenor = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M']
    #model.fitting_curve.value = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229]

    model.fitting_curve.tenor = ['1D', '3M', '6M', '12M', '24M', '30M']
    model.fitting_curve.value = [0.0147, 0.01664, 0.01631, 0.01625, 0.01638, 0.01652]

    model.alpha_curve.tenor = ['36M']
    model.alpha_curve.value = [0.1]
    model.sigma_curve.tenor = ['12M', '24M', '36M']
    model.sigma_curve.value = [0.01, 0.01, 0.01]

    model.sections["PARA_ALPHA_FIXES"] = [False]
    model.sections["PARA_SIGMA_FIXES"] = [False, False, False]

    return model


def vasicek(process_name):
    model = xen.Vasicek1F(process_name)

    model.r0 = 0.03
    model.alpha = 0.1
    model.longterm = 0.1
    model.sigma = 0.01

    return model