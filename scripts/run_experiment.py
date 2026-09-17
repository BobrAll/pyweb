import hashlib
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "experiment.csv"
CACHE_DIR = ROOT / ".build" / "experiment"
OUT_DATA_DIR = ROOT / "docs" / "_data"
OUT_IMG_DIR = ROOT / "docs" / "experiments" / "images"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def git_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        return out.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return "unknown"


def load_data() -> tuple[np.ndarray, np.ndarray]:
    raw = np.genfromtxt(DATA_PATH, delimiter=",", names=True)
    return raw["t"], raw["amplitude"]


def fit_decay(t: np.ndarray, y: np.ndarray) -> dict:
    slope, intercept = np.polyfit(t, np.log(y), 1)
    tau = -1.0 / slope
    a = float(np.exp(np.log(y) - slope * t).mean())
    ln_fit = np.log(a) - t / tau
    ln_y = np.log(y)
    ss_res = float(np.sum((ln_y - ln_fit) ** 2))
    ss_tot = float(np.sum((ln_y - ln_y.mean()) ** 2))
    return {
        "A": round(a, 4),
        "tau": round(tau, 4),
        "r2": round(1 - ss_res / ss_tot, 4),
        "residual_std": round(float(np.std(ln_y - ln_fit)), 4),
    }


def render_outputs(t: np.ndarray, y: np.ndarray, fit: dict) -> str:
    t_fit = np.linspace(t.min(), t.max(), 200)
    model = fit["A"] * np.exp(-t_fit / fit["tau"])

    fig, ax = plt.subplots(figsize=(7, 4), dpi=150)
    ax.scatter(t, y, s=28, color="tab:blue", label="измерения", zorder=3)
    ax.plot(t_fit, model, color="tab:red", label=f"модель, tau = {fit['tau']:.2f} с")
    ax.set_xlabel("Время, с")
    ax.set_ylabel("Амплитуда")
    ax.set_title("Экспериментальная кривая и подгонка")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_IMG_DIR / "exp-static.png")
    plt.close(fig)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=t, y=y, mode="markers", name="измерения"))
    fig2.add_trace(go.Scatter(x=t_fit, y=model, mode="lines", name="модель"))
    fig2.update_layout(
        title="Экспериментальная кривая (Plotly)",
        xaxis_title="Время, с",
        yaxis_title="Амплитуда",
        width=720,
        height=420,
    )
    (OUT_IMG_DIR / "exp-plotly.html").write_text(
        fig2.to_html(full_html=False, include_plotlyjs="cdn")
    )

    result = {
        "A": fit["A"],
        "tau": fit["tau"],
        "r2": fit["r2"],
        "residual_std": fit["residual_std"],
        "n_points": int(t.size),
        "amplitude_start": round(float(y[0]), 4),
        "amplitude_end": round(float(y[-1]), 4),
        "points": [
            {"t": round(float(ti), 1), "amplitude": round(float(yi), 4)}
            for ti, yi in zip(t, y)
        ],
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


def main() -> None:
    started = time.perf_counter()
    data_sha = sha256_file(DATA_PATH)
    script_sha = sha256_file(Path(__file__))
    OUT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUT_IMG_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    manifest_path = CACHE_DIR / "manifest.json"
    manifest = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())

    prev_pipeline_path = OUT_DATA_DIR / "pipeline.json"
    prev_pipeline = {}
    if prev_pipeline_path.exists():
        prev_pipeline = json.loads(prev_pipeline_path.read_text())

    cached_files_exist = all(
        (CACHE_DIR / name).exists()
        for name in ("experiment.json", "exp-static.png", "exp-plotly.html")
    )
    cache_hit = (
        manifest.get("data_sha") == data_sha
        and manifest.get("script_sha") == script_sha
        and cached_files_exist
    )

    if cache_hit:
        (OUT_DATA_DIR / "experiment.json").write_text(
            (CACHE_DIR / "experiment.json").read_text()
        )
        (OUT_IMG_DIR / "exp-static.png").write_bytes(
            (CACHE_DIR / "exp-static.png").read_bytes()
        )
        (OUT_IMG_DIR / "exp-plotly.html").write_text(
            (CACHE_DIR / "exp-plotly.html").read_text()
        )
        elapsed = round(time.perf_counter() - started, 3)
        fresh_seconds = (
            manifest.get("fresh_seconds")
            or prev_pipeline.get("fresh_seconds")
            or elapsed
        )
        pipeline = {
            "last_run": "cached",
            "fresh_seconds": fresh_seconds,
            "cached_seconds": elapsed,
            "saved_percent": round(
                (fresh_seconds - elapsed) / fresh_seconds * 100, 1
            ) if fresh_seconds else None,
            "dataset_version": data_sha,
        }
        print(f"cache hit: results loaded in {elapsed} s")
    else:
        t, y = load_data()
        fit = fit_decay(t, y)
        experiment_json = render_outputs(t, y, fit)
        elapsed = round(time.perf_counter() - started, 3)
        (CACHE_DIR / "experiment.json").write_text(experiment_json)
        (OUT_DATA_DIR / "experiment.json").write_text(experiment_json)
        (CACHE_DIR / "exp-static.png").write_bytes(
            (OUT_IMG_DIR / "exp-static.png").read_bytes()
        )
        (CACHE_DIR / "exp-plotly.html").write_text(
            (OUT_IMG_DIR / "exp-plotly.html").read_text()
        )
        cached_seconds = (
            manifest.get("cached_seconds")
            or prev_pipeline.get("cached_seconds")
        )
        pipeline = {
            "last_run": "fresh",
            "fresh_seconds": elapsed,
            "cached_seconds": cached_seconds,
            "saved_percent": round(
                (elapsed - cached_seconds) / elapsed * 100, 1
            ) if cached_seconds else None,
            "dataset_version": data_sha,
        }
        print(f"cache miss: recomputed in {elapsed} s")

    manifest = {
        "data_sha": data_sha,
        "script_sha": script_sha,
        "fresh_seconds": pipeline["fresh_seconds"],
        "cached_seconds": pipeline["cached_seconds"],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2))
    (OUT_DATA_DIR / "pipeline.json").write_text(json.dumps(pipeline, indent=2))

    build_info = {
        "commit": git_commit(),
        "build_date": datetime.now(ZoneInfo("Europe/Moscow")).strftime(
            "%Y-%m-%d %H:%M МСК"
        ),
        "build_ts": datetime.now(ZoneInfo("Europe/Moscow")).isoformat(
            timespec="seconds"
        ),
        "dataset_version": data_sha,
        "dataset_file": "data/experiment.csv",
    }
    (OUT_DATA_DIR / "build_info.json").write_text(json.dumps(build_info, indent=2))


if __name__ == "__main__":
    main()
