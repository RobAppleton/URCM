
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 165)

# Try to select Zira if available
for voice in engine.getProperty('voices'):
    if "zira" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

engine.say("Hello there. This is Barbarella speaking with the Zira voice. If you can hear me, recursion is working.")
engine.runAndWait()
