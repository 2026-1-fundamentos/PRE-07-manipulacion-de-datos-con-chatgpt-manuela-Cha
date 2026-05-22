"""Manipulación de datos de conductores con pandas."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

INPUT_DRIVERS = Path("files/input/drivers.csv")
INPUT_TIMESHEET = Path("files/input/timesheet.csv")
OUTPUT_SUMMARY = Path("files/output/summary.csv")
OUTPUT_PLOT = Path("files/plots/top10_drivers.png")


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    drivers = pd.read_csv(INPUT_DRIVERS)
    timesheet = pd.read_csv(INPUT_TIMESHEET)
    return drivers, timesheet


def build_summary(drivers: pd.DataFrame, timesheet: pd.DataFrame) -> pd.DataFrame:
    merged = timesheet.merge(drivers, on="driverId")
    certified = merged.query("certified == 'Y'")

    summary = (
        certified.groupby(["driverId", "name"], as_index=False)[
            ["hours-logged", "miles-logged"]
        ]
        .sum()
        .sort_values("hours-logged", ascending=False)
    )
    return summary


def save_summary(summary: pd.DataFrame) -> None:
    OUTPUT_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUTPUT_SUMMARY, index=False)


def plot_top10(summary: pd.DataFrame) -> None:
    top10 = summary.nlargest(10, "hours-logged")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top10["name"], top10["hours-logged"], color="darkorange")
    ax.set_xlabel("Horas registradas")
    ax.set_ylabel("Conductor")
    ax.set_title("Top 10 conductores por horas")
    ax.invert_yaxis()
    fig.tight_layout()
    OUTPUT_PLOT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PLOT)
    plt.close(fig)


def main() -> None:
    drivers, timesheet = load_data()
    summary = build_summary(drivers, timesheet)
    save_summary(summary)
    plot_top10(summary)


if __name__ == "__main__":
    main()
