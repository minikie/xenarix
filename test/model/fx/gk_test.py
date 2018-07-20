# coding=euc-kr
import xenarix as scen

def test():
    model = scen.GarmanKohlhagen('gk_model')

    model.sections["X0"] = 100
    model.sections["DOMESTIC_RF_CURVE_TENOR"] = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M', '100Y']
    model.sections["DOMESTIC_RF_CURVE_VALUE"] = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229, 0.0229]

    model.sections["FOREIGN_RF_CURVE_TENOR"] = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M', '100Y']
    model.sections["FOREIGN_RF_CURVE_VALUE"] = [0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005]

    model.sections["SIGMA_CURVE_TENOR"] = ['5Y', '100Y']
    model.sections["SIGMA_CURVE_VALUE"] = [0.3, 0.2]

    scen1 = scen.Scenario()
    scen1.add_model(model)
    scen1.save_as('gk_test')
    scen1.generate('gk_test', 'gk_result')

if __name__ == "__main__":
    test()