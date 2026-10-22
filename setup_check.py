from pathlib import Path

import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


print(f"NumPy: {np.__version__}")
print(f"Matplotlib: {matplotlib.__version__}")
print(f"OpenCV: {cv2.__version__}")

x = np.arange(5)
y = x**2

plt.plot(x, y, marker="o", markersize=8)
plt.xlabel("x")
plt.ylabel("y = x^2")
plt.savefig(Path(__file__).with_name("setup_check.png"))
plt.show()
