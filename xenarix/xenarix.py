# coding=utf-8
import numpy as np
import os
from collections import OrderedDict
import datetime
from calculations import *
import results as xen_r


class General(Tag):
    def __init__(self):
        Tag.__init__(self, "GENERAL")

        self.scenario_id = "TESTSCENID1"
        self.reference_date = "20150902"
        self.scenario_num = 30
        self.delimiter = "SPACE"
        self.maxyear = 30
        self.n_peryear = 52
        self.rnd_type = "SOBOL"
        self.rnd_subtype = "SOBOL"
        self.rnd_seed = 1
        self.rnd_skip = 0
        self.moment_match = False
        self.frequency = TimeGridFrequency.Day
        self.frequency_month = 1
        self.frequency_day = 1
        self.result_id = "TESTRESULTID1"
        self.base_currency = "USD"
        self.thread_num = 1

    def pre_build(self):
        d = OrderedDict()

        self.sections["SCENARIO_ID"] = self.scenario_id
        self.sections["REFERENCE_DATE"] = self.reference_date
        self.sections["SCENARIO_NUM"] = self.scenario_num
        self.sections["DELIMITER"] = self.delimiter
        self.sections["MAXYEAR"] = self.maxyear
        self.sections["N_PERYEAR"] = self.n_peryear
        self.sections["RND_TYPE"] = self.rnd_type
        self.sections["RND_SUBTYPE"] = self.rnd_subtype
        self.sections["RND_SEED"] = self.rnd_seed
        self.sections["RND_SKIP"] = self.rnd_skip
        self.sections["MOMENTMATCH"] = self.moment_match
        self.sections["FREQUENCY"] = self.frequency
        self.sections["FREQUENCY_MONTH"] = self.frequency_month
        self.sections["FREQUENCY_DAY"] = self.frequency_day
        self.sections["RESULT_ID"] = self.result_id
        self.sections["BASE_CURRENCY"] = self.base_currency
        self.sections["THREADNUM"] = self.thread_num


        return d


class CalibrationGeneral(Tag):
    def __init__(self):
        Tag.__init__(self, "CALIBRATIONGENERAL")

        self.sections["CALIBRATION_ID"] = "TESTCALIID1"
        self.sections["RESULT_ID"] = "TESTRESULTID1"
        self.sections["REFERENCE_DATE"] = "20150902"
        self.sections["SCENARIO_NUM"] = 30
        self.sections["DELIMITER"] = "SPACE"
        self.sections["MAXYEAR"] = 30
        self.sections["N_PERYEAR"] = 52
        self.sections["RND_TYPE"] = "DEFAULT"
        self.sections["RND_SEED"] = 1


class ShockItem:
    def __init__(self, name, target_variable, type, value):
        self.name = name
        self.target_variable = target_variable
        self.type = type
        self.value = value


class VariableShock(Tag):
    def __init__(self, variableshocks_name):
        Tag.__init__(self, 'VARIABLESHOCK')
        self.sections['NAME'] = variableshocks_name
        self.shock_name = variableshocks_name
        self.shock_items = OrderedDict()

    def add_shock_item(self, target_variable, type, value):
        #nm_str = 'SHOCK' + ':' + target_variable.name + ':' + target_variable.name + '_' + type
        nm_str = target_variable.var_name + '_' + type
        self.shock_items[nm_str] = ShockItem(nm_str, target_variable, type, value)

    # SHOCK_VAR:VALUE:TESTVALUENAME1:NAME1:USE=1.0;
	# SHOCK_VAR:CURVE:TESTYIELDCURVENAME1:PARALLELADDUP:USE=1.0;
    def pre_build(self):
        for s in self.shock_items.values():
            nm_str = 'SHOCK_VAR' + ':' + s.type +  ':' + s.target_variable.var_name + ':' + s.name
            self.sections[nm_str.upper()] = 1.0

    # def add_shock(self, variable_nm, shock_nm, weight):
    #     nm_str = 'SHOCK' + ':' + variable_nm + ':' + shock_nm
    #     self.sections[nm_str] = weight
    #
    # def remove_shock(self, variable_nm, shock_nm):
    #     nm_str = 'SHOCK' + ':' + variable_nm + ':' + shock_nm
    #     self.sections.pop(nm_str)


class ProcessShock(Tag):
    def __init__(self, processshocks_name, owner_scen, category):
        Tag.__init__(self, 'PROCESSSHOCK')
        self.owner_scen = owner_scen
        self.shock_name = processshocks_name
        self.shock_items = OrderedDict()
        self.sections['NAME'] = processshocks_name
        self.category = category

    def set(self, shock_name, **kwargs):
        pass

    def load_tag(self, tag):
        isinstance(tag, Tag)
        for key in tag.sections.keys():
            self.sections[key] = tag.sections[key]

        return self


# processhock_name 은 각 모델에 있는 shock들의 집합
# shock_name이랑 구분해야함.
class ProcessShockUnderlying(ProcessShock):
    def __init__(self, processshocks_name, owner_scen, category):
        ProcessShock.__init__(self, processshocks_name, owner_scen, category)

    def set(self, shock_name, **kwargs):
        v = kwargs['value']

        # add shock to model and ref to section
        for model in self.owner_scen.models.values():
            if model.is_category(self.category):
                model.add_shock(shock_name.upper(), model.underlying_key(), model.underlying_shock_value(v))
                shock_key = 'SHOCK_REF:{}'.format(model.model_name)
                self.sections[shock_key] = shock_name.upper()

    def clear_shock(self):
        for k in self.sections.keys():
            if 'SHOCK_REF' in k:
                self.sections.pop(k)


class ProcessShockVolatility(ProcessShock):
    def __init__(self, processshocks_name, owner_scen, category):
        ProcessShock.__init__(self, processshocks_name, owner_scen, category)


