import logging
import os
import sys

from utils.logging import get_logger

CORE_MODULES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'core_modules')
MODULES_PATHS = [CORE_MODULES_PATH]

logger = get_logger('module', logging.DEBUG)


class BaseModule(object):
    """
    Base class for creating a module.

    Attributes:
        id          Unique identifier for this module
        title       Title of the app
        description Description of the app
        handlers    List of irc handlers
    """
    identifier = ''
    title = ''
    description = ''
    handlers = []

    _config = None

    @property
    def menus(self):
        """
        Menus of this module.
        Should be a list such as the following:

        [
            {
                "title": "My module menu",
                "icon": "list",  # Fontawesome icon name: http://fortawesome.github.io/Font-Awesome/icons/
                "menu": [
                    {
                        "title": "My module page",
                        "view": "my_module_page"  # Bottle view name
                    },
                    {
                        "title": "My module other page",
                        "view": "my_module_other_page"
                    },
                ]
            },
        ]
        """
        return []

    @property
    def dashboard(self):
        """
        Dashboard  panels of this moduel.
        Should be a list such as the following:

        [
            {
                "title": "My module dashboard",
                "html": "<p>I am a paragraph</p>"
            },
        ]
        """
        return []

    @property
    def config(self):
        if self._config is not None:
            return self._config

        from utils.config import Configuration, ModuleConfiguration

        configuration = Configuration.get()
        self._config = ModuleConfiguration.get_or_create(identifier=self.identifier, configuration=configuration)[0]
        return self._config

    def install(self):
        """ Method called when activating the module for the first time. """
        logger.debug('installing module {0}'.format(self.identifier))
        self.config.activated = True
        self.config.installed = True
        self.config.save()

    def uninstall(self):
        """ Method called when uninstalling the module. """
        logger.debug('uninstalling module {0}'.format(self.id))
        self.config.activated = False
        self.config.installed = False
        self.config.save()


def load_modules():
    """ Search through all modules directory and import the detected modules. """
    global modules

    logger.debug("Loading all modules start.")
    modules = {}
    saved_paths = sys.path
    for path in MODULES_PATHS:
        # We overwrite sys.path temporarily
        sys.path = [path]
        for file in os.listdir(path):
            # Only try to import python file
            if file[-3:] != '.py' and not os.path.isdir('{0}/{1}'.format(path, file)):
                continue
            if file[-3:] == '.py':
                file = file[:-3]
            try:
                module = __import__(file).module
            # except ImportError:
            #     logger.warning('Error importing {0}'.format(file))
            except AttributeError:
                pass
            else:
                if isinstance(module, BaseModule):
                    logger.debug('Adding {0}'.format(module.identifier))
                    modules[module.identifier] = module
    sys.path = saved_paths
    logger.debug("Loading all modules end.")
    return modules

modules = load_modules()