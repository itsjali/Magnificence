import requests

from django.conf import settings
from django.http import HttpRequest
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import InboundSerializer, OutboundSerializer
from api.services import GetMagnificent7


class GetMagnificenceDataView(APIView):
    """
    A view to fetch and process magnificence data from an external API and return the top 7 
    players across the league, optionally filtered by a specific team.

    This view handles a GET request to retrieve data from an external API endpoint. The response 
    from the external API is validated using the `InboundSerializer`. If the data is valid, 
    the data sets `elements` and `element_types` is used to generate the top 7 players using 
    the `GetMagnificent7` service.

    The user can optionally filter the top 7 players by passing a `team_name` query parameter. 
    If a `team_name` is provided, the view attempts to find the team and the `team_id` is passed 
    in the `GetMagnificent7` service. If the team name does not match any teams, an error message 
    is returned. Else, the top 7 players across the league are returned.

    Once the top 7 players are determined, the data is serialized using `OutboundSerializer`. 
    The view returns a successful response if all data is valid, or appropriate error messages 
    if validation fails.

    Query Parameters:
        - team_name (str, optional): The name of the team to filter players by.

    Responses:
        - 200 OK: Returns the top 7 players if the data is processed successfully.
        - 400 Bad Request: Returned if the inbound data fails validation, or if the provided 
          `team_name` is not valid.
        - 500 Internal Server Error: Returned if the outbound data fails validation.

    Args:
        request (HttpRequest): The incoming request object.

    Returns:
        A JSON response containing either the top 7 players, validation errors, or an error 
        message if the external API fails to respond.
    """
    def get(self, request: HttpRequest) -> Response:
        api_url = settings.MAGNIFICENCE_API_URL
        response = requests.get(api_url)

        if response.status_code == 200:
            response_data = response.json()
            inbound_serializer = InboundSerializer(data=response_data)
            if not inbound_serializer.is_valid():
                return Response(inbound_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            elements = response_data["elements"]
            element_types = response_data["element_types"]
            teams = response_data["teams"]

            team_name = request.query_params.get("team_name") # optional param
            team_id = None
            if team_name:
                for team in teams:
                    if team["name"].lower() == team_name.lower():
                        team_id = team["id"]
                        break

                if not team_id:
                    return Response(
                        {"error": f"'{team_name}' is not a valid team."}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            magnificent_7_data = GetMagnificent7(elements, element_types, team_id).run()
            
            outbound_serializer = OutboundSerializer(data=magnificent_7_data)
            if not outbound_serializer.is_valid():
                return Response(
                    outbound_serializer.errors, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            return Response(magnificent_7_data, status=status.HTTP_200_OK)

        return Response({"error": "Failed to fetch data"}, status=status.HTTP_400_BAD_REQUEST)
