from itertools import accumulate
import json
import requests

def moderate_text(text, lang):
  payload = {"text":text,"lang":lang,"mode":"standard","api_user":"","api_secret":""}
  res = requests.request("POST", "https://api.sightengine.com/1.0/text/check.json",
                      data=payload,
                      headers={"Content-Type": "multipart/form-data"})
  if (res.status_code != 200):
    raise Exception(res.content)
  
  moderations = json.loads(res.text)
  checks = ["link", "personal","profanity"]
  results = map(lambda check: moderations[check], checks)
  matches = sum(results)
  print(matches)

moderate_text("5034351574", "en")
