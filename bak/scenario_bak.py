## coding=utf-8
#import numpy as np
#import sqlite3
#import os
#import pandas as pd
#from enum import Enum
#from collections import OrderedDict

#_bin_dir = os.environ['XENARIX_BINPATH'].replace(';', '')
#_scen_input_dir = _bin_dir + "\\scen_input_file"
#_scen_result_dir = _bin_dir + "\\scen_results"

#_cali_input_dir = _bin_dir + "\\cali_input_file"
#_cali_result_dir = _bin_dir + "\\cali_results"

#_extension = '.xen'

#class Interpolation(Enum):
#    BackwardFlat = 'BACKWARDFLAT'
#    ForwardFlat = 'FORWARDFLAT'
#    Linear = 'LINEAR'
#    LogLinear = 'LOGLINEAR'
#    CubicNaturalSpline = 'CUBICNATURALSPLINE'
#    LogCubicNaturalSpline = 'LOGCUBICNATURALSPLINE'
#    MonotonicCubicNaturalSpline = 'MONOTONICCUBICNATURALSPLINE'
#    MonotonicLogCubicNaturalSpline = 'MONOTONICLOGCUBICNATURALSPLINE'
#    KrugerCubic = 'KRUGERCUBIC'
#    KrugerLogCubic = 'KRUGERLOGCUBIC'
#    FritschButlandCubic = 'FRITSCHBUTLANDCUBIC'
#    FritschButlandLogCubic = 'FRITSCHBUTLANDLOGCUBIC'
#    Parabolic = 'PARABOLIC'
#    LogParabolic = 'LOGPARABOLIC'
#    MonotonicParabolic = 'MONOTONICPARABOLIC'
#    MonotonicLogParabolic = 'MONOTONICLOGPARABOLIC'


#class KeyValue:
#    def __init__(self, line):
#        s = line.split('=')
#        self.key = s[0]
#        self.value = None

#        if s[1].find('(') > 0:
#            self.value = []
#            ss = s[1].replace('(', ' ')
#            ss = ss.replace(')', ' ')
#            rows = ss.split(',')

#            for row in rows:
#                self.value.append(filter(None, row.split('|')))

#        elif s[1].find('|') > 0:
#            self.value = filter(None, s[1].split('|'))
#        else:
#            self.value = s[1]


#def value_to_string(v):
#    s = ''
#    if isinstance(v, list):
#        if len(v) == 1:
#            s = str(v[0])
#        else:
#            s = '|'.join([str(vv) for vv in v])
#    else:
#        s = str(v)

#    return s


## entire input information , like DOM
#class InputParser:
#    def __init__(self, contents):
#        self.contents = contents
#        self.category_names = ['GENERATIONENVIROMENT', 'PROCESSINFO', 'SHOCKINFO', 'CALCULATIONINFO']
#        self.categories = OrderedDict()

#        for nm in self.category_names:
#            self.categories[nm] = Category(nm)

#        self.load_str(self.contents)

#    def __setitem__(self, key, item):
#        self.categories[key] = item

#    def __getitem__(self, key):
#        return self.categories[key]

#    def load_str(self, contents):
#        # category ???? ????
#        contents = contents.replace('\n', '')
#        contents = contents.replace(' ', '')
#        for nm in self.category_names:
#            s = contents[contents.find('#' + nm) + len(nm) + 1:contents.find('#' + nm + '_END')]
#            self.categories[nm].category_name = nm
#            self.categories[nm].load_str(s)


#class Category:
#    def __init__(self, category_name):
#        self.category_name = category_name
#        self.tags = []

#    # ?????? tag?? ??? ??????
#    def build(self):
#        contents = ['#' + self.category_name]
#        for tag in self.tags:
#            contents.append(tag.build())

#        contents.append('#' + self.category_name + '_END')
#        contents.append('\n')

#        return '\n'.join(contents)

#    def json_dict(self):
#        v = OrderedDict()
#        for tag in self.tags:
#            if not v.has_key(tag.tag_name):
#                v[tag.tag_name] = []
#                v[tag.tag_name].append(tag.sections)
#            else:
#                v[tag.tag_name].append(tag.sections)

#        return v

#    def load_str(self, contents):
#        pos_start = contents.find('[')
#        pos_end = contents.find(']')

#        while pos_end != -1:
#            pos_start_next = contents.find('[', pos_start + 1)
#            if pos_start_next == -1:
#                pos_start_next = len(contents)

#            nm = contents[pos_start + 1:pos_end]
#            tag_contents = contents[pos_start:pos_start_next]
#            tag = Tag()
#            tag.load_str(tag_contents)
#            self.tags.append(tag)

#            pos_start = pos_start_next
#            pos_end = contents.find(']', pos_end + 1)


## ?̰? []?̰ɷ? ???ΰ?
#class Tag:
#    def __init__(self, tag_name='unknown'):
#        self.sections = OrderedDict()
#        self.tag_name = tag_name
#        self.tag_wrapper = '[]'

#    # string from sections
#    def build(self):
#        line = ['[{}]'.format(self.tag_name)]

#        # if list ?̸? ?ؾߴ?.
#        for k, v in self.sections.items():
#            if k.find('MATRIX') > 0:
#                s = '('
#                for a in v:
#                    s += '|'.join([str(e) for e in a])
#                    s += ','
#                s = s[:-1]
#                s += ')'
#                line.append(k + '=' + s + ';')
#            elif isinstance(v, list):
#                if len(v) == 1:
#                    line.append(k + '=' + str(v[0]).upper() + '|;')
#                else:
#                    line.append(k + '=' + '|'.join(str(a) for a in v) + ';')
#            else:
#                line.append(k + '=' + str(v).upper() + ';')

#        return '\n'.join(line)

#    def build_json(self):
#        return json.dumps(self.sections)

#    def load_tag(self, tag):
#        isinstance(tag, Tag)
#        for key in self.sections.keys():
#            self.sections[key] = tag.sections[key]

#        return self

#    def load_str(self, contents):
#        pos_start = contents.find('[')
#        pos_end = contents.find(']')
#        self.tag_name = contents[pos_start + 1:pos_end]

#        lines = contents[pos_end + 1:].split(';')

#        for line in lines:
#            if line != '':
#                kv = KeyValue(line)
#                self.sections[kv.key] = kv.value

#        return self

#    def set_sections(self, **kwargs):
#        for k, v in kwargs.items():
#            self.sections[k.upper()] = value_to_string(v).upper()


#class General(Tag):
#    def __init__(self):
#        Tag.__init__(self, "GENERAL")

#        self.sections["SCENARIO_ID"] = "TESTSCENID1"
#        self.sections["RESULT_ID"] = "TESTRESULTID1"
#        self.sections["REFERENCE_DATE"] = "20150902"
#        self.sections["SCENARIO_NUM"] = 30
#        self.sections["DELIMITER"] = "SPACE"
#        self.sections["MAXYEAR"] = 30
#        self.sections["N_PERYEAR"] = 52
#        self.sections["RND_TYPE"] = "DEFAULT"
#        self.sections["RND_SEED"] = 1


#class CalibrationGeneral(Tag):
#    def __init__(self):
#        Tag.__init__(self, "CALIBRATIONGENERAL")

#        self.sections["CALIBRATION_ID"] = "TESTCALIID1"
#        self.sections["RESULT_ID"] = "TESTRESULTID1"
#        self.sections["REFERENCE_DATE"] = "20150902"
#        self.sections["SCENARIO_NUM"] = 30
#        self.sections["DELIMITER"] = "SPACE"
#        self.sections["MAXYEAR"] = 30
#        self.sections["N_PERYEAR"] = 52
#        self.sections["RND_TYPE"] = "DEFAULT"
#        self.sections["RND_SEED"] = 1


#class Variable(Tag):
#    def __init__(self, variable_nm):
#        Tag.__init__(self, "VARIABLE")
#        self.sections['NAME'] = variable_nm


#class ValueVariable(Variable):
#    def __init__(self, variable_nm):
#        Variable.__init__(self, variable_nm)
#        self.sections['VALUE'] = 1000
#        self.sections['SHOCK:UP_MULTI:MULTIPLE'] = 1.1
#        self.sections['SHOCK:DOWN_MULTI:MULTIPLE'] = 0.9
#        self.sections['SHOCK:UP_ADD:ADD'] = 100
#        self.sections['SHOCK:DOWN_ADD:ADD'] = -100


#class ArrayVariable(Variable):
#    def __init__(self, variable_nm):
#        Variable.__init__(self, variable_nm)
#        value = np.array([1000, 1000, 1000, 1000, 1000])
#        self.sections['VALUE'] = value

#        self.sections['SHOCK:MULTIPLEUP:MULTIPLE'] = value * 1.1
#        self.sections['SHOCK:MULTIPLEDOWN:MULTIPLE'] = value * 0.9
#        self.sections['SHOCK:ADDUP:ADD'] = value + 100
#        self.sections['SHOCK:ADDDOWN:ADD'] = value - 100


