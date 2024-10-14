from collections import Counter

from rest_framework import serializers


# Inbound Serializer
class InboundSerializer(serializers.Serializer):
    """
    Serializer for processing the inbound data structure received from an external API.

    This serializer is used to validate the expected structure of the inbound data, ensuring that 
    all required fields are present and in the correct format.

    Fields:
        events (list): A list of event data, each represented as a dictionary.
        game_settings (dict): A dictionary containing configuration and settings.
        phases (list): A list of game phases.
        teams (list): A list of teams, each represented as a dictionary.
        total_players (int): The total number of players in the system.
        elements (list): A list of player data, where each player is represented as a dictionary
            containing details like goals, assists, and their position.
        element_stats (list): A list of dictionaries representing various player statistics.
        element_types (list): A list of position types (e.g., goalkeeper, defender), where each 
            type is represented as a dictionary with position metadata.

    Example:
        data = {
            "events": [...],
            "game_settings": {...},
            "phases": [...],
            "teams": [...],
            "total_players": 10000,
            "elements": [...],
            "element_stats": [...],
            "element_types": [...]
        }
        serializer = InboundSerializer(data=data)
        if serializer.is_valid():
            processed_data = serializer.validated_data
        else:
            serializer.errors
    """
    events = serializers.ListField()
    game_settings = serializers.DictField()
    phases = serializers.ListField()
    teams = serializers.ListField()
    total_players = serializers.IntegerField()
    elements = serializers.ListField()
    element_stats = serializers.ListField()
    element_types = serializers.ListField()


# Outbound Serializers
class Magnificent7Serializer(serializers.Serializer):
    """
    Serializer for representing individual player data processed from the 
    `GetMagnificent7` service.

    This serializer validates the data for each player, including the player's name, total sum of 
    their goals and assists, and their position. It ensures that the player data is structured 
    correctly.

    Fields:
        name (str): The name of the player.
        total_goals_assists (int): The total number of goals and assists made by the player.
        position (str): The position of the player, represented as a three-character string.
    """
    name = serializers.CharField(max_length=50)
    total_goals_assists = serializers.IntegerField()
    position = serializers.CharField(max_length=3)


class OutboundSerializer(serializers.ListSerializer):
    """
    A serializer for validating the list of Magnificent 7 players.

    This serializer validates that the list of players matches the required structure ensuring 
    that exactly 7 players are included and the correct number of players for each position
    (1 GKP, 2 DEF, 3 MID, 1 FWD). If one of these validation fails an error message is returned.

    Example:
        data = [
            {"name": "Bruce Lee", "total_goals_assists": 10, "position": "GKP"},
            {"name": "Mo Salah", "total_goals_assists": 8, "position": "DEF"},
            {"name": "Kobe Bryant", "total_goals_assists": 5, "position": "DEF"},
            {"name": "LeBron James", "total_goals_assists": 12, "position": "MID"},
            {"name": "Michael Jordan", "total_goals_assists": 11, "position": "MID"},
            {"name": "Luka Doncic", "total_goals_assists": 9, "position": "MID"},
            {"name": "Jayson Tatum", "total_goals_assists": 15, "position": "FWD"},
        ]

        outbound_serializer = OutboundSerializer(data=data)
        if outbound_serializer.is_valid():
            processed_data = outbound_serializer.validated_data
        else:
            errors = outbound_serializer.errors
    """
    child = Magnificent7Serializer()

    def validate(self, value):
        if len(value) != 7:
            raise serializers.ValidationError({"players": "The list must only contain 7 players."})
    
        expected_positions = {"GKP": 1, "DEF": 2, "MID": 3, "FWD": 1}

        actual_positions = Counter(player.get("position") for player in value)
        for position, count in expected_positions.items():
            actual_count = actual_positions.get(position)
            if actual_count != count:
                raise serializers.ValidationError({
                    "position": f"Too many position count for {position}. There can only be {count} {position}."
                })
        
        return value
