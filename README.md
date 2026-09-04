# Integrated C-UAS System Architecture

A modular systems-engineering framework for studying an **integrated Counter-Unmanned Aircraft System (C-UAS) architecture**, combining synthetic aerial-object detection, target tracking, state estimation, risk assessment, and safety-oriented response management.

The project focuses on the **system-level integration and information flow** between individual C-UAS subsystems rather than on a single detection, tracking, or control algorithm.

The current public implementation demonstrates the following pipeline:

```text
Detection
    ↓
Tracking
    ↓
State Estimation
    ↓
Risk Assessment
    ↓
Decision Support
    ↓
Safety-Oriented Response
```

The framework is designed for research and educational studies in **C-UAS systems engineering, autonomous systems, multi-sensor architectures, target tracking, state estimation, decision support, and airspace safety**.

> **Note:** The public implementation is intentionally generic and sanitized. It contains no weapon-control logic, physical engagement mechanisms, platform-specific operational parameters, restricted sensor specifications, or real-world mission data.

---

## System Architecture

The overall architecture is organized into modular functional layers.

```text
             Aerial Object / UAV
                     |
                     v
          +---------------------+
          |   Detection Layer   |
          | Synthetic Sensors   |
          +---------------------+
                     |
                     v
             Object Detection
                     |
                     v
          +---------------------+
          |   Tracking Layer    |
          |   Kalman Filter     |
          +---------------------+
                     |
                     v
          Estimated Track State
             [x, y, vx, vy]
                     |
                     v
          +---------------------+
          | Risk Assessment     |
          |                     |
          | • Proximity         |
          | • Motion            |
          | • Track State       |
          +---------------------+
                     |
                     v
               Risk Level
          LOW / MEDIUM / HIGH
                     |
                     v
          +---------------------+
          | Response Manager    |
          +---------------------+
                     |
                     v
          Safety Response State

          LOW      → MONITOR
          MEDIUM   → VERIFY
          HIGH     → ALERT
```

This modular structure allows individual components to be replaced or extended without redesigning the complete architecture.

---

# 1. Detection Layer

The first stage represents a generic aerial-object detection subsystem.

The current implementation uses **synthetic Cartesian detections** generated from the true target position.

For a true target position

```text
p_target = [x, y]^T
```

the measurement is represented as

```text
z_k = p_target + v_k
```

where

```text
v_k
```

represents synthetic measurement noise.

A configurable detection probability is also included.

Therefore, the detection layer can produce either

```text
Detection available
```

or

```text
No detection
```

at each simulation step.

This provides a simple representation of imperfect sensing.

---

# 2. Detection Uncertainty

Real sensing systems do not provide perfect measurements.

The public simulation therefore introduces measurement uncertainty:

```text
True Target Position
        |
        v
 Measurement Noise
        |
        v
 Synthetic Detection
```

The detection layer also includes a probability of missed detection.

Conceptually,

```text
P_detection < 1
```

which means that the tracker must remain functional even when measurements are temporarily unavailable.

This is particularly useful for demonstrating the importance of state estimation.

---

# 3. Tracking Layer

Detected aerial objects are passed to the tracking subsystem.

The tracker maintains an estimate of the target state:

```text
x_hat =
[x, y, vx, vy]^T
```

where

```text
x, y   = estimated position
vx, vy = estimated velocity
```

The tracking subsystem is based on a discrete **constant-velocity Kalman filter**.

---

# 4. State-Space Tracking Model

The target dynamics are represented using

```text
x_k =
F x_(k-1) + w_k
```

with

```text
F =

[1  0  dt  0 ]
[0  1  0   dt]
[0  0  1   0 ]
[0  0  0   1 ]
```

The measurement equation is

```text
z_k =
H x_k + v_k
```

where

```text
H =

[1  0  0  0]
[0  1  0  0]
```

The tracker therefore estimates velocity even though the synthetic detection layer directly measures only position.

---

# 5. Kalman Prediction

When a track already exists, the filter predicts the next state:

```text
x_hat(k|k-1) =
F x_hat(k-1|k-1)
```

