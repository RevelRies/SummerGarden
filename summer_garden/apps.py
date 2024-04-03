from django.apps import AppConfig


class SummerGardenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'summer_garden'

    def ready(self):
        import summer_garden.signals