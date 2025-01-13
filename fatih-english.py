import speech_recognition as sr
import os
import time
from gtts import gTTS
from playsound import playsound
import webbrowser
import wave
import threading
import vlc  # VLC library added for audio playback

# Function to play music
def play_audio(file):
    player = vlc.MediaPlayer(file)
    player.play()
    while player.is_playing():
        time.sleep(1)  # Wait while music is playing

def help():
    speak("Fatih Assistant Commands:")
    speak("1. 'Sleep' command: Enters sleep mode.")
    speak("2. 'Exit' command: Closes the assistant.")
    speak("3. 'Hello' command: Greets the assistant.")
    speak("4. 'Shutdown' command: Turns off the computer.")
    speak("5. 'Open browser' command: Launches Chrome browser.")
    speak("6. 'Open notepad' command: Launches Notepad.")
    speak("7. 'Play video' command: Opens YouTube.")
    speak("8. 'Search for' command: Performs a Google search.")
    speak("9. 'Play music' command: Plays music from YouTube.")
    speak("10. 'Help' command: Displays the list of commands.")

def speak(text):
    audio_path = "response.mp3"
    if os.path.exists(audio_path):
        os.remove(audio_path)
    tts = gTTS(text=text, lang='en')
    tts.save(audio_path)
    playsound(audio_path)

def save_audio(audio_data, filename="recorded_audio.wav"):
    with wave.open(filename, "wb") as wav_file:
        wav_file.setnchannels(1)  # Mono channel
        wav_file.setsampwidth(audio_data.sample_width)
        wav_file.setframerate(audio_data.sample_rate)
        wav_file.writeframes(audio_data.frame_data)

def get_audio_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            save_audio(audio)
            command = recognizer.recognize_google(audio, language='en-US')
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand. Please try again.")
            return ""
        except sr.RequestError:
            speak("There is an issue with the service. Please check your internet.")
            return ""
        except Exception as e:
            speak("An error occurred. Please try again.")
            return ""

def reminder_system():
    while True:
        speak("What would you like me to remind you?")
        reminder = get_audio_input()
        if reminder:
            speak(f"I will remind you to {reminder}.")
            speak("When should I remind you? Please say in minutes.")
            duration_str = get_audio_input()
            try:
                duration = int(duration_str)
                speak(f"I will remind you about {reminder} in {duration} minutes.")
                time.sleep(duration * 60)
                speak(f"Time to {reminder}.")
            except ValueError:
                speak("Invalid input. Please provide a valid duration.")

def sleep_mode():
    speak("Entering sleep mode. Please specify the duration in minutes.")
    duration_str = input("Duration (minutes): ")
    try:
        duration = int(duration_str) if duration_str else 0
        speak(f"Sleeping for {duration} minutes.")
        time.sleep(duration * 60)
        speak("I am awake now!")
    except ValueError:
        speak("Invalid duration. Please try again.")

def listen_continuously():
    while True:
        command = get_audio_input()
        if "remind" in command:
            threading.Thread(target=reminder_system).start()
        elif "hello" in command:
            speak("Hello! How can I assist you?")
        elif "shutdown" in command:
            speak("Goodbye!")
            os.system("shutdown /s /f /t 0")
        elif "open browser" in command:
            speak("Opening browser.")
            os.system("start chrome.exe")
        elif "open notepad" in command:
            speak("Opening Notepad.")
            os.system("start notepad.exe")
        elif "play video" in command:
            speak("Opening YouTube.")
            os.system("start chrome.exe https://www.youtube.com")
        elif "search for" in command:
            speak("What do you want to search for?")
            query = get_audio_input()
            if query:
                speak(f"Searching for {query}.")
                webbrowser.open(f"https://www.google.com/search?q={query}")
        elif "play music" in command:
            speak("Playing music.")
            os.system("start chrome.exe https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # Example link
        elif "help" in command:
            help()

def start_assistant():
    listen_thread = threading.Thread(target=listen_continuously)
    listen_thread.daemon = True
    listen_thread.start()
    while True:
        time.sleep(1)

# Start the assistant
start_assistant()
