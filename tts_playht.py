import requests
import random
from IPython.display import Audio, display, clear_output
import time
import json

AUTHORIZATION = ""
X_USER_ID = ""

def init(AUTHORIZATION, X_USER_ID):
  AUTHORIZATION = this.AUTHORIZATION
  X_USER_ID = this.X_USER_ID

def generate_transcript(contentArray, voice = "en-AU-Neural2-A", style = ""):
  if (AUTHORIZATION =="" or X_USER_ID == ""):
    print("no Authorization or id")
    return null
  url = "https://play.ht/api/v1/convert"
  content = contentArray#["hello world, my name is Matthew.", "and i want to say some things to the world"]

  payload = {
      "content": content,
      "voice": voice,
      "narrationStyle": style
  }
  headers = {
      "accept": "application/json",
      "content-type": "application/json",
      "AUTHORIZATION": AUTHORIZATION,
      "X-USER-ID": X_USER_ID
  }
  
  response = requests.post(url, json=payload, headers=headers)
  i = 10
  while(response.status_code == 400 and i>=0 ):
    time.sleep(random.choice(range(5)))
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    i-=1
  transcriptionId = response.json()["transcriptionId"]

  #print(response.text)
  return transcriptionId
def generate_sound(transcriptionId):
  url = "https://play.ht/api/v1/articleStatus?transcriptionId=" + transcriptionId

  headers = {
      "accept": "application/json",
      "AUTHORIZATION": AUTHORIZATION,
      "X-USER-ID": X_USER_ID
  }
  response = requests.get(url, headers=headers)
  while (response.json()["converted"] == False):
    response = requests.get(url, headers=headers)
    time.sleep(1.5)

  #print(response.text)

  audio_url = response.json()["audioUrl"]

  return audio_url


def play_sound(audio_url, file_name = "temp_audio.mp3"):
  r = requests.get(audio_url, allow_redirects=True)
  open(file_name, 'wb').write(r.content)
  display(Audio('temp_audio.mp3', autoplay=True))

def get_sounds():
  url = "https://play.ht/api/v1/getVoices"
  headers = {
      "accept": "application/json",
      "AUTHORIZATION": AUTHORIZATION,
      "X-USER-ID": X_USER_ID
  }

  response = requests.get(url, headers=headers)
  print(response.json())
  voices_list = response.json()["voices"]

  # Filter out the elements that have a "language" key that does not contain the substring "English"
  filtered_list = [element for element in voices_list if "language" in element and "English" in element["language"]]
  i = 0
  for e in filtered_list:
    print(i)
    print(e["value"],e["gender"], e["voiceType"],e["sample"] )
    print(e.get("styles", "empty"))
    #play_sound(e["sample"], file_name = "sample.mp3")
    print()
    i+=1
