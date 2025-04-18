import datetime
import os
import sys
import time
import webbrowser
import pyautogui
import pyttsx3
import speech_recognition as sr
import psutil
import json
import pickle
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import load_model
import random
from tensorflow.keras.preprocessing.sequence import pad_sequences

with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder = pickle.load(encoder_file)


def initialize_engine():
    # This function is no longer needed when using ElevenLabs
    # But we'll keep it as a placeholder for compatibility
    pass


def speak(text):
    try:
        # Import the elevenlabs library
        import requests

        # ElevenLabs API configuration
        ELEVEN_LABS_API_KEY = "sk_b9ee02eec661ecfad17a625bf58784b3473f28ae8cf52e16"  # Replace with your actual API key
        VOICE_ID = "UgBBYS2sOqTuMpoF3BR0"  # Marc's voice ID

        # API endpoint for text-to-speech
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

        # Request headers
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVEN_LABS_API_KEY
        }

        # Request body
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        print("Generating speech with ElevenLabs...")

        # Make the API request
        response = requests.post(url, json=data, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the audio to a temporary file
            temp_file = "temp_speech.mp3"
            with open(temp_file, "wb") as f:
                f.write(response.content)

            # Play the audio
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()

            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            # Clean up
            pygame.mixer.quit()

            # Optional: remove the temporary file
            # import os
            # os.remove(temp_file)

        else:
            print(f"Error generating speech: {response.status_code}")
            print(response.text)
            # Fall back to pyttsx3 if ElevenLabs fails
            engine = pyttsx3.init("sapi5")
            voices = engine.getProperty("voices")
            engine.setProperty("voices", voices[0].id)
            engine.say(text)
            engine.runAndWait()

    except Exception as e:
        print(f"Error with ElevenLabs: {e}")
        # Fall back to pyttsx3 if there's any issue
        engine = pyttsx3.init("sapi5")
        voices = engine.getProperty("voices")
        engine.setProperty("voices", voices[0].id)
        engine.say(text)
        engine.runAndWait()


def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...", end="", flush=True)
        r.pause_threshold = 1.0
        r.phrase_threshold = 0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold = True
        r.operation_timeout = 4
        r.non_speaking_duration = 0.5
        r.dynamic_energy_adjustment = 2
        r.energy_threshold = 4000
        r.phrase_time_limit = 10
        # print(sr.Microphone.list_microphone_names())
        audio = r.listen(source)
    try:
        print("\r", end="", flush=True)
        print("Recognizing......", end="", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print("\r", end="", flush=True)
        print(f"User said : {query}\n")
    except Exception as e:
        print("Say that again please")
        return "None"
    return query


def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(day_of_week)
    return day_of_week


def wishMe():
    hour = int(datetime.datetime.now().hour)
    current_time = time.strftime("%I:%M:%p")

    # Extract hour and minute values
    hour_val = int(time.strftime("%I"))
    minute_val = int(time.strftime("%M"))
    am_pm = time.strftime("%p")

    day = cal_day()

    # Construct time phrase naturally (without saying "colon")
    time_phrase = f"{hour_val} "
    if minute_val == 0:
        time_phrase += f"o'clock {am_pm}"
    else:
        time_phrase += f"{minute_val} {am_pm}"

    if (hour >= 0) and (hour <= 12) and ('AM' in current_time):
        speak(f"Good morning, it's {time_phrase} on {day}")
    elif (hour >= 12) and (hour <= 16) and ('PM' in current_time):
        speak(f"Good afternoon, it's {time_phrase} on {day}")
    else:
        speak(f"Good evening, it's {time_phrase} on {day}")


def social_media(command):
    if 'facebook' in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif 'discord' in command:
        speak("Opening Discord")
        webbrowser.open("https://www.discord.com")
    elif 'whatsapp' in command:
        speak("Opening WhatsApp")
        webbrowser.open("https://web.whatsapp.com")
    elif 'youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif 'instagram' in command:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")
    elif 'twitter' in command:
        speak("Opening Twitter")
        webbrowser.open("https://x.com/?lang=en")
    elif 'X' in command:
        speak("Opening X")
        webbrowser.open("https://x.com/?lang=en")
    elif 'twitch' in command:
        speak("Opening Twitch")
        webbrowser.open("https://www.twitch.tv")
    elif 'reddit' in command:
        speak("Opening Reddit")
        webbrowser.open("https://www.reddit.com")
    elif 'github' in command:
        speak("Opening GitHub")
        webbrowser.open("https://www.github.com")
    elif 'stackoverflow' in command:
        speak("Opening Stack Overflow")
        webbrowser.open("https://www.stackoverflow.com")
    elif 'sis' in command:
        speak("Opening Antonine")
        webbrowser.open("https://ua.edu.lb")
    else:
        speak("cannot open website")


def schedule():
    day = cal_day().lower()
    speak(f"Today's schedule is as follows:")
    week = {
        "monday": "5:00 PM - 8:00 PM: Database Programming",
        "tuesday": "8:30 AM - 11:30 AM: UI Ux\n11:30 AM - 2:30 PM: operating system",
        "wednesday": "11:30 PM - 2:30 PM: Web Development",
        "thursday": "8:30 AM - 11:30 AM: Artificial Intelligence",
        "friday": "no classes but do a quick revision",
        "saturday": "you're free but work on you homeworks!",
        "sunday": "just have fun!"
    }

    if day in week:
        schedule = week[day]
        speak(schedule)


def openApp(command):
    try:
        if "notepad" in command:
            speak("Opening Notepad")
            os.startfile("notepad")
        elif "calculator" in command:
            speak("Opening Calculator")
            os.startfile("calc")
        elif "cmd" in command:
            speak("Opening Command Prompt")
            os.startfile("cmd")
        elif "vs code" in command or "visual studio code" in command:
            speak("Opening Visual Studio Code")
            try:
                # Try common VS Code paths
                possible_paths = [
                    os.path.join(os.environ['LOCALAPPDATA'], "Programs", "Microsoft VS Code", "Code.exe"),
                    "C:\\Program Files\\Microsoft VS Code\\Code.exe",
                    "C:\\Program Files (x86)\\Microsoft VS Code\\Code.exe"
                ]

                for path in possible_paths:
                    if os.path.exists(path):
                        os.startfile(path)
                        return

                # If none of the paths worked, try starting via command
                os.system("code")
            except Exception as e:
                speak("Could not open Visual Studio Code")
                print(f"Error opening VS Code: {e}")
        elif "power point" in command:
            speak("Opening PowerPoint")
            try:
                os.system("start powerpnt")
            except:
                speak("Could not open PowerPoint")
        elif "word" in command:
            speak("Opening Word")
            try:
                os.system("start winword")
            except:
                speak("Could not open Word")
        elif "paint" in command:
            speak("Opening Paint")
            try:
                os.system("start mspaint")
            except:
                speak("Could not open Paint")
        elif "excel" in command:
            speak("Opening Excel")
            try:
                os.system("start excel")
            except:
                speak("Could not open Excel")
        else:
            speak("Cannot open application")
    except Exception as e:
        speak("Error opening application")
        print(f"Error: {e}")


def closeApp(command):
    try:
        if "notepad" in command:
            speak("Closing Notepad")
            os.system("taskkill /f /im notepad.exe")

        elif "calculator" in command:
            speak("Closing Calculator")
            os.system("taskkill /f /im calc.exe")

        elif "cmd" in command:
            speak("Closing Command Prompt")
            os.system("taskkill /f /im cmd.exe")

        elif "vs code" in command or "visual studio code" in command:
            speak("Closing Visual Studio Code")
            os.system("taskkill /f /im Code.exe")

        elif "power point" in command:
            speak("Closing PowerPoint")
            os.system("taskkill /f /im POWERPNT.EXE")

        elif "word" in command:
            speak("Closing Word")
            os.system("taskkill /f /im WINWORD.EXE")

        elif "paint" in command:
            speak("Closing Paint")
            os.system("taskkill /f /im mspaint.exe")

        elif "excel" in command:
            speak("Closing Excel")
            os.system("taskkill /f /im EXCEL.EXE")

        else:
            speak("Could not identify which application to close")

    except Exception as e:
        speak("Error occurred while closing the application")
        print(f"Error closing application: {e}")


def browsing(query):
    if 'google' in query:
        # Extract the search term if it's in the query
        if 'search' in query and 'for' in query:
            search_term = query.split('for', 1)[1].strip()
            search_url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
            speak(f"Searching Google for {search_term}")
            webbrowser.open(search_url)
        else:
            # Ask for the search term if not provided
            speak("What should I search on Google?")
            search_term = command()
            if search_term != "None":
                search_url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
                speak(f"Searching Google for {search_term}")
                webbrowser.open(search_url)


def condition():
    usage = str(psutil.cpu_percent())
    speak(f"cpu is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"your battery is {percentage} percent")
    if percentage >= 80:
        speak("we have enough charging to continue")
    elif (percentage >= 40) and (percentage <= 75):
        speak("we should connect our system as soon as possible!")
    else:
        speak("we have very low power, better charge our system!")


def get_movie_suggestion():
    """Provide a random movie suggestion"""
    movie_suggestions = [
        "The Shawshank Redemption is a classic worth watching.",
        "You might enjoy Inception if you like mind-bending plots.",
        "The Lord of the Rings trilogy is always a great choice.",
        "How about watching The Matrix? It's a sci-fi classic.",
        "Pulp Fiction by Quentin Tarantino is a unique film experience."
    ]
    return random.choice(movie_suggestions)


def get_food_suggestion():
    """Provide a random food suggestion"""
    food_suggestions = [
        "Pasta is always a good choice! Quick to make and delicious.",
        "How about trying something new? Maybe explore Thai cuisine?",
        "Tacos are always a good idea!",
        "A homemade pizza could be fun to make and delicious to eat!",
        "Perhaps try a healthy salad with grilled chicken?"
    ]
    return random.choice(food_suggestions)


def handle_special_intents(tag):
    """Handle intents that need special processing"""
    if tag == "datetime":
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        day_of_week = cal_day()
        speak(f"It's {current_time} on {day_of_week}, {current_date}")
        return True
    elif tag == "weather":
        speak(
            "I don't have access to real-time weather data. You might want to check a weather service for that information.")
        return True
    elif tag == "movies":
        suggestion = get_movie_suggestion()
        speak(suggestion)
        return True
    elif tag == "food":
        suggestion = get_food_suggestion()
        speak(suggestion)
        return True
    elif tag == "capabilities":
        speak(
            "I can answer questions, provide information, tell jokes, have conversations, help with your schedule, open applications and websites, and assist with various tasks. Just ask!")
        return True
    return False


if __name__ == "__main__":
    wishMe()
    while True:
        query = command().lower()
        # query = input("Enter your command: ")
        # Check for specific commands first
        if "schedule" in query or "university time table" in query or "university timetable" in query:
            schedule()
        elif any(platform in query for platform in ["facebook", "discord", "whatsapp", "youtube",
                                                    "instagram", "twitter", "twitch", "reddit", "github",
                                                    "stackoverflow", "sis"]) or query.strip() == "x":
            social_media(query)
        elif ("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup")
            speak("Volume increased")
        elif ("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown")
            speak("Volume decreased")
        elif ("mute" in query) or ("silent" in query):
            pyautogui.press("volumemute")
            speak("Volume muted")
        elif "open" in query:
            openApp(query)
        elif "close" in query:
            closeApp(query)
        elif ("search on google" in query) or ("open google" in query):
            browsing(query)
        elif ("system condition" in query) or ("condition" in query):
            speak("checking the system condition")
            condition()
        elif ("exit" in query) or ("quit" in query):
            speak("Goodbye!")
            sys.exit()
        else:
            padded_sequence = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
            result = model.predict(padded_sequence)
            tag = label_encoder.inverse_transform([np.argmax(result)])
            tag = tag[0]  # Extract the string from the array

            # Check for special intents that need custom handling
            if not handle_special_intents(tag):
                # Find and speak the appropriate response for the detected intent
                for i in data['intents']:
                    if i['tag'] == tag:
                        response = np.random.choice(i['responses'])
                        speak(response)
                        print(response)
                        break