#class CurveVariable(Variable):
#    def __init__(self, variable_nm):
#        Variable.__init__(self, variable_nm)
#        tenor = ['3M', '6M', '9M', '1Y', '2Y']
#        value = np.array([0.02, 0.02, 0.02, 0.02, 0.02])

#        self.sections["FITTING_CURVE_TENOR"] = tenor
#        self.sections["FITTING_CURVE_VALUE"] = value
#        self.sections["FITTING_CURVE_INTERPOLATION"] = "LINEAR"
#        self.sections['SHOCK:PARALLELMULTIPLEUP:MULTIPLE'] = value * 1.1
#        self.sections['SHOCK:PARALLELMULTIPLEDOWN:MULTIPLE'] = value * 0.9
#        self.sections['SHOCK:PARALLELADDUP:ADD'] = value + 0.01
#        self.sections['SHOCK:PARALLELADDDOWN:ADD'] = value - 0.01


#class VariableShock(Tag):
#    def __init__(self, variableshocks_name, owner_variable, category):
#        Tag.__init__(self, 'VARIABLESHOCK')
#        self.owner_variable = owner_variable
#        self.sections['NAME'] = variableshocks_name
#        self.category = category

#    def add_shock(self, variable_nm, shock_nm, weight):
#        nm_str = 'SHOCK' + ':' + variable_nm + ':' + shock_nm
#        self.sections[nm_str] = weight

#    def remove_shock(self, variable_nm, shock_nm):
#        nm_str = 'SHOCK' + ':' + variable_nm + ':' + shock_nm
#        self.sections.pop(nm_str)


#class ProcessShock(Tag):
#    def __init__(self, processshocks_name, owner_scen, category):
#        Tag.__init__(self, 'PROCESSSHOCK')
#        self.owner_scen = owner_scen
#        self.sections['NAME'] = processshocks_name
#        self.category = category

#    def set(self, shock_name, **kwargs):
#        pass

#    def load_tag(self, tag):
#        isinstance(tag, Tag)
#        for key in tag.sections.keys():
#            self.sections[key] = tag.sections[key]

#        return self


## processhock_name ?? ?? ?𵨿? ?ִ? shock???? ????
## shock_name?̶? ?????ؾ???.
#class ProcessShockUnderlying(ProcessShock):
#    def __init__(self, processshocks_name, owner_scen, category):
#        ProcessShock.__init__(self, processshocks_name, owner_scen, category)

#    def set(self, shock_name, **kwargs):
#        v = kwargs['value']

#        # add shock to model and ref to section
#        for model in self.owner_scen.models.values():
#            if model.is_category(self.category):
#                model.add_shock(shock_name.upper(), model.underlying_key(), model.underlying_shock_value(v))
#                shock_key = 'SHOCK_REF:{}'.format(model.model_name)
#                self.sections[shock_key] = shock_name.upper()

#    def clear_shock(self):
#        for k in self.sections.keys():
#            if 'SHOCK_REF' in k:
#                self.sections.pop(k)


#class ProcessShockVolatility(ProcessShock):
#    def __init__(self, processshocks_name, owner_scen, category):
#        ProcessShock.__init__(self, processshocks_name, owner_scen, category)


## category ????????
#class ProcessShockCustom(ProcessShock):
#    def __init__(self, processshocks_name, owner_scen):
#        ProcessShock.__init__(self, processshocks_name, owner_scen, 'one')

#    # shock_name -> shock_name in model
#    def set(self, shock_name, **kwargs):
#        model_nm = kwargs.pop('model_name')
#        shock_tuple = kwargs.popitem()
#        shk_nm = shock_name.upper()
#        target = shock_tuple[0].upper()
#        value = shock_tuple[1]

#        # if model_nm.upper() not in self.owner_scen.models:
#        #     return

#        self.owner_scen.models[model_nm.upper()].add_shock(shk_nm, target, value)
#        shock_key = 'SHOCK_REF:{}'.format(model_nm.upper())

#        if shock_key in self.sections:
#            self.sections[shock_key] = self.sections[shock_key].append(shk_nm)
#        else:
#            self.sections[shock_key] = [shk_nm]


#class ProcessShockBase(ProcessShock):
#    def __init__(self, processshocks_name, owner_scen):
#        ProcessShock.__init__(self, processshocks_name, owner_scen, 'one')


#class Correlation(Tag):
#    def __init__(self):
#        Tag.__init__(self, "CORRELATION")
#        # self.corr_matrix = np.identity(dim)

#        self.sections["CORR_LIST"] = []
#        self.sections["CORR_MATRIX"] = [[1.0]]

#    def add_model(self, model):
#        model.factor()
#        # self.corr_matrix = np.identity(dim)

#    def set_identity(self, dim):
#        self.sections['CORR_MATRIX'] = np.identity(dim)


## process model factory
#def get_model(tag):
#    isinstance(tag, Tag)
#    if tag.tag_name != 'PROCESS':
#        return None

#    model_type = tag.sections['MODEL_TYPE']
#    model_name = tag.sections['NAME']

#    if model_type == "HULLWHITE1F":
#        return HullWhite1F(model_name).load_tag(tag)
#    elif model_type == "VASICEK1F":
#        return Vasicek1F(model_name).load_tag(tag)
#    elif model_type == "BK1F":
#        return BK1F(model_name).load_tag(tag)
#    elif model_type == "EXPVASICEK1F":
#        return ExpVasicek1F(model_name).load_tag(tag)
#    elif model_type == "CIR1F":
#        return CIR1F(model_name).load_tag(tag)
#    elif model_type == "CIR1FEXT":
#        return CIR1FExt(model_name).load_tag(tag)
#    elif model_type == "G2":
#        return G2(model_name).load_tag(tag)
#    elif model_type == "G2EXT":
#        return G2Ext(model_name).load_tag(tag)
#    elif model_type == "GBM_CONST":
#        return GBMConst(model_name).load_tag(tag)
#    elif model_type == "GBM":
#        return GBM(model_name).load_tag(tag)
#    elif model_type == "GBM_LOCALVOL":
#        return GBMLocalVol(model_name).load_tag(tag)
#    elif model_type == "CEV_CONST":
#        return CEVConst(model_name).load_tag(tag)
#    elif model_type == "CEV":
#        return CEV(model_name).load_tag(tag)
#    elif model_type == "CEV_LOCALVOL":
#        return CEVLocalVol(model_name).load_tag(tag)
#    elif model_type == "HESTON":
#        return HESTON(model_name).load_tag(tag)
#    elif model_type == "GARMANKOHLHAGEN":
#        return GarmanKohlhagen(model_name).load_tag(tag)
#    else:
#        return UnknownModel(model_name, model_type)


#class ProcessModel(Tag):
#    def __init__(self, model_name, model_type):
#        Tag.__init__(self, "PROCESS")
#        self.model_name = model_name
#        self.model_type = model_type

#        self.sections["NAME"] = self.model_name
#        self.sections["MODEL_TYPE"] = self.model_type
#        self.sections['CALCULATION'] = ['VALUE']

#    def is_category(self, category):
#        pass

#    def underlying_key(self):
#        pass

#    def underlying_shock_value(self, value):
#        pass

#    def factor(self):
#        pass

#    def check_type(self, calc):
#        return True

#    def add_shock(self, shock_name, target, value):
#        key = target + ':SHOCK:' + shock_name
#        self.sections[key] = value_to_string(value)

#    def add_calc(self, calc):
#        calc_name = calc.sections['NAME'].upper()

#        if not self.check_type(calc):
#            raise Exception('not valid calculation')

#        if calc_name not in self.sections['CALCULATION']:
#            self.sections['CALCULATION'].append(calc_name)


#class UnknownModel(ProcessModel):
#    def __init__(self, model_name, model_type):
#        ProcessModel.__init__(self, model_name, model_type)


#class Ir1FModel(ProcessModel):
#    def __init__(self, model_name, model_type):
#        ProcessModel.__init__(self, model_name, model_type)

#    def factor(self):
#        return 1

#    def is_category(self, category):
#        if category.upper() == 'ALL':
#            return True
#        elif category.upper() == 'IR':
#            return True
#        else:
#            return False

#    def underlying_key(self):
#        return 'R0'

#    def underlying_shock_value(self, value):
#        return value


#class Ir2FModel(ProcessModel):
#    def __init__(self, model_name, model_type):
#        ProcessModel.__init__(self, model_name, model_type)

#    def factor(self):
#        return 2

#    def is_category(self, category):
#        if category.upper() == 'ALL':
#            return True
#        elif category.upper() == 'IR':
#            return True
#        else:
#            return False

#    def underlying_key(self):
#        return 'R0'

#    def underlying_shock_value(self, value):
#        return value


#class HullWhite1F(Ir1FModel):
#    def __init__(self, model_name):
#        Ir1FModel.__init__(self, model_name, "HULLWHITE1F")

