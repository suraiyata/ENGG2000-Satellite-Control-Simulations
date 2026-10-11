
import numpy as np
import matplotlib.pyplot as plt

Kp, Kd = 2.0, 0.8
MIN_PWM, MAX_PWM = 70, 140

errors = np.linspace(-90, 90, 500)

def motor_pwm(error, gyro):
    u = Kp * error - Kd * gyro
    return np.where(
        abs(u) < 1,
        0,
        np.sign(u) * np.clip(abs(u), MIN_PWM, MAX_PWM)
    )

plt.figure(figsize=(9, 5))

for gyro in [-30, 0, 30]:
    plt.plot(
        errors, motor_pwm(errors, gyro),
        label=f"Gyro = {gyro:+d} deg/s"
    )

plt.axhline(0, color="gray", linewidth=0.7)
plt.axvline(0, color="gray", linewidth=0.7)
plt.title("Figure C - PD Control Law Simulated Output")
plt.xlabel("Bearing error (degrees)")
plt.ylabel("Commanded motor PWM (-140 to +140)")
plt.grid(alpha=0.25)
plt.legend()
plt.tight_layout()
plt.savefig("Figure_C.png", dpi=300)
plt.show()
