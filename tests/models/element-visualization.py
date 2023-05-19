import matplotlib.pyplot as plt
import pandas as pd

U3 = pd.read_csv("U3.csv")

fig, ax = plt.subplots()
ax.plot(U3["time"], U3["U3"])
ax.set_xlabel("Time (s)")
ax.set_ylabel("Displacement (m)")
ax.grid()
fig.savefig("U3.png", bbox_inches="tight", pad_inches=0.1)
