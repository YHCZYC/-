"""第2章 1、分析的基础范式 - RFM模型

迁移自: 1-2RFM模型-参考.xlsx

RFM模型通过三个维度衡量用户价值:
- R (Recency): 最近一次消费时间
- F (Frequency): 消费频次
- M (Monetary): 消费金额

根据R/F/M的高低组合, 将用户分为8类:
- 重要价值用户(R高F高M高)
- 重要发展用户(R高F高M低)
- 重要保持用户(R高F低M高)
- 重要挽留用户(R高F低M低)
- 一般价值用户(R低F高M高)
- 一般发展用户(R低F高M低)
- 一般保持用户(R低F低M高)
- 一般挽留用户(R低F低M低)
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import save_df, save_fig
from paths import chapter


def load_data():
    """加载原始销售数据"""
    xlsx = chapter(2) / "1、分析的基础范式" / "data-有答案" / "1-2RFM模型-参考.xlsx"
    raw = pd.read_excel(xlsx, sheet_name="原始数据", engine="openpyxl")
    # 清理空列
    raw = raw.dropna(axis=1, how="all")
    raw["销售日期"] = pd.to_datetime(raw["销售日期"])
    return raw


def calculate_rfm(raw: pd.DataFrame):
    """计算RFM指标并分类"""
    # 分析时点: 数据中最大日期 + 1天
    analysis_date = raw["销售日期"].max() + pd.Timedelta(days=1)

    # 按用户聚合
    user_rfm = (
        raw.groupby("用户编号")
        .agg(
            最近一次消费日期=("销售日期", "max"),
            消费频次=("销售日期", "count"),
            消费金额=("销售金额", "sum"),
        )
        .reset_index()
    )

    # 计算R: 距离分析时点的天数
    user_rfm["消费时间间隔"] = (
        analysis_date - user_rfm["最近一次消费日期"]
    ).dt.days

    # 计算R/F/M的均值作为分界线
    r_mean = user_rfm["消费时间间隔"].mean()
    f_mean = user_rfm["消费频次"].mean()
    m_mean = user_rfm["消费金额"].mean()

    # 注意: R是反向指标(越小越好), 所以R高=消费时间间隔<均值
    user_rfm["R程度"] = user_rfm["消费时间间隔"].apply(
        lambda x: "高" if x < r_mean else "低"
    )
    user_rfm["F程度"] = user_rfm["消费频次"].apply(
        lambda x: "高" if x >= f_mean else "低"
    )
    user_rfm["M程度"] = user_rfm["消费金额"].apply(
        lambda x: "高" if x >= m_mean else "低"
    )

    # 用户分类
    def classify_user(row):
        r, f, m = row["R程度"], row["F程度"], row["M程度"]
        if r == "高" and f == "高" and m == "高":
            return "重要价值用户"
        elif r == "高" and f == "高" and m == "低":
            return "重要发展用户"
        elif r == "高" and f == "低" and m == "高":
            return "重要保持用户"
        elif r == "高" and f == "低" and m == "低":
            return "重要挽留用户"
        elif r == "低" and f == "高" and m == "高":
            return "一般价值用户"
        elif r == "低" and f == "高" and m == "低":
            return "一般发展用户"
        elif r == "低" and f == "低" and m == "高":
            return "一般保持用户"
        else:  # r低 f低 m低
            return "一般挽留用户"

    user_rfm["用户类别"] = user_rfm.apply(classify_user, axis=1)

    return user_rfm, r_mean, f_mean, m_mean, analysis_date


def visualize_rfm(user_rfm, analysis_date):
    """可视化RFM分析结果"""
    # 1. 用户类别分布
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # 左图: 用户类别数量
    category_counts = user_rfm["用户类别"].value_counts()
    colors = plt.cm.Set3(range(len(category_counts)))
    axes[0].barh(category_counts.index, category_counts.values, color=colors)
    axes[0].set_xlabel("用户数量")
    axes[0].set_title("RFM用户类别分布", fontweight="bold")
    for i, v in enumerate(category_counts.values):
        axes[0].text(v + v * 0.01, i, str(v), va="center", fontsize=9)

    # 右图: 各类别消费金额占比
    category_amount = (
        user_rfm.groupby("用户类别")["消费金额"].sum().sort_values(ascending=False)
    )
    category_amount_pct = category_amount / category_amount.sum() * 100
    axes[1].barh(category_amount_pct.index, category_amount_pct.values, color=colors)
    axes[1].set_xlabel("消费金额占比 (%)")
    axes[1].set_title("各类别消费金额贡献", fontweight="bold")
    for i, v in enumerate(category_amount_pct.values):
        axes[1].text(v + v * 0.01, i, f"{v:.1f}%", va="center", fontsize=9)

    plt.tight_layout()
    save_fig(fig, "ch02/rfm_user_distribution.png")
    plt.close(fig)

    # 2. 3D散点图: R/F/M
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")

    category_colors = {
        "重要价值用户": "#FF6B6B",
        "重要发展用户": "#4ECDC4",
        "重要保持用户": "#45B7D1",
        "重要挽留用户": "#FFA07A",
        "一般价值用户": "#98D8C8",
        "一般发展用户": "#F7DC6F",
        "一般保持用户": "#BB8FCE",
        "一般挽留用户": "#85C1E2",
    }

    for category, color in category_colors.items():
        subset = user_rfm[user_rfm["用户类别"] == category]
        if len(subset) > 0:
            ax.scatter(
                subset["消费时间间隔"],
                subset["消费频次"],
                subset["消费金额"],
                c=color,
                label=category,
                alpha=0.6,
                s=20,
            )

    ax.set_xlabel("消费时间间隔(天) - R")
    ax.set_ylabel("消费频次 - F")
    ax.set_zlabel("消费金额 - M")
    ax.set_title("RFM三维分布", fontweight="bold")
    ax.legend(loc="upper left", fontsize=8)

    save_fig(fig, "ch02/rfm_3d_scatter.png")
    plt.close(fig)


def main():
    print("=" * 60)
    print("2.2 RFM模型分析")
    print("=" * 60)

    raw = load_data()
    print(f"\n原始数据: {raw.shape}")
    print(f"  用户数: {raw['用户编号'].nunique()}")
    print(f"  时间跨度: {raw['销售日期'].min()} ~ {raw['销售日期'].max()}")

    user_rfm, r_mean, f_mean, m_mean, analysis_date = calculate_rfm(raw)

    print(f"\n分析时点: {analysis_date.date()}")
    print(f"R均值(消费时间间隔): {r_mean:.2f} 天")
    print(f"F均值(消费频次): {f_mean:.2f} 次")
    print(f"M均值(消费金额): {m_mean:.2f} 元")

    print(f"\n用户RFM汇总: {user_rfm.shape}")
    print(user_rfm.head(10).to_string(index=False))

    # 保存结果
    save_df(user_rfm, "ch02/rfm_user_classification.csv")

    # 用户类别统计
    print("\n" + "=" * 60)
    print("用户类别分布:")
    category_stats = (
        user_rfm.groupby("用户类别")
        .agg(
            用户数=("用户编号", "count"),
            平均消费金额=("消费金额", "mean"),
            总消费金额=("消费金额", "sum"),
        )
        .sort_values("总消费金额", ascending=False)
    )
    category_stats["金额占比"] = (
        category_stats["总消费金额"] / category_stats["总消费金额"].sum() * 100
    )
    print(category_stats.to_string())
    print("=" * 60)

    # 可视化
    visualize_rfm(user_rfm, analysis_date)


if __name__ == "__main__":
    from common import run_main

    sys.exit(run_main(main))