#        self.sections["FITTING_CURVE_TENOR"] = []
#        self.sections["FITTING_CURVE_VALUE"] = []
#        self.sections["PARA_ALPHA_TENOR"] = []
#        self.sections["PARA_SIGMA_TENOR"] = []
#        self.sections["PARA_ALPHA_VALUE"] = []
#        self.sections["PARA_SIGMA_VALUE"] = []
#        self.sections["PARA_ALPHA_FIXES"] = []
#        self.sections["PARA_SIGMA_FIXES"] = []

#        # self.fitting_curve_tenor = self.sections["FITTING_CURVE_TENOR"]
#        # self.fitting_curve_value = self.sections["FITTING_CURVE_VALUE"]
#        self.sections["FITTING_CURVE_INTERPOLATION"] = "LINEAR"

#        # self.para_tenor = self.sections["PARA_TENOR"]
#        # self.para_alpha_value = self.sections["PARA_ALPHA_VALUE"]
#        # self.para_sigma_value = self.sections["PARA_SIGMA_VALUE"]

#    def underlying_key(self):
#        return 'FITTING_CURVE_VALUE'

#    def underlying_shock_value(self, value):
#        v = value

#        if not isinstance(value, list):
#            v = [value] * len(self.sections['FITTING_CURVE_VALUE'])

#        return v


## brigo 93p : humped vol model
#class MV1F(Ir1FModel):
#    def __init__(self, model_name):
#        Ir1FModel.__init__(self, model_name, "HULLWHITE1F")

#        self.sections["FITTING_CURVE_TENOR"] = []
#        self.sections["FITTING_CURVE_VALUE"] = []
#        self.sections["PARA_ALPHA_TENOR"] = []
#        self.sections["PARA_SIGMA_TENOR"] = []
#        self.sections["PARA_ALPHA_VALUE"] = []
#        self.sections["PARA_SIGMA_VALUE"] = []
#        self.sections["PARA_ALPHA_FIXES"] = []
#        self.sections["PARA_SIGMA_FIXES"] = []

#        # self.fitting_curve_tenor = self.sections["FITTING_CURVE_TENOR"]
#        # self.fitting_curve_value = self.sections["FITTING_CURVE_VALUE"]
#        self.sections["FITTING_CURVE_INTERPOLATION"] = "LINEAR"

#        # self.para_tenor = self.sections["PARA_TENOR"]
#        # self.para_alpha_value = self.sections["PARA_ALPHA_VALUE"]
#        # self.para_sigma_value = self.sections["PARA_SIGMA_VALUE"]

#    def underlying_key(self):
#        return 'FITTING_CURVE_VALUE'

#    def underlying_shock_value(self, value):
#        v = value

#        if not isinstance(value, list):
#            v = [value] * len(self.sections['FITTING_CURVE_VALUE'])

#        return v


#class Vasicek1F(Ir1FModel):
#    def __init__(self, model_name):
#        Ir1FModel.__init__(self, model_name, "VASICEK1F")
#        # self.r0 = 0.03
#        # self.para_alpha = 0.1
#        # self.para_sigma = 0.1
#        # self.para_longterm = 0.1

#        self.sections["R0"] = 0.03
#        self.sections["PARA_R0_FIX"] = False

#        self.sections["PARA_ALPHA"] = 0.1
#        self.sections["PARA_ALPHA_FIX"] = False
#        self.sections["PARA_SIGMA"] = 0.1
#        self.sections["PARA_SIGMA_FIX"] = False
#        self.sections["PARA_LONGTERM"] = 0.1
#        self.sections["PARA_LONGTERM_FIX"] = False


#class BK1F(Ir1FModel):
#    def __init__(self, model_name):
#        Ir1FModel.__init__(self, model_name, "BK1F")

#        self.sections["FITTING_CURVE_TENOR"] = []
#        self.sections["FITTING_CURVE_VALUE"] = []
#        self.sections["PARA_ALPHA_TENOR"] = []
#        self.sections["PARA_SIGMA_TENOR"] = []
#        self.sections["PARA_ALPHA_VALUE"] = []
#        self.sections["PARA_SIGMA_VALUE"] = []

#        # self.fitting_curve_tenor = self.sections["FITTING_CURVE_TENOR"]
#        # self.fitting_curve_value = self.sections["FITTING_CURVE_VALUE"]
#        self.sections["FITTING_CURVE_INTERPOLATION"] = "LINEAR"

#        # self.para_tenor = self.sections["PARA_TENOR"]
#        # self.para_alpha_value = self.sections["PARA_ALPHA_VALUE"]
#        # self.para_sigma_value = self.sections["PARA_SIGMA_VALUE"]

#    def underlying_key(self):
#        return 'FITTING_CURVE_VALUE'

#    def underlying_shock_value(self, value):
#        v = value

#        if not isinstance(value, list):
#            v = [value] * len(self.sections['FITTING_CURVE_VALUE'])

#        return v


#class ExpVasicek1F(Ir1FModel):
#    def __init__(self, model_name):
#        Ir1FModel.__init__(self, model_name, "EXPVASICEK1F")
#        # self.r0 = 0.03
#        # self.para_alpha = 0.1
#        # self.para_sigma = 0.1
#        # self.para_longterm = 0.1

#        self.sections["R0"] = 0.03
#        self.sections["PARA_ALPHA"] = 0.1
#        self.sections["PARA_ALPHA_FIX"] = False
#        self.sections["PARA_SIGMA"] = 0.1
#        self.sections["PARA_SIGMA_FIX"] = False
#        self.sections["PARA_LONGTERM"] = 0.1
#        self.sections["PARA_LONGTERM_FIX"] = False


#class CIR1F(Ir1FModel):
#    def __init__(self, model_name):
#        Ir1FModel.__init__(self, model_name, "CIR1F")
#        # self.r0 = 0.03
#        # self.para_alpha = 0.1
#        # self.para_sigma = 0.1
#        # self.para_longterm = 0.1

#        self.sections["R0"] = 0.03
#        self.sections["PARA_R0_FIX"] = False

#        self.sections["PARA_ALPHA"] = 0.1
#        self.sections["PARA_ALPHA_FIX"] = False
#        self.sections["PARA_SIGMA"] = 0.1
#        self.sections["PARA_SIGMA_FIX"] = False
#        self.sections["PARA_LONGTERM"] = 0.1
#        self.sections["PARA_LONGTERM_FIX"] = False


#class CIR1FExt(Ir1FModel):
#    def __init__(self, model_name):
#        Ir1FModel.__init__(self, model_name, "CIR1FEXT")
#        # self.r0 = 0.03
#        # self.para_alpha = 0.1
#        # self.para_sigma = 0.1
#        # self.para_longterm = 0.1

#        self.sections["FITTING_CURVE_TENOR"] = []
#        self.sections["FITTING_CURVE_VALUE"] = []

#        self.sections["R0"] = 0.03
#        self.sections["PARA_R0_FIX"] = False

#        self.sections["PARA_ALPHA"] = 0.1
#        self.sections["PARA_ALPHA_FIX"] = False
#        self.sections["PARA_SIGMA"] = 0.1
#        self.sections["PARA_SIGMA_FIX"] = False
#        self.sections["PARA_LONGTERM"] = 0.1
#        self.sections["PARA_LONGTERM_FIX"] = False

#        # self.fitting_curve_tenor = self.sections["FITTING_CURVE_TENOR"]
#        # self.fitting_curve_value = self.sections["FITTING_CURVE_VALUE"]
#        self.sections["FITTING_CURVE_INTERPOLATION"] = "LINEAR"


#class G2(Ir2FModel):
#    def __init__(self, model_name):
#        Ir2FModel.__init__(self, model_name, "G2")

#        self.sections["R0"] = 0.03
#        self.sections["PARA_R0_FIX"] = False

#        self.sections["PARA_ALPHA1"] = []
#        self.sections["PARA_SIGMA1"] = []
#        self.sections["PARA_ALPHA1_FIX"] = []
#        self.sections["PARA_SIGMA1_FIX"] = []

#        self.sections["PARA_ALPHA2"] = []
#        self.sections["PARA_SIGMA2"] = []
#        self.sections["PARA_ALPHA2_FIX"] = []
#        self.sections["PARA_SIGMA2_FIX"] = []
        
#        self.sections["RHO"] = 0.5

#        # self.fitting_curve_tenor = self.sections["FITTING_CURVE_TENOR"]
#        # self.fitting_curve_value = self.sections["FITTING_CURVE_VALUE"]
#        self.sections["FITTING_CURVE_INTERPOLATION"] = "LINEAR"

#        # self.para_tenor = self.sections["PARA_TENOR"]
#        # self.para_alpha_value = self.sections["PARA_ALPHA_VALUE"]
#        # self.para_sigma_value = self.sections["PARA_SIGMA_VALUE"]

#    def underlying_key(self):
#        return 'FITTING_CURVE_VALUE'

#    def underlying_shock_value(self, value):
#        v = value

#        if not isinstance(value, list):
#            v = [value] * len(self.sections['FITTING_CURVE_VALUE'])

#        return v


