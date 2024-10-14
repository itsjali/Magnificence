import json
import pytest
from unittest.mock import patch, MagicMock

from django.test import RequestFactory
from django.urls import reverse

from api.views import GetMagnificenceDataView

factory = RequestFactory()
request = factory.get(reverse("get_magnificence_data"))
view = GetMagnificenceDataView.as_view()


@pytest.mark.vcr(record_mode="once")
def test_get_magnificence_data_view_returns_200():
    response = view(request)
    response.render()
    
    response_data = json.loads(response.content.decode("utf-8"))
    assert response.status_code == 200
    assert len(response_data) == 7


@pytest.mark.vcr(record_mode="once")
def test_get_magnificence_data_view_returns_200_with_valid_optional_team_name_param():
    request = factory.get(reverse("get_magnificence_data"), {"team_name": "Liverpool"})
    response = view(request)
    response.render()
    
    response_data = json.loads(response.content.decode("utf-8"))
    assert response.status_code == 200
    assert len(response_data) == 7


@patch("requests.get")
def test_get_magnificence_data_view_returns_400_if_api_request_fails(mock_get):
    mock_get.return_value.status_code = 500

    response = view(request)
    response.render()
    
    response_data = json.loads(response.content.decode("utf-8"))
    assert response.status_code == 400
    assert response_data == {"error": "Failed to fetch data"}


@patch("requests.get")
def test_get_magnificence_data_view_returns_400_if_inbound_serializer_is_invalid(mock_get):
    invalid_api_response = {
        "game_settings": [],
        "total_players": [],
        "elements": {},
    }

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = invalid_api_response

    response = view(request)
    response.render()

    response_data = json.loads(response.content.decode("utf-8"))
    assert response.status_code == 400
    assert response_data == {
        "events": ["This field is required."],
        "game_settings": ['Expected a dictionary of items but got type "list".'],
        "phases": ["This field is required."],
        "teams": ["This field is required."],
        "total_players": ["A valid integer is required."],
        "elements": ['Expected a list of items but got type "dict".'],
        "element_stats": ["This field is required."],
        "element_types": ["This field is required."]
    }


@patch("requests.get")
@patch("api.services.GetMagnificent7")
def test_get_magnificence_data_view_returns_500_if_outbound_serializer_is_invalid(
    mock_get_magnificent_7,
    mock_get
):
    mock_get.return_value.status_code = 200
    valid_api_response = {
        "events": [],
        "game_settings": {},
        "phases": [],
        "teams": [],
        "total_players": 10,
        "elements": [],
        "element_stats": [],
        "element_types": [],
    }
    mock_get.return_value.json.return_value = valid_api_response

    mock_get_magnificent_7_instance = MagicMock()
    mock_get_magnificent_7_instance.run.return_value = [
        {"name": "LeBron", "total_goals_assists": 3, "position": "GKP"},
        {"name": "Kobe", "total_goals_assists": 4, "position": "DEF"},
        {"name": "Salah", "total_goals_assists": 5, "position": "MID"}
    ]
    mock_get_magnificent_7.return_value = mock_get_magnificent_7_instance

    response = view(request)
    response.render()

    response_data = json.loads(response.content.decode("utf-8"))
    assert response.status_code == 500
    assert response_data == {"players": ["The list must only contain 7 players."]}


@patch("requests.get")
def test_get_magnificence_data_view_returns_400_if_team_name_is_not_valid(mock_get):
    valid_api_response = {
        "events": [],
        "game_settings": {},
        "phases": [],
        "teams": [{"id": 1, "name": "Liverpool"}],
        "total_players": 10,
        "elements": [],
        "element_stats": [],
        "element_types": [],
    }

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = valid_api_response

    request = factory.get(reverse("get_magnificence_data"), {"team_name": "FakeTeam"})
    response = view(request)
    response.render()

    response_data = json.loads(response.content.decode("utf-8"))
    assert response.status_code == 400
    assert response_data == {"error": "'FakeTeam' is not a valid team."}
