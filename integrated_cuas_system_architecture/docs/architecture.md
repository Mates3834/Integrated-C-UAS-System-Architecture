# Architecture Notes

The public prototype demonstrates interface separation between:

1. Detection
2. Tracking / state estimation
3. Risk assessment
4. Abstract response management
5. Evaluation

The design is intentionally platform-independent. The response layer exposes
only MONITOR, VERIFY and ALERT states. This makes the repository suitable for
systems-engineering demonstrations without implementing physical engagement or
defeat mechanisms.
