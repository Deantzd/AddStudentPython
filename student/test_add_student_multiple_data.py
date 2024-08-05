import json
import requests
from datetime import datetime

from student.Library import Common

APIURI = "https://thetestingworldapi.com/"
postURI = "api/studentsDetails"

def test_add_multiple_students():
    api_url = APIURI + postURI

    common = Common("C:/Users/Deant/Documents/Bla/test_data.xlsx", "Sheet1")

    rows = common.fetch_row_count()
    key_list = common.fetch_key_name()

    for i in range(2, rows + 1):  # Start from the second row to skip headers
        json_input = {
            "first_name": "",
            "middle_name": "",
            "last_name": "",
            "date_of_birth": ""
        }

        json_input = common.update_request_with_data(i, json_input, key_list)
        json_input["date_of_birth"] = common.format_date(json_input["date_of_birth"])  # Format date

        request_json = json.dumps(json_input)

        response = requests.post(api_url, data=request_json, headers={"Content-Type": "application/json"})

        print(f"Response for student {i - 1}: {response.text}")

        assert response.status_code == 201, f"Expected status code 200, but got {response.status_code}"
