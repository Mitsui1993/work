from django.apps import AppConfig

class MyadminConfig(AppConfig):
    name = 'MyAdmin'
    def ready(self):
        super(MyadminConfig,self).ready()

        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('reg')