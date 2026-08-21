from os import getenv
import requests
import json
from dotenv import load_dotenv

def check_api_IP(ip_adress, method="GET"):
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
    print(f"Checking IP: {ip_adress}")
    response = requests.request(method=method, url=url, headers=header, params=query_info)
    decodedResponse = json.loads(response.text)
    print(json.dumps(decodedResponse, sort_keys=True, indent=4))
