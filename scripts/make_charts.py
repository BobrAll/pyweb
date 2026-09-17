import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parent.parent

x = np.linspace(0, 10, 100)
y1 = np.exp(-x / 5) * np.cos(x)
y2 = np.exp(-x / 8) * np.cos(x) * 0.7

fig, ax = plt.subplots(figsize=(7, 4), dpi=150)
ax.plot(x, y1, label=r"$\exp(-x/5)\cos x$")
ax.plot(x, y2, label=r"$0.7\,\exp(-x/8)\cos x$")
ax.set_xlabel("Время, с")
ax.set_ylabel("Амплитуда")
ax.set_title("Затухающие колебания (matplotlib)")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()

for dest in [ROOT / "docs" / "report" / "images", ROOT / "sphinx" / "stress"]:
    dest.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest / "static-chart.png")

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=x, y=y1, mode="lines", name="серия 1"))
fig2.add_trace(go.Scatter(x=x, y=y2, mode="lines", name="серия 2"))
fig2.update_layout(
    title="Интерактивный график (Plotly)",
    xaxis_title="Время, с",
    yaxis_title="Амплитуда",
    width=720,
    height=420,
)

plotly_html = fig2.to_html(full_html=False, include_plotlyjs="cdn")
plotly_dir = ROOT / "sphinx" / "_static"
plotly_dir.mkdir(parents=True, exist_ok=True)
(ROOT / "docs" / "stress" / "plotly.html").write_text(plotly_html)
(plotly_dir / "plotly.html").write_text(plotly_html)
