"""Path configuration for CDA textbook Python migration.

All source data lives in the read-only textbook folder. Outputs go to
``output/`` relative to this file.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
TEXTBOOK_ROOT = Path(r"E:\BaiduNetdiskDownload\1《CDA 一级认证教材：商业数据分析》")
OUTPUT_ROOT = PROJECT_ROOT / "output"
OUTPUT_ROOT.mkdir(exist_ok=True)


def chapter(n: int) -> Path:
    """Return the textbook folder for chapter *n*."""
    for p in TEXTBOOK_ROOT.iterdir():
        if p.is_dir() and p.name.startswith(f"第{n}章"):
            return p
    raise FileNotFoundError(f"Chapter {n} folder not found under {TEXTBOOK_ROOT}")
