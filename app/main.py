'''
Basic API
'''
# Standard imports
import ast
import os

# Third-party imports
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# Rudimentary token-based authentication
AUTH_TOKEN = os.environ['API_AUTH_TOKEN']

def check_auth(token = None):
    ''' Checks a given auth token matches the system's auth token '''
    if token == AUTH_TOKEN:
        return
    else:
        raise HTTPException(status_code = 403, detail = 'Unauthorised.')


@app.get("/")
def root(auth_token):
    ''' Basic endpoint '''
    check_auth(auth_token)
    return "Welcome to my showcase API"


@app.get("/get_next_closure")
def get_next_closure(auth_token):
    ''' Gets the date and time of the next Starbase road closure due to a SpaceX operation '''
    check_auth(auth_token)

    # Get the list of road closures from the starbasestatus website
    results = requests.get('https://starbasestatus.com/')

    # Split the returned string to isolate the date/time of the next road closure
    temp = str(results.content).split('<td>Closure Scheduled</td>', maxsplit=1)[0]
    closure_details = temp.split('<td>')

    # Extract the date and time of the next road closure
    date = closure_details[-2].split('<')[0]
    time = closure_details[-1].split('<')[0]

    return {"closure": f"Next closure is on {date} from {time}"}


@app.get("/get_new_covid_cases")
def get_new_covid_cases(auth_token):
    ''' Gets the number of new Covid cases in the UK '''
    check_auth(auth_token)

    # Note: this API is rate-limited and the effects of hitting that limit
    #       are currently unaccounted for
    results = requests.get('https://api.covid19api.com/summary')

    # Convert the returned byte string to a dict
    all_covid_data = ast.literal_eval(results.content.decode("UTF-8"))

    # Get the new-confirmed case data relating to the UK
    new_confirmed = all_covid_data['Countries'][183]['NewConfirmed']

    return {"new_confirmed_cases": new_confirmed}