# category 사용안함
class ProcessShockCustom(ProcessShock):
    def __init__(self, processshocks_name, owner_scen):
        ProcessShock.__init__(self, processshocks_name, owner_scen, 'one')

    # shock_name -> shock_name in model
    def set(self, shock_name, **kwargs):
        model_nm = kwargs.pop('model_name')
        shock_tuple = kwargs.popitem()
        shk_nm = shock_name.upper()
        target = shock_tuple[0].upper()
        value = shock_tuple[1]

        # if model_nm.upper() not in self.owner_scen.models:
        #     return

        self.owner_scen.models[model_nm.upper()].add_shock(shk_nm, target, value)
        shock_key = 'SHOCK_REF:{}'.format(model_nm.upper())

        if shock_key in self.sections:
            self.sections[shock_key] = self.sections[shock_key].append(shk_nm)
        else:
            self.sections[shock_key] = [shk_nm]


class ProcessShockBase(ProcessShock):
    def __init__(self, processshocks_name, owner_scen):
        ProcessShock.__init__(self, processshocks_name, owner_scen, 'one')


class Correlation(Tag):
    def __init__(self):
        Tag.__init__(self, "CORRELATION")
        # self.corr_matrix = np.identity(dim)

        self.sections["CORR_LIST"] = []
        self.sections["CORR_MATRIX"] = [[1.0]]

    def add_model(self, model):
        model.factor()
        # self.corr_matrix = np.identity(dim)

    def set_identity(self, dim):
        self.sections['CORR_MATRIX'] = np.identity(dim)


# process model factory
def get_model(tag):
    isinstance(tag, Tag)
    if tag.tag_name != 'PROCESS':
        return None

    model_type = tag.sections['MODEL_TYPE']
    model_name = tag.sections['NAME']

    if model_type == "HULLWHITE1F":
        return HullWhite1F(model_name).load_tag(tag)
    elif model_type == "VASICEK1F":
        return Vasicek1F(model_name).load_tag(tag)
    elif model_type == "BK1F":
        return BK1F(model_name).load_tag(tag)
    elif model_type == "EXPVASICEK1F":
        return ExpVasicek1F(model_name).load_tag(tag)
    elif model_type == "CIR1F":
        return CIR1F(model_name).load_tag(tag)
    elif model_type == "CIR1FEXT":
        return CIR1FExt(model_name).load_tag(tag)
    elif model_type == "G2":
        return G2(model_name).load_tag(tag)
    elif model_type == "G2EXT":
        return G2Ext(model_name).load_tag(tag)
    elif model_type == "GBM_CONST":
        return GBMConst(model_name).load_tag(tag)
    elif model_type == "GBM":
        return GBM(model_name).load_tag(tag)
    elif model_type == "GBM_LOCALVOL":
        return GBMLocalVol(model_name).load_tag(tag)
    elif model_type == "CEV_CONST":
        return CEVConst(model_name).load_tag(tag)
    elif model_type == "CEV":
        return CEV(model_name).load_tag(tag)
    elif model_type == "CEV_LOCALVOL":
        return CEVLocalVol(model_name).load_tag(tag)
    elif model_type == "HESTON":
        return HESTON(model_name).load_tag(tag)
    elif model_type == "GARMANKOHLHAGEN":
        return GarmanKohlhagen(model_name).load_tag(tag)
    else:
        return UnknownModel(model_name, model_type)


class UnknownModel(ProcessModel):
    def __init__(self, model_name, model_type):
        ProcessModel.__init__(self, model_name, model_type)


class Ir1FModel(ProcessModel):
    def __init__(self, model_name, model_type):
        ProcessModel.__init__(self, model_name, model_type)

    def factor(self):
        return 1

    def is_category(self, category):
        if category.upper() == 'ALL':
            return True
        elif category.upper() == 'IR':
            return True
        else:
            return False

    def underlying_key(self):
        return 'R0'

    def underlying_shock_value(self, value):
        return value


class Ir2FModel(ProcessModel):
    def __init__(self, model_name, model_type):
        ProcessModel.__init__(self, model_name, model_type)

    def factor(self):
        return 2

    def is_category(self, category):
        if category.upper() == 'ALL':
            return True
        elif category.upper() == 'IR':
            return True
        else:
            return False

    def underlying_key(self):
        return 'R0'

    def underlying_shock_value(self, value):
        return value


class YieldCurve:
    def __init__(self, owner_model):
        self.owner_model = owner_model
        self.tenor = []
        self.value = []
        self.ref = None
        self.ref_using = False
        self.interpolation = Interpolation.Linear
        self.extrapolation = Extrapolation.FLAT

    def get_sections(self, curve_name):
        d = OrderedDict()

        d[curve_name + "_CURVE_TENOR"] = self.tenor
        d[curve_name + "_CURVE_VALUE"] = self.value
        d[curve_name + "_CURVE_REF"] = 'NULL' if self.ref is None else self.ref
        d[curve_name + "_CURVE_REF_USING"] = 'FALSE' if self.ref_using else self.ref_using
        d[curve_name + "_CURVE_INTERPOLATION"] = self.interpolation.value
        d[curve_name + "_CURVE_EXTRAPOLATION"] = self.extrapolation.value

        return d


class ParaCurve:
    def __init__(self, owner_model):
        self.owner_model = owner_model
        self.tenor = []
        self.value = []
        self.ref = None
        self.ref_using = False
        self.interpolation = Interpolation.Linear
        self.extrapolation = Extrapolation.FLAT

    def get_sections(self, para_name):
        d = OrderedDict()

        d['PARA_' + para_name + "_CURVE_TENOR"] = self.tenor
        d['PARA_' + para_name + "_CURVE_VALUE"] = self.value
        d['PARA_' + para_name + "_CURVE_REF"] = 'NULL' if self.ref is None else self.ref
        d['PARA_' + para_name + "_CURVE_REF_USING"] = 'FALSE' if self.ref_using else self.ref_using
        d['PARA_' + para_name + "_CURVE_INTERPOLATION"] = self.interpolation.value

        return d


class VolSurface:
    def __init__(self, owner_model):
        self.owner_model = owner_model
        self.tenor = []
        self.strike = []
        self.matrix = []

        self.ref = None
        self.ref_using = False
        self.interpolation = Interpolation.Linear
        self.extrapolation = Extrapolation.FLAT

    def get_sections(self, surface_name):
        d = OrderedDict()

        d[surface_name + "_SURFACE_TENOR"] = self.tenor
        d[surface_name + "_SURFACE_STRIKE"] = self.strike
        d[surface_name + "_SURFACE_MATRIX"] = self.matrix
        d[surface_name + "_SURFACE_REF"] = 'NULL' if self.ref is None else self.ref
        d[surface_name + "_SURFACE_REF_USING"] = 'FALSE' if self.ref_using else self.ref_using
        d[surface_name + "_SURFACE_INTERPOLATION"] = self.interpolation.value
        d[surface_name + "_SURFACE_EXTRAPOLATION"] = self.extrapolation.value

        return d