The covariance is propagated as

```text
P(k|k-1) =
F P(k-1|k-1) F^T + Q
```

where `Q` represents process uncertainty.

This prediction stage is particularly important when a detection is temporarily unavailable.

---

# 6. Measurement Update

When a new detection is received, the innovation is

```text
y_k =
z_k - H x_hat(k|k-1)
```

and the innovation covariance is

```text
S_k =
H P(k|k-1) H^T + R
```

The Kalman gain becomes

```text
K_k =
P(k|k-1) H^T S_k^-1
```

The state estimate is then corrected:

```text
x_hat(k|k) =
x_hat(k|k-1) + K_k y_k
```

The resulting track is passed to the next layer of the architecture.

---

# 7. Track State

The output of the tracking layer contains an estimated aerial-object state:

```text
Track State
    |
    +--> Position
    |
    +--> Velocity
    |
    +--> Covariance
```

The public architecture primarily uses estimated position and velocity for the risk-assessment layer.

This creates a clean interface between sensing and higher-level decision support:

```text
Sensor
   ↓
Detection
   ↓
Tracker
   ↓
State Estimate
   ↓
Decision Layer
```

---

# 8. Risk Assessment Layer

The risk-assessment subsystem converts the estimated track into a simple and explainable **risk score**.

The current public implementation uses two generic indicators:

```text
1. Proximity
2. Estimated target speed
```

The objective is not to classify a real-world threat.

Instead, the module demonstrates how state-estimation outputs can be converted into higher-level system information.

---

# 9. Proximity Indicator

The distance between the tracked object and a generic protected reference point is calculated as

```text
d =
||p_track - p_reference||
```

A normalized proximity score is then generated.

Conceptually:

```text
Large Distance
     ↓
 Low Proximity Score

Small Distance
     ↓
 High Proximity Score
```

This creates an intuitive relationship between the estimated track and the abstract system-risk level.

---

# 10. Motion Indicator

The estimated target velocity is used to calculate speed:

```text
V =
sqrt(vx^2 + vy^2)
```

A normalized motion score is generated from this value.

The architecture therefore uses

```text
Estimated Position
        +
Estimated Velocity
        ↓
Risk Assessment
```

rather than relying on a single instantaneous measurement.

---

# 11. Risk Score

The public implementation combines the indicators using a weighted score:

```text
Risk Score =
w_p * Proximity
+
w_v * Motion
```

where

```text
w_p = proximity weight
w_v = motion weight
```

The resulting value is mapped to an abstract risk level:

```text
LOW
MEDIUM
HIGH
```

The thresholds are generic simulation parameters and should not be interpreted as operational criteria.

---

# 12. Explainable Decision Architecture

A key design objective of the project is **interpretability**.

Instead of using a black-box decision system, the architecture provides an easily understandable flow:

```text
Target detected
       ↓
Target tracked
       ↓
Position estimated
       ↓
Velocity estimated
       ↓
Proximity evaluated
       ↓
Motion evaluated
       ↓
Risk score calculated
       ↓
Response state selected
```

This makes the framework useful for systems-engineering studies where subsystem behavior and interfaces need to be clearly understood.

---

# 13. Response Management

The final subsystem converts the risk level into an abstract safety response.

The current implementation uses only:

| Risk Level | Response |
|---|---|
| UNKNOWN | MONITOR |
| LOW | MONITOR |
| MEDIUM | VERIFY |
| HIGH | ALERT |

The response layer deliberately stops at decision-support states.

No physical engagement or defeat mechanism is implemented.

---

# 14. Response States

### MONITOR

The track remains under observation.

```text
Track
  ↓
MONITOR
```

---

### VERIFY

Additional verification is conceptually requested.

```text
Track
  ↓
MEDIUM Risk
  ↓
VERIFY
```

This could represent a requirement for additional sensing or operator review in a future system.

---

### ALERT

A high abstract risk score generates an alert state.

```text
Track
  ↓
HIGH Risk
  ↓
ALERT
```

The public architecture intentionally terminates at this point.

---

# 15. End-to-End Information Flow

