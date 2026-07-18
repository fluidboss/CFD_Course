"""Load and plot OpenFOAM v2312 cavity centre-line samples.

Expected case output:
    postProcessing/sampleDict/<time>/verticalCentreLine_U_p.xy
    postProcessing/sampleDict/<time>/horizontalCentreLine_U_p.xy

The loader also accepts p_U ordering and separate *_U.xy / *_p.xy files.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class SampleLine:
    distance: np.ndarray
    Ux: np.ndarray
    Uy: np.ndarray
    Uz: np.ndarray
    p: np.ndarray

    @property
    def speed(self) -> np.ndarray:
        return np.sqrt(self.Ux**2 + self.Uy**2 + self.Uz**2)


def latest_time_directory(sample_root: str | Path) -> Path:
    """Return the numerically latest OpenFOAM time directory."""
    root = Path(sample_root)
    if not root.is_dir():
        raise FileNotFoundError(
            f"Sampling directory not found: {root}\n"
            "Run: postProcess -func sampleDict -fields '(U p)' -latestTime"
        )

    numeric_directories: list[tuple[float, Path]] = []
    for path in root.iterdir():
        if not path.is_dir():
            continue
        try:
            numeric_directories.append((float(path.name), path))
        except ValueError:
            pass

    if not numeric_directories:
        raise FileNotFoundError(f"No numerical time directories found in {root}")

    return max(numeric_directories, key=lambda item: item[0])[1]


def _read_xy(path: Path) -> np.ndarray:
    data = np.loadtxt(path, comments="#", ndmin=2)
    if data.size == 0:
        raise ValueError(f"The sample file is empty: {path}")
    return data


def load_sample_line(time_directory: str | Path, line_name: str) -> SampleLine:
    """Load one OpenFOAM raw-format sampled line."""
    directory = Path(time_directory)

    # Normal v2312 output for fields (U p): s Ux Uy Uz p
    combined_candidates = [
        (directory / f"{line_name}_U_p.xy", "U_p"),
        (directory / f"{line_name}_p_U.xy", "p_U"),
    ]
    for path, order in combined_candidates:
        if not path.exists():
            continue
        data = _read_xy(path)
        if data.shape[1] < 5:
            raise ValueError(f"Expected at least 5 columns in {path}; found {data.shape[1]}")
        if order == "U_p":
            return SampleLine(data[:, 0], data[:, 1], data[:, 2], data[:, 3], data[:, 4])
        return SampleLine(data[:, 0], data[:, 2], data[:, 3], data[:, 4], data[:, 1])

    # Some installations/writers produce one file per field.
    u_path = directory / f"{line_name}_U.xy"
    p_path = directory / f"{line_name}_p.xy"
    if u_path.exists() and p_path.exists():
        u_data = _read_xy(u_path)
        p_data = _read_xy(p_path)
        if u_data.shape[1] < 4 or p_data.shape[1] < 2:
            raise ValueError("Unexpected column count in separate U or p sample file")
        pressure = np.interp(u_data[:, 0], p_data[:, 0], p_data[:, 1])
        return SampleLine(u_data[:, 0], u_data[:, 1], u_data[:, 2], u_data[:, 3], pressure)

    available = ", ".join(path.name for path in sorted(directory.glob("*.xy"))) or "none"
    raise FileNotFoundError(
        f"Could not find samples for {line_name!r} in {directory}.\n"
        f"Available .xy files: {available}"
    )


def load_cavity_samples(case_directory: str | Path = ".") -> tuple[Path, SampleLine, SampleLine]:
    """Load both centre lines from the latest sampled time."""
    sample_root = Path(case_directory) / "postProcessing" / "sampleDict"
    time_directory = latest_time_directory(sample_root)
    vertical = load_sample_line(time_directory, "verticalCentreLine")
    horizontal = load_sample_line(time_directory, "horizontalCentreLine")
    return time_directory, vertical, horizontal


def plot_cavity_samples(
    vertical: SampleLine,
    horizontal: SampleLine,
    cavity_length: float = 0.1,
    title: str = "Cavity-flow centre-line samples",
) -> tuple[plt.Figure, np.ndarray]:
    """Plot U components, speed and p on both cavity centre lines."""
    # sampleDict starts 1 mm inside each wall, so restore the physical coordinate.
    y_over_h = (vertical.distance + 0.001) / cavity_length
    x_over_l = (horizontal.distance + 0.001) / cavity_length

    fig, axes = plt.subplots(2, 2, figsize=(11, 8), constrained_layout=True)

    axes[0, 0].plot(vertical.Ux, y_over_h, label=r"$U_x$")
    axes[0, 0].plot(vertical.Uy, y_over_h, label=r"$U_y$")
    axes[0, 0].plot(vertical.speed, y_over_h, "--", label=r"$|U|$")
    axes[0, 0].set(xlabel="Velocity [m/s]", ylabel=r"$y/H$", title="Vertical centre line")

    axes[0, 1].plot(vertical.p, y_over_h, color="#b45309")
    axes[0, 1].set(xlabel=r"Kinematic pressure $p$ [m$^2$/s$^2$]", ylabel=r"$y/H$", title="Vertical pressure")

    axes[1, 0].plot(x_over_l, horizontal.Ux, label=r"$U_x$")
    axes[1, 0].plot(x_over_l, horizontal.Uy, label=r"$U_y$")
    axes[1, 0].plot(x_over_l, horizontal.speed, "--", label=r"$|U|$")
    axes[1, 0].set(xlabel=r"$x/L$", ylabel="Velocity [m/s]", title="Horizontal centre line")

    axes[1, 1].plot(x_over_l, horizontal.p, color="#b45309")
    axes[1, 1].set(xlabel=r"$x/L$", ylabel=r"Kinematic pressure $p$ [m$^2$/s$^2$]", title="Horizontal pressure")

    for axis in axes.flat:
        axis.grid(True, alpha=0.25)
    axes[0, 0].legend()
    axes[1, 0].legend()
    fig.suptitle(title, fontsize=15)
    return fig, axes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", nargs="?", default=".", help="OpenFOAM case directory")
    parser.add_argument("--length", type=float, default=0.1, help="Cavity side length in metres")
    parser.add_argument("--output", default="cavity_profiles.png", help="Output PNG filename")
    parser.add_argument("--show", action="store_true", help="Display the plot interactively")
    args = parser.parse_args()

    time_directory, vertical, horizontal = load_cavity_samples(args.case)
    print(f"Loaded samples from: {time_directory}")
    fig, _ = plot_cavity_samples(
        vertical,
        horizontal,
        cavity_length=args.length,
        title=f"Cavity-flow centre lines — time {time_directory.name}",
    )
    fig.savefig(args.output, dpi=200, bbox_inches="tight")
    print(f"Saved plot: {Path(args.output).resolve()}")
    if args.show:
        plt.show()


if __name__ == "__main__":
    main()
