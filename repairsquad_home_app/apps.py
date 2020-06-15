from django.apps import AppConfig


class RepairsquadHomeAppConfig(AppConfig):
    name = 'repairsquad_home_app'
    
    def ready(self):
        import repairsquad_home_app.signals
