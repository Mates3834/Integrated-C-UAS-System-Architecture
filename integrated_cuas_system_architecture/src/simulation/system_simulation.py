import numpy as np
from src.detection.detection_layer import synthetic_detection
from src.tracking.kalman_tracker import KalmanTracker
from src.assessment.risk_assessment import assess_track
from src.decision.response_manager import select_response

def target_position(t):
    return np.array([900.0-7.0*t, 300.0+70.0*np.sin(0.04*t)])

def run(duration=80.0,dt=0.2,seed=4):
    rng=np.random.default_rng(seed)
    tracker=KalmanTracker(dt=dt)
    logs=[]
    for t in np.arange(0,duration+dt,dt):
        truth=target_position(t)
        detection=synthetic_detection(truth,rng)
        track=tracker.step(detection)
        risk=assess_track(track)
        response=select_response(risk["level"])
        logs.append({
            "time":float(t),"truth":truth,"detection":detection,
            "track":None if track is None else track.copy(),
            "risk":risk,"response":response
        })
    return logs
