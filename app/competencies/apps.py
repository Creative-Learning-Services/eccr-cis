from django.apps import AppConfig


class CompetenciesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'competencies'

    def ready(self):
        super().ready()
        import competencies.signals
        competencies.signals.create_neo_domain  # pylint: disable=pointless-statement
