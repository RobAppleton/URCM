import json
import datetime
from pathlib import Path

class BarbMemory:
    def __init__(self, memory_path="BarbMem.json"):
        self.memory_path = Path(memory_path)
        self.load()

    def load(self):
        if self.memory_path.exists():
            with open(self.memory_path, "r", encoding="utf-8") as f:
                self.memory = json.load(f)
        else:
            self.memory = {"conversations": []}

    def append_entry(self, user_message, assistant_response):
        timestamp = datetime.datetime.now().isoformat()
        self.memory["conversations"].append({
            "timestamp": timestamp,
            "user": user_message,
            "barbarella": assistant_response
        })

    def save(self):
        with open(self.memory_path, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2)

    def summary(self, n=5):
        return self.memory["conversations"][-n:]

# Example interactive usage
if __name__ == "__main__":
    barb = BarbMemory()
    print("Barbarella memory system loaded.")
    print("Use barb.append_entry(user, response) to log dialogue.")
    print("Use barb.summary() to view recent exchanges.")
    print("Use barb.save() at end of session.")