class HullWhite1F(Ir1FModel):
    def __init__(self, model_name):
        Ir1FModel.__init__(self, model_name, "HULLWHITE1F")
        self.fitting_curve = YieldCurve(self)
        self.alpha_curve = ParaCurve(self)
        self.sigma_curve = ParaCurve(self)

    def pre_build(self):
        self.sections.update(self.fitting_curve.get_sections('FITTING'))
        self.sections.update(self.alpha_curve.get_sections('ALPHA'))
        self.sections.update(self.sigma_curve.get_sections('SIGMA'))

    def underlying_key(self):
        return 'FITTING_CURVE_VALUE'

    def underlying_shock_value(self, value):
        v = value

        if not isinstance(value, list):
            v = [value] * len(self.sections['FITTING_CURVE_VALUE'])

        return v


# brigo 93p : humped vol model
class MV1F(Ir1FModel):
    def __init__(self, model_name):
        Ir1FModel.__init__(self, model_name, "HULLWHITE1F")

        self.sections["FITTING_CURVE_TENOR"] = []
        self.sections["FITTING_CURVE_VALUE"] = []
        self.sections["PARA_ALPHA_TENOR"] = []
        self.sections["PARA_SIGMA_TENOR"] = []
        self.sections["PARA_ALPHA_VALUE"] = []
        self.sections["PARA_SIGMA_VALUE"] = []
        self.sections["PARA_ALPHA_FIXES"] = []
        self.sections["PARA_SIGMA_FIXES"] = []

        # self.fitting_curve_tenor = self.sections["FITTING_CURVE_TENOR"]
        # self.fitting_curve_value = self.sections["FITTING_CURVE_VALUE"]
        self.sections["FITTING_CURVE_INTERPOLATION"] = "LINEAR"

        # self.para_tenor = self.sections["PARA_TENOR"]
        # self.para_alpha_value = self.sections["PARA_ALPHA_VALUE"]
        # self.para_sigma_value = self.sections["PARA_SIGMA_VALUE"]

    def underlying_key(self):
        return 'FITTING_CURVE_VALUE'

    def underlying_shock_value(self, value):
        v = value

        if not isinstance(value, list):
            v = [value] * len(self.sections['FITTING_CURVE_VALUE'])

        return v


class Vasicek1F(Ir1FModel):
    def __init__(self, model_name):
        Ir1FModel.__init__(self, model_name, "VASICEK1F")
        self.r0 = 0.03
        self.alpha = 0.1
        self.sigma = 0.1
        self.longterm = 0.1

        self.sections["PARA_R0_FIX"] = False
        self.sections["PARA_ALPHA_FIX"] = False
        self.sections["PARA_SIGMA_FIX"] = False
        self.sections["PARA_LONGTERM_FIX"] = False


    def pre_build(self):
        self.sections["R0"] = self.r0
        self.sections["PARA_ALPHA"] = self.alpha
        self.sections["PARA_SIGMA"] = self.sigma
        self.sections["PARA_LONGTERM"] = self.longterm


class BK1F(Ir1FModel):
    def __init__(self, model_name):
        Ir1FModel.__init__(self, model_name, "BK1F")

        self.fitting_curve = YieldCurve(self)
        self.alpha_curve = ParaCurve(self)
        self.sigma_curve = ParaCurve(self)

    def pre_build(self):
        self.sections.update(self.fitting_curve.get_sections('FITTING'))
        self.sections.update(self.alpha_curve.get_sections('ALPHA'))
        self.sections.update(self.sigma_curve.get_sections('SIGMA'))

    def underlying_key(self):
        return 'FITTING_CURVE_VALUE'

    def underlying_shock_value(self, value):
        v = value

        if not isinstance(value, list):
            v = [value] * len(self.sections['FITTING_CURVE_VALUE'])

        return v


class ExpVasicek1F(Ir1FModel):
    def __init__(self, model_name):
        Ir1FModel.__init__(self, model_name, "EXPVASICEK1F")
        self.r0 = 0.03
        self.alpha = 0.1
        self.sigma = 0.1
        self.longterm = 0.1

        self.sections["PARA_ALPHA_FIX"] = False
        self.sections["PARA_SIGMA_FIX"] = False
        self.sections["PARA_LONGTERM_FIX"] = False

    def pre_build(self):
        self.sections["R0"] = self.r0
        self.sections["PARA_ALPHA"] = self.alpha
        self.sections["PARA_SIGMA"] = self.sigma
        self.sections["PARA_LONGTERM"] = self.longterm


class CIR1F(Ir1FModel):
    def __init__(self, model_name):
        Ir1FModel.__init__(self, model_name, "CIR1F")

        self.r0 = 0.03
        self.alpha = 0.1
        self.sigma = 0.1
        self.longterm = 0.1

        self.sections["PARA_R0_FIX"] = False
        self.sections["PARA_ALPHA_FIX"] = False
        self.sections["PARA_SIGMA_FIX"] = False
        self.sections["PARA_LONGTERM_FIX"] = False

    def pre_build(self):
        self.sections["R0"] = self.r0
        self.sections["PARA_ALPHA"] = self.alpha
        self.sections["PARA_SIGMA"] = self.sigma
        self.sections["PARA_LONGTERM"] = self.longterm


class CIR1FExt(Ir1FModel):
    def __init__(self, model_name):
        Ir1FModel.__init__(self, model_name, "CIR1FEXT")
        self.fitting_curve = YieldCurve(self)

        self.r0 = 0.03
        self.alpha = 0.1
        self.sigma = 0.1
        self.longterm = 0.1

        self.sections["PARA_R0_FIX"] = False
        self.sections["PARA_ALPHA_FIX"] = False
        self.sections["PARA_SIGMA_FIX"] = False
        self.sections["PARA_LONGTERM_FIX"] = False

    def pre_build(self):
        self.sections.update(self.fitting_curve.get_sections('FITTING'))
        self.sections["R0"] = self.r0
        self.sections["PARA_ALPHA"] = self.alpha
        self.sections["PARA_SIGMA"] = self.sigma
        self.sections["PARA_LONGTERM"] = self.longterm


