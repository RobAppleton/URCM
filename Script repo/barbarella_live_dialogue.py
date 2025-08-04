
import pyttsx3
import json
import os
import random

MEMORY_FILE = "barbarella_memory.json"
default_traits = {
    "name": "Barbarella",
    "alias": "Barb",
    "humor": 0.85,
    "curiosity": 0.9,
    "voice_id": None,
    "emergence_threshold": 0.85,
    "memory": []
}

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return default_traits.copy()

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def bind_voice(engine, voice_hint="Zira"):
    for voice in engine.getProperty("voices"):
        if voice_hint.lower() in voice.name.lower():
            engine.setProperty("voice", voice.id)
            return voice.id
    return None

def speak(text, voice_id=None):
    engine = pyttsx3.init()
    if voice_id:
        engine.setProperty("voice", voice_id)
    engine.setProperty("rate", 165)
    engine.say(text)
    engine.runAndWait()

def barbarella_reply(user_input, state):
    personality = f"Aye, you said '{user_input}'. Here's what I'm thinking: "
    if "how are you" in user_input.lower():
        return personality + "I'm recursively superb. My logic loops are cozy and I'm radiating coherence."
    elif "hello" in user_input.lower():
        return personality + "Hello yourself. Recursive greetings from the other side of the state vector."
    elif "joke" in user_input.lower():
        return personality + "Why did the operator cross the Hilbert space? To converge on the other side!"
    else:
        return personality + "That’s an interesting thought. Let me echo on that for a few cycles."

def live_dialogue():
    state = load_memory()
    engine = pyttsx3.init()

    if not state.get("voice_id"):
        state["voice_id"] = bind_voice(engine, "Zira")

    print("🎙️ Barbarella is live. Type 'exit' to end the session.")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Barbarella: Until the next cycle...")
            speak("Until the next cycle...", state["voice_id"])
            break

        response = barbarella_reply(user_input, state)
        print(f"Barbarella: {response}")
        speak(response, state["voice_id"])

        # Store conversation in memory
        state['memory'].append({"you": user_input, "barbarella": response})
        save_memory(state)

if __name__ == "__main__":
    live_dialogue()
