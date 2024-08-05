import os
import pytest
import requests
import json

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
    # Create a new student
    json_input = {
        "first_name": "Daba",
        "middle_name": "Didi",
        "last_name": "Du",
        "date_of_birth": "02/02/1992"
    }

    request_json = json.dumps(json_input)
    response = requests.post(APIURI + postURI, data=request_json, headers={"Content-Type": "application/json"})
    response_json = json.loads(response.text)
    studentID = str(response_json.get("id"))
    student_data["studentID"] = studentID

    print("Student response:", response.text)

    # Update technical skills
    techApi = "api/technicalskills"
    tech_json_input = {
        "id": studentID,
        "language": ["sample string 1", "sample string 2"],
        "yearexp": "sample string 2",
        "lastused": "sample string 3",
        "st_id": studentID  # Ensure this is the correct student ID
    }

    tech_request_json = json.dumps(tech_json_input)
    tech_response = requests.post(APIURI + techApi, data=tech_request_json,
                                  headers={"Content-Type": "application/json"})

    print("Technical skills response status code:", tech_response.status_code)
    print("Technical skills response text:", tech_response.text)

    # Update address
    addressApi = "api/addresses"
    address_json_input = {
        "Permanent_Address": {
            "House_Number": "sample string 1",
            "City": "sample string 2",
            "State": "sample string 3",
            "Country": "sample string 4",
            "PhoneNumber": [
                {"Std_Code": "sample string 1", "Home": "sample string 2", "Mobile": "sample string 3"},
                {"Std_Code": "sample string 1", "Home": "sample string 2", "Mobile": "sample string 3"}
            ]
        },
        "Current_Address": {
            "House_Number": "sample string 1",
            "City": "sample string 2",
            "State": "sample string 3",
            "Country": "sample string 4",
            "PhoneNumber": [
                {"Std_Code": "sample string 1", "Home": "sample string 2", "Mobile": "sample string 3"},
                {"Std_Code": "sample string 1", "Home": "sample string 2", "Mobile": "sample string 3"}
            ]
        },
        "stId": studentID
    }

    address_request_json = json.dumps(address_json_input)
    address_response = requests.post(APIURI + addressApi, data=address_request_json,
                                     headers={"Content-Type": "application/json"})

    print("Address response status code:", address_response.status_code)
    print("Address response text:", address_response.text)

    # Fetch final student details
    getURI = "api/FinalStudentDetails/" + studentID
    getResponse = requests.get(APIURI + getURI, headers={"Content-Type": "application/json"})

    print("Final student details response status code:", getResponse.status_code)
    print("Final student details response content:", getResponse.text)

    assert getResponse.status_code == 200

    # Parse the final response to ensure data was updated
    final_response_json = json.loads(getResponse.text)
    assert final_response_json['data']['TechnicalDetails'] != []
    assert final_response_json['data']['Address'] != []




@pytest.mark.dependency(depends=["test_add_student_data"])
def test_get_student_data(student_data):
    studentID = student_data["studentID"]
    assert studentID is not None, "studentID should not be None"
    getURI = "api/studentsDetails/" + str(studentID)  # Construct getURI inside the test
    print("Constructed getURI:", getURI)  # Print the getURI for debugging

    response = requests.get(APIURI + getURI, headers={"Content-Type": "application/json"})
    print("Response status code:", response.status_code)
    print("Response content:", response.text)
    print("Student ID from test_get_student_data:", studentID)

    # Assert that the get request was successful
    assert response.status_code == 200
    response_json = json.loads(response.text)

    # Correctly navigate to the "id" in the nested JSON structure
    assert str(response_json["data"]["id"]) == str(studentID)