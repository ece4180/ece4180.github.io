import matplotlib
import matplotlib.pyplot as plt

def get_angle(x):
    print('raw flex', x)
    return 0.538*x - 16410

def save_plot(time, readings):
    fig, ax = plt.subplots()
    ax.plot(time, readings)
    ax.set(xlabel='Time (s)', ylabel='Goniometer reading (degrees)')
    ax.grid()
    fig.savefig("public/images/dynamic_reading.png")