The complete system operates as:

```text
             UAV / Aerial Object
                     |
                     v
             Synthetic Sensor
                     |
                     v
                 Detection
                     |
                     v
               Kalman Tracker
                     |
                     v
              State Estimation
                     |
                     v
          Position + Velocity
                     |
                     v
             Risk Assessment
                     |
                     v
                Risk Level
                     |
                     v
            Response Manager
                     |
                     v
        MONITOR / VERIFY / ALERT
```

This demonstrates the interaction between sensing, estimation, assessment, and decision-support components within a unified architecture.

---

# 16. Systems Engineering Perspective

The main objective of this project is not the complexity of any individual algorithm.

Instead, the focus is on **integration between heterogeneous system functions**.

The architecture separates the system into functional blocks:

```text
Sensing
   ↓
Perception
   ↓
Tracking
   ↓
Estimation
   ↓
Assessment
   ↓
Decision Support
```

Each subsystem has a clearly defined input and output.

This modular structure makes it possible to replace components independently.

For example:

```text
Synthetic Detection
        ↓
could become
        ↓
Radar / Camera Detection
```

or

```text
Kalman Filter
      ↓
could become
      ↓
EKF / UKF / IMM
```

without fundamentally changing the overall system architecture.

---

# 17. Relationship to the Other UAV Projects

This repository represents the **system-level architecture** of the UAV/C-UAS project group.

The three related repositories can be conceptually organized as:

```text
UAV Detection, Tracking
and Sensor Fusion
        |
        | perception
        v
Integrated C-UAS
System Architecture
        |
        | system-level coordination
        v
Autonomous UAV
Pursuit / Rendezvous
        |
        | autonomy / GNC
        v
UAV Motion
```

Therefore:

```text
Project 10
Detection + Tracking + Sensor Fusion

Project 11
Systems Integration + Risk Assessment + Decision Support

Project 9
UAV Guidance + Estimation + Autonomous Pursuit
```

Together, these projects demonstrate different layers of an autonomous aerial-systems architecture.

---

# 18. Repository Structure

```text
integrated_cuas_system_architecture/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   │
│   ├── detection/
│   │   ├── __init__.py
│   │   └── detection_layer.py
│   │
│   ├── tracking/
│   │   ├── __init__.py
│   │   └── kalman_tracker.py
│   │
│   ├── assessment/
│   │   ├── __init__.py
│   │   └── risk_assessment.py
│   │
│   ├── decision/
│   │   ├── __init__.py
│   │   └── response_manager.py
│   │
│   └── simulation/
│       ├── __init__.py
│       └── system_simulation.py
│
├── examples/
│   └── run_demo.py
│
└── docs/
    └── architecture.md
```

---

# 19. Module Description

| Module | Purpose |
|---|---|
| `detection_layer.py` | Synthetic aerial-object detection |
| `kalman_tracker.py` | Target tracking and state estimation |
| `risk_assessment.py` | Explainable abstract risk scoring |
| `response_manager.py` | Safety-oriented response-state selection |
| `system_simulation.py` | Integrated end-to-end simulation |
| `run_demo.py` | Demonstration and visualization |
| `architecture.md` | System architecture documentation |

---

# 20. Running the Project

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the integrated demonstration:

```bash
python examples/run_demo.py
```

The example performs the complete sequence:

```text
Target generation
       ↓
Synthetic detection
       ↓
Kalman tracking
       ↓
Risk assessment
       ↓
Response selection
       ↓
Visualization
```

---

# 21. Example Outputs

The current framework can produce:

- True aerial-object trajectory
- Estimated target track
- Tracking behavior during missed detections
- Risk-score evolution
- Risk-level transitions
- Final response state

Recommended repository figures:

```text
results/
├── system_architecture.png
├── target_tracking.png
├── risk_score_history.png
└── response_state_history.png
```

---

# 22. Evaluation Metrics

Several system-level metrics can be considered.

### Tracking Error

```text
e_tracking =
||p_true - p_estimated||
```

---

### Detection Availability

```text
Detection Rate =
N_detected / N_total
```

