from common import *


class Calculation(Tag):
    def __init__(self, calc_name):
        Tag.__init__(self, 'CALCULATION')
        self.sections['NAME'] = calc_name
        self.calc_name = calc_name
        self.calc_type = ''


class UnknownCalculation(Calculation):
    def __init__(self, calc_name):
        Calculation.__init__(self, calc_name)

        self.sections['MODEL_CATEGORY'] = 'ALL'


class RandomZ(Calculation):
    def __init__(self):
        Calculation.__init__(self, 'RANDOMZ')

        self.sections['MODEL_CATEGORY'] = 'ALL'
        self.sections['CALC_TYPE'] = 'RANDOMZ'


class Expectation(Calculation):
    def __init__(self):
        Calculation.__init__(self, 'EXPECTATION')

        self.sections['MODEL_CATEGORY'] = 'ALL'
        self.sections['CALC_TYPE'] = 'EXPECTATION'


class UnconditionalExpectation(Calculation):
    def __init__(self):
        Calculation.__init__(self, 'UNCONDITIONALEXPECTATION')

        self.sections['MODEL_CATEGORY'] = 'ALL'
        self.sections['CALC_TYPE'] = 'UNCONDITIONALEXPECTATION'


class Drift(Calculation):
    def __init__(self):
        Calculation.__init__(self, 'DRIFT')

        self.sections['MODEL_CATEGORY'] = 'ALL'
        self.sections['CALC_TYPE'] = 'DRIFT'


class Diffusion(Calculation):
    def __init__(self):
        Calculation.__init__(self, 'DIFFUSION')

        self.sections['MODEL_CATEGORY'] = 'ALL'
        self.sections['CALC_TYPE'] = 'DIFFUSION'


class XFirstFactor(Calculation):
    def __init__(self):
        Calculation.__init__(self, 'XFIRSTFACTOR')

        self.sections['MODEL_CATEGORY'] = 'ALL'
        self.sections['CALC_TYPE'] = 'XFIRSTFACTOR'


class YSecondFactor(Calculation):
    def __init__(self):
        Calculation.__init__(self, 'YSECONDFACTOR')

        self.sections['MODEL_CATEGORY'] = 'ALL'
        self.sections['CALC_TYPE'] = 'YSECONDFACTOR'


class FittingTheta(Calculation):
    def __init__(self):
        Calculation.__init__(self, 'FITTINGTHETA')

        self.sections['MODEL_CATEGORY'] = 'TERMSTRUCTUREFITTINGMODEL'
        self.sections['CALC_TYPE'] = 'DRIFT'


class FittingAlpha(Calculation):
    def __init__(self):
        Calculation.__init__(self, 'FITTINGALPHA')

        self.sections['MODEL_CATEGORY'] = 'TERMSTRUCTUREFITTINGMODEL'
        self.sections['CALC_TYPE'] = 'FITTINGALPHA'


class FittingForward(Calculation):
    def __init__(self):
        Calculation.__init__(self, 'FITTINGFORWARD')

        self.sections['MODEL_CATEGORY'] = 'TERMSTRUCTUREFITTINGMODEL'
        self.sections['CALC_TYPE'] = 'FITTINGFORWARD'


class FittingSpot(Calculation):
    def __init__(self):
        Calculation.__init__(self, 'FITTINGSPOT')

        self.sections['MODEL_CATEGORY'] = 'TERMSTRUCTUREFITTINGMODEL'
        self.sections['CALC_TYPE'] = 'FITTINGSPOT'


class FittingDiscount(Calculation):
    def __init__(self):
        Calculation.__init__(self, 'FITTINGDISCOUNT')

        self.sections['MODEL_CATEGORY'] = 'TERMSTRUCTUREFITTINGMODEL'
        self.sections['CALC_TYPE'] = 'FITTINGDISCOUNT'


class Rate(Calculation):
    def __init__(self, calc_name):
        Calculation.__init__(self, calc_name)

        self.sections['MODEL_CATEGORY'] = 'IR'


class Spot(Rate):
    def __init__(self, calc_name, **kwargs):
        Calculation.__init__(self, calc_name)

        self.sections['CALC_TYPE'] = 'SPOT'
        self.sections['MATURITY'] = '10Y'
        self.sections['COMPOUND'] = 'ANNUAL'
        self.sections['OUT_VALUE_TYPE'] = 'VALUE'

        self.set_sections(**kwargs)