#class G2Ext(Ir2FModel):
#    def __init__(self, model_name):
#        Ir2FModel.__init__(self, model_name, "G2EXT")

#        self.sections["FITTING_CURVE_TENOR"] = []
#        self.sections["FITTING_CURVE_VALUE"] = []
#        self.sections["PARA_ALPHA1_TENOR"] = []
#        self.sections["PARA_SIGMA1_TENOR"] = []
#        self.sections["PARA_ALPHA1_VALUE"] = []
#        self.sections["PARA_SIGMA1_VALUE"] = []
#        self.sections["PARA_ALPHA1_FIXES"] = []
#        self.sections["PARA_SIGMA1_FIXES"] = []

#        self.sections["PARA_ALPHA2_TENOR"] = []
#        self.sections["PARA_SIGMA2_TENOR"] = []
#        self.sections["PARA_ALPHA2_VALUE"] = []
#        self.sections["PARA_SIGMA2_VALUE"] = []
#        self.sections["PARA_ALPHA2_FIXES"] = []
#        self.sections["PARA_SIGMA2_FIXES"] = []

#        # self.fitting_curve_tenor = self.sections["FITTING_CURVE_TENOR"]
#        # self.fitting_curve_value = self.sections["FITTING_CURVE_VALUE"]
#        self.sections["FITTING_CURVE_INTERPOLATION"] = "LINEAR"

#        # self.para_tenor = self.sections["PARA_TENOR"]
#        # self.para_alpha_value = self.sections["PARA_ALPHA_VALUE"]
#        # self.para_sigma_value = self.sections["PARA_SIGMA_VALUE"]

#    def underlying_key(self):
#        return 'FITTING_CURVE_VALUE'

#    def underlying_shock_value(self, value):
#        v = value

#        if not isinstance(value, list):
#            v = [value] * len(self.sections['FITTING_CURVE_VALUE'])

#        return v


#class Eq1FModel(ProcessModel):
#    def __init__(self, model_name, model_type):
#        ProcessModel.__init__(self, model_name, model_type)

#    def factor(self):
#        return 1

#    def underlying_key(self):
#        return 'X0'

#    def is_category(self, category):
#        if category.upper() == 'ALL':
#            return True
#        elif category.upper() == 'EQ':
#            return True
#        else:
#            return False

#    def underlying_shock_value(self, value):
#        return float(self.sections['X0']) * value


#class Eq2FModel(ProcessModel):
#    def __init__(self, model_name, model_type):
#        ProcessModel.__init__(self, model_name, model_type)

#    def factor(self):
#        return 2

#    def is_category(self, category):
#        if category == 'all':
#            return True
#        elif category == 'eq':
#            return True
#        else:
#            return False

#    def underlying_key(self):
#        return 'X0'

#    def underlying_shock_value(self, value):
#        return float(self.sections['X0']) * value


#class GBM(Eq1FModel):
#    def __init__(self, model_name, **arg):
#        Eq1FModel.__init__(self, model_name, "GBM")

#        # self.x0 = 100
#        # self.curve_tenor = []
#        # self.rf_curve_value = []
#        # self.div_curve_value = []
#        # self.sigma_curve_value = []
#        #
#        # self.rf_curve_interpolation = "LINEAR"
#        # self.div_curve_interpolation = "LINEAR"
#        # self.sigma_curve_interpolation = "LINEAR"

#        self.sections["X0"] = 100
#        self.sections["RF_CURVE_TENOR"] = []
#        self.sections["RF_CURVE_VALUE"] = []

#        self.sections["DIVIDEND_CURVE_TENOR"] = []
#        self.sections["DIVIDEND_CURVE_VALUE"] = []

#        self.sections["SIGMA_CURVE_TENOR"] = []
#        self.sections["SIGMA_CURVE_VALUE"] = []

#        self.sections["RF_CURVE_INTERPOLATION"] = "LINEAR"
#        self.sections["DIVIDEND_CURVE_INTERPOLATION"] = "LINEAR"
#        self.sections["SIGMA_CURVE_INTERPOLATION"] = "LINEAR"


#class GBMConst(Eq1FModel):
#    def __init__(self, model_name, **arg):
#        Eq1FModel.__init__(self, model_name, "GBM_CONST")
#        # self.x0 = 100
#        # self.rf = 0.03
#        # self.div = 0.01
#        # self.sigma = 0.3

#        self.sections["X0"] = 100
#        self.sections["RF"] = 0.03
#        self.sections["DIVIDEND"] = 0.01
#        self.sections["SIGMA"] = 0.3


#class GBMLocalVol(Eq1FModel):
#    def __init__(self, model_name, **arg):
#        Eq1FModel.__init__(self, model_name, "GBM_LOCALVOL")

#        # self.x0 = 100
#        # self.curve_tenor = []
#        # self.rf_curve_value = []
#        # self.rf_curve_interpolation = "LINEAR"
#        #
#        # self.div_curve_value = []
#        # self.div_curve_interpolation = "LINEAR"
#        #
#        # self.sigma_surface_moneyness = []
#        # self.sigma_surface_value = []
#        # self.sigma_surface_interpolation = "LINEAR"

#        self.sections["X0"] = 100
#        self.sections["RF_CURVE_TENOR"] = []
#        self.sections["RF_CURVE_VALUE"] = []

#        self.sections["DIVIDEND_CURVE_TENOR"] = []
#        self.sections["DIVIDEND_CURVE_VALUE"] = []

#        self.sections["SIGMA_SURFACE_TENOR"] = []
#        self.sections["SIGMA_SURFACE_STRIKE"] = []
#        self.sections["SIGMA_SURFACE_MATRIX"] = []

#        self.sections["RF_CURVE_INTERPOLATION"] = "LINEAR"
#        self.sections["DIVIDEND_CURVE_INTERPOLATION"] = "LINEAR"
#        self.sections["SIGMA_SURFACE_INTERPOLATION"] = "LINEAR"


#class CEV(Eq1FModel):
#    def __init__(self, model_name, **arg):
#        Eq1FModel.__init__(self, model_name, "CEV")

#        # self.x0 = 100
#        # self.curve_tenor = []
#        # self.rf_curve_value = []
#        # self.div_curve_value = []
#        # self.sigma_curve_value = []
#        #
#        # self.rf_curve_interpolation = "LINEAR"
#        # self.div_curve_interpolation = "LINEAR"
#        # self.sigma_curve_interpolation = "LINEAR"

#        self.sections["X0"] = 100
#        self.sections["RF_CURVE_TENOR"] = []
#        self.sections["RF_CURVE_VALUE"] = []

#        self.sections["DIVIDEND_CURVE_TENOR"] = []
#        self.sections["DIVIDEND_CURVE_VALUE"] = []

#        self.sections["SIGMA_CURVE_TENOR"] = []
#        self.sections["SIGMA_CURVE_VALUE"] = []

#        self.sections["RF_CURVE_INTERPOLATION"] = "LINEAR"
#        self.sections["DIVIDEND_CURVE_INTERPOLATION"] = "LINEAR"
#        self.sections["SIGMA_CURVE_INTERPOLATION"] = "LINEAR"

#        self.sections["LEVERAGE"] = 1.0


#class CEVConst(Eq1FModel):
#    def __init__(self, model_name, **arg):
#        Eq1FModel.__init__(self, model_name, "CEV_CONST")

#        # self.x0 = 100
#        # self.rf = 0.03
#        # self.div = 0.01
#        # self.sigma = 0.3

#        self.sections["X0"] = 100
#        self.sections["RF"] = 0.03
#        self.sections["DIVIDEND"] = 0.01
#        self.sections["SIGMA"] = 0.3
#        self.sections["LEVERAGE"] = 1.0


#class CEVLocalVol(Eq1FModel):
#    def __init__(self, model_name, **arg):
#        Eq1FModel.__init__(self, model_name, "CEV_LOCALVOL")

#        # self.x0 = 100
#        # self.curve_tenor = []
#        # self.rf_curve_value = []
#        # self.rf_curve_interpolation = "LINEAR"
#        #
#        # self.div_curve_value = []
#        # self.div_curve_interpolation = "LINEAR"
#        #
#        # self.sigma_surface_moneyness = []
#        # self.sigma_surface_value = []
#        # self.sigma_surface_interpolation = "LINEAR"

#        self.sections["X0"] = 100
#        self.sections["RF_CURVE_TENOR"] = []
#        self.sections["RF_CURVE_VALUE"] = []

#        self.sections["DIVIDEND_CURVE_TENOR"] = []
#        self.sections["DIVIDEND_CURVE_VALUE"] = []

#        self.sections["SIGMA_SURFACE_TENOR"] = []
#        self.sections["SIGMA_SURFACE_STRIKE"] = []
#        self.sections["SIGMA_SURFACE_MATRIX"] = []

#        self.sections["RF_CURVE_INTERPOLATION"] = "LINEAR"
#        self.sections["DIVIDEND_CURVE_INTERPOLATION"] = "LINEAR"
#        self.sections["SIGMA_SURFACE_INTERPOLATION"] = "LINEAR"
#        self.sections["LEVERAGE"] = 1.0


