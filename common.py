"""Shared helpers used across chapter scripts."""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial"]
matplotlib.rcParams["axes.unicode_minus"] = False

# The textbook CSVs are GBK-encoded.
GBK_CSV = {"encoding": "gbk"}


def save_fig(fig, rel: str) -> Path:
    """Save *fig* under ``output/`` and return the path."""
    from paths import OUTPUT_ROOT

    out = OUTPUT_ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"  -> saved {out}")
    return out


def save_df(df: pd.DataFrame, rel: str) -> Path:
    from paths import OUTPUT_ROOT

    out = OUTPUT_ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    if rel.endswith(".csv"):
        df.to_csv(out, index=False, encoding="utf-8-sig")
    else:
        df.to_excel(out, index=False)
    print(f"  -> saved {out}")
    return out


def show() -> None:
    plt.show(block=False)
    plt.pause(0.1)


def run_main(main) -> int:
    """Entry-point wrapper: catch exceptions, print a clean trace."""
    try:
        main()
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1
    return 0
