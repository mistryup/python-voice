# To install PyAudio/flac on mac, try:
# brew install portaudio && pip3 install PyAudio && brew install flac 

# import openai_secret_manager
import openai
import speech_recognition as sr
from gtts import gTTS
import os

# Fetching the keys
# assert "openai" in openai_secret_manager.get_services()
# secrets = openai_secret_manager.get_secret("openai")
# openai_api_key = openai_secret_manager.get_secret("openai")["api_key"]

# Authenticate with the API key
openai.api_key = os.environ.get('CHATGPT_KEY')
print("openai.api_key",openai.api_key)

def get_audio():
    print("Listening...")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    return said.lower()

def respond(text):
    print(text)
    tts = gTTS(text=text)
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")

while True:
    text = get_audio()
    if not text.strip():  # Check if value is empty or whitespace
        print("Got empty audio: "+text)
        continue  # Return from the function if value is blank
    else:
        print("Got a question...")
        response = openai.Completion.create(
            engine="text-davinci-003",  # davinci
            prompt=text,
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.2,
        )
        print("Response is: "+str(response))
        text_response = response.choices[0].text.strip()
        if text_response:
            respond(text_response)
            print("SAY:"+text_response+":END")
        else:
            respond("Sorry, I didn't understand what you said.")
            print("SAY:"+"No, Comprende!")
