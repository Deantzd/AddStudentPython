import os
import pytest
import requests
import json
import jsonpath

APIURI = "https://thetestingworldapi.com/"
postURI = "api/studentsDetails"
studentID = None
getURI = "api/studentsDetails/" + str(studentID)

@pytest.fixture(scope="module")
def student_data():
    data = {
        "studentID": None
    }
    return data

@pytest.mark.dependency()
def test_add_student_data(student_data):
    json_input = {
    "first_name": "Daba",
    "middle_name": "Didi",
    "last_name": "Du",
    "date_of_birth": "02/02/1992"
    }

    request_json = json.dumps(json_input)
    response = requests.post(APIURI+postURI, data=request_json, headers={"Content-Type": "application/json"})
    response_json = json.loads(response.text)
    student_data["studentID"] = str(response_json.get("id"))
    print(response.text)


def test_add_student_data_read_json_from_file(student_data):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'student', 'jsonFileAddStudent.txt')
    print("Current script directory:", current_dir)
    print("Constructed file path:", file_path)


    file = open(file_path, 'r')
    json_input = file.read()
    request_json = json.loads(json_input)


    response = requests.post(APIURI + postURI, data=json.dumps(request_json),
                             headers={"Content-Type": "application/json"})
    print("Response status code:", response.status_code)
    print("Response content:", response.text)

    assert response.status_code == 201

@pytest.mark.dependency(depends=["test_add_student_data"])
def test_update_student_data(student_data):
    studentID = student_data["studentID"]
    assert studentID is not None, "studentID should not be None"
    json_input = {
        "id": studentID,
        "first_name": "Daba",
        "middle_name": "Dada",
        "last_name": "Du",
        "date_of_birth": "02/02/2000"
    }

    request_json = json.dumps(json_input)

    updateURI = "api/studentsDetails/" + str(studentID)
    print("Constructed updateURI:", updateURI)

    response = requests.put(APIURI + updateURI, data=request_json, headers={"Content-Type": "application/json"})
    print("Response status code:", response.status_code)
    print("Response content:", response.text)

    assert response.status_code == 200

@pytest.mark.dependency(depends=["test_add_student_data"])
def test_get_student_data(student_data):
    studentID = student_data["studentID"]
    assert studentID is not None, "studentID should not be None"
    getURI = "api/studentsDetails/" + str(studentID)
    print("Constructed getURI:", getURI)

    response = requests.get(APIURI + getURI, headers={"Content-Type": "application/json"})
    print("Response status code:", response.status_code)
    print("Response content:", response.text)
    print("Student ID from test_get_student_data:", studentID)

    assert response.status_code == 200
    response_json = json.loads(response.text)
    id = jsonpath.jsonpath(response_json, "data.id")
    #assert str(response_json["data"]["id"]) == str(studentID)
    assert str(id[0]) == str(studentID)

@pytest.mark.dependency(depends=["test_add_student_data"])
def test_delete_student_data(student_data):
    studentID = student_data["studentID"]
    assert studentID is not None, "studentID should not be None"
    deleteURI = "api/studentsDetails/" + str(studentID)
    print("Constructed getURI:", deleteURI)

    response = requests.delete(APIURI + deleteURI, headers={"Content-Type": "application/json"})
    print("Response status code:", response.status_code)
    print("Response content:", response.text)
    assert response.status_code == 200



