
import numpy as np
import matplotlib.pyplot as plt

# Controller parameters
Kp = 2.0
Kd = 0.8
MIN_PWM = 70
MAX_PWM = 140

# Assumed plant parameters (not measured)
MOTOR_EFFECT = 0.16
BODY_DAMPING = 0.5

dt = 0.005
time = np.arange(0, 3, dt)

# Start 45 degrees away from the target
bearing = 45.0
gyro = 0.0

bearing_history = []
pwm_history = []

for t in time:
    control = Kp * bearing - Kd * gyro

    if abs(control) < 1:
        pwm = 0
    else:
        pwm = np.sign(control) * np.clip(
            abs(control), MIN_PWM, MAX_PWM
        )

    # Simplified rotational plant
    angular_acceleration = (
        -MOTOR_EFFECT * pwm
        - BODY_DAMPING * gyro
    )

    gyro += angular_acceleration * dt
    bearing += gyro * dt

    bearing_history.append(bearing)
    pwm_history.append(pwm)

fig, axes = plt.subplots(
    2, 1, figsize=(9, 7), sharex=True
)

axes[0].axhspan(
    -10, 10, alpha=0.12, color="green",
    label="Alignment tolerance +/- 10 degrees"
)
axes[0].plot(time, bearing_history)
axes[0].axhline(0, color="gray", linewidth=0.7)
axes[0].set_ylabel("Bearing error (degrees)")
axes[0].legend()
axes[0].grid(alpha=0.2)

axes[1].plot(time, pwm_history, color="firebrick")
axes[1].axhline(0, color="gray", linewidth=0.7)
axes[1].set_xlabel("Time (seconds)")
axes[1].set_ylabel("Commanded PWM")
axes[1].grid(alpha=0.2)

fig.suptitle(
    "Figure E - Predicted V2 Closed-Loop Response"
)
plt.tight_layout()
plt.savefig("Figure_E.png", dpi=300)
plt.show()
