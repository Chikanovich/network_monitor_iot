from django.apps import AppConfig


class MonitorConfig(AppConfig):
    name = 'monitor'

    def ready(self):
        # NOTE: import must be here!
        from monitor import scheduler
        scheduler.start()