class G2(Ir2FModel):
    def __init__(self, model_name):
        Ir2FModel.__init__(self, model_name, "G2")

        self.sections["R0"] = 0.03
        self.sections["PARA_R0_FIX"] = False

        self.sections["PARA_ALPHA1"] = []
        self.sections["PARA_SIGMA1"] = []
        self.sections["PARA_ALPHA1_FIX"] = []
        self.sections["PARA_SIGMA1_FIX"] = []

        self.sections["PARA_ALPHA2"] = []
        self.sections["PARA_SIGMA2"] = []
        self.sections["PARA_ALPHA2_FIX"] = []
        self.sections["PARA_SIGMA2_FIX"] = []
        
        self.sections["RHO"] = 0.5

        # self.fitting_curve_tenor = self.sections["FITTING_CURVE_TENOR"]
        # self.fitting_curve_value = self.sections["FITTING_CURVE_VALUE"]
        self.sections["FITTING_CURVE_INTERPOLATION"] = "LINEAR"

        # self.para_tenor = self.sections["PARA_TENOR"]
        # self.para_alpha_value = self.sections["PARA_ALPHA_VALUE"]
        # self.para_sigma_value = self.sections["PARA_SIGMA_VALUE"]

    def underlying_key(self):
        return 'FITTING_CURVE_VALUE'

    def underlying_shock_value(self, value):
        v = value

        if not isinstance(value, list):
            v = [value] * len(self.sections['FITTING_CURVE_VALUE'])

        return v


class G2Ext(Ir2FModel):
    def __init__(self, model_name):
        Ir2FModel.__init__(self, model_name, "G2EXT")

        self.sections["FITTING_CURVE_TENOR"] = []
        self.sections["FITTING_CURVE_VALUE"] = []
        self.sections["PARA_ALPHA1_TENOR"] = []
        self.sections["PARA_SIGMA1_TENOR"] = []
        self.sections["PARA_ALPHA1_VALUE"] = []
        self.sections["PARA_SIGMA1_VALUE"] = []
        self.sections["PARA_ALPHA1_FIXES"] = []
        self.sections["PARA_SIGMA1_FIXES"] = []

        self.sections["PARA_ALPHA2_TENOR"] = []
        self.sections["PARA_SIGMA2_TENOR"] = []
        self.sections["PARA_ALPHA2_VALUE"] = []
        self.sections["PARA_SIGMA2_VALUE"] = []
        self.sections["PARA_ALPHA2_FIXES"] = []
        self.sections["PARA_SIGMA2_FIXES"] = []

        # self.fitting_curve_tenor = self.sections["FITTING_CURVE_TENOR"]
        # self.fitting_curve_value = self.sections["FITTING_CURVE_VALUE"]
        self.sections["FITTING_CURVE_INTERPOLATION"] = "LINEAR"

        # self.para_tenor = self.sections["PARA_TENOR"]
        # self.para_alpha_value = self.sections["PARA_ALPHA_VALUE"]
        # self.para_sigma_value = self.sections["PARA_SIGMA_VALUE"]

    def underlying_key(self):
        return 'FITTING_CURVE_VALUE'

    def underlying_shock_value(self, value):
        v = value

        if not isinstance(value, list):
            v = [value] * len(self.sections['FITTING_CURVE_VALUE'])

        return v


class Eq1FModel(ProcessModel):
    def __init__(self, model_name, model_type):
        ProcessModel.__init__(self, model_name, model_type)

    def factor(self):
        return 1

    def underlying_key(self):
        return 'X0'

    def is_category(self, category):
        if category.upper() == 'ALL':
            return True
        elif category.upper() == 'EQ':
            return True
        else:
            return False

    def underlying_shock_value(self, value):
        return float(self.sections['X0']) * value


class Eq2FModel(ProcessModel):
    def __init__(self, model_name, model_type):
        ProcessModel.__init__(self, model_name, model_type)

    def factor(self):
        return 2

    def is_category(self, category):
        if category == 'all':
            return True
        elif category == 'eq':
            return True
        else:
            return False

    def underlying_key(self):
        return 'X0'

    def underlying_shock_value(self, value):
        return float(self.sections['X0']) * value




class GBM(Eq1FModel):
    def __init__(self, model_name, **arg):
        Eq1FModel.__init__(self, model_name, "GBM")

        self.x0 = 100
        self.rf_curve = YieldCurve(self)
        self.div_curve = YieldCurve(self)
        self.sigma_curve = YieldCurve(self)

    def pre_build(self):
        self.sections['X0'] = self.x0
        self.sections.update(self.rf_curve.get_sections('RF'))
        self.sections.update(self.div_curve.get_sections('DIVIDEND'))
        self.sections.update(self.sigma_curve.get_sections('SIGMA'))


class GBMConst(Eq1FModel):
    def __init__(self, model_name, **arg):
        Eq1FModel.__init__(self, model_name, "GBM_CONST")

        self.x0 = 100
        self.rf = 0.03
        self.div = 0.01
        self.sigma = 0.3




    def pre_build(self):
        self.pre_build_value('X0', self.x0)
        self.pre_build_value('RF', self.rf)
        self.pre_build_value('DIVIDEND', self.div)
        self.pre_build_value('SIGMA', self.sigma)


class GBMLocalVol(Eq1FModel):
    def __init__(self, model_name, **arg):
        Eq1FModel.__init__(self, model_name, "GBM_LOCALVOL")

        self.x0 = 100
        self.rf_curve = YieldCurve(self)
        self.div_curve = YieldCurve(self)
        self.sigma_surface = VolSurface(self)

        self.sections["SIGMA_SURFACE_TENOR"] = []
        self.sections["SIGMA_SURFACE_STRIKE"] = []
        self.sections["SIGMA_SURFACE_MATRIX"] = []

    def pre_build(self):
        self.sections['X0'] = self.x0
        self.sections.update(self.rf_curve.get_sections('RF'))
        self.sections.update(self.div_curve.get_sections('DIVIDEND'))
        self.sections.update(self.sigma_surface.get_sections('SIGMA'))


