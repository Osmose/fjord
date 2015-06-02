import logging

from django.apps import AppConfig
from django.conf import settings

from fjord.suggest import _SUGGESTERS
from fjord.base.plugin_utils import load_providers


logger = logging.getLogger('i.suggest')


class SuggestConfig(AppConfig):
    name = 'fjord.suggest'

    def ready(self):
        # Load Suggestersand store them in _SUGGESTERS stomping on
        # whatever was there.
        _SUGGESTERS[:] = load_providers(settings.SUGGEST_PROVIDERS, logger)
