
import subprocess

def speak_with_festival(text):
    """Speak the given text using Festival with Scottish voice."""
    try:
        # Set voice to Scottish (assuming installed)
        command = f"(voice_cstr_scottish_english_female) (SayText \"{text}\")"
        subprocess.run(['festival', '--pipe'], input=command.encode(), check=True)
    except Exception as e:
        print(f"Error using Festival TTS: {e}")

if __name__ == "__main__":
    speak_with_festival("Hello, this is Barbarella. I speak with a proper Scottish voice, powered by Festival.")
