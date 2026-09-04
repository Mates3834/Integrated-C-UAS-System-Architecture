import numpy as np
import matplotlib.pyplot as plt
from src.simulation.system_simulation import run

logs=run()
truth=np.array([x["truth"] for x in logs])
track=np.array([x["track"][:2] if x["track"] is not None else [np.nan,np.nan] for x in logs])
time=np.array([x["time"] for x in logs])
risk=np.array([x["risk"]["score"] for x in logs])

print("Final response state:", logs[-1]["response"])
print("Final risk level:", logs[-1]["risk"]["level"])

plt.figure()
plt.plot(truth[:,0],truth[:,1],label="True trajectory")
plt.plot(track[:,0],track[:,1],linestyle="--",label="Estimated track")
plt.xlabel("x [m]"); plt.ylabel("y [m]")
plt.title("Integrated Airspace Tracking Architecture")
plt.grid(True); plt.legend(); plt.axis("equal")
plt.show()

plt.figure()
plt.plot(time,risk)
plt.xlabel("Time [s]"); plt.ylabel("Risk score")
plt.title("Abstract Risk Assessment")
plt.grid(True)
plt.show()
