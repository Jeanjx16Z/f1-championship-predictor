import matplotlib.pyplot as plt
import fastf1.plotting
import pandas as pd
import numpy as np
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
    import matplotlib.pyplot as plt

    drivers = laps['Driver'].unique()
    fig, ax = plt.subplots(figsize=(10,6))

    # fallback color palette
    default_colors = plt.cm.tab20.colors

    for i, drv in enumerate(drivers):
        drv_laps = laps.pick_driver(drv)

        if drv_laps.empty:
            continue

        positions = drv_laps['Position']
        lap_number = drv_laps['LapNumber']

        # Try team color → fallback matplotlib color
        try:
            color = "#" + drv_laps['TeamColor'].iloc[0]
        except:
            color = default_colors[i % len(default_colors)]

        ax.plot(
            lap_number,
            positions,
            color=color,
            linewidth=2
        )

        # label driver di akhir
        try:
            last_lap = lap_number.iloc[-1]
            last_pos = positions.iloc[-1]

            ax.text(
                last_lap + 0.3,
                last_pos,
                drv,
                fontsize=8,
                color=color,
                verticalalignment='center'
            )
        except:
            pass

    ax.set_title("Race Position Changes")
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Position")

    ax.invert_yaxis()
    ax.grid(True, linestyle='--', alpha=0.4)

    return fig