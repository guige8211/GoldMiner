import urllib.request
import urllib.parse
import json

with open("rogue_miner_project.zip", "rb") as f:
    data = f.read()

req = urllib.request.Request("https://0x0.st", data=data)
try:
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))
except Exception as e:
    print(e)
