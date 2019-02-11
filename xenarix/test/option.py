import xenarix as xen
import xenarix.results as xen_r
import xenarix.sample as xen_s
import numpy as np
from math import log, e, exp
from scipy.stats import norm


def impliedVolatility(className, args, callPrice=None, putPrice=None, high=500.0, low=0.0):
	'''Returns the estimated implied volatility'''
	if callPrice:
		target = callPrice
		restimate = eval(className)(args, volatility=high, performance=True).callPrice
		if restimate < target:
			return high
		if args[0]>args[1] + callPrice:
			return 0.001
	if putPrice:
		target = putPrice
		restimate = eval(className)(args, volatility=high, performance=True).putPrice
		if restimate < target:
			return high
		if args[1]>args[0] + putPrice:
			return 0.001
	decimals = len(str(target).split('.')[1])		# Count decimals
	for i in range(10000):	# To avoid infinite loops
		mid = (high + low) / 2
		if mid < 0.00001:
			mid = 0.00001
		if callPrice:
			estimate = eval(className)(args, volatility=mid, performance=True).callPrice
		if putPrice:
			estimate = eval(className)(args, volatility=mid, performance=True).putPrice
		if round(estimate, decimals) == target:
			break
		elif estimate > target:
			high = mid
		elif estimate < target:
			low = mid
	return mid


