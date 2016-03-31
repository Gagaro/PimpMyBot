""" Parameters for modules apis """


class BaseParameter(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.title = kwargs.get('title', name)
        self.help_text = kwargs.get('help_text', '')

    def normalize(self, value):
        """ Convert the value from the form input to python. """
        return value

    def render(self, value=None):
        """ HTML input rendering. """
        raise NotImplementedError


class CharParameter(BaseParameter):
    def render(self, value=''):
        return '<input class="form-control" name="{0}" value="{1}" />'.format(self.name, value)


class IntParameter(BaseParameter):
    def normalize(self, value):
        try:
            return int(value)
        except ValueError:
            return 0

    def render(self, name, value=0):
        return '<input type="int" class="form-control" name="{0}" value="{1}" />'.format(self.name, value)
