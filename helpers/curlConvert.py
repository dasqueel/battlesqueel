import curlconverter
import argparse
import pprint
import shlex
import requests
import json

def parse_curl_command(curl_command, position):
    # Split the cURL command into arguments
    parts = shlex.split(curl_command)
    
    # Remove the initial 'curl' command
    parts = parts[1:]
    
    url = None
    headers = {}
    params = {}
    data = None
    method = 'get'
    
    i = 0
    while i < len(parts):
        part = parts[i]
        if part.startswith('-'):
            if part in ['-X', '--request']:
                method = parts[i + 1].lower()
                i += 2
            elif part in ['-H', '--header']:
                header = parts[i + 1]
                key, value = header.split(":", 1)
                headers[key.strip()] = value.strip()
                i += 2
            elif part in ['-d', '--data', '--data-raw', '--data-binary']:
                data = parts[i + 1]
                i += 2
            elif part == '--compressed':
                i += 1
            else:
                i += 1
        else:
            if not url:
                url = part
            i += 1
    
    # Update the position parameter in the URL
    if url:
        from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
        url_parts = list(urlparse(url))
        query = parse_qs(url_parts[4])
        query['position'] = position
        url_parts[4] = urlencode(query, doseq=True)
        url = urlunparse(url_parts)
    
    return method, url, headers, data

def getPlayers():
    parser = argparse.ArgumentParser(description='Convert cURL command to Python requests with a dynamic position')
    parser.add_argument('-curlCom', type=str, help='The cURL command to convert', required=True)
    parser.add_argument('-position', type=str, help='The position to replace in the URL', required=True)
    args = parser.parse_args()
    
    method, url, headers, data = parse_curl_command(args.curlCom, args.position)
    
    response = requests.get(url, headers=headers)
    
    if response:
        jsonResp = response.json()

        players = jsonResp['players']
        cleanPlayerObjs = []

        for player in players:
            if not player['draft']:
                cleanPlayerObj = {k: v for k, v in player.items() if v is not None}
                cleanPlayerObjs.append(cleanPlayerObj)

        file_path = f'{args.position}.json'
        with open(file_path, 'w') as json_file:
            json.dump(cleanPlayerObjs, json_file, indent=4)

if __name__ == "__main__":
    getPlayers()
