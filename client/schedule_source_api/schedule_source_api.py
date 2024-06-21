import requests
import json
import http
from urllib.parse import urlencode

import os
import sys

from client.schedule_source_api.credentials import load_creds

from utils.Paths import Paths
from utils.URLs import URLs
from utils.helperFunctions import parse_tsv


#Used to sign in to mgr portal of schedule source. 
#Params: "code" - facility code used to sign in ("ISU For all")
#        "username" - mgr username used to sign in 
#        "password" - mgr password used to sign in
#
#  Returns: API token and Session ID codes. Needed to be used as headers to retrieve information from API
def authenticate():
    ##########  Part 1 #########
    url = URLs.AUTHENTICATE.value
    creds = load_creds()
    payload = json.dumps(
        {
            "ExternalId": "",
            "Request": {
                "Portal": "mgr",
                "Code": creds.code,
                "Username": creds.user,
                "Password": creds.password,
            },
        }
    )
    headers = {
        "Content-Type": "application/json",
        "BuildCookie": "24060420361420.32735534d2ac453faeb6fc50bf314f4d",
        "Cookie": "BuildCookie=24060420361420.32735534d2ac453faeb6fc50bf314f4d",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = response.json()
    api_token = response_json["Response"]["APIToken"]
    session_id = response_json["Response"]["SessionId"]
    return {"sessionId": session_id, "apiToken": api_token}


#Direct API Call to retrieve a list of locations and their respective ID's
#Returns a list of the json data retrieved from the API call
#No Parameter values
#Returns list of json data that are valid location facility codes
def getLocations():
    credentials = authenticate()
    conn = http.client.HTTPSConnection("test.tmwork.net")
    payload = ""

    headers = {
        "Content-Type": "application/json",
        "x-session-id": credentials["sessionId"],
        "x-api-token": credentials["apiToken"],
    }

    base_url = Paths.SS_LOCATIONS.value
    url = (
        f"{base_url}"
        "?Fields=ExternalBusinessId"
    )
    
    conn.request(
        "GET",
        url,
        payload,
        headers,
    )
    
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data)
    filtered_data = []
    for item in json_data:
        if item["ExternalBusinessId"] is not None:
            if not(isinstance(item["ExternalBusinessId"], int)):
                filtered_data.append(item)
    
    print(filtered_data)        
    return filtered_data


# API call to update (PUT) the availability of a student employee
# Param - newAvailability - list of json objects that contain AvailableRanges field
# Replaces the employee's current available ranges with the new available ranges brought in from class schedule
# No Return value
def updateAvailability(newAvailability):
    credentials = authenticate()
    conn = http.client.HTTPSConnection("test.tmwork.net")
    payload = newAvailability

    headers = {
        "Content-Type": "application/json",
        "x-session-id": credentials["sessionId"],
        "x-api-token": credentials["apiToken"],
    }

    payload_json = json.dumps(payload)
    
    url = Paths.SS_AVAILABILITY.value
    conn.request("PUT", url, payload_json, headers)
    res = conn.getresponse()
    data = res.read()
    

#API call to retrieve active employees at a given facility
#Param - location - the facility code we are interested in
#Returns a list of employees at the given location
def getEmployeesAtLocation(location):
    credentials = authenticate()
    conn = http.client.HTTPSConnection("test.tmwork.net")
    payload = ""
    
    headers = {
        "Content-Type": "application/json",
        "x-session-id": credentials["sessionId"],
        "x-api-token": credentials["apiToken"],
    }
    
    path = Paths.SS_EMPLOYEES_LOCATION.value
    query_params = {
        "Fields": "ExternalId",
        "BusinessExternalId": location,
        "TermDate": "{NULL}"
    }
    
    encoded_query_params = urlencode(query_params)
    url = f"{path}?{encoded_query_params}"

    conn.request(
        "GET",
        url,
        payload,
        headers,
    )
    
    res = conn.getresponse()
    data = res.read().decode('utf-8')
    data = parse_tsv(data)
    
    id_list = []
    for item in data:
        id_list.append(item["ExternalId"])
        
    print(id_list)  
    return id_list

