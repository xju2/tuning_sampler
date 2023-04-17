"""
This module primarily does two things, based on the input information.
1. sampling the parameter in its valid phase space if needed.
Currently sample the parameter evenly.
2. prepare a string for pythia or rivet configuration.
"""
from tuning_sampler.utils import find_precision


class Parameter(object):
    """
    Must contain a unique name,
    id, nickname and description are optional.
    It is designed in the view of tuing Pythia parameters
    """
    def __init__(self, name, min_val, max_val,
                 nominal,
                 values, nickname,
                 description="None",
                 id_=-1, type_="pythia",
                 **kwargs
                 ):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.nominal = nominal

        # get a list of values of this parameter
        # used in one-to-one and factorial DOE
        if type(values) is list:
            self.values = values
        elif type(values) is int:
            self.values = self.get_even_values(values)
        else:
            raise ValueError("%s not supported" % values)

        self.nickname = nickname
        self.description = description
        self.id_ = id_
        self.run_values = []  # actual values used to generate events
        self.type_ = type_
        self.other_opt = kwargs
        print("Parameter {}({},{})".format(self.name, self.min_val, self.max_val))
        # print("  {}".format(self.description))
        print("  {}".format(self.values))

    def get_even_values(self, values):
        if values < 2:
            return [self.nominal]

        scale = max(find_precision(self.max_val)[1],
                    find_precision(self.min_val)[1],
                    find_precision(self.nominal)[1],
                    find_precision(values)[0]) + 1
        step = (self.max_val - self.min_val) / (values - 1)
        return [round(self.min_val + x * step, scale) for x in range(values - 1)] + [self.max_val]

    def jsonDefault(self):
        return self.__dict__

    def to_str(self):
        return "{} {} [{}] ({}, {}, {}), {}".format(self.id_, self.name, self.nickname,
                                                    self.min_val , self.nominal, self.max_val, len(self.values))

    def __repr__(self):
        return "Parameter {}({},{})".format(self.name, self.min_val , self.max_val)

    def __str__(self):
        return self.to_str()

    def __eq__(self, other):
        return self.nickname == other.nickname

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.nickname))

    def prof_config(self, value):
        """return a string for configuring the Professor"""
        return "{} {}".format(self.nickname, value)

    def config(self, value):
        """return a string for configuring the Pythia8"""
        return "{:<40} = {:<10} \t! {}".format(self.name, value, self.description)


class DetectorParameter(Parameter):
    def __init__(self, name, min_, max_,
                 nominal,
                 values, nickname, eta, pT,
                 description="None",
                 id_=-1):
        """nominal_hist2D is YODA::Hist2D object"""
        super(DetectorParameter, self).__init__(
            name, min_, max_, nominal, values, nickname, description, id_
        )
        self.eta = eta
        self.pT = pT
