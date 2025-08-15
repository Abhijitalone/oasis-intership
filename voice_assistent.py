import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# Initialize speech recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
        return ""

def respond_to_command(command):
    if "hello" in command:
        speak("Hello! How can I help you?")
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")
    elif "date" in command:
        date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today's date is {date}")
    elif "search for" in command:
        search_query = command.split("search for")[-1].strip()
        speak(f"Searching for {search_query}")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("I'm sorry, I don't understand that command.")

# Main loop
speak("Voice assistant initialized. Say 'hello' to begin.")
while True:
    user_command = listen()
    if user_command:
        respond_to_command(user_command)
