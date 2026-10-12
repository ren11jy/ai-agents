"""蒲丰投针实验：随机投针、统计相交比例，并写出真实的 CSV 结果。

本模块可被 import：import 时不启动实验、不写文件。
直接运行写入当前工作目录的 results.csv：

    uv run --locked python experiment.py
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from pathlib import Path


DEFAULT_LENGTH = 0.5
DEFAULT_SPACING = 1.0
DEFAULT_SEED = 42
DEFAULT_SIZES = (1000, 10000, 100000)
CSV_FIELDS = (
    "seed", "n", "crossings", "pi_estimate", "needle_length", "line_spacing"
)


def _validate_geometry(length: float, spacing: float) -> None:
    """检查几何参数，非法值直接报错，不静默修改。"""

    if not math.isfinite(length) or not math.isfinite(spacing):
        raise ValueError("length 和 spacing 必须是有限数值")
    if spacing <= 0:
        raise ValueError("spacing 必须大于 0")
    if length <= 0:
        raise ValueError("length 必须大于 0")
    if length > spacing:
        raise ValueError("要求 0 < length <= spacing")


def crosses_line(
    distance: float,
    angle: float,
    length: float = DEFAULT_LENGTH,
    spacing: float = DEFAULT_SPACING,
) -> bool:
    """判断一根针是否与平行线相交（接触到线也算相交）。

    输入范围：0 <= distance <= spacing/2，0 <= angle <= pi/2。
    相交判据：distance <= (length / 2) * sin(angle)。
    """

    _validate_geometry(length, spacing)
    if not math.isfinite(distance) or not math.isfinite(angle):
        raise ValueError("distance 和 angle 必须是有限数值")
    if not 0.0 <= distance <= spacing / 2:
        raise ValueError("distance 必须落在 [0, spacing/2]")
    if not 0.0 <= angle <= math.pi / 2:
        raise ValueError("angle 必须落在 [0, pi/2]")
    return distance <= (length / 2) * math.sin(angle)


def estimate_pi(
    n: int,
    crossings: int,
    length: float = DEFAULT_LENGTH,
    spacing: float = DEFAULT_SPACING,
) -> float:
    """由投针总数与相交数估计圆周率：2 * length * n / (spacing * crossings)。"""

    _validate_geometry(length, spacing)
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise ValueError("n 必须是正整数")
    if isinstance(crossings, bool) or not isinstance(crossings, int):
        raise ValueError("crossings 必须是整数")
    if crossings <= 0:
        raise ValueError("crossings 必须为正；相交数为 0 时无法估计")
    if crossings > n:
        raise ValueError("crossings 不能超过 n")
    return 2 * length * n / (spacing * crossings)


def simulate(
    n: int,
    seed: int = DEFAULT_SEED,
    length: float = DEFAULT_LENGTH,
    spacing: float = DEFAULT_SPACING,
) -> dict:
    """投 n 根针，返回本次实际结果。

    每次调用在循环外初始化随机数生成器一次，循环内持续取样；
    不会在每一次投针时重设 seed。
    """

    _validate_geometry(length, spacing)
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise ValueError("n 必须是正整数")

    rng = random.Random(seed)
    half_spacing = spacing / 2
    half_pi = math.pi / 2
    crossings = 0
    for _ in range(n):
        distance = rng.uniform(0.0, half_spacing)
        angle = rng.uniform(0.0, half_pi)
        if crosses_line(distance, angle, length=length, spacing=spacing):
            crossings += 1

    if crossings == 0:
        raise ValueError("本次模拟没有针接触到线，无法用公式估计圆周率")

    return {
        "seed": seed,
        "n": n,
        "crossings": crossings,
        "pi_estimate": estimate_pi(n, crossings, length=length, spacing=spacing),
        "needle_length": length,
        "line_spacing": spacing,
    }


def run_experiments(
    sizes: tuple[int, ...],
    seed: int,
    length: float,
    spacing: float,
    output_path: Path,
) -> list[dict]:
    """依次运行每个投针数，把真实结果写入 CSV。"""

    rows: list[dict] = []
    for n in sizes:
        result = simulate(n, seed=seed, length=length, spacing=spacing)
        rows.append(result)
        print(
            f"n={result['n']}: crossings={result['crossings']}, "
            f"pi_estimate={result['pi_estimate']:.6f}"
        )

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in CSV_FIELDS})
    print(f"已写入 {output_path}")
    return rows


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="用蒲丰投针估计圆周率，并把真实结果写入 results.csv",
    )
    parser.add_argument(
        "--seed", type=int, default=DEFAULT_SEED, help="每组实验的随机种子",
    )
    parser.add_argument(
        "--n",
        type=int,
        action="append",
        dest="sizes",
        metavar="N",
        help="投针数；可重复传入以增加组数，默认 1000/10000/100000",
    )
    parser.add_argument(
        "--length", type=float, default=DEFAULT_LENGTH, help="针长 L",
    )
    parser.add_argument(
        "--spacing", type=float, default=DEFAULT_SPACING, help="平行线间距 d",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    sizes = tuple(args.sizes) if args.sizes else DEFAULT_SIZES
    run_experiments(
        sizes,
        seed=args.seed,
        length=args.length,
        spacing=args.spacing,
        output_path=Path("results.csv"),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