#class HESTON(Eq2FModel):
#    def __init__(self, model_name, **arg):
#        Eq2FModel.__init__(self, model_name, "HESTON")

#        # self.x0 = 100
#        # self.curve_tenor = []
#        # self.rf_curve_value = []
#        # self.div_curve_value = []
#        #
#        # self.rf_curve_interpolation = "LINEAR"
#        # self.div_curve_interpolation = "LINEAR"
#        #
#        # self.sigma = []
#        # self.v0 = 0.3
#        # self.rho = 0.5
#        # self.long_variance = 0.3
#        # self.kapa = 0.1
#        # self.volofvol = 0.3

#        self.sections["X0"] = 100
#        self.sections["RF_CURVE_TENOR"] = []
#        self.sections["RF_CURVE_VALUE"] = []

#        self.sections["DIVIDEND_CURVE_TENOR"] = []
#        self.sections["DIVIDEND_CURVE_VALUE"] = []

#        self.sections["RF_CURVE_INTERPOLATION"] = "LINEAR"
#        self.sections["DIVIDEND_CURVE_INTERPOLATION"] = "LINEAR"

#        self.sections["V0"] = 0.3
#        self.sections["KAPA"] = 0.1
#        self.sections["LONG_VARIANCE"] = 0.3
#        self.sections["VOLOFVOL"] = 0.3
#        self.sections["RHO"] = 0.5


#class GarmanKohlhagen(Eq1FModel):
#    def __init__(self, model_name, **arg):
#        Eq1FModel.__init__(self, model_name, "GARMANKOHLHAGEN")

#        self.sections["X0"] = 100

#        self.sections["DOMESTIC_RF_CURVE_TENOR"] = []
#        self.sections["DOMESTIC_RF_CURVE_VALUE"] = []

#        self.sections["FOREIGN_RF_CURVE_TENOR"] = []
#        self.sections["FOREIGN_RF_CURVE_VALUE"] = []

#        self.sections["SIGMA_CURVE_TENOR"] = []
#        self.sections["SIGMA_CURVE_VALUE"] = []

#        self.sections["DOMESTIC_RF_CURVE_INTERPOLATION"] = "LINEAR"
#        self.sections["FOREIGN_RF_CURVE_INTERPOLATION"] = "LINEAR"


#class Calculation(Tag):
#    def __init__(self, calc_name):
#        Tag.__init__(self, 'CALCULATION')
#        self.sections['NAME'] = calc_name
#        self.calc_name = calc_name
#        self.calc_type = ''


#class UnknownCalculation(Calculation):
#    def __init__(self, calc_name):
#        Calculation.__init__(self, calc_name)

#        self.sections['MODEL_CATEGORY'] = 'ALL'


#class Drift(Calculation):
#    def __init__(self):
#        Calculation.__init__(self, 'DRIFT')

#        self.sections['MODEL_CATEGORY'] = 'ALL'
#        self.sections['CALC_TYPE'] = 'DRIFT'


#class Diffusion(Calculation):
#    def __init__(self):
#        Calculation.__init__(self, 'DIFFUSION')

#        self.sections['MODEL_CATEGORY'] = 'ALL'
#        self.sections['CALC_TYPE'] = 'DIFFUSION'


#class XFirstFactor(Calculation):
#    def __init__(self):
#        Calculation.__init__(self, 'XFIRSTFACTOR')

#        self.sections['MODEL_CATEGORY'] = 'ALL'
#        self.sections['CALC_TYPE'] = 'XFIRSTFACTOR'


#class YSecondFactor(Calculation):
#    def __init__(self):
#        Calculation.__init__(self, 'YSECONDFACTOR')

#        self.sections['MODEL_CATEGORY'] = 'ALL'
#        self.sections['CALC_TYPE'] = 'YSECONDFACTOR'


#class FittingTheta(Calculation):
#    def __init__(self):
#        Calculation.__init__(self, 'FITTINGTHETA')

#        self.sections['MODEL_CATEGORY'] = 'TERMSTRUCTUREFITTINGMODEL'
#        self.sections['CALC_TYPE'] = 'DRIFT'


#class FittingAlpha(Calculation):
#    def __init__(self):
#        Calculation.__init__(self, 'FITTINGALPHA')

#        self.sections['MODEL_CATEGORY'] = 'TERMSTRUCTUREFITTINGMODEL'
#        self.sections['CALC_TYPE'] = 'FITTINGALPHA'


#class FittingForward(Calculation):
#    def __init__(self):
#        Calculation.__init__(self, 'FITTINGFORWARD')

#        self.sections['MODEL_CATEGORY'] = 'TERMSTRUCTUREFITTINGMODEL'
#        self.sections['CALC_TYPE'] = 'FITTINGFORWARD'


#class FittingSpot(Calculation):
#    def __init__(self):
#        Calculation.__init__(self, 'FITTINGSPOT')

#        self.sections['MODEL_CATEGORY'] = 'TERMSTRUCTUREFITTINGMODEL'
#        self.sections['CALC_TYPE'] = 'FITTINGSPOT'


#class FittingDiscount(Calculation):
#    def __init__(self):
#        Calculation.__init__(self, 'FITTINGDISCOUNT')

#        self.sections['MODEL_CATEGORY'] = 'TERMSTRUCTUREFITTINGMODEL'
#        self.sections['CALC_TYPE'] = 'FITTINGDISCOUNT'


#class Rate(Calculation):
#    def __init__(self, calc_name):
#        Calculation.__init__(self, calc_name)

#        self.sections['MODEL_CATEGORY'] = 'IR'


#class Spot(Rate):
#    def __init__(self, calc_name, **kwargs):
#        Calculation.__init__(self, calc_name)

#        self.sections['CALC_TYPE'] = 'SPOT'
#        self.sections['MATURITY'] = '10Y'
#        self.sections['COMPOUND'] = 'ANNUAL'
#        self.sections['OUT_VALUE_TYPE'] = 'VALUE'

#        self.set_sections(**kwargs)


## tenor ?? maturity?? ???? ???? ?????????? ??????.
#class Forward(Rate):
#    def __init__(self, calc_name, **kwargs):
#        Calculation.__init__(self, calc_name)

#        self.sections['CALC_TYPE'] = 'FORWARD'
#        self.sections['START_TENOR'] = '10Y'
#        self.sections['MATURITY'] = '10Y'
#        self.sections['FORWARD_PERIOD'] = '3M'
#        self.sections['COMPOUND'] = 'ANNUAL'
#        self.sections['OUT_VALUE_TYPE'] = 'VALUE'

#        self.set_sections(**kwargs)


#class Discount(Rate):
#    def __init__(self, calc_name, **kwargs):
#        Calculation.__init__(self, calc_name)

#        self.sections['CALC_TYPE'] = 'DISCOUNT'
#        self.sections['OUT_VALUE_TYPE'] = 'VALUE'
#        self.sections['MATURITY'] = '10Y'

#        self.set_sections(**kwargs)


#class Bond(Calculation):
#    def __init__(self, calc_name):
#        Calculation.__init__(self, calc_name)

#        self.sections['MODEL_CATEGORY'] = 'IR'


#class ZeroBond(Bond):
#    def __init__(self, calc_name, **kwargs):
#        Calculation.__init__(self, calc_name)

#        self.sections['CALC_TYPE'] = 'ZERO_BOND'

#        self.sections['NOTIONAL'] = 1.0
#        self.sections['MATURITY'] = '3Y'
#        self.sections['CONST_MATURITY'] = True
#        self.sections['ROLLOVER'] = True
#        self.sections['OUT_VALUE_TYPE'] = 'VALUE'

#        self.set_sections(**kwargs)


#class CMT(Bond):
#    def __init__(self, calc_name, **kwargs):
#        Bond.__init__(self, calc_name)

#        self.sections['CALC_TYPE'] = 'FIXED_BOND'

#        self.sections['NOTIONAL'] = 1.0
#        self.sections['MATURITY'] = '3Y'
#        self.sections['COUPON_TENOR'] = '3M'
#        self.sections['COUPON_RATE'] = 0.03
#        self.sections['DAYCOUNTER'] = 'ACTACT'
#        self.sections['COMPOUNDING'] = 'ANNUAL'
#        self.sections['CONST_MATURITY'] = True
#        self.sections['ROLLOVER'] = True
#        self.sections['OUT_VALUE_TYPE'] = 'VALUE'

#        self.set_sections(**kwargs)


#class CMS(Bond):
#    def __init__(self, calc_name, **kwargs):
#        Bond.__init__(self, calc_name)

#        self.sections['CALC_TYPE'] = 'FIXED_BOND'

#        self.sections['NOTIONAL'] = 1.0
#        self.sections['MATURITY'] = '3Y'
#        self.sections['COUPON_TENOR'] = '3M'
#        self.sections['COUPON_RATE'] = 0.03
#        self.sections['DAYCOUNTER'] = 'ACTACT'
#        self.sections['COMPOUNDING'] = 'ANNUAL'
#        self.sections['CONST_MATURITY'] = True
#        self.sections['ROLLOVER'] = True
#        self.sections['OUT_VALUE_TYPE'] = 'VALUE'

