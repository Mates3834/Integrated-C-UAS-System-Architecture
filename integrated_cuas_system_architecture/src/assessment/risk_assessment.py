import numpy as np

def assess_track(track_state, protected_center=(0.0,0.0)):
    """
    Generic, explainable airspace-risk score based only on proximity and speed.
    Intended for systems-engineering demonstrations.
    """
    if track_state is None:
        return {"score":0.0, "level":"UNKNOWN"}

    p=np.asarray(track_state[:2],float)
    v=np.asarray(track_state[2:4],float)
    d=np.linalg.norm(p-np.asarray(protected_center,float))
    speed=np.linalg.norm(v)

    proximity=np.clip(1.0-d/1200.0,0.0,1.0)
    motion=np.clip(speed/30.0,0.0,1.0)
    score=float(0.75*proximity+0.25*motion)

    level="LOW" if score < 0.35 else ("MEDIUM" if score < 0.65 else "HIGH")
    return {"score":score,"level":level,"distance":float(d),"speed":float(speed)}
