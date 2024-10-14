class GetMagnificent7:
    """
    A service that processes a list of players and returns the top 7 based on their total goals 
    and assists, optionally filtered by a specific team.

    The service takes a list of players (`elements`) and their corresponding position types 
    (`element_types`). It filters players by their position, sorts them by their combined total 
    of goals and assists, and selects the top players in each position 
    (1 GKP, 2 DEF, 3 MID, 1 FWD).

    Optionally, the service can filter the players by a specific team if a `team_id` is provided. 
    If no `team_id` is provided, the top 7 players from the entire league are returned.

    Attributes:
        elements (list): A list of dictionaries containing details of each player.
        element_types (list): A list of dictionaries containing position metadata.
        team_id (int, optional): The ID of the team to filter the players by.

    Example:
        elements = [
            {"element_type": 1, "goals_scored": 1, "assists": 2, "web_name": "Bruce Lee"},
            {"element_type": 2, "goals_scored": 1, "assists": 1, "web_name": "Mo Salah"},
        ]
        element_types = [
            {"id": 1, "singular_name_short": "GKP"},
            {"id": 2, "singular_name_short": "DEF"}
        ]
        team_id = 1  # Optional team_id to filter by "Arsenal", for example
        GetMagnificent7(elements, element_types, team_id).run()
    """
    def __init__(self, elements: list[dict], element_types: list[dict], team_id: int = None):
        self.elements = elements
        self.element_types = element_types
        self.team_id = team_id

    def _get_position_name(self, position: int) -> str:
        """
        Retrieves the short name for the position based on the position ID.
        """
        for element_type in self.element_types:
            if element_type["id"] == position:
                return element_type["singular_name_short"]
        return ""
    
    def _filter_by_position(self, position_id: int) -> list[dict]:
        """
        Filters players based on player's position, if team_id is present then filter 
        players in that team.
        """
        players = [player for player in self.elements if player["element_type"] == position_id]

        if self.team_id:
            players = [player for player in players if player.get("team") == self.team_id]
        
        return players
    
    def _top_players_in_position(
            self, position_name: str, 
            players: list[dict], 
            position_count: int
        ) -> list[dict]:
        """
        Sorts the players in descending order by their total goals and assists, and selects 
        the top players for a given position, handling cases where there are fewer players 
        than required.
        """
        players_sorted = sorted(
            players, 
            key=lambda p: p["goals_scored"] + p["assists"], 
            reverse=True
        )

        top_players = []
        actual_count = min(position_count, len(players_sorted))
        for i in range(actual_count):
            player = players_sorted[i]
            total_goals_assists = player["goals_scored"] + player["assists"]
            top_players.append({
                "name": player["web_name"],
                "total_goals_assists": total_goals_assists,
                "position": position_name,
            })
        
        return top_players
    
    def run(self) -> list[dict]:
        """
        Main method that process the selection of the top 7 players by position. It filters 
        players by position, sorts them, and returns the top players according to predefined 
        requirements for each position.
        """
        position_requirements = {
            1: 1,  # Goalkeepers
            2: 2,  # Defenders
            3: 3,  # Midfielders
            4: 1   # Forwards
        }

        magnificent_7 = []
        for element_type, count in position_requirements.items():
            position_name = self._get_position_name(element_type)
            players = self._filter_by_position(element_type)
            magnificent_7 += self._top_players_in_position(position_name, players, count)

        return magnificent_7