class BS:
    '''Black-Scholes
    Used for pricing European options on stocks without dividends

    BS([underlyingPrice, strikePrice, interestRate, daysToExpiration], \
            volatility=x, callPrice=y, putPrice=z)

    eg:
        c = mibian.BS([1.4565, 1.45, 1, 30], volatility=20)
        c.callPrice				# Returns the call price
        c.putPrice				# Returns the put price
        c.callDelta				# Returns the call delta
        c.putDelta				# Returns the put delta
        c.callDelta2			# Returns the call dual delta
        c.putDelta2				# Returns the put dual delta
        c.callTheta				# Returns the call theta
        c.putTheta				# Returns the put theta
        c.callRho				# Returns the call rho
        c.putRho				# Returns the put rho
        c.vega					# Returns the option vega
        c.gamma					# Returns the option gamma

        c = mibian.BS([1.4565, 1.45, 1, 30], callPrice=0.0359)
        c.impliedVolatility		# Returns the implied volatility from the call price

        c = mibian.BS([1.4565, 1.45, 1, 30], putPrice=0.0306)
        c.impliedVolatility		# Returns the implied volatility from the put price

        c = mibian.BS([1.4565, 1.45, 1, 30], callPrice=0.0359, putPrice=0.0306)
        c.putCallParity			# Returns the put-call parity
        '''

    def __init__(self, args, volatility=None, callPrice=None, putPrice=None, \
                 performance=None):
        self.underlyingPrice = float(args[0])
        self.strikePrice = float(args[1])
        self.interestRate = float(args[2])
        self.daysToExpiration = float(args[3])

        for i in ['callPrice', 'putPrice', 'callDelta', 'putDelta', \
                  'callDelta2', 'putDelta2', 'callTheta', 'putTheta', \
                  'callRho', 'putRho', 'vega', 'gamma', 'impliedVolatility', \
                  'putCallParity']:
            self.__dict__[i] = None

        if volatility:
            self.volatility = float(volatility)

            self._a_ = self.volatility * self.daysToExpiration ** 0.5
            self._d1_ = (log(self.underlyingPrice / self.strikePrice) + \
                         (self.interestRate + (self.volatility ** 2) / 2) * \
                         self.daysToExpiration) / self._a_
            self._d2_ = self._d1_ - self._a_
            if performance:
                [self.callPrice, self.putPrice] = self._price()
            else:
                [self.callPrice, self.putPrice] = self._price()
                [self.callDelta, self.putDelta] = self._delta()
                [self.callDelta2, self.putDelta2] = self._delta2()
                [self.callTheta, self.putTheta] = self._theta()
                [self.callRho, self.putRho] = self._rho()
                self.vega = self._vega()
                self.gamma = self._gamma()
                self.exerciceProbability = norm.cdf(self._d2_)
        if callPrice:
            self.callPrice = round(float(callPrice), 6)
            self.impliedVolatility = impliedVolatility( \
                self.__class__.__name__, args, callPrice=self.callPrice)
        if putPrice and not callPrice:
            self.putPrice = round(float(putPrice), 6)
            self.impliedVolatility = impliedVolatility( \
                self.__class__.__name__, args, putPrice=self.putPrice)
        if callPrice and putPrice:
            self.callPrice = float(callPrice)
            self.putPrice = float(putPrice)
            self.putCallParity = self._parity()

    def _price(self):
        '''Returns the option price: [Call price, Put price]'''
        if self.volatility == 0 or self.daysToExpiration == 0:
            call = max(0.0, self.underlyingPrice - self.strikePrice)
            put = max(0.0, self.strikePrice - self.underlyingPrice)
        if self.strikePrice == 0:
            raise ZeroDivisionError('The strike price cannot be zero')
        else:
            call = self.underlyingPrice * norm.cdf(self._d1_) - \
                   self.strikePrice * e ** (-self.interestRate * \
                                            self.daysToExpiration) * norm.cdf(self._d2_)
            put = self.strikePrice * e ** (-self.interestRate * \
                                           self.daysToExpiration) * norm.cdf(-self._d2_) - \
                  self.underlyingPrice * norm.cdf(-self._d1_)
        return [call, put]

    def _delta(self):
        '''Returns the option delta: [Call delta, Put delta]'''
        if self.volatility == 0 or self.daysToExpiration == 0:
            call = 1.0 if self.underlyingPrice > self.strikePrice else 0.0
            put = -1.0 if self.underlyingPrice < self.strikePrice else 0.0
        if self.strikePrice == 0:
            raise ZeroDivisionError('The strike price cannot be zero')
        else:
            call = norm.cdf(self._d1_)
            put = -norm.cdf(-self._d1_)
        return [call, put]

    def _delta2(self):
        '''Returns the dual delta: [Call dual delta, Put dual delta]'''
        if self.volatility == 0 or self.daysToExpiration == 0:
            call = -1.0 if self.underlyingPrice > self.strikePrice else 0.0
            put = 1.0 if self.underlyingPrice < self.strikePrice else 0.0
        if self.strikePrice == 0:
            raise ZeroDivisionError('The strike price cannot be zero')
        else:
            _b_ = e ** -(self.interestRate * self.daysToExpiration)
            call = -norm.cdf(self._d2_) * _b_
            put = norm.cdf(-self._d2_) * _b_
        return [call, put]

    def _vega(self):
        '''Returns the option vega'''
        if self.volatility == 0 or self.daysToExpiration == 0:
            return 0.0
        if self.strikePrice == 0:
            raise ZeroDivisionError('The strike price cannot be zero')
        else:
            return self.underlyingPrice * norm.pdf(self._d1_) * \
                   self.daysToExpiration ** 0.5 / 100

    def _theta(self):
        '''Returns the option theta: [Call theta, Put theta]'''
        _b_ = e ** -(self.interestRate * self.daysToExpiration)
        call = -self.underlyingPrice * norm.pdf(self._d1_) * self.volatility / \
               (2 * self.daysToExpiration ** 0.5) - self.interestRate * \
               self.strikePrice * _b_ * norm.cdf(self._d2_)
        put = -self.underlyingPrice * norm.pdf(self._d1_) * self.volatility / \
              (2 * self.daysToExpiration ** 0.5) + self.interestRate * \
              self.strikePrice * _b_ * norm.cdf(-self._d2_)
        return [call / 365, put / 365]

    def _rho(self):
        '''Returns the option rho: [Call rho, Put rho]'''
        _b_ = e ** -(self.interestRate * self.daysToExpiration)
        call = self.strikePrice * self.daysToExpiration * _b_ * \
               norm.cdf(self._d2_) / 100
        put = -self.strikePrice * self.daysToExpiration * _b_ * \
              norm.cdf(-self._d2_) / 100
        return [call, put]

    def _gamma(self):
        '''Returns the option gamma'''
        return norm.pdf(self._d1_) / (self.underlyingPrice * self._a_)

    def _parity(self):
        '''Put-Call Parity'''
        return self.callPrice - self.putPrice - self.underlyingPrice + \
               (self.strikePrice / \
                ((1 + self.interestRate) ** self.daysToExpiration))


class VanillaEqOption:
    def __init__(self, X, maturity_date):
        self.X = X
        self.maturity_date = maturity_date

    def price(self, timegrid, resultModel, rf):
        if not isinstance(resultModel, xen_r.ResultModel):
            raise Exception('ResultModel type is needed')

        if not isinstance(timegrid, xen_r.TimeGrid):
            raise Exception('TimeGrid type is needed')

        date_exist = timegrid.has_date(self.maturity_date)
        #tf_t = time_grid.has_t(t)
        t_row = timegrid.find_row_by_date(self.maturity_date, interpolation=True)

        values = resultModel.interpolated_values(t_row)
        return np.average(np.maximum(0.0, values - self.X)) * exp(-rf)

    def price2(self, timegrid, S, rf, div, sigma):
        if not isinstance(timegrid, xen_r.TimeGrid):
            raise Exception('TimeGrid type is needed')

        # BS([underlyingPrice, strikePrice, interestRate, daysToExpiration], volatility=x, callPrice=y, putPrice=z)
        t_row = timegrid.find_row_by_date(self.maturity_date, interpolation=True)

        bs = BS([S, self.X, rf-div, t_row.T], volatility=sigma)
        return bs.callPrice


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

