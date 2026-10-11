
import numpy as np
import matplotlib.pyplot as plt

NUM_IR = 6
SENSOR_SPACING = 30
LASER_SENSOR_INDEX = 3
SIGMA = 25
MIN_CONFIDENCE = 0.10

sensor_angles = (
    np.arange(NUM_IR) - LASER_SENSOR_INDEX
) * SENSOR_SPACING

true_angles = np.linspace(-90, 60, 300)
estimated = []

for true_angle in true_angles:
    confidence = np.exp(
        -0.5 * ((true_angle - sensor_angles) / SIGMA)**2
    )
    confidence[confidence < MIN_CONFIDENCE] = 0

    if confidence.sum() > 0:
        bearing = np.sum(
            confidence * sensor_angles
        ) / confidence.sum()
    else:
        bearing = np.nan

    estimated.append(bearing)

estimated = np.array(estimated)
error = estimated - true_angles

fig, axes = plt.subplots(2, 1, figsize=(9, 7),
                        sharex=True)

axes[0].plot(true_angles, true_angles,
             "--", label="Ideal (y = x)")
axes[0].plot(true_angles, estimated,
             label="Weighted-mean estimator")
axes[0].set_ylabel("Estimated bearing (degrees)")
axes[0].legend()
axes[0].grid(alpha=0.2)

axes[1].axhspan(-5, 5, alpha=0.12,
                color="green", label="+/- 5 deg tolerance")
axes[1].plot(true_angles, error, color="firebrick")
axes[1].axhline(0, color="gray", linewidth=0.7)
axes[1].set_xlabel("True beacon bearing (degrees)")
axes[1].set_ylabel("Estimation error (degrees)")
axes[1].legend()
axes[1].grid(alpha=0.2)

fig.suptitle("Figure D - Bearing Estimator Simulation")
plt.tight_layout()
plt.savefig("Figure_D.png", dpi=300)
plt.show()
