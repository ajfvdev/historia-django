from django.urls import path
from .views import contractController, ratesController, formController

urlpatterns = [
    path("api/contract", contractController, name="contract"),
    path("api/rates", ratesController, name="rate"),
    path("", formController, name="form")
]