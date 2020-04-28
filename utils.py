import matplotlib
import matplotlib.pyplot as plt

def get_angle(x):
    return 90.2 - (8.71*x) + (0.428 * (x ** 2)) - (0.0118 * (x ** 3))

def save_plot(time, readings):
    fig, ax = plt.subplots()
    ax.plot(time, readings)
    ax.set(xlabel='Time (s)', ylabel='Goniometer reading (degrees)')
    ax.grid()
    fig.savefig("public/images/dynamic_reading.png")