class CEV(Eq1FModel):
    def __init__(self, model_name, **arg):
        Eq1FModel.__init__(self, model_name, "CEV")

        # self.x0 = 100
        # self.curve_tenor = []
        # self.rf_curve_value = []
        # self.div_curve_value = []
        # self.sigma_curve_value = []
        #
        # self.rf_curve_interpolation = "LINEAR"
        # self.div_curve_interpolation = "LINEAR"
        # self.sigma_curve_interpolation = "LINEAR"

        self.sections["X0"] = 100
        self.sections["RF_CURVE_TENOR"] = []
        self.sections["RF_CURVE_VALUE"] = []

        self.sections["DIVIDEND_CURVE_TENOR"] = []
        self.sections["DIVIDEND_CURVE_VALUE"] = []

        self.sections["SIGMA_CURVE_TENOR"] = []
        self.sections["SIGMA_CURVE_VALUE"] = []

        self.sections["RF_CURVE_INTERPOLATION"] = "LINEAR"
        self.sections["DIVIDEND_CURVE_INTERPOLATION"] = "LINEAR"
        self.sections["SIGMA_CURVE_INTERPOLATION"] = "LINEAR"

        self.sections["LEVERAGE"] = 1.0


class CEVConst(Eq1FModel):
    def __init__(self, model_name, **arg):
        Eq1FModel.__init__(self, model_name, "CEV_CONST")

        # self.x0 = 100
        # self.rf = 0.03
        # self.div = 0.01
        # self.sigma = 0.3

        self.sections["X0"] = 100
        self.sections["RF"] = 0.03
        self.sections["DIVIDEND"] = 0.01
        self.sections["SIGMA"] = 0.3
        self.sections["LEVERAGE"] = 1.0


class CEVLocalVol(Eq1FModel):
    def __init__(self, model_name, **arg):
        Eq1FModel.__init__(self, model_name, "CEV_LOCALVOL")

        # self.x0 = 100
        # self.curve_tenor = []
        # self.rf_curve_value = []
        # self.rf_curve_interpolation = "LINEAR"
        #
        # self.div_curve_value = []
        # self.div_curve_interpolation = "LINEAR"
        #
        # self.sigma_surface_moneyness = []
        # self.sigma_surface_value = []
        # self.sigma_surface_interpolation = "LINEAR"

        self.sections["X0"] = 100
        self.sections["RF_CURVE_TENOR"] = []
        self.sections["RF_CURVE_VALUE"] = []

        self.sections["DIVIDEND_CURVE_TENOR"] = []
        self.sections["DIVIDEND_CURVE_VALUE"] = []

        self.sections["SIGMA_SURFACE_TENOR"] = []
        self.sections["SIGMA_SURFACE_STRIKE"] = []
        self.sections["SIGMA_SURFACE_MATRIX"] = []

        self.sections["RF_CURVE_INTERPOLATION"] = "LINEAR"
        self.sections["DIVIDEND_CURVE_INTERPOLATION"] = "LINEAR"
        self.sections["SIGMA_SURFACE_INTERPOLATION"] = "LINEAR"
        self.sections["LEVERAGE"] = 1.0


class HESTON(Eq2FModel):
    def __init__(self, model_name, **arg):
        Eq2FModel.__init__(self, model_name, "HESTON")

        self.x0 = 100
        self.rf_curve = YieldCurve(self)
        self.div_curve = YieldCurve(self)
        self.sigma_curve = YieldCurve(self)

        self.v0 = 0.3
        self.kapa = 0.1
        self.long_variance = 0.3
        self.volofvol = 0.3
        self.rho = 0.5

    def pre_build(self):
        self.sections['X0'] = self.x0
        self.sections.update(self.rf_curve.get_sections('RF'))
        self.sections.update(self.div_curve.get_sections('DIVIDEND'))
        self.sections.update(self.sigma_curve.get_sections('SIGMA'))
        self.sections["V0"] = self.v0
        self.sections["KAPA"] = self.kapa
        self.sections["LONG_VARIANCE"] = self.long_variance
        self.sections["VOLOFVOL"] = self.volofvol
        self.sections["RHO"] = self.rho


class GarmanKohlhagen(Eq1FModel):
    def __init__(self, model_name, **arg):
        Eq1FModel.__init__(self, model_name, "GARMANKOHLHAGEN")

        self.x0 = 100
        self.dom_rf_curve = YieldCurve(self)
        self.for_rf_curve = YieldCurve(self)
        self.sigma_curve = YieldCurve(self)

    def pre_build(self):
        self.sections['X0'] = self.x0
        self.sections.update(self.dom_rf_curve.get_sections('DOMESTIC_RF'))
        self.sections.update(self.for_rf_curve.get_sections('FOREIGN_RF'))
        self.sections.update(self.sigma_curve.get_sections('SIGMA'))


class CalibrationTool(Tag):
    def __init__(self, tool_name):
        Tag.__init__(self, 'CALIBRATIONTOOL')
        self.sections['NAME'] = tool_name
        self.tool_name = tool_name
        self.tool_type = ''


class CapTool(CalibrationTool):
    def __init__(self, tool_name, **kwargs):
        CalibrationTool.__init__(self, tool_name)

        self.sections['CALIBRATION_TOOL_TYPE'] = 'CAP'

        self.sections['DISCOUNT_CURVE_VALUE'] = [0.03, 0.031, 0.032, 0.033]
        self.sections['DISCOUNT_CURVE_TENOR'] = ['1Y', '2Y', '3Y', '4Y']
        self.sections['DISCOUNT_CURVE_INTERPOLATION'] = 'MONOTONICCUBICNATURALSPLINE'

        self.sections['CAP_VOL_CURVE_VALUE'] = [0.3, 0.31, 0.32, 0.33]
        self.sections['CAP_VOL_CURVE_TENOR'] = ['3M', '6M', '9M', '12M']

        self.sections['CAP_VOL_CURVE_STRIKE'] = [0.03, 0.03, 0.03, 0.03]

        self.sections['REF_INDEX'] = 'CD91'

        self.set_sections(**kwargs)