#        self.set_sections(**kwargs)


#class FixedBond(Bond):
#    def __init__(self, calc_name, **kwargs):
#        Bond.__init__(self, calc_name)

#        self.sections['CALC_TYPE'] = 'FIXED_BOND'

#        self.sections['NOTIONAL'] = 1.0
#        self.sections['MATURITY'] = '3Y'
#        self.sections['COUPON_TENOR'] = '3M'
#        self.sections['COUPON_RATE'] = 0.03
#        self.sections['DAYCOUNTER'] = 'ACTACT'
#        self.sections['COMPOUNDING'] = 'ANNUAL'
#        self.sections['CONST_MATURITY'] = True
#        self.sections['ROLLOVER'] = True
#        self.sections['OUT_VALUE_TYPE'] = 'VALUE'

#        self.set_sections(**kwargs)


#class FloatingBond(Bond):
#    def __init__(self, calc_name, **kwargs):
#        Bond.__init__(self, calc_name)

#        self.sections['CALC_TYPE'] = 'FLOATING_BOND'

#        self.sections['NOTIONAL'] = 1.0
#        self.sections['MATURITY'] = '3Y'
#        self.sections['COUPON_TENOR'] = '3M'
#        self.sections['GEARING'] = 1.0
#        self.sections['SPREAD'] = 0.03
#        self.sections['DAYCOUNTER'] = 'ACTACT'
#        self.sections['COMPOUNDING'] = 'ANNUAL'
#        self.sections['CONST_MATURITY'] = True
#        self.sections['ROLLOVER'] = True
#        self.sections['OUT_VALUE_TYPE'] = 'VALUE'

#        self.set_sections(**kwargs)


##class InverseFloatingBond(Bond):
##    def __init__(self, calc_name, **kwargs):
##        Bond.__init__(self, calc_name)

##        self.sections['NOTIONAL'] = 1.0
##        self.sections['MATURITY'] = '3Y'
##        self.sections['COUPON_TENOR'] = '3M'
##        self.sections['FIXED_RATE'] = 0.04
##        self.sections['GEARING'] = 1.0
##        self.sections['SPREAD'] = 0.03
##        self.sections['DAYCOUNTER'] = 'ACTACT'
##        self.sections['COMPOUNDING'] = 'ANNUAL'
##        self.sections['CONST_MATURITY'] = True
##        self.sections['ROLLOVER'] = True
##        self.sections['OUT_VALUE_TYPE'] = 'VALUE'

##        self.set_sections(**kwargs)


#class Option(Calculation):
#    def __init__(self, calc_name):
#        Calculation.__init__(self, calc_name)

#        self.sections['MODEL_CATEGORY'] = 'EQ'


#class VanillaOption(Option):
#    def __init__(self, calc_name, **kwargs):
#        Option.__init__(self, calc_name)

#        self.sections['CALC_TYPE'] = 'VANILLAEQOPTION'

#        self.sections['NOTIONAL'] = 1.0
#        self.sections['PRICING_MODEL'] = 'BLACK'
#        self.sections['MATURITY'] = '3Y'
#        self.sections['RF'] = 0.03
#        self.sections['VOL'] = 0.3
#        self.sections['STRIKE'] = 1000
#        self.sections['CONST_MATURITY'] = True
#        self.sections['ROLLOVER'] = True
#        self.sections['OUT_VALUE_TYPE'] = 'VALUE'

#        self.set_sections(**kwargs)


#class BarrierOption(Option):
#    def __init__(self, calc_name, **kwargs):
#        Option.__init__(self, calc_name)


#class CapFloor(Option):
#    pass


#class Swaption(Option):
#    pass


#class Volatility(Calculation):
#    def __init__(self, calc_name):
#        Calculation.__init__(self, calc_name)

#        self.sections['MODEL_CATEGORY'] = 'ALL'


#class HistVolatility(Volatility):
#    def __init__(self, calc_name, **kwargs):
#        Volatility.__init__(self, calc_name)

#        self.sections['CALC_TYPE'] = 'HISTVOLATILITY'
#        self.sections['AVER_PEORIOD'] = '1Y'

#        self.set_sections(**kwargs)


#class EwmaVolatility(Volatility):
#    def __init__(self, calc_name, **kwargs):
#        Volatility.__init__(self, calc_name)

#        self.sections['CALC_TYPE'] = 'EWMAVOLATILITY'

#        self.sections['AVER_PEORIOD'] = '1Y'
#        self.sections['LAMBDA'] = 0.9

#        self.set_sections(**kwargs)

## class VanillaIRS(Calculation):
##     def __init__(self):
##         pass


## class Cash(Calculation):
##     def __init__(self):
##         pass


## class Futures(Calculation):
##     def __init__(self):
##         pass

## calculation factory

#def get_calculation(tag):
#    isinstance(tag, Tag)
#    # if tag.tag_name != '':
#    #     return None

#    calc_type = tag.sections['CALC_TYPE']
#    calc_name = tag.sections['NAME']

#    if calc_type == "SPOT":
#        return Spot(calc_name).load_tag(tag)
#    elif calc_type == "FORWARD":
#        return Forward(calc_name).load_tag(tag)
#    elif calc_type == "DISCOUNT":
#        return Discount(calc_name).load_tag(tag)
#    elif calc_type == "CMT":
#        return CMT(calc_name).load_tag(tag)
#    elif calc_type == "CMS":
#        return CMS(calc_name).load_tag(tag)
#    elif calc_type == "ZERO_BOND":
#        return ZeroBond(calc_name).load_tag(tag)
#    elif calc_type == "FIXED_BOND":
#        return FixedBond(calc_name).load_tag(tag)
#    elif calc_type == "FLOATING_BOND":
#        return FloatingBond(calc_name).load_tag(tag)
#    # elif calc_type == "INVERSE_FLOATING_BOND":
#    #    return InverseFloatingBond(calc_name).load_tag(tag)
#    elif calc_type == "VANILLAEQOPTION":
#        return VanillaOption(calc_name).load_tag(tag)
#    elif calc_type == "BARRIEREQOPTION":
#        return BarrierOption(calc_name).load_tag(tag)
#    elif calc_type == "HISTVOLATILITY":
#        return HistVolatility(calc_name).load_tag(tag)
#    elif calc_type == "EWMAVOLATILITY":
#        return EwmaVolatility(calc_name).load_tag(tag)
#    else:
#        return UnknownCalculation(calc_name)


#class CalibrationTool(Tag):
#    def __init__(self, tool_name):
#        Tag.__init__(self, 'CALIBRATIONTOOL')
#        self.sections['NAME'] = tool_name
#        self.tool_name = tool_name
#        self.tool_type = ''


#class CapTool(CalibrationTool):
#    def __init__(self, tool_name, **kwargs):
#        CalibrationTool.__init__(self, tool_name)

#        self.sections['CALIBRATION_TOOL_TYPE'] = 'CAP'

#        self.sections['DISCOUNT_CURVE_VALUE'] = [0.03, 0.031, 0.032, 0.033]
#        self.sections['DISCOUNT_CURVE_TENOR'] = ['1Y', '2Y', '3Y', '4Y']
#        self.sections['DISCOUNT_CURVE_INTERPOLATION'] = 'MONOTONICCUBICNATURALSPLINE'

#        self.sections['CAP_VOL_CURVE_VALUE'] = [0.3, 0.31, 0.32, 0.33]
#        self.sections['CAP_VOL_CURVE_TENOR'] = ['3M', '6M', '9M', '12M']

#        self.sections['CAP_VOL_CURVE_STRIKE'] = [0.03, 0.03, 0.03, 0.03]

#        self.sections['REF_INDEX'] = 'CD91'

#        self.set_sections(**kwargs)


#class SwaptionTool(CalibrationTool):
#    def __init__(self, tool_name, **kwargs):
#        CalibrationTool.__init__(self, tool_name)

#        self.sections['CALIBRATION_TOOL_TYPE'] = 'SWAPTION'

#        self.sections['DISCOUNT_CURVE_VALUE'] = [0.03, 0.031, 0.032, 0.033]
#        self.sections['DISCOUNT_CURVE_TENOR'] = ['3M', '6M', '9M', '12M']
#        self.sections['DISCOUNT_CURVE_INTERPOLATION'] = 'MONOTONICCUBICNATURALSPLINE'

#        self.sections['SWAPTION_VOL_SURFACE_VALUE'] = [0.03, 0.031, 0.032, 0.033]
#        self.sections['SWAPTION_VOL_SURFACE_EXPIRY'] = ['3M', '6M', '9M', '12M', ]
#        self.sections['SWAPTION_VOL_SURFACE_STRIKE'] = [0.03, 0.03, 0.03, 0.03]
#        self.sections['SWAP_MATURITY'] = '1Y'
#        self.sections['REF_INDEX'] = 'CD91'

