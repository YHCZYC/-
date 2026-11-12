"""第2章 1、分析的基础范式 - 波士顿矩阵(BCG Matrix)

迁移自: 1-1波士顿矩阵-参考.xlsx

波士顿矩阵通过"市场占有率"和"增长率"两个维度将产品/品牌分为四类:
- 明星(Star): 高占有率 + 高增长
- 现金牛(Cash Cow): 高占有率 + 低增长
- 问题(Query Mark): 低占有率 + 高增长
- 瘦狗(Dog): 低占有率 + 低增长
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import save_df, save_fig
from paths import chapter


def load_data():
    """加载销售数据"""
    xlsx = chapter(2) / "1、分析的基础范式" / "data-有答案" / "1-1波士顿矩阵-参考.xlsx"
    sales = pd.read_excel(xlsx, sheet_name="销售表", engine="openpyxl")
    sales["销售日期"] = pd.to_datetime(sales["销售日期"])
    sales["月份"] = sales["销售日期"].dt.to_period("M")
    return sales


def calculate_bcg_metrics(sales: pd.DataFrame):
    """计算波士顿矩阵指标: 市场占有率、增长率"""
    # 1. 计算每个品牌每月的销售额
    brand_month = (
        sales.groupby(["品牌", "月份"])["订单金额"].sum().reset_index(name="销售额")
    )

    # 2. 计算每月总市场销售额
    monthly_total = (
        sales.groupby("月份")["订单金额"].sum().reset_index(name="月度总额")
    )

    # 3. 合并并计算市场占有率
    brand_month = brand_month.merge(monthly_total, on="月份")
    brand_month["市场占有率"] = brand_month["销售额"] / brand_month["月度总额"]

    # 4. 计算环比增长率(相比上月)
    brand_month = brand_month.sort_values(["品牌", "月份"])
    brand_month["上月销售额"] = brand_month.groupby("品牌")["销售额"].shift(1)
    brand_month["环比增长率"] = (
        brand_month["销售额"] - brand_month["上月销售额"]
    ) / brand_month["上月销售额"]

    # 5. 汇总每个品牌的平均市场占有率和平均增长率
    brand_summary = (
        brand_month.groupby("品牌")
        .agg(平均市场占有率=("市场占有率", "mean"), 平均增长率=("环比增长率", "mean"))
        .reset_index()
    )

    # 6. 计算市场平均占有率(用于划分高低)
    avg_share = brand_summary["平均市场占有率"].mean()
    avg_growth = brand_summary["平均增长率"].mean()

    # 7. 分类: 明星/现金牛/问题/瘦狗
    def classify(row):
        high_share = row["平均市场占有率"] >= avg_share
        high_growth = row["平均增长率"] >= avg_growth
        if high_share and high_growth:
            return "明星(Star)"
        elif high_share and not high_growth:
            return "现金牛(Cash Cow)"
        elif not high_share and high_growth:
            return "问题(Query Mark)"
        else:
            return "瘦狗(Dog)"

    brand_summary["分类"] = brand_summary.apply(classify, axis=1)

    return brand_summary, avg_share, avg_growth, brand_month


def visualize_bcg(brand_summary, avg_share, avg_growth):
    """绘制波士顿矩阵图"""
    fig, ax = plt.subplots(figsize=(12, 10))

    # 颜色映射
    colors = {
        "明星(Star)": "#FF6B6B",
        "现金牛(Cash Cow)": "#4ECDC4",
        "问题(Query Mark)": "#FFE66D",
        "瘦狗(Dog)": "#95E1D3",
    }

    # 绘制散点
    for category, color in colors.items():
        subset = brand_summary[brand_summary["分类"] == category]
        ax.scatter(
            subset["平均市场占有率"],
            subset["平均增长率"],
            s=subset["平均市场占有率"] * 2000,
            c=color,
            alpha=0.6,
            label=category,
            edgecolors="black",
            linewidth=1,
        )
        # 标注品牌名
        for _, row in subset.iterrows():
            ax.annotate(
                row["品牌"],
                (row["平均市场占有率"], row["平均增长率"]),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=9,
                fontweight="bold",
            )

    # 绘制分界线
    ax.axvline(avg_share, color="gray", linestyle="--", linewidth=1, alpha=0.5)
    ax.axhline(avg_growth, color="gray", linestyle="--", linewidth=1, alpha=0.5)

    # 添加象限标签
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    ax.text(
        (avg_share + xlim[1]) / 2,
        (avg_growth + ylim[1]) / 2,
        "明星\n(Star)",
        ha="center",
        va="center",
        fontsize=14,
        color="#FF6B6B",
        fontweight="bold",
        alpha=0.3,
    )
    ax.text(
        (xlim[0] + avg_share) / 2,
        (avg_growth + ylim[1]) / 2,
        "问题\n(Query Mark)",
        ha="center",
        va="center",
        fontsize=14,
        color="#FFE66D",
        fontweight="bold",
        alpha=0.3,
    )
    ax.text(
        (avg_share + xlim[1]) / 2,
        (ylim[0] + avg_growth) / 2,
        "现金牛\n(Cash Cow)",
        ha="center",
        va="center",
        fontsize=14,
        color="#4ECDC4",
        fontweight="bold",
        alpha=0.3,
    )
    ax.text(
        (xlim[0] + avg_share) / 2,
        (ylim[0] + avg_growth) / 2,
        "瘦狗\n(Dog)",
        ha="center",
        va="center",
        fontsize=14,
        color="#95E1D3",
        fontweight="bold",
        alpha=0.3,
    )

    ax.set_xlabel("平均市场占有率", fontsize=12)
    ax.set_ylabel("平均环比增长率", fontsize=12)
    ax.set_title("波士顿矩阵(BCG Matrix)分析", fontsize=14, fontweight="bold")
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    save_fig(fig, "ch02/bcg_matrix.png")
    plt.close(fig)


def main():
    print("=" * 60)
    print("2.1 波士顿矩阵(BCG Matrix)分析")
    print("=" * 60)

    sales = load_data()
    print(f"\n销售数据: {sales.shape}")
    print(f"  品牌数: {sales['品牌'].nunique()}")
    print(f"  时间跨度: {sales['月份'].min()} ~ {sales['月份'].max()}")

    brand_summary, avg_share, avg_growth, brand_month = calculate_bcg_metrics(sales)

    print(f"\n市场基准:")
    print(f"  平均市场占有率: {avg_share:.4f}")
    print(f"  平均环比增长率: {avg_growth:.4f}")

    print(f"\n品牌分类结果:")
    print(brand_summary.to_string(index=False))

    # 保存结果
    save_df(brand_summary, "ch02/bcg_brand_summary.csv")
    save_df(brand_month, "ch02/bcg_brand_monthly_detail.csv")

    # 可视化
    visualize_bcg(brand_summary, avg_share, avg_growth)

    # 输出各分类的品牌
    print("\n" + "=" * 60)
    print("分类汇总:")
    for cat in ["明星(Star)", "现金牛(Cash Cow)", "问题(Query Mark)", "瘦狗(Dog)"]:
        brands = brand_summary[brand_summary["分类"] == cat]["品牌"].tolist()
        print(f"  {cat:20s}: {', '.join(brands) if brands else '无'}")
    print("=" * 60)


if __name__ == "__main__":
    from common import run_main

    sys.exit(run_main(main))
