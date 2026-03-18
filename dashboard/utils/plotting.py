import matplotlib.pyplot as plt

#Base Style

def setup_ax(ax, title):
    ax.set_title(title, fontsize=14)
    ax.grid(True, linestyle="--", alpha=0.3)

# 1 Lap Time Comparison

def plot_lap_times(laps, drivers): 

    fig, ax = plt.subplots()

    for drv in drivers :
        drv_laps = laps.pick_driver(drv).pick_quicklaps()

        lap_times = drv_laps["LapTime"].dt.total_seconds()

        ax.plot(
            drv_laps["LapNumber"],
            lap_times,
            label=drv
        )

    setup_ax(ax, "Lap Time Comparison")

    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time (s)")

    ax.legend()

    return fig

# 2. Speed Telemetry

def plot_speed_trace(lap, label):
    fig, ax = plt.subplots()

    tel = lap.get_car_data().add_distance()

    ax.plot(
        tel["Distance"],
        tel["Speed"],
        label=label
    )

    setup_ax(ax, f"Speed Trace -- {label}")

    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Speed (km/h)")

    ax.legend()

    return fig

# 3.Position Changes

def plot_position_changes(laps):

    fig, ax = plt.subplots()

    drivers =  laps["Driver"].unique()

    for drv in drivers:
        drv_laps = laps.pick_driver(drv)

        ax.plot(
            drv_laps["LapNumber"],
            drv_laps["Position"],
            label=drv
        )

    setup_ax(ax, "Race Position Changes")

    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Position")

    ax.invert_yaxis()

    return fig