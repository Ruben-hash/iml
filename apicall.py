from os import getenv
import requests
import json
from dotenv import load_dotenv

def check_api_IP(ip_adress:str):
    load_dotenv()
    url = 'https://api.abuseipdb.com/api/v2/check'
    query_info = {
        "ipAddress": ip_adress,
        "maxAgeInDays": 90
    }
    header = {
        'Accept': 'application/json',
        'Key':  getenv("ABUSEIPDB_API_KEY")
    }
    response = requests.request(method="GET", url=url, headers=header, params=query_info)
    decodedResponse = json.loads(response.text)
    print(decodedResponse)
    return json.dumps(decodedResponse, sort_keys=True, indent=4)
