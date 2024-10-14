# Magnificence

Magnificence is a Django-based web application that is able to provide the top 7 players in the English Premier League using data from an external API.

A Django Rest-Framework view is configured to handle a GET request to retrieve the data and is validated using Serializers. An `InboundSerializer` to validate the response data from the API and an `OutboundSerializer` to validate the data that processes the retrieval of the Magnificent 7. Additionally, a param can be passed to in the request to specifically find the top 7 players in a team.

## Installation 
```
git clone https://github.com/itsjali/Magnificence.git
cd Magnificence

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Application
```
./manage.py runserver
```

In a separate terminal you can use a curl command to make a GET request to the Magnificence endpoint. 
```
curl -X GET http://127.0.0.1:8000/api/get-magnificence-data/

# Optionally you can specify a team
curl -X GET http://127.0.0.1:8000/api/get-magnificence-data/?team_name=Liverpool
```

## Running tests
```
pytest tests/  --disable-warnings
```
