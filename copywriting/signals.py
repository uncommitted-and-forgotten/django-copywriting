from django.dispatch import Signal

ready_to_publish = Signal(providing_args=["articleID"])