---

### Risk Score

The evolution of the abstract risk score can be evaluated over time.

---

### Response-State Transitions

The number and timing of transitions between

```text
MONITOR
VERIFY
ALERT
```

can be recorded.

These metrics provide a basis for evaluating the complete architecture rather than only the target tracker.

---

# Technologies

- Python
- NumPy
- Matplotlib
- Kalman Filtering
- State Estimation
- Systems Engineering
- Modular System Architecture
- Decision Support

---

# Research Areas

The project is related to:

- Counter-UAS Systems
- Autonomous Systems
- Systems Engineering
- UAV Detection and Tracking
- State Estimation
- Sensor Integration
- Airspace Monitoring
- Decision Support
- Risk Assessment
- Multi-Sensor Architectures
- Guidance, Navigation and Control

---

# Project Motivation

Counter-UAS and autonomous airspace-monitoring systems are inherently **multi-disciplinary systems**.

A complete architecture may require information to move through several functional stages:

```text
Detection
    ↓
Tracking
    ↓
State Estimation
    ↓
Situation Assessment
    ↓
Decision Support
```

Developing these components independently is not sufficient to understand the behavior of the complete system.

The purpose of this project is therefore to investigate **system integration and subsystem interfaces**.

The framework provides a modular environment in which different sensing, tracking, estimation, and assessment algorithms can be integrated and compared.

---

# Future Extensions

The architecture can be expanded with more advanced research components.

### Perception

- RGB UAV detection
- Thermal UAV detection
- Radar-like sensing
- Multi-sensor fusion
- Confidence-aware detections

### Tracking

- Extended Kalman Filter
- Unscented Kalman Filter
- Interacting Multiple Model filtering
- Multi-target tracking
- Track management
- Data association

### System Architecture

- Multiple sensor nodes
- Distributed tracking
- Sensor-task management
- Multi-agent airspace monitoring
- Human-in-the-loop verification
- Confidence-aware decision support

### Simulation

- 3-D target trajectories
- Multiple aerial objects
- Environmental uncertainty
- Sensor field-of-view constraints
- Communication delays
- Detection dropouts
- Monte Carlo evaluation

A future research architecture could therefore become:

```text
          Radar       RGB       Thermal
             \         |         /
              \        |        /
               v       v       v
               Multi-Sensor Fusion
                        |
                        v
                  Track Manager
                        |
                        v
               State Estimation
                        |
                        v
               Situation Assessment
                        |
                        v
                 Decision Support
                        |
                        v
              Human / Safety Layer
```

---

# Public Implementation Notice

The source code in this repository contains **generic and sanitized implementations** developed for systems-engineering and autonomous-systems research demonstrations.

The public implementation intentionally excludes:

- Operational sensor specifications
- Restricted surveillance information
- Platform-specific parameters
- Real-world protected-site configurations
- Operational detection thresholds
- Threat-classification databases
- Weapon-control logic
- Payload-control logic
- Physical engagement mechanisms
- Defeat mechanisms
- Interceptor-control commands
- Terminal guidance
- Restricted mission data
- Classified or sensitive system information

The response-management layer is intentionally limited to:

```text
MONITOR
VERIFY
ALERT
```

The repository should therefore be interpreted as a **generic C-UAS / autonomous airspace-safety systems-engineering framework**, not as an operational countermeasure system.

---

# Status

**Research-oriented systems architecture prototype / active development**

The current implementation includes:

- Synthetic aerial-object detection
- Kalman-based target tracking
- State estimation
- Explainable risk assessment
- Abstract response management
- End-to-end simulation

More advanced perception, sensor fusion, multi-target tracking, and system-level evaluation methods may be incorporated in future versions.

---

# Author

**Mehmet Ateş**

Research interests:

- Autonomous Systems
- Guidance, Navigation and Control (GNC)
- UAV Autonomy
- Counter-UAS Systems
- Systems Engineering
- Target Tracking
- State Estimation
- Sensor Fusion
- Path Planning
- Reinforcement Learning
- Marine and Aerial Robotics
```

