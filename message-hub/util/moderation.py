import os
from itertools import accumulate
import json
import requests

def moderate_text(text, lang):
  payload = {"text":text,"lang":lang,"mode":"standard","api_user":os.environ['API_KEY'],"api_secret":os.environ['API_SECRET']}

  res = requests.post("https://api.sightengine.com/1.0/text/check.json",
                      data=payload)
  if (res.status_code != 200):
    raise Exception(res.content)
  
  moderations = json.loads(res.text)
  print(moderations)
  checks = ["link", "personal","profanity"]
  results = map(lambda check: moderations[check], checks)
  #matches = sum(results)
  #print(matches)
  print(results)

moderate_text("5034351574", "en")
