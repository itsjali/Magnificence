import pytest

from api.serializers import InboundSerializer, OutboundSerializer


# Inbound Serializer

def test_inbound_serializer_with_valid_data_types():
    data = {
        "events": [],
        "game_settings": {},
        "phases": [],
        "teams": [],
        "total_players": 10,
        "elements": [],
        "element_stats": [],
        "element_types": [],
    }

    serializer = InboundSerializer(data=data)

    assert serializer.is_valid()


def test_inbound_serializer_raises_error_for_invalid_data_types():
    data = {
        "events": {},
        "phases": [],
        "teams": 20,
        "total_players": 10,
        "elements": {},
        "element_stats": [],
        "element_types": [],
    }

    serializer = InboundSerializer(data=data)
    serializer.is_valid()
    
    assert serializer.errors == {
        "events": ['Expected a list of items but got type "dict".'],
        "game_settings": ["This field is required."],
        "teams": ['Expected a list of items but got type "int".'],
        "elements": ['Expected a list of items but got type "dict".'],
    }
    

# Outbound Serializer

def test_outbound_serializer_with_valid_data_types():
    expected_positions = [
        ("GKP", 1),
        ("DEF", 2),
        ("MID", 3),
        ("FWD", 1)
    ]
    data = []
    for position, count in expected_positions:
        for _ in range(count):
            data.append({
                "name": f"Bruce Lee",
                "total_goals_assists": 80,
                "position": position,
            })

    serializer = OutboundSerializer(data=data)

    assert serializer.is_valid()


def test_outbound_serializer_raises_error_for_invalid_data_types():
    data = [
        {
            "name": "Bruce Lee",
            "total_goals_assists": 80,
            "position": "FWD",
        }
        for i in range(6)
    ]

    data.append(
        {
            "name": [],
            "total_goals_assists": "Bruce Lee",
            "position": [],
        }
    )

    serializer = OutboundSerializer(data=data)
    serializer.is_valid()

    assert serializer.errors[6] == {
        "name": ["Not a valid string."],
        "total_goals_assists": ["A valid integer is required."],
        "position": ["Not a valid string."],

    }


def test_outbound_serializer_raises_error_for_more_than_seven_players():
    data = [
        {
            "name": "Bruce Lee",
            "total_goals_assists": 80,
            "position": "FWD",
        }
        for i in range(9)
    ]

    serializer = OutboundSerializer(data=data)
    serializer.is_valid()

    assert serializer.errors == {
        "players": ["The list must only contain 7 players."],
    }


def test_outbound_serializer_raises_error_for_too_many_positions_in_data():
    expected_positions = [
        ("GKP", 1),
        ("DEF", 2),
        ("MID", 2),
        ("FWD", 2)
    ]
    
    data = []
    for position, count in expected_positions:
        for _ in range(count):
            data.append({
                "name": f"Bruce Lee",
                "total_goals_assists": 80,
                "position": position,
            })

    serializer = OutboundSerializer(data=data)
    serializer.is_valid()

    assert serializer.errors == {
        "position": ["Too many position count for MID. There can only be 3 MID."]
    }
