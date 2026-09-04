import numpy as np

class KalmanTracker:
    """Constant-velocity 2-D tracker with state [x,y,vx,vy]."""
    def __init__(self, dt=0.2, q=2.0, r=144.0):
        self.F=np.array([[1,0,dt,0],[0,1,0,dt],[0,0,1,0],[0,0,0,1]],float)
        self.H=np.array([[1,0,0,0],[0,1,0,0]],float)
        self.Q=q*np.eye(4)
        self.R=r*np.eye(2)
        self.P=100*np.eye(4); self.x=np.zeros(4); self.ready=False

    def step(self,z):
        if not self.ready:
            if z is None: return None
            self.x[:2]=z; self.ready=True; return self.x.copy()
        self.x=self.F@self.x
        self.P=self.F@self.P@self.F.T+self.Q
        if z is not None:
            y=z-self.H@self.x
            S=self.H@self.P@self.H.T+self.R
            K=self.P@self.H.T@np.linalg.inv(S)
            self.x=self.x+K@y
            self.P=(np.eye(4)-K@self.H)@self.P
        return self.x.copy()
