from __future__ import absolute_import, unicode_literals

import logging
import os
import sys

from utils.logging import get_logger

CORE_MODULES_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'core_modules')
MODULES_PATHS = [CORE_MODULES_PATH]

logger = get_logger('module', logging.DEBUG)


class BaseModule(object):
    """
    Base class for creating a module.

    Attributes:
        id          Unique identifier for this module
        title       Title of the app
        description Description of the app
        dependencies    List of other module needed for this one to work.
        handlers    List of irc handlers
    """
    identifier = ''
    title = ''
    description = ''
    dependencies = []
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
    def widgets(self):
        """
        Widget of this module for the dashboard panel.
        Should be a dict such as the following:

        {
            'id_of_widget': {
                "title": "My module widget",
                "html": "<p>I am a paragraph</p>"
            },
        }
        """
        return {}

    @property
    def api(self):
        """
        List of methods exposed by this module.

        :example:

        def square_root(irc_client, number):
            return number * number

        {
            'title': 'Square Root',
            'method': square_root,
            'parameters': {
                'number': IntParameter(),
            }
        }
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

    def activate(self):
        logger.debug('activating module {0}'.format(self.identifier))
        self.config.activated = True
        self.config.save()
        if not self.config.installed:
            self.install()

    def deactivate(self):
        logger.debug('deactivating module {0}'.format(self.identifier))
        self.config.activated = False
        self.config.save()

    def install(self):
        """ Method called when activating the module for the first time. """
        logger.debug('installing module {0}'.format(self.identifier))
        assert self.config.activated
        self.config.installed = True
        self.config.upgrades = len(self.upgrades)
        self.config.save()

    def uninstall(self):
        """ Method called when uninstalling the module. """
        logger.debug('uninstalling module {0}'.format(self.identifier))
        assert not self.config.activated
        self.config.installed = False
        self.config.save()

    @property
    def upgrades(self):
        """
        upgrades is a list of methods to call in order to upgrade the module.

        These methods will NOT be called when install is called. It is there
        to ensure compatibility when the module is already installed.
        """
        return []

    def run_upgrades(self):
        """
        Run needed upgrades.
        """
        upgrades = self.upgrades[self.config.upgrades:]
        for upgrade in upgrades:
            upgrade()
        self.config.upgrades = len(self.upgrades)
        self.config.save()

    def need_upgrades(self):
        """ True if upgrade needed. """
        return len(self.upgrades) != self.config.upgrades


class ModulesList(dict):
    """ Load modules only when needed to avoid circular  import. """

    def __getattribute__(self, name):
        if not self and name != 'load_modules':
            self.load_modules()
        return dict.__getattribute__(self, name)
    
    def __getitem__(self, item):
        if not self:
            self.load_modules()
        return super(ModulesList, self).__getitem__(item)
    
    def load_modules(self):
        """ Search through all modules directory and import the detected modules. """
        logger.debug("Loading all modules start.")
        saved_paths = sys.path
        for path in MODULES_PATHS:
            # We overwrite sys.path temporarily
            sys.path = [path] + saved_paths
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
                except ImportError:
                    logger.debug("Could not import module '{0}'".format(file))
                else:
                    if isinstance(module, BaseModule):
                        logger.debug('Adding {0}'.format(module.identifier))
                        self[module.identifier] = module
        sys.path = saved_paths
        logger.debug("Loading all modules end.")

modules = ModulesList()


def get_activated_modules():
    return [module for module in modules.values() if module.config.activated]


def get_deactivated_modules():
    return [module for module in modules.values() if not module.config.activated]
