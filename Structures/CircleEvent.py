from Event import Event
from Arc import Arc

class CircleEvent(Event):
    def __init__(self, alpha: Arc):
        super().__init__()
        self.alpha = alpha