# tenor 랑 maturity가 같은 경우 순간선도로 계산함.
class Forward(Rate):
    def __init__(self, calc_name, **kwargs):
        Calculation.__init__(self, calc_name)

        self.sections['CALC_TYPE'] = 'FORWARD'
        self.sections['START_TENOR'] = '10Y'
        self.sections['MATURITY'] = '10Y'
        self.sections['FORWARD_PERIOD'] = '3M'
        self.sections['COMPOUND'] = 'ANNUAL'
        self.sections['OUT_VALUE_TYPE'] = 'VALUE'

        self.set_sections(**kwargs)


class Discount(Rate):
    def __init__(self, calc_name, **kwargs):
        Calculation.__init__(self, calc_name)

        self.sections['CALC_TYPE'] = 'DISCOUNT'
        self.sections['OUT_VALUE_TYPE'] = 'VALUE'
        self.sections['MATURITY'] = '10Y'

        self.set_sections(**kwargs)


class Bond(Calculation):
    def __init__(self, calc_name):
        Calculation.__init__(self, calc_name)

        self.sections['MODEL_CATEGORY'] = 'IR'


class ZeroBond(Bond):
    def __init__(self, calc_name, **kwargs):
        Calculation.__init__(self, calc_name)

        self.sections['CALC_TYPE'] = 'ZERO_BOND'

        self.sections['NOTIONAL'] = 1.0
        self.sections['MATURITY'] = '3Y'
        self.sections['CONST_MATURITY'] = True
        self.sections['ROLLOVER'] = True
        self.sections['OUT_VALUE_TYPE'] = 'VALUE'

        self.set_sections(**kwargs)


class CMT(Bond):
    def __init__(self, calc_name, **kwargs):
        Bond.__init__(self, calc_name)

        self.sections['CALC_TYPE'] = 'FIXED_BOND'

        self.sections['NOTIONAL'] = 1.0
        self.sections['MATURITY'] = '3Y'
        self.sections['COUPON_TENOR'] = '3M'
        self.sections['COUPON_RATE'] = 0.03
        self.sections['DAYCOUNTER'] = 'ACTACT'
        self.sections['COMPOUNDING'] = 'ANNUAL'
        self.sections['CONST_MATURITY'] = True
        self.sections['ROLLOVER'] = True
        self.sections['OUT_VALUE_TYPE'] = 'VALUE'

        self.set_sections(**kwargs)


class CMS(Bond):
    def __init__(self, calc_name, **kwargs):
        Bond.__init__(self, calc_name)

        self.sections['CALC_TYPE'] = 'FIXED_BOND'

        self.sections['NOTIONAL'] = 1.0
        self.sections['MATURITY'] = '3Y'
        self.sections['COUPON_TENOR'] = '3M'
        self.sections['COUPON_RATE'] = 0.03
        self.sections['DAYCOUNTER'] = 'ACTACT'
        self.sections['COMPOUNDING'] = 'ANNUAL'
        self.sections['CONST_MATURITY'] = True
        self.sections['ROLLOVER'] = True
        self.sections['OUT_VALUE_TYPE'] = 'VALUE'

        self.set_sections(**kwargs)


class FixedBond(Bond):
    def __init__(self, calc_name, **kwargs):
        Bond.__init__(self, calc_name)

        self.sections['CALC_TYPE'] = 'FIXED_BOND'

        self.sections['NOTIONAL'] = 1.0
        self.sections['MATURITY'] = '3Y'
        self.sections['COUPON_TENOR'] = '3M'
        self.sections['COUPON_RATE'] = 0.03
        self.sections['DAYCOUNTER'] = 'ACTACT'
        self.sections['COMPOUNDING'] = 'ANNUAL'
        self.sections['CONST_MATURITY'] = True
        self.sections['ROLLOVER'] = True
        self.sections['OUT_VALUE_TYPE'] = 'VALUE'

        self.set_sections(**kwargs)


class FloatingBond(Bond):
    def __init__(self, calc_name, **kwargs):
        Bond.__init__(self, calc_name)

        self.sections['CALC_TYPE'] = 'FLOATING_BOND'

        self.sections['NOTIONAL'] = 1.0
        self.sections['MATURITY'] = '3Y'
        self.sections['COUPON_TENOR'] = '3M'
        self.sections['GEARING'] = 1.0
        self.sections['SPREAD'] = 0.03
        self.sections['DAYCOUNTER'] = 'ACTACT'
        self.sections['COMPOUNDING'] = 'ANNUAL'
        self.sections['CONST_MATURITY'] = True
        self.sections['ROLLOVER'] = True
        self.sections['OUT_VALUE_TYPE'] = 'VALUE'

        self.set_sections(**kwargs)


#class InverseFloatingBond(Bond):
#    def __init__(self, calc_name, **kwargs):
#        Bond.__init__(self, calc_name)

#        self.sections['NOTIONAL'] = 1.0
#        self.sections['MATURITY'] = '3Y'
#        self.sections['COUPON_TENOR'] = '3M'
#        self.sections['FIXED_RATE'] = 0.04
#        self.sections['GEARING'] = 1.0
#        self.sections['SPREAD'] = 0.03
#        self.sections['DAYCOUNTER'] = 'ACTACT'
#        self.sections['COMPOUNDING'] = 'ANNUAL'
#        self.sections['CONST_MATURITY'] = True
#        self.sections['ROLLOVER'] = True
#        self.sections['OUT_VALUE_TYPE'] = 'VALUE'

#        self.set_sections(**kwargs)


class Option(Calculation):
    def __init__(self, calc_name):
        Calculation.__init__(self, calc_name)

        self.sections['MODEL_CATEGORY'] = 'EQ'


class VanillaOption(Option):
    def __init__(self, calc_name, **kwargs):
        Option.__init__(self, calc_name)

        self.sections['CALC_TYPE'] = 'VANILLAEQOPTION'

        self.sections['NOTIONAL'] = 1.0
        self.sections['PRICING_MODEL'] = 'BLACK'
        self.sections['MATURITY'] = '3Y'
        self.sections['RF'] = 0.03
        self.sections['VOL'] = 0.3
        self.sections['STRIKE'] = 1000
        self.sections['CONST_MATURITY'] = True
        self.sections['ROLLOVER'] = True
        self.sections['OUT_VALUE_TYPE'] = 'VALUE'

        self.set_sections(**kwargs)


class BarrierOption(Option):
    def __init__(self, calc_name, **kwargs):
        Option.__init__(self, calc_name)


class CapFloor(Option):
    pass


class Swaption(Option):
    pass


class Volatility(Calculation):
    def __init__(self, calc_name):
        Calculation.__init__(self, calc_name)

        self.sections['MODEL_CATEGORY'] = 'ALL'


class HistVolatility(Volatility):
    def __init__(self, calc_name, **kwargs):
        Volatility.__init__(self, calc_name)

        self.sections['CALC_TYPE'] = 'HISTVOLATILITY'
        self.sections['AVER_PEORIOD'] = '1Y'

        self.set_sections(**kwargs)


class EwmaVolatility(Volatility):
    def __init__(self, calc_name, **kwargs):
        Volatility.__init__(self, calc_name)

        self.sections['CALC_TYPE'] = 'EWMAVOLATILITY'

        self.sections['AVER_PEORIOD'] = '1Y'
        self.sections['LAMBDA'] = 0.9

        self.set_sections(**kwargs)

# class VanillaIRS(Calculation):
#     def __init__(self):
#         pass


# class Cash(Calculation):
#     def __init__(self):
#         pass


# class Futures(Calculation):
#     def __init__(self):
#         pass

# calculation factory

def get_calculation(tag):
    isinstance(tag, Tag)
    # if tag.tag_name != '':
    #     return None

    calc_type = tag.sections['CALC_TYPE']
    calc_name = tag.sections['NAME']

    if calc_type == "SPOT":
        return Spot(calc_name).load_tag(tag)
    elif calc_type == "FORWARD":
        return Forward(calc_name).load_tag(tag)
    elif calc_type == "DISCOUNT":
        return Discount(calc_name).load_tag(tag)
    elif calc_type == "CMT":
        return CMT(calc_name).load_tag(tag)
    elif calc_type == "CMS":
        return CMS(calc_name).load_tag(tag)
    elif calc_type == "ZERO_BOND":
        return ZeroBond(calc_name).load_tag(tag)
    elif calc_type == "FIXED_BOND":
        return FixedBond(calc_name).load_tag(tag)
    elif calc_type == "FLOATING_BOND":
        return FloatingBond(calc_name).load_tag(tag)
    # elif calc_type == "INVERSE_FLOATING_BOND":
    #    return InverseFloatingBond(calc_name).load_tag(tag)
    elif calc_type == "VANILLAEQOPTION":
        return VanillaOption(calc_name).load_tag(tag)
    elif calc_type == "BARRIEREQOPTION":
        return BarrierOption(calc_name).load_tag(tag)
    elif calc_type == "HISTVOLATILITY":
        return HistVolatility(calc_name).load_tag(tag)
    elif calc_type == "EWMAVOLATILITY":
        return EwmaVolatility(calc_name).load_tag(tag)
    else:
        return UnknownCalculation(calc_name)
