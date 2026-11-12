"""第2章 1、分析的基础范式 - 漏斗图与相关分析

迁移自: 2-1漏斗图-参考.xlsx, 3-1相关分析-参考.xlsx

漏斗图: 展示销售流程各阶段的用户转化情况
相关分析: 研究两个变量之间的线性关系
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import save_df, save_fig
from paths import chapter


def funnel_analysis():
    """销售漏斗分析"""
    print("=" * 60)
    print("2.5 漏斗图分析")
    print("=" * 60)

    # 数据
    data = {
        "阶段": ["潜在", "接触", "意向", "明确", "谈判", "成交"],
        "用户数": [100, 90, 80, 70, 60, 50],
    }
    df = pd.DataFrame(data)

    # 计算转化率
    df["转化率"] = df["用户数"] / df["用户数"].shift(1)
    df["转化率"].iloc[0] = 1.0  # 第一阶段转化率为100%
    df["总体转化率"] = df["用户数"] / df["用户数"].iloc[0]

    print("\n销售漏斗数据:")
    print(df.to_string(index=False))

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 8))

    # 绘制漏斗
    colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(df)))
    y_pos = np.arange(len(df))

    # 漏斗宽度按比例
    widths = df["用户数"] / df["用户数"].max() * 0.8

    for i, (idx, row) in enumerate(df.iterrows()):
        width = widths[i]
        left = 0.5 - width / 2
        right = 0.5 + width / 2
        bottom = i
        top = i + 0.9

        # 绘制梯形
        polygon = plt.Polygon(
            [[left, bottom], [right, bottom], [right - 0.02, top], [left + 0.02, top]],
            facecolor=colors[i],
            edgecolor="black",
            linewidth=1.5,
        )
        ax.add_patch(polygon)

        # 标注文字
        ax.text(
            0.5,
            i + 0.45,
            f"{row['阶段']}\n{row['用户数']}人\n转化率: {row['转化率']:.1%}",
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold",
        )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(df))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("销售漏斗分析", fontsize=14, fontweight="bold", pad=20)

    plt.tight_layout()
    save_fig(fig, "ch02/funnel_chart.png")
    plt.close(fig)

    # 保存结果
    save_df(df, "ch02/funnel_analysis.csv")

    return df


def correlation_analysis():
    """相关分析"""
    print("\n" + "=" * 60)
    print("2.6 相关分析")
    print("=" * 60)

    # 加载数据
    xlsx = chapter(2) / "1、分析的基础范式" / "data-有答案" / "3-1相关分析-参考.xlsx"
    data = pd.read_excel(xlsx, sheet_name="原始数据", engine="openpyxl")

    print(f"\n数据规模: {data.shape}")
    print(f"变量: x, y")
    print(data.describe().to_string())

    # 计算相关系数
    correlation, p_value = stats.pearsonr(data["x"], data["y"])
    print(f"\nPearson相关系数: {correlation:.4f}")
    print(f"P值: {p_value:.6f}")

    # 线性回归
    slope, intercept, r_value, p_value_reg, std_err = stats.linregress(
        data["x"], data["y"]
    )
    print(f"\n线性回归:")
    print(f"  斜率: {slope:.4f}")
    print(f"  截距: {intercept:.4f}")
    print(f"  R2: {r_value**2:.4f}")

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 7))

    # 散点图
    ax.scatter(data["x"], data["y"], alpha=0.6, s=50, color="steelblue", label="数据点")

    # 回归线
    x_line = np.linspace(data["x"].min(), data["x"].max(), 100)
    y_line = slope * x_line + intercept
    ax.plot(x_line, y_line, color="red", linewidth=2, label=f"回归线: y={slope:.2f}x+{intercept:.2f}")

    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("y", fontsize=12)
    ax.set_title(f"相关分析 (r={correlation:.3f}, p={p_value:.4f})", fontsize=14, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    # 添加统计信息
    textstr = f"Pearson r = {correlation:.4f}\nP-value = {p_value:.6f}\nR2 = {r_value**2:.4f}"
    props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)
    ax.text(
        0.05,
        0.95,
        textstr,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=props,
    )

    plt.tight_layout()
    save_fig(fig, "ch02/correlation_analysis.png")
    plt.close(fig)

    # 保存结果
    result = pd.DataFrame(
        {
            "指标": ["Pearson相关系数", "P值", "R²", "斜率", "截距"],
            "值": [correlation, p_value, r_value**2, slope, intercept],
        }
    )
    save_df(result, "ch02/correlation_statistics.csv")

    return result


def main():
    funnel_analysis()
    correlation_analysis()
    print("\n" + "=" * 60)
    print("漏斗图与相关分析完成!")
    print("=" * 60)


if __name__ == "__main__":
    from common import run_main

    sys.exit(run_main(main))
