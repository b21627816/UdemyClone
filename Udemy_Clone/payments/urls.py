from django.urls import path
from payments.views import PaymentHandler, Webhook

urlpatterns = [
    path("", PaymentHandler.as_view(), name="payment"),
    path("webhook/", Webhook.as_view(), name="webhook"),
]
