import json
import os

import requests
from datetime import datetime

from student.Library import Common

APIURI = "https://thetestingworldapi.com/"
postURI = "api/studentsDetails"

def test_add_multiple_students():
    api_url = APIURI + postURI
    common = Common("C:/Users/Deant/Documents/Bla/test_data.xlsx", "Sheet1")
    file_path = common.construct_file_path('..', 'student', 'jsonFileAddStudent.txt')
    file = open(file_path, 'r')
    json_input = file.read()
    request_json = json.loads(json_input)

    row = common.fetch_row_count()
    col = common.fetch_column_count()
    key_list = common.fetch_key_name()

    for i in range(2, row+1):
        updated_json_request = common.update_request_with_data(i, request_json, key_list)
        response = requests.post(api_url, updated_json_request)
        print(response)
        print(response.text)