class SwaptionTool(CalibrationTool):
    def __init__(self, tool_name, **kwargs):
        CalibrationTool.__init__(self, tool_name)

        self.sections['CALIBRATION_TOOL_TYPE'] = 'SWAPTION'

        self.sections['DISCOUNT_CURVE_VALUE'] = [0.03, 0.031, 0.032, 0.033]
        self.sections['DISCOUNT_CURVE_TENOR'] = ['3M', '6M', '9M', '12M']
        self.sections['DISCOUNT_CURVE_INTERPOLATION'] = 'MONOTONICCUBICNATURALSPLINE'

        self.sections['SWAPTION_VOL_SURFACE_VALUE'] = [0.03, 0.031, 0.032, 0.033]
        self.sections['SWAPTION_VOL_SURFACE_EXPIRY'] = ['3M', '6M', '9M', '12M', ]
        self.sections['SWAPTION_VOL_SURFACE_STRIKE'] = [0.03, 0.03, 0.03, 0.03]
        self.sections['SWAP_MATURITY'] = '1Y'
        self.sections['REF_INDEX'] = 'CD91'

        self.set_sections(**kwargs)


class UnknownCalibrationTool(CalibrationTool):
    pass


def get_calibrationtool(tag):
    isinstance(tag, Tag)
    # if tag.tag_name != '':
    #     return None

    tool_type = tag.sections['CALIBRATION_TOOL_TYPE']
    tool_name = tag.sections['NAME']

    if tool_type == "CAP":
        return CapTool(tool_name).load_tag(tag)
    elif tool_type == "SWAPTION":
        return SwaptionTool(tool_name).load_tag(tag)
    else:
        return UnknownCalibrationTool(tool_name)


# global method
# def get_calibrator(cali_id):
#     cali = Calibrator()
#     cali.load(cali_id)
#
#     return scen


class Calibrator:
    def __init__(self):
        self.contents = ''
        self.calibration_enviroment_category = Category('CALIBRATIONENVIROMENT')
        self.calibrationinfo_category = Category('CALIBRATIONINFO')

        self.general = CalibrationGeneral()
        self.calibrationtools = OrderedDict()
        self.model = None

    def save_as(self, new_id):
        self.general.sections['CALIBRATION_ID'] = new_id
        self.build()
        f = open(xen_cali_input_dir + '\\' + new_id + xen_extension, 'w')
        f.write(self.contents)
        f.close()

    def load(self, id):
        fpath = xen_cali_input_dir + '\\' + id + xen_extension
        if not os.path.exists(fpath):
            raise IOError()

        f = open(fpath, 'r')

        contents = f.read()

        self.load_contents(contents)

    def load_contents(self, contents):

        self.contents = contents

        # dom 을 만듬
        inputParser = InputParser(self.contents)
        # dom 에서 generalenv 을 가져옴

        for env_tag in inputParser['GENERATIONENVIROMENT'].tags:
            if env_tag.tag_name == 'GENERAL':
                self.general.load_tag(env_tag)

        # for 문을 돌려서 TOOL FACTORY로 정보를 계속 박음
        for cali_tag in inputParser['CALIBRATIONINFO'].tags:
            if cali_tag.tag_name == 'CALIBRATIONTOOL':
                tool = get_calibrationtool(cali_tag)
                if isinstance(tool, UnknownCalibrationTool):
                    raise Exception('unknown model type : {}'.format(tool.tool_type))
                if tool.tool_name not in self.calibrationtools:
                    self.calibrationtools[tool.tool_name] = tool
                elif tool.tool_name in self.calibrationtools:
                    raise Exception('duplicated model name : {}'.format(tool.tool_name))
            elif cali_tag.tag_name == 'PROCESS':
                model = get_model(cali_tag)
                if isinstance(model, UnknownModel):
                    raise Exception('unknown model type : {}'.format(model.model_type))
                self.model = model

    def calibrate(self, cali_id=None, result_id=None):
        if cali_id is None:
            cali_id = self.general.sections['CALIBRATION_ID']
        self.general.sections['CALIBRATION_ID'] = cali_id.upper()

        if result_id is None:
            result_id = self.general.sections['RESULT_ID']
        self.general.sections['RESULT_ID'] = result_id.upper()

        self.save_as(cali_id)

        exe_nm = 'scenarioGeneratorExe.exe'
        arg_str = ['--calibrate_file', '--calibratefilename={}'.format(cali_id) + cali_extension]

        res = os.system(xen_bin_dir + '\\' + exe_nm + ' ' + ' '.join(arg_str))

        print(res)

    def build(self):
        self.contents = ""

        del self.calibration_enviroment_category.tags[:]
        del self.calibrationinfo_category.tags[:]

        self.calibration_enviroment_category.tags.append(self.general)

        self.calibrationinfo_category.tags.append(self.model)

        for tool in self.calibrationtools.values():
            self.calibrationinfo_category.tags.append(tool)

        self.contents = self.calibration_enviroment_category.build() \
                      + self.calibrationinfo_category.build()


