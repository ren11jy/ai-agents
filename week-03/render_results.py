"""读取真实的 results.csv，生成参数说明、LaTeX 表格与静态图。

不重新投针、不编造结果；所有输出都来自同一份 CSV。

    uv run --locked python render_results.py
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


CSV_NAME = "results.csv"
TABLE_NAME = "results-table.tex"
PARAMS_NAME = "results-params.tex"
FIGURE_NAME = "results.png"


def read_results(path: Path) -> list[dict]:
    """读取 CSV 中的实际参数与结果；文件缺失或为空时明确报错。"""

    if not path.exists():
        raise SystemExit(f"找不到 {path.name}，请先运行 experiment.py")

    rows: list[dict] = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for raw in reader:
            rows.append(
                {
                    "seed": int(raw["seed"]),
                    "n": int(raw["n"]),
                    "crossings": int(raw["crossings"]),
                    "pi_estimate": float(raw["pi_estimate"]),
                    "needle_length": float(raw["needle_length"]),
                    "line_spacing": float(raw["line_spacing"]),
                }
            )
    if not rows:
        raise SystemExit(f"{path.name} 没有数据行，请先运行 experiment.py")
    return rows


def write_table(rows: list[dict], path: Path) -> None:
    lines = [
        r"\begin{tabular}{rrr}",
        r"\toprule",
        r"投针数 $N$ & 相交数 $K$ & 估计 $\widehat{\pi}$ \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(
            f"{row['n']} & {row['crossings']} & {row['pi_estimate']:.4f} \\\\"
        )
    lines += [r"\bottomrule", r"\end{tabular}"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_params(rows: list[dict], path: Path) -> None:
    seed = rows[0]["seed"]
    sizes = "、".join(str(row["n"]) for row in rows)
    length = rows[0]["needle_length"]
    spacing = rows[0]["line_spacing"]
    text = (
        f"本次实验随机种子为 {seed}，投针数为 {sizes}；"
        f"针长 $L={length:g}$，线间距 $d={spacing:g}$。"
        "以下表格与图均来自同一次模拟的 \\texttt{results.csv}。"
    )
    path.write_text(text + "\n", encoding="utf-8")


def write_figure(rows: list[dict], path: Path) -> None:
    sizes = [row["n"] for row in rows]
    estimates = [row["pi_estimate"] for row in rows]

    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ax.axhline(math.pi, color="gray", linestyle="--", linewidth=1.0, label="pi")
    ax.plot(sizes, estimates, marker="o", color="tab:blue", label="estimate")
    ax.set_xscale("log")
    ax.set_xlabel("number of needles n")
    ax.set_ylabel("pi estimate")
    ax.set_title("Buffon's needle: estimate vs n")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> int:
    directory = Path(".")
    rows = read_results(directory / CSV_NAME)
    write_table(rows, directory / TABLE_NAME)
    write_params(rows, directory / PARAMS_NAME)
    write_figure(rows, directory / FIGURE_NAME)
    print(f"已由 {CSV_NAME} 生成 {TABLE_NAME}、{PARAMS_NAME}、{FIGURE_NAME}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
