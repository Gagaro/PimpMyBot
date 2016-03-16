""" Parameters for modules apis """


class BaseParameter(object):
    @staticmethod
    def normalize(value):
        """ Convert the value from the form input to python. """
        return value

    @staticmethod
    def render(name, value=None):
        """ HTML input rendering. """
        raise NotImplementedError


class CharParameter(BaseParameter):
    @staticmethod
    def render(name, value=''):
        return '<input class="form-control" name="{0}" value="{1}" />'.format(name, value)


class IntParameter(BaseParameter):
    @staticmethod
    def normalize(value):
        try:
            return int(value)
        except ValueError:
            return 0

    @staticmethod
    def render(name, value=0):
        return '<input type="int" class="form-control" name="{0}" value="{1}" />'.format(name, value)
