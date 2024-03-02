import os
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3 
import pywhatkit
import re
from datetime import timedelta
from turtle import *
import colorsys
import datetime
import wikipedia
import pyjokes
import openai

load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "**the__key**"

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet():
    speak("I'm your ATH Chatbot")
    speak("How may I assist you in your endeavors?")
    print("I'm your ATH Chatbot")
    print("How may I assist you in your endeavors?")

def talk(text, emotion="happy"):
    emotions = {
        "happy": {"rate": 150, "volume": 1.0},
        "sad": {"rate": 100, "volume": 0.8},
        "angry": {"rate": 120, "volume": 1.2}
    }
    engine.setProperty("rate", emotions[emotion]["rate"])
    engine.setProperty("volume", emotions[emotion]["volume"])
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print("Hey, oh bearer of curiosity...")
            talk("Hey, oh bearer of curiosity...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice, show_all=False)
            command = command.lower()
            if "ATH Chatbot" in command:
                command = command.replace("ATH Chatbot", "")
                talk("Nice to listen to you, fellow adventurer of the digital realm")
                print(command)
                speak(command)
        return command

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return None

def chatgpt_search(query):
    response = openai.Completion.create(
        engine="davinci",
        prompt=query,
        max_tokens=100,
        n=3,  # Number of search results to retrieve
        stop=None,
        temperature=0.6,
        log_level="info"
    )

    search_results = []
    for choice in response.choices:
        search_results.append(choice.text.strip())

    return search_results

def run_ATH_Chatbot():
    command = take_command()
    if command is None:
        return

    if "play" in command:
        song = command.replace("play", "")
        talk("Playing " + song)
        print("Playing " + song)
        start_time = datetime.datetime.now()
        pywhatkit.playonyt(song)
        end_time = datetime.datetime.now()
        load_time = end_time - start_time
        load_time_seconds = load_time.total_seconds()

        if load_time_seconds > 1:
            speed(0)
            hideturtle()
            bgcolor("black")
            tracer(5)
            width(2)
            h = 0.0001

            for i in range(90):
                color(colorsys.hsv_to_rgb(h, 1, 1))
                forward(100)
                left(60)
                forward(100)
                right(120)
                circle(50)
                left(240)
                forward(100)
                left(60)
                forward(100)
                h += 0.02
                color(colorsys.hsv_to_rgb(h, 1, 1))
                forward(100)
                right(60)
                forward(100)
                left(120)

                circle(-50)
                right(240)
                forward(100)
                right(60)
                forward(100)
                left(2)
                h += 0.02

            done()

        pywhatkit.playonyt(song)

    elif load_time_seconds < 1:
        pywhatkit.playonyt(song)

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + current_time)
        print(current_time)

    elif 'where is ' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)

    elif 'what do you mean by' in command:
        person = command.replace('whta do you mean by', '')
        info = wikipedia.summary(person, 5)
        print(info)
        talk(info)

    elif 'who is' in command:
        person = command.replace('who the hell is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)

    elif 'what is ' in command:
        person = command.replace('what is', '')
        info = wikipedia.summary(person, 3)
        print(info)
        talk(info)

    elif 'explain' in command:
        person = command.replace('explain', '')
        info = wikipedia.summary(person, 4)
        print(info)
        talk(info)

    elif 'describe' in command:
        person = command.replace('describe', '')
        info = wikipedia.summary(person, 8)
        print(info)
        talk(info)

    elif 'would you like to be in a relationship' in command:
        talk("Life as a digital nomad has its perks, but there's no denying that my WiFi connection is my one true love")

    elif 'send message' in command or 'send WhatsApp message' in command:
        phone_number = re.search(r'\d{10}', command).group()
        message = command.replace('send message', '').replace('send WhatsApp message', '')
        pywhatkit.sendwhatmsg(phone_number, message, 0, 0)
        talk("WhatsApp message sent!")

    elif 'joke' in command:
        talk(pyjokes.get_joke())

    else:
        search_query = command
        search_results = chatgpt_search(search_query)

        if search_results:
            talk("Here are some search results:")
            for i, result in enumerate(search_results):
                talk(f"Result {i + 1}: {result}")
        else:
            talk("Sorry, I couldn't find any relevant search results.")

while True:
    greet()
    run_ATH_Chatbot()
    speak("What's your next command?")
