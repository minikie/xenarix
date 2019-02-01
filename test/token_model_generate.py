# assumption

# Daily Transaction ( Each country )
# Exchange Rate ( ex) USD/KRW , JPY/KRW ... )
# InterestRate of each country

# result
#

import xenarix as xen

def generate(scenSetID, scenID, resultID):
    maturity_tenors = ['5Y']

    scen_set = xen.ScenarioSet(scenSetID)
    scen = xen.Scenario(scenID, resultID)

    usd_curve = xen.YieldCurve(None)
    usd_curve.tenor = maturity_tenors
    usd_curve.value = [ 0.02 ]

    krw_curve = xen.YieldCurve(None)
    krw_curve.tenor = maturity_tenors
    krw_curve.value = [ 0.015 ]

    jpy_curve = xen.YieldCurve(None)
    jpy_curve.tenor = maturity_tenors
    jpy_curve.value = [0.005]


    vasicek_usd = xen.Vasicek1F('usd_shortrate')
    vasicek_usd.r0 = 0.02
    vasicek_usd.alpha = 0.1
    vasicek_usd.sigma = 0.1
    vasicek_usd.longterm = 0.1

    vasicek_krw = xen.Vasicek1F('krw_shortrate')
    vasicek_krw.r0 = 0.02
    vasicek_krw.alpha = 0.1
    vasicek_krw.sigma = 0.1
    vasicek_krw.longterm = 0.1

    vasicek_jpy = xen.Vasicek1F('jpy_shortrate')
    vasicek_jpy.r0 = 0.02
    vasicek_jpy.alpha = 0.1
    vasicek_jpy.sigma = 0.1
    vasicek_jpy.longterm = 0.1


    # fx model
    usd_krw_fx = xen.GarmanKohlhagen('usd_krw_fx')
    usd_krw_fx.x0 = 1120
    usd_krw_fx.dom_rf_curve = krw_curve
    usd_krw_fx.for_rf_curve = usd_curve

    usd_krw_fx.sigma_curve = xen.YieldCurve(None)
    usd_krw_fx.sigma_curve.tenor = maturity_tenors
    usd_krw_fx.sigma_curve.value = [0.1]

    jpy_krw_fx = xen.GarmanKohlhagen('jpy_krw_fx')
    jpy_krw_fx.x0 = 1000
    jpy_krw_fx.dom_rf_curve = krw_curve
    jpy_krw_fx.for_rf_curve = jpy_curve

    jpy_krw_fx.sigma_curve = xen.YieldCurve(None)
    jpy_krw_fx.sigma_curve.tenor = maturity_tenors
    jpy_krw_fx.sigma_curve.value = [0.1]

    usd_jpy_fx = xen.GarmanKohlhagen('usd_jpy_fx')

    usd_jpy_fx.x0 = 1.1
    usd_jpy_fx.dom_rf_curve = jpy_curve
    usd_jpy_fx.for_rf_curve = usd_curve

    usd_jpy_fx.sigma_curve = xen.YieldCurve(None)
    usd_jpy_fx.sigma_curve.tenor = maturity_tenors
    usd_jpy_fx.sigma_curve.value = [0.1]

    #
    scen.add_model(vasicek_usd)
    scen.add_model(vasicek_krw)
    scen.add_model(vasicek_jpy)
    scen.add_model(usd_krw_fx)
    scen.add_model(jpy_krw_fx)
    scen.add_model(usd_jpy_fx)

    scen.refresh_corr()
    scen_set.add_scenario(scen)

    scen_set.generate()


if __name__ == '__main__':
    generate('set1','scen1','res1')