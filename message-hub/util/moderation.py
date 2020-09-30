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
  checks = ["link", "personal","profanity"]
  results = map(lambda check: moderations[check], checks)

  matches = []
  for result in results:
   matches.extend(result["matches"])
  types = list(map(lambda match: match["type"], matches))

  return len(types)>0, types
