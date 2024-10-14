from django.urls import path
from api.views import GetMagnificenceDataView

urlpatterns = [
    path("get-magnificence-data/", GetMagnificenceDataView.as_view(), name="get_magnificence_data"),
]