import json

import jsonpath
import requests

APIURI = "https://thetestingworldapi.com/"
HEADER = {"Content-Type": "application/json"}

def test_create_student():
    global id

    postURI = "api/studentsDetails"
    json_input = {
        "first_name": "Daba",
        "middle_name": "Didi",
        "last_name": "Du",
        "date_of_birth": "02/02/1992"
    }
    request_json = json.dumps(json_input)
    response = requests.post(APIURI + postURI, data=request_json, headers=HEADER)
    print(response.status_code)
    print(response.text)
    response_json = json.loads(response.text)
    id = jsonpath.jsonpath(response_json, "id")
    assert response.status_code == 201

def test_add_student():
    getURI = "api/studentsDetails" + str(id[0])

    response = requests.get(APIURI + getURI, headers=HEADER)
    print(response.status_code)
    print(response.text)
