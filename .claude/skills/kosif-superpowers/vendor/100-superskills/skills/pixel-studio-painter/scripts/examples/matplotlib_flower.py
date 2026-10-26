import numpy as np
import matplotlib.pyplot as plt
t = np.linspace(0, 2 * np.pi, 2000)
r = np.sin(6 * t) + 0.3
fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"projection": "polar"})
ax.fill(t, np.abs(r), color="#e91e63", alpha=.75)
ax.plot(t, np.abs(r), color="#880e4f", lw=2)
ax.set_axis_off()
plt.show()
