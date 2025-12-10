import matplotlib.pyplot as plt

def init_plot():
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 1000)
    ax.set_xlabel("Frekvens (Hz)")
    ax.set_ylabel("Amplitude")
    return fig, ax, line

def update_plot(ax, line, xf, yf):
    line.set_data(xf, yf)
    for coll in ax.collections:
        coll.remove()
    ax.axvspan(0.1, 0.5, color='blue', alpha=0.2)
    ax.axvspan(0.5, 2.0, color='green', alpha=0.2)
    ax.axvspan(2.0, 5.0, color='red', alpha=0.2)
    ax.relim()
    ax.autoscale_view()
    plt.draw()
    plt.pause(0.001)