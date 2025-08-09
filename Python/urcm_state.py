
# urcm_state.py
import uuid
from datetime import datetime

class URCM_State:
    def __init__(self):
        self.run_id = str(uuid.uuid4())
        self.timestamp = datetime.now().isoformat()
        self.entropy_map = {}
        self.operator_chain = []
        self.metrics = {}
        self.feedback = {}
        self.iteration = 0
        self.log = []
        self.commentary = []
        self.output_bundle = {}

    def record(self, message):
        self.log.append(f"[Step {self.iteration}] {message}")

    def comment(self, msg):
        self.commentary.append(msg)

    def finalize(self):
        self.output_bundle = {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "entropy": self.entropy_map,
            "operator_chain": self.operator_chain,
            "metrics": self.metrics,
            "feedback": self.feedback,
            "commentary": self.commentary
        }