class Scenario:
    def __init__(self, scen_id, result_id):

        self.contents = ''

        self.general = General()

        # self.general.sections["SCENARIO_ID"] = scen_id
        # self.general.sections["RESULT_ID"] = result_id

        self.general.scenario_id = scen_id
        self.general.result_id = result_id

        self.variables = OrderedDict()
        #self.exchange = OrderedDict() # not implemeted
        #self.processshocks = OrderedDict()
        self.shocks = OrderedDict()
        self.models = OrderedDict()
        self.calculations = OrderedDict()
        self.correlation = Correlation()

        self.generation_enviroment_category = Category("GENERATIONENVIROMENT")
        self.variableinfo_category = Category("VARIABLEINFO")
        self.exchangeinfo_category = Category("EXCHANGEINFO")
        self.calculationinfo_category = Category("CALCULATIONINFO")
        self.processinfo_category = Category("PROCESSINFO")
        self.shockinfo_category = Category("SHOCKINFO")
        self.add_shock(ProcessShockBase('BASE', self))

    def get_scen_id(self):
        return self.general.scenario_id

    def set_scen_id(self, scen_id):
        self.general.scenario_id = scen_id

    def get_result_id(self):
        return self.general.result_id

    def set_result_id(self, result_id):
        self.general.result_id = result_id

    # def save_as(self, new_id):
    #     self.build()
    #     f = open(xen_input_dir + '\\' + new_id + xen_extension, 'w')
    #     f.write(self.contents)
    #     f.close()
    #
    # def load(self, id):
    #     fpath = xen_input_dir + '\\' + id + xen_extension
    #     if not os.path.exists(fpath):
    #         raise IOError()
    #
    #     f = open(fpath, 'r')
    #
    #     contents = f.read()
    #
    #     self.load_contents(contents)

    def load_contents(self, contents):

        self.contents = contents

        # dom 을 만듬
        inputParser = InputParser(self.contents)
        # dom 에서 generalenv 을 가져옴

        for env_tag in inputParser['GENERATIONENVIROMENT'].tags:
            if env_tag.tag_name == 'GENERAL':
                self.general.load_tag(env_tag)

        # shockinfo를 가져와서
        # for 문을 돌려서 PROCESSSHOCK 정보를 계속 박음
        for shk_tag in inputParser['SHOCKINFO'].tags:
            processshock_name = shk_tag.sections['NAME']
            ps = ProcessShockCustom(processshock_name, self)
            ps.load_tag(shk_tag)
            self.processshocks[processshock_name] = ps

        # calculationinfo를 가져와서
        # for 문을 돌려서 CALCULATION FACTORY로 정보를 계속 박음
        for calc_tag in inputParser['CALCULATIONINFO'].tags:
            calc_name = calc_tag.sections['NAME']
            calc = get_calculation(calc_tag)
            if isinstance(calc, UnknownCalculation):
                raise Exception('unknown calc type : {}'.format(calc.calc_type))
            if calc_name not in self.calculations:
                self.calculations[calc_name] = calc
            elif calc_name in self.calculations:
                raise Exception('duplicated calc name : {}'.format(calc.calc_type))

        # for 문을 돌려서 MODEL FACTORY로 정보를 계속 박음
        for model_tag in inputParser['PROCESSINFO'].tags:
            if model_tag.tag_name == 'PROCESS':
                model = get_model(model_tag)
                if isinstance(model, UnknownModel):
                    raise Exception('unknown model type : {}'.format(model.model_type))
                if model.model_name not in self.models:
                    self.models[model.model_name] = model
                elif model.model_name in self.models:
                    raise Exception('duplicated model name : {}'.format(model.model_name))
            elif model_tag.tag_name == 'CORRELATION':
                self.correlation.load_tag(model_tag)

    def add_variable(self, variable):
        if not isinstance(variable, Variable):
            raise Exception('Variable type is needed')

        if variable.var_name in self.models:
            raise Exception('duplicated varaible name : ' + variable.var_name)
        self.variables[variable.var_name] = variable

    def add_model(self, model):
        if not isinstance(model, ProcessModel):
            raise Exception('ProcessModel type is needed')

        if model.model_name in self.models:
            raise Exception('duplicated model_name : ' + model.model_name)
        self.models[model.model_name] = model

    def add_shock(self, shock):
        if shock.shock_name in self.shocks:
            raise Exception('duplicated shock name : ' + shock.shock_name)
        self.shocks[shock.shock_name] = shock

    def refresh_corr(self):
        dim = sum([m.factor() for m in self.models.values()])
        self.correlation.sections['CORR_LIST'] = [nm.upper() for nm in self.models.keys()]
        self.correlation.set_identity(dim)

    def build(self):
        self.contents = ""

        del self.generation_enviroment_category.tags[:]
        del self.variableinfo_category.tags[:]
        del self.exchangeinfo_category.tags[:]
        del self.shockinfo_category.tags[:]
        del self.calculationinfo_category.tags[:]
        del self.processinfo_category.tags[:]

        PROCESSMODELNAME_LIST = []
        for model in self.models.values():
            PROCESSMODELNAME_LIST.append(model.model_name)

        self.general.sections["PROCESSMODELNAME_LIST"] = PROCESSMODELNAME_LIST

        self.generation_enviroment_category.tags.append(self.general)

        for vari in self.variables.values():
            self.variableinfo_category.tags.append(vari)

        for shock in self.shocks.values():
            self.shockinfo_category.tags.append(shock)

        for calc in self.calculations.values():
            self.calculationinfo_category.tags.append(calc)

        for model in self.models.values():
            self.processinfo_category.tags.append(model)

        self.processinfo_category.tags.append(self.correlation)

        self.contents = self.generation_enviroment_category.build() \
                        + self.variableinfo_category.build() \
                        + self.exchangeinfo_category.build() \
                        + self.calculationinfo_category.build() \
                        + self.processinfo_category.build() \
                        + self.shockinfo_category.build()

        # correlation 쪽에서 ndarray 가 json 변환이 에러났음.아직 미해결

        # json_dict = OrderedDict()
        #
        # json_dict[self.generation_enviroment_category.category_name] = self.generation_enviroment_category.json_dict()
        # json_dict[self.variableinfo_category.category_name] = self.variableinfo_category.json_dict()
        # json_dict[self.processinfo_category.category_name] = self.processinfo_category.json_dict()
        # json_dict[self.shockinfo_category.category_name] = self.shockinfo_category.json_dict()
        # json_dict[self.calculationinfo_category.category_name] = self.calculationinfo_category.json_dict()

        # self.json_contents = json.dumps(json_dict)
        #
        # print(self.json_contents)

    def generate(self, scen_set_nm):
        #scen_set_nm = 'defaultsetname'

        scen_id = self.general.scenario_id
        result_id = self.general.result_id

        self.set_shock_variables()
        self.set_calculations()
        self.check_error()

        temp_filename = self.save_temp(scen_id)

        # --setname=debug --scenario_file_temp --scenariofilename=lastgen.xen
        arg_str = ['--gen',
                   '--repo={}'.format(get_repository()),
                   '--setname={}'.format(scen_set_nm),
                   '--file={}'.format(temp_filename)]

        #run_command = xen_bin_dir + '\\' + exe_nm + ' ' + ' '.join(arg_str)
        #run_command = '.\\' + exe_nm + ' ' + ' '.join(arg_str)
        run_command = engine_path + ' ' + ' '.join(arg_str)
        print(run_command)
        res = os.system(run_command)

        print(res)

    def save_temp(self, scen_id):
        self.build()
        timestamp_str = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        filename = scen_id + '_' + timestamp_str + xen_extension
        f = open(xen_input_temp_dir() + '\\' + filename, 'w')
        f.write(self.contents)
        f.close()

        return filename

    def parsing(self):
        pass
    # 그놈한테 parsing시킴

    # result를 로드함.
    # [REF_DT]         NVARCHAR (8)  NULL,
    # [RESULT_ID]      NVARCHAR (12) NULL,
    # [RESULT_NM]      NVARCHAR (50) NULL,
    # [SCENARIO_ID]    NVARCHAR (12) NULL,
    # [SHOCK_NAME]     NVARCHAR (12) NULL,
    # [SHOCK_SEQ]      INT           NULL,
    # [REF_INDEX_CD]   NVARCHAR (8)  NULL,
    # [CALCULATION]    NVARCHAR (8)  NULL,
    # [SCENARIO_NUM]   INT           NULL,
    # [T_COUNT]        INT           NULL,
    # [STEP_PER_YEAR]  INT           NULL,
    # [GEN_START_TIME] NVARCHAR (17) NULL,
    # [GEN_END_TIME]   NVARCHAR (17) NULL,
    # [GEN_TYPE]       INT           NULL,
    # [STATUS_MESSAGE] NVARCHAR (50) NULL,
    # [STATUS]         INT           NULL,
    # [DESCRIPTION]    NVARCHAR (50) NULL,
    # [FILEPATH]       NVARCHAR (50) NULL

    # def get_result(self, result_id):
    #     res = results.ResultObj(self.general.scenario_id)
    #     res.load(result_id)
    #
    #     return res
    #
    # def get_result_list(self):
    #     return result_list(self. self.general.scenario_id)


    # def get_shock(self, shock_name, **kwargs):
    #     typ = kwargs['type']
    #     category = None
    #     shk_nm = shock_name.upper()
    #
    #     if 'category' in kwargs:
    #         category = kwargs['category']
    #
    #     if typ == 'underlying':
    #         return ProcessShockUnderlying(shk_nm, self, category)
    #     elif typ == 'base':
    #         return ProcessShockBase(shk_nm, self, category)
    #     elif typ == 'volatility':
    #         return ProcessShockVolatility(shk_nm, self, category)
    #     else:
    #         return ProcessShockCustom(shk_nm, self)

    # set shockdef to each variable
    def set_shock_variables(self):
        for shock_obj in self.shocks.values():
            for shock_item in shock_obj.shock_items.values():
                self.variables[shock_item.target_variable.var_name].add_shockdef(shock_item)


    # set calc_obj from ProcessModel class to Scenario
    # common calculation is needed
    def set_calculations(self):
        self.calculations.clear()

        for model in self.models.values():
            for calc_obj in model.calculations.values():
                self.regist_calc(calc_obj)

    def clear_calc(self):
        self.calculations.clear()

        for model in self.models.values():
            model.sections['CALCULATION'] = ['VALUE']

    def regist_calc(self, calc):
        nm = calc.sections['NAME']

        if nm in self.calculations:
            raise Exception('duplicated calc_name')

        self.calculations[nm] = calc

    def add_calc(self, calc, **kwargs):
        model_name = kwargs['model_name'].upper()
        self.models[model_name].add_calc(calc)

    def check_error(self):
        # correlation
        corr_dim = len(self.correlation.sections["CORR_MATRIX"])
        process_dim = sum([m.factor() for m in self.models.values()])

        if corr_dim != process_dim:
            raise Exception('warning - correlation dim : ' + str(corr_dim) + ' , process num : ' + str(process_dim))


