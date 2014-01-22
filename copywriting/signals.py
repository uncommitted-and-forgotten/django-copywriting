from django.dispatch import Signal

ready_to_review = Signal(providing_args=["articleID"])
ready_to_publish = Signal(providing_args=["articleID"])