import requests
import random
from IPython.display import Audio, display, clear_output
import time
import json

AUTHORIZATION = ""
X_USER_ID = ""

def init(auth, user_id):
  global AUTHORIZATION
  global X_USER_ID
  AUTHORIZATION = auth
  X_USER_ID = user_id


def generate_transcript(contentArray, voice = "en-AU-Neural2-A", style = ""):
  if (AUTHORIZATION =="" or X_USER_ID == ""):
    print("no Authorization or id")
    return null
  url = "https://play.ht/api/v1/convert"
  content = contentArray#["hello world, my name is Matthew.", "and i want to say some things to the world"]
  sounds = get_sounds()
  if(not(style in sounds.get(voice))):
    style = ""
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
  i = 1
  while(response.status_code == 400 and i>=0 ):
    time.sleep(random.choice(range(5)))
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    if(response.json() == "{}"):
      print("you are probably out of words.")
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


def play_sound(audio_url = "", file_name = "speech_file.mp3"):
  if(audio_url != ""):
    r = requests.get(audio_url, allow_redirects=True)
    open(file_name, 'wb').write(r.content)
  display(Audio(file_name, autoplay=True))


def text_to_sound_file(contentArray, voice = "en-AU-Neural2-A", style = "",file_name = ""):
  trans = generate_transcript(contentArray,voice,style)
  url = generate_sound(trans)
  r = requests.get(url, allow_redirects=True)
  if(file_name == ""):
    file_name = voice+"_file.mp3"
  open(file_name, 'wb').write(r.content)

def get_sounds(language = "all"):
  url = "https://play.ht/api/v1/getVoices"
  headers = {
      "accept": "application/json",
      "AUTHORIZATION": AUTHORIZATION,
      "X-USER-ID": X_USER_ID
  }

  response = requests.get(url, headers=headers)
  if(response.status_code == 403):
    print("your auth data are wrong or missing, use init to configure it.")
    return 
  # print(response.json())
  voices_list = response.json()["voices"]

  # Filter out the elements that have a "language" key that does not contain the substring "English"
  filtered_list = voices_list
  if language != "all":
    filtered_list = [element for element in voices_list if "language" in element and language in element["language"]]
  i = 0
  models = {}
  for e in filtered_list:
    # print(i)
    
    models[e.get("value", "empty")] = (e.get("gender", "empty"), e.get("voiceType", "empty"),e.get("sample", "empty"),e.get("styles", "no_style"))
    #print(e)
    # print(e.get("styles", "empty"))
    # #play_sound(e["sample"], file_name = "sample.mp3")
    # print()
    i+=1
  return models