#        self.set_sections(**kwargs)


#class UnknownCalibrationTool(CalibrationTool):
#    pass


#def get_calibrationtool(tag):
#    isinstance(tag, Tag)
#    # if tag.tag_name != '':
#    #     return None

#    tool_type = tag.sections['CALIBRATION_TOOL_TYPE']
#    tool_name = tag.sections['NAME']

#    if tool_type == "CAP":
#        return CapTool(tool_name).load_tag(tag)
#    elif tool_type == "SWAPTION":
#        return SwaptionTool(tool_name).load_tag(tag)
#    else:
#        return UnknownCalibrationTool(tool_name)


## global method
#def get_calibrator(cali_id):
#    cali = Calibrator()
#    cali.load(cali_id)

#    return scen


#class Calibrator:
#    def __init__(self):
#        self.contents = ''
#        self.calibration_enviroment_category = Category('CALIBRATIONENVIROMENT')
#        self.calibrationinfo_category = Category('CALIBRATIONINFO')

#        self.general = CalibrationGeneral()
#        self.calibrationtools = OrderedDict()
#        self.model = None

#    def save_as(self, new_id):
#        self.general.sections['CALIBRATION_ID'] = new_id
#        self.build()
#        f = open(_cali_input_dir + '\\' + new_id + _extension, 'w')
#        f.write(self.contents)
#        f.close()

#    def load(self, id):
#        fpath = _cali_input_dir + '\\' + id + _extension
#        if not os.path.exists(fpath):
#            raise IOError()

#        f = open(fpath, 'r')

#        contents = f.read()

#        self.load_contents(contents)

#    def load_contents(self, contents):

#        self.contents = contents

#        # dom ?? ????
#        inputParser = InputParser(self.contents)
#        # dom ???? generalenv ?? ??????

#        for env_tag in inputParser['GENERATIONENVIROMENT'].tags:
#            if env_tag.tag_name == 'GENERAL':
#                self.general.load_tag(env_tag)

#        # for ???? ?????? TOOL FACTORY?? ?????? ???? ????
#        for cali_tag in inputParser['CALIBRATIONINFO'].tags:
#            if cali_tag.tag_name == 'CALIBRATIONTOOL':
#                tool = get_calibrationtool(cali_tag)
#                if isinstance(tool, UnknownCalibrationTool):
#                    raise Exception('unknown model type : {}'.format(tool.tool_type))
#                if tool.tool_name not in self.calibrationtools:
#                    self.calibrationtools[tool.tool_name] = tool
#                elif tool.tool_name in self.calibrationtools:
#                    raise Exception('duplicated model name : {}'.format(tool.tool_name))
#            elif cali_tag.tag_name == 'PROCESS':
#                model = get_model(cali_tag)
#                if isinstance(model, UnknownModel):
#                    raise Exception('unknown model type : {}'.format(model.model_type))
#                self.model = model

#    def calibrate(self, cali_id=None, result_id=None):
#        if cali_id is None:
#            cali_id = self.general.sections['CALIBRATION_ID']
#        self.general.sections['CALIBRATION_ID'] = cali_id.upper()

#        if result_id is None:
#            result_id = self.general.sections['RESULT_ID']
#        self.general.sections['RESULT_ID'] = result_id.upper()

#        self.save_as(cali_id)

#        exe_nm = 'scenarioGeneratorExe.exe'
#        arg_str = ['--calibrate_file', '--calibratefilename={}'.format(cali_id) + _extension]

#        res = os.system(_bin_dir + '\\' + exe_nm + ' ' + ' '.join(arg_str))

#        print res

#    def build(self):
#        self.contents = ""

#        del self.calibration_enviroment_category.tags[:]
#        del self.calibrationinfo_category.tags[:]

#        self.calibration_enviroment_category.tags.append(self.general)

#        self.calibrationinfo_category.tags.append(self.model)

#        for tool in self.calibrationtools.values():
#            self.calibrationinfo_category.tags.append(tool)

#        self.contents = self.calibration_enviroment_category.build() \
#                      + self.calibrationinfo_category.build()


#class Scenario:
#    def __init__(self):

#        self.contents = ''

#        self.general = General()
#        self.variables = OrderedDict()
#        self.processshocks = OrderedDict()
#        self.models = OrderedDict()
#        self.calculations = OrderedDict()
#        self.correlation = Correlation()

#        self.generation_enviroment_category = Category("GENERATIONENVIROMENT")
#        self.variableinfo_category = Category("VARIABLEINFO")
#        self.processinfo_category = Category("PROCESSINFO")
#        self.calculationinfo_category = Category("CALCULATIONINFO")
#        self.shockinfo_category = Category("SHOCKINFO")
#        self.add_shock(ProcessShockBase('BASE', self))

#    def save_as(self, new_id):
#        self.build()
#        f = open(_scen_input_dir + '\\' + new_id + _extension, 'w')
#        f.write(self.contents)
#        f.close()

#    def load(self, id):
#        fpath = _scen_input_dir + '\\' + id + _extension
#        if not os.path.exists(fpath):
#            raise IOError()

#        f = open(fpath, 'r')

#        contents = f.read()

#        self.load_contents(contents)

#    def load_contents(self, contents):

#        self.contents = contents

#        # dom ?? ????
#        inputParser = InputParser(self.contents)
#        # dom ???? generalenv ?? ??????

#        for env_tag in inputParser['GENERATIONENVIROMENT'].tags:
#            if env_tag.tag_name == 'GENERAL':
#                self.general.load_tag(env_tag)

#        # shockinfo?? ?????ͼ?
#        # for ???? ?????? PROCESSSHOCK ?????? ???? ????
#        for shk_tag in inputParser['SHOCKINFO'].tags:
#            processshock_name = shk_tag.sections['NAME']
#            ps = ProcessShockCustom(processshock_name, self)
#            ps.load_tag(shk_tag)
#            self.processshocks[processshock_name] = ps

#        # calculationinfo?? ?????ͼ?
#        # for ???? ?????? CALCULATION FACTORY?? ?????? ???? ????
#        for calc_tag in inputParser['CALCULATIONINFO'].tags:
#            calc_name = calc_tag.sections['NAME']
#            calc = get_calculation(calc_tag)
#            if isinstance(calc, UnknownCalculation):
#                raise Exception('unknown calc type : {}'.format(calc.calc_type))
#            if calc_name not in self.calculations:
#                self.calculations[calc_name] = calc
#            elif calc_name in self.calculations:
#                raise Exception('duplicated calc name : {}'.format(calc.calc_type))

#        # for ???? ?????? MODEL FACTORY?? ?????? ???? ????
#        for model_tag in inputParser['PROCESSINFO'].tags:
#            if model_tag.tag_name == 'PROCESS':
#                model = get_model(model_tag)
#                if isinstance(model, UnknownModel):
#                    raise Exception('unknown model type : {}'.format(model.model_type))
#                if model.model_name not in self.models:
#                    self.models[model.model_name] = model
#                elif model.model_name in self.models:
#                    raise Exception('duplicated model name : {}'.format(model.model_name))
#            elif model_tag.tag_name == 'CORRELATION':
#                self.correlation.load_tag(model_tag)

#    def generate(self, scen_id=None, result_id=None):
#        if scen_id is None:
#            scen_id = self.general.sections['SCENARIO_ID']
#        self.general.sections['SCENARIO_ID'] = scen_id.upper()

#        if result_id is None:
#            result_id = self.general.sections['RESULT_ID']
#        self.general.sections['RESULT_ID'] = result_id.upper()

#        self.check_error()

#        self.save_as(scen_id)

#        exe_nm = 'scenarioGeneratorExe.exe'
#        arg_str = ['--scenario_file', '--scenariofilename={}'.format(scen_id) + _extension]

#        run_command = _bin_dir + '\\' + exe_nm + ' ' + ' '.join(arg_str)
#        print run_command
#        res = os.system(run_command)

#        print res

#    def add_model(self, model):
#        self.models[model.model_name] = model

#    def refresh_corr(self):
#        dim = sum([m.factor() for m in self.models.values()])
#        self.correlation.sections['CORR_LIST'] = [nm.upper() for nm in self.models.keys()]
#        self.correlation.set_identity(dim)

#    def build(self):
#        self.contents = ""

#        del self.generation_enviroment_category.tags[:]
#        del self.variableinfo_category.tags[:]
#        del self.shockinfo_category.tags[:]
#        del self.calculationinfo_category.tags[:]
#        del self.processinfo_category.tags[:]

#        self.generation_enviroment_category.tags.append(self.general)

#        for vari in self.variables.values():
#            self.variableinfo_category.tags.append(vari)

#        for shock in self.processshocks.values():
#            self.shockinfo_category.tags.append(shock)

#        for calc in self.calculations.values():
#            self.calculationinfo_category.tags.append(calc)

#        for model in self.models.values():
#            self.processinfo_category.tags.append(model)

#        self.processinfo_category.tags.append(self.correlation)

