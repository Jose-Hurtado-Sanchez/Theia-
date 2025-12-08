# fall detection program that can connect to flutterr via app.py.
# The detector consumes accelerometer samples m/s^2
# and outputs events through callbacks: on_detect, on_cancel, on_escalate.

from dataclasses import dataclass
from time import monotonic

# Gravity constant 
G = 9.80665

@dataclass
class FallConfig:
  
    # thresholds for fall detection
   
    impact_g: float = 2.5            # magnitude threshold to consider impact
    inactivity_g: float = 0.20       # if magnitutde is under, device is considered not moving
    inactivity_window_s: float = 1.2 # duration of not moving after impact to confirm fall
    debounce_s: float = 3.0          # ignore new triggers for N seconds after a detection
    countdown_s: int = 10            # seconds to answer "Are you OK?" quesiton
@dataclass
class FallEvent:
    # container representing a detected impact event
    t_impact: float
    peak_g: float

class FallDetector:
    """
    fall detection logic:
      - When idle, wait for a spike greater than impact_g
      - After impact, waiting for inactivity less than inactivity_g for inactivity_window_s
      - When inactivity follows impact, start countdown and if it expires, escalate
    detector logic:
      - feed_accel(ax,ay,az, t=None) using samples 
      - tick(t=None), call periodically to allow countdowns to expire
      - cancel(), cancel active countdown from user input
    Callbacks:
      - on_detect(FallEvent, countdown_seconds)
      - on_cancel()
      - on_escalate()
    """

    def __init__(self, config: FallConfig, on_detect, on_cancel, on_escalate):
        self.cfg = config
        self.on_detect = on_detect
        self.on_cancel = on_cancel
        self.on_escalate = on_escalate

        
        self._state = "idle"
        self._impact_time = None
        self._peak_g = 0.0
        self._last_trigger = -1e9
        self._countdown_deadline = None
        self._countdown_active = False

    def _now(self):
        return monotonic()

    def feed_accel(self, ax: float, ay: float, az: float, t: float | None = None):
        
        # Use accelerometer sample for detector, ax, ay, az in m/s^2.
       
        t = t if t is not None else self._now()

        # magnitude in g
        mag_g = (ax*ax + ay*ay + az*az) ** 0.5 / G

        # debounce, ignore input soon after a trigger to prevent repeated alerts
        if t < self._last_trigger + self.cfg.debounce_s:
            return

        if self._state == "idle":
            # Detect impact spike
            if mag_g >= self.cfg.impact_g:
                self._state = "post_impact"
                self._impact_time = t
                self._peak_g = mag_g

        elif self._state == "post_impact":
            # If device is still for inactivity window, then fall
            if mag_g < self.cfg.inactivity_g and (t - self._impact_time) >= self.cfg.inactivity_window_s:
                self._state = "countdown"
                self._countdown_active = True
                self._countdown_deadline = t + self.cfg.countdown_s
                self._last_trigger = t
                # Start callback for listeners/UI
                self.on_detect(FallEvent(self._impact_time, self._peak_g), self.cfg.countdown_s)
            # If too much time has passed without inactivity then resets to idle
            elif (t - self._impact_time) > 2.5:
                self._state = "idle"

        elif self._state == "countdown":
            # feed loop, countdown expiration handled by tick()
            pass

    def tick(self, t: float | None = None):
        
        # Should be called periodically, checks countdown deadlines and escalates when countdown expires.
        
        if self._state != "countdown" or not self._countdown_active:
            return
        t = t if t is not None else self._now()
        if t >= self._countdown_deadline:
            self._countdown_active = False
            self._state = "idle"
            self.on_escalate()

    def cancel(self):
        
        # Called when user cancels the alert, outputs on_cancel() callback for logging/UI.
       
        if self._state == "countdown" and self._countdown_active:
            self._countdown_active = False
            self._state = "idle"
            self.on_cancel()

    # for demo, simulates an impact then inactivity samples
    def simulate_fall(self):
        # Impact spike 
        for _ in range(3):
            self.feed_accel(0.0, 0.0, 3.2 * G)
        # Inactivity window, simulate 1.2s of no motion
        for _ in range(60):  # ~60 samples at 50Hz -> ~1.2s
            self.feed_accel(0.02 * G, 0.02 * G, 0.02 * G)
