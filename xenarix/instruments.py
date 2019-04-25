import numpy as np
import xenarix.mxqlib as mxq
from collections import namedtuple


class Jsonizable:
    def __init__(self):
        pass


CashFlow_Item = namedtuple('CashFlow_Item', 'DATE IN OUT')

class Instrument(Jsonizable):
    def __init__(self):
        Jsonizable.__init__(self)


class Option(Instrument):
    def __init__(self):
        Instrument.__init__(self)

class DayCounter:
    def __init__(self):
        pass

    def yearfrac(self, d1, d2):
        return 1.0

class Act365(DayCounter):
    def __init__(self):
        DayCounter.__init__(self)


class Kospi2_IndexOption(Option):
    def __init__(self, strike, maturity_date, option_type='call', side='buy'):
        Option.__init__(self)
        self.daycounter = Act365()

        self.strike = strike
        self.maturity_date = maturity_date
        self.option_type = option_type
        self.side = side

    def average_cashflow(self, refdate, rm, discount_curve):
        t_row = rm.timegrid.find_row_by_date(self.maturity_date)
        values = rm.interpolated_values(t_row)
        maturity_T = self.daycounter.yearfrac(refdate, self.maturity_date)
        df = discount_curve.discount(maturity_T)
        v = 0.0

        if self.option_type == 'call':
            v = np.average(np.maximum(self.strike - values, 0.0)) * df
        else:
            v = np.average(np.maximum(values - self.strike, 0.0)) * df

        cf = CashFlow_Item(self.maturity_date, v, 0.0) if self.side == 'buy' else CashFlow_Item(self.maturity_date, 0.0, v)

        return cf

    def black_price(self, refdate, x, drift, sigma):
        maturity_T = self.daycounter.yearfrac(refdate, self.maturity_date)

        # c++ 코드 python 으로 wrapping하는거 는 그냥 method 만 밖으로 빼내서 쓰자요.
        # class를 빼내기에는 약간 애매함.

        return mxq.option_blackformula(x, self.strike, maturity_T, drift, 0.0, sigma, self.option_type)


# 이걸 다시 짜야대나....? ㅡ.ㅡㅋ
# 그냥 ql.vanila 해서 가져오면 대는디...? 굳이 repacking을 할게 있나....
class DiscountCurve:
    def __init__(self):
        pass

    def discount(self, t):
        return 1.0


class FlatDiscountCurve(DiscountCurve):
    # default annual
    def __init__(self, rate):
        DiscountCurve.__init__(self)


class Pricer:
    def __init__(self, refdate, discount_curve):
        self.refdate = refdate
        self.discount_curve = discount_curve


class ScenarioPricer(Pricer):
    def __init__(self, refdate, discount_curve):
        Pricer.__init__(self, refdate, discount_curve)

    def price(self, instrument, rm_list):
        rm = rm_list[0]

        cf = instrument.average_cashflow(self.refdate, rm, self.discount_curve)

        v = np.sum(cf.IN - cf.OUT)

        return v


# ## test
# option = Kospi2_IndexOption(type='call',
#                             strike=100,
#                             T=1.0)
#
# option.price(s0=100, drift=0.03, div=0.01, sigma=0.3)
# option.delta(s0=100)