#        self.contents = self.generation_enviroment_category.build() \
#                        + self.variableinfo_category.build() \
#                        + self.shockinfo_category.build() \
#                        + self.calculationinfo_category.build() \
#                        + self.processinfo_category.build()

#        json_dict = OrderedDict()

#        json_dict[self.generation_enviroment_category.category_name] = self.generation_enviroment_category.json_dict()
#        json_dict[self.variableinfo_category.category_name] = self.variableinfo_category.json_dict()
#        json_dict[self.processinfo_category.category_name] = self.processinfo_category.json_dict()
#        json_dict[self.shockinfo_category.category_name] = self.shockinfo_category.json_dict()
#        json_dict[self.calculationinfo_category.category_name] = self.calculationinfo_category.json_dict()

#        self.json_contents = json.dumps(json_dict)

#        print self.json_contents

#    def parsing(self):
#        pass
#    # ?׳????? parsing??Ŵ

#    # result?? ?ε???.
#    # [REF_DT]         NVARCHAR (8)  NULL,
#    # [RESULT_ID]      NVARCHAR (12) NULL,
#    # [RESULT_NM]      NVARCHAR (50) NULL,
#    # [SCENARIO_ID]    NVARCHAR (12) NULL,
#    # [SHOCK_NAME]     NVARCHAR (12) NULL,
#    # [SHOCK_SEQ]      INT           NULL,
#    # [REF_INDEX_CD]   NVARCHAR (8)  NULL,
#    # [CALCULATION]    NVARCHAR (8)  NULL,
#    # [SCENARIO_NUM]   INT           NULL,
#    # [T_COUNT]        INT           NULL,
#    # [STEP_PER_YEAR]  INT           NULL,
#    # [GEN_START_TIME] NVARCHAR (17) NULL,
#    # [GEN_END_TIME]   NVARCHAR (17) NULL,
#    # [GEN_TYPE]       INT           NULL,
#    # [STATUS_MESSAGE] NVARCHAR (50) NULL,
#    # [STATUS]         INT           NULL,
#    # [DESCRIPTION]    NVARCHAR (50) NULL,
#    # [FILEPATH]       NVARCHAR (50) NULL

#    def get_result(self, result_id):
#        res = Result(self.general.sections['SCENARIO_ID'])
#        res.load(result_id)

#        return res

#    def get_result_list(self):
#        return result_list(self.general.sections['SCENARIO_ID'])

#    def get_shock_list(self):
#        return self.processshocks.keys()

#    def get_shock(self, shock_name, **kwargs):
#        typ = kwargs['type']
#        category = None
#        shk_nm = shock_name.upper()

#        if 'category' in kwargs:
#            category = kwargs['category']

#        if typ == 'underlying':
#            return ProcessShockUnderlying(shk_nm, self, category)
#        elif typ == 'base':
#            return ProcessShockBase(shk_nm, self, category)
#        elif typ == 'volatility':
#            return ProcessShockVolatility(shk_nm, self, category)
#        else:
#            return ProcessShockCustom(shk_nm, self)

#    def add_shock(self, shock):
#        self.processshocks[shock.sections['NAME']] = shock

#    def clear_calc(self):
#        self.calculations.clear()

#        for model in self.models.values():
#            model.sections['CALCULATION'] = ['VALUE']

#    def regist_calc(self, calc):
#        nm = calc.sections['NAME']

#        if nm in self.calculations:
#            raise Exception('duplicated calc_name')

#        self.calculations[calc.sections['NAME']] = calc

#    def add_calc(self, calc, **kwargs):
#        model_name = kwargs['model_name'].upper()
#        self.models[model_name].add_calc(calc)

#    def check_error(self):
#        # correlation
#        corr_dim = len(self.correlation.sections["CORR_MATRIX"])
#        process_dim = sum([m.factor() for m in self.models.values()])

#        if corr_dim != process_dim:
#            raise Exception('warning - correlation dim : ' + str(corr_dim) + ' , process num : ' + str(process_dim))


## global method
#def get_scenario(scen_id):
#    scen = Scenario()
#    scen.load(scen_id)

#    return scen


#def scenario_list():
#    return [scenario.replace(_extension, '') for scenario in os.listdir(_scen_input_dir)]


#def result_list(scen_id, filter=''):
#    result_id_list = []
#    items = os.listdir(_scen_result_dir + "\\" + scen_id)

#    for item in items:
#        if not os.path.isfile(item):
#            result_id_list.append(item)

#    return result_id_list


#class Result:
#    def __init__(self, scen_id):
#        self.scen_data_ = None
#        self.result_id_list_ = []
#        self.shock_names = []
#        self.under_names = []
#        self.scen_id_ = scen_id
#        self.result_id_ = None

#        self.result_id_list_ = self.result_list()
#        self.result_data_info = None

#    # scen id?? ?????? ?ִ? result???? ?ʱ?ȭ??.
#    # db ?׳? ?????ͷ? ?????? ?????? ????.
#    # np.vstact?
#    def result_list(self):
#        return result_list(self.scen_id_)

#    # [shock][under_nm][scen_num][t]
#    # [shock][under_nm][add_calc?][scen_num][t]
#    def load(self, result_id):
#        # resultinfo file ?? ?а?,
#        self.result_id_ = result_id
#        res_path = _scen_result_dir + '/' + self.scen_id_ + '/' + result_id + '/' + 'RESULTINFO.TXT'
#        if not os.path.exists(res_path):
#            print "result info load error. file not exist."

#        self.result_data_info = pd.read_table(res_path, delimiter='|')

#        # under
#        under_group = self.result_data_info['REF_INDEX_CD'].groupby(self.result_data_info['REF_INDEX_CD'])
#        for under_name in under_group.indices:
#            self.under_names.append(under_name)

#        # shock
#        shock_group = self.result_data_info['SHOCK_NAME'].groupby(self.result_data_info['SHOCK_NAME'])
#        for shock_name in shock_group.indices:
#            self.shock_names.append(shock_name)

#        scenario_num = self.result_data_info['SCENARIO_NUM'][0]
#        t_count = self.result_data_info['T_COUNT'][0]
#        step_per_year = self.result_data_info['STEP_PER_YEAR'][0]

#        self.scen_data_ = np.ndarray((len(self.shock_names), len(self.under_names), scenario_num, t_count),
#                                     dtype=np.float)

#        for shk_i, shk_nm in enumerate(self.shock_names):
#            for under_i, file_info in enumerate(
#                    self.result_data_info[self.result_data_info['SHOCK_NAME'] == shk_nm]['FILEPATH']):
#                if os.path.exists(file_info):
#                    self.scen_data_[shk_i][under_i] = np.memmap(file_info, np.float, mode='r',
#                                                                shape=(scenario_num, t_count))

#                    # for i, file_info in enumerate(self.result_data_info['FILEPATH']):
#                    #     if os.path.exists(file_info):
#                    #         self.scen_data_[0][i] = np.memmap(file_info, np.float, mode='r', shape=(scenario_num, t_count))

#    def export(self):
#        pass

#    def shocks(self):
#        pass

#    def get_scenario_clone(self):
#        scen = Scenario()
#        input_path = _scen_result_dir + "/" + self.scen_id_ + "/" + self.result_id_ + "INPUTINFO.TXT"
#        f = open(input_path, 'r')
#        scen.load_contents(f.read())

#        return scen


#if __name__ == "__main__":
#    _scen_id = "testscenid1"
#    scen = Scenario()
#    scen.load(_scen_id)
#    _new_scen_id = 'testnewid'
#    _result_id = 'testresultid'

#    scen.generate(_new_scen_id, _result_id)

#    model1 = GBM("kospi200_1")
#    model1.curve_tenor = ['1Y', '2Y', '3Y']
#    model1.rf_value = [0.03, 0.03, 0.03]
#    model1.div_value = [0.01, 0.01, 0.01]
#    model1.sigma_value = [0.3, 0.3, 0.3]

#    scen.add_model(model1)

#    model2 = GBMConst("kospi200_2")
#    model2.rf = 0.03
#    model2.div = 0.01
#    model2.sigma = 0.3

#    scen.add_model(model2)

#    model3 = GBMLocalVol("kospi200_3")
#    model3.curve_tenor = ['1Y', '2Y', '3Y']
#    model3.rf_value = [0.03, 0.03, 0.03]
#    model3.div_value = [0.01, 0.01, 0.01]

#    model3.sigma_surface_moneyness = [0.1, 0.2, 0.3]
#    model3.sigma_surface_value = [0.01, 0.01, 0.01]

#    scen.add_model(model3)

#    model4 = HullWhite1F("krwcd_1")
#    model4.fitting_curve_tenor = ['1Y', '2Y', '3Y']
#    model4.fitting_curve_value = [0.03, 0.03, 0.03]
#    model4.para_tenor = ['100Y']
#    model4.para_alpha_value = [0.1]
#    model4.para_sigma_value = [0.01]

#    scen.add_model(model4)

#    # scen.generate()

#    # using




