import xenarix as xen
import xenarix.results as xen_r
import xenarix.sample as xen_s

class VanillaEqOption:
    def __init__(self, X, maturity_date):
        self.X = X
        self.maturity_date = maturity_date

    def price(self, time_grid, resultModel):
        if not isinstance(resultModel, xen_r.ResultModel):
            raise Exception('ResultModel type is needed')

        if not isinstance(time_grid, xen_r.TimeGrid):
            raise Exception('TimeGrid type is needed')

        tf_d = time_grid.has_date(self.maturity_date)
        #tf_t = time_grid.has_t(t)

        t_row = time_grid.find_row_by_date(self.maturity_date, interpolation=False)

        resultModel.interpolate()








def eq_up_out_call():
    scen_set = xen.ScenarioSet('test_set')
    scen = xen.Scenario('eq_multi', 'pricing1')

    model_eq1 = xen_s.gbmconst('eq1')
    model_eq2 = xen_s.gbmconst('eq2')

    scen.add_model(model_eq1)
    scen.add_model(model_eq2)
    scen.refresh_corr()

    scen_set.add_scenario(scen)

    scen_set.generate()

# eq_up_out_call()