class ScenarioSet:
    def __init__(self, set_name):
        self.set_name = set_name
        self.scenario_list = []

    def add_scenario(self, scenario):
        self.scenario_list.append(scenario)

    def generate(self):
        for scen in self.scenario_list:
            scen.generate(self.set_name)

    def save(self):
        self.save_as(self.set_name)

    def save_as(self, new_set_name):
        contents=''

        for scen in self.scenario_list:
            scen.build()
            contents += scen.contents
            contents += '@'

        f = open(xen_input_dir() + '\\' + new_set_name + xenset_extension, 'w')
        f.write(contents)
        f.close()


# global method
def get_scenario(scen_id):
    scen = Scenario()
    scen.load(scen_id)

    return scen


def scenario_list():
    return [scenario.replace(xen_extension, '') for scenario in os.listdir(xen_input_dir())]


# def result_list(set_nm, scen_id, filter=''):
#     result_id_list = []
#     items = os.listdir(xen_result_dir() + "\\" + set_nm + "\\" + scen_id)
#
#     for item in items:
#         if not os.path.isfile(item):
#             result_id_list.append(item)
#
#     return result_id_list


def test_martingale():
    pass


def test_generate(scenSetID, scenID, resultID):

    maturity_tenors = ['5Y']

    scen_set = ScenarioSet(scenSetID)
    scen = Scenario(scenID, resultID)

    usd_curve = YieldCurve(None)
    usd_curve.tenor = maturity_tenors
    usd_curve.value = [0.02]

    krw_curve = YieldCurve(None)
    krw_curve.tenor = maturity_tenors
    krw_curve.value = [0.015]

    model1 = GBM("kospi200_1")
    model1.rf_curve = krw_curve
    model1.div_curve.tenor = maturity_tenors
    model1.div_curve.value = [0.005]
    model1.sigma_curve.tenor = maturity_tenors
    model1.sigma_curve.value = [0.3]

    scen.add_model(model1)

    model2 = GBMConst("kospi200_2")
    model2.rf = 0.03
    model2.div = 0.01
    model2.sigma = 0.3

    scen.add_model(model2)

    model4 = HullWhite1F("krwcd_1")
    model4.fitting_curve = krw_curve
    model4.alpha_curve.tenor = ['100Y']
    model4.alpha_curve.value = [0.1]

    model4.sigma_curve.tenor = ['100Y']
    model4.sigma_curve.value = [0.01]

    scen.add_model(model4)

    scen.refresh_corr()
    scen_set.add_scenario(scen)

    scen_set.generate()




