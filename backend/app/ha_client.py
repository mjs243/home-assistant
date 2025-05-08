import os
import requests

HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}

def call_service(domain, service, data):
    """Call Home Assistant services"""
    url = f"{HA_URL}/api/services/{domain}/{service}"
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error calling service: {response.status_code} - {response.text}")
    
def get_states():
    """Get the states of all entities in Home Assistant"""
    url = f"{HA_URL}/api/states"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching states: {response.status_code} - {response.text}")
    
def get_entity_state(entity_id):
    """Get the state of a specific entity in Home Assistant"""
    url = f"{HA_URL}/api/states/{entity_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching entity state: {response.status_code} - {response.text}")
    
def get_services():
    """Get all available services in Home Assistant"""
    url = f"{HA_URL}/api/services"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching services: {response.status_code} - {response.text}")