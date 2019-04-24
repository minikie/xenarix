
class Jsonizable:
    def __init__(self):
        pass


class Instrument(Jsonizable):
    def __init__(self):
        Jsonizable.__init__(self)


class Option(Instrument):
    def __init__(self):
        Instrument.__init__(self)


class Kospi2_IndexOption(Option):
    def __init__(self):
        Option.__init__(self)



## test

option = Kospi2_IndexOption(type='call', strike=1.0)
