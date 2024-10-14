import pytest
import requests

from django.conf import settings

from api.serializers import OutboundSerializer
from api.services import GetMagnificent7


@pytest.mark.vcr(record_mode="once")
def test_get_magnificent_7_service():
    response = requests.get(settings.MAGNIFICENCE_API_URL)

    response_data = response.json()
    elements = response_data["elements"]
    element_types = response_data["element_types"]

    result = GetMagnificent7(elements, element_types).run()

    # Use Outbound Serializer to assert the data from the service
    serializer = OutboundSerializer(data=result)
    assert serializer.is_valid()


