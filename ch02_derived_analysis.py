"""第2章 2、由基础分析范式引申出的分析方法

迁移自: 趋势分析、对比分析、构成分析、分布分析、关系分析、桑基图

本脚本实现6种基础分析方法的可视化:
1. 趋势分析: 时间序列趋势
2. 对比分析: 类别对比
3. 构成分析: 占比构成
4. 分布分析: 数据分布特征
5. 关系分析: 变量关系
6. 桑基图: 流量转移
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import save_df, save_fig
from paths import chapter


def trend_analysis():
    """趋势分析"""
    print("=" * 60)
    print("2.2.1 趋势分析")
    print("=" * 60)

    xlsx = chapter(2) / "2、由基础分析范式引申出的分析方法" / "data-有答案" / "1趋势分析-参考.xlsx"
    df = pd.read_excel(xlsx, sheet_name="趋势图", engine="openpyxl", header=None)
    # 清理数据: 跳过前2行(空行和表头), 取第2、3列
    df = df.iloc[2:, 1:3].copy()
    df.columns = ["year", "订单量"]
    df = df.dropna()
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["订单量"] = pd.to_numeric(df["订单量"], errors="coerce")
    df = df.dropna()
    df["year"] = df["year"].astype(int)
    df["订单量"] = df["订单量"].astype(int)

    print(f"\n数据: {df.shape}")
    print(df.to_string(index=False))

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["year"], df["订单量"], marker="o", linewidth=2, markersize=8, color="steelblue")
    ax.fill_between(df["year"], df["订单量"], alpha=0.3, color="steelblue")

    for i, (year, val) in enumerate(zip(df["year"], df["订单量"])):
        ax.annotate(str(val), (year, val), textcoords="offset points", xytext=(0, 10), ha="center", fontsize=9)

    ax.set_xlabel("年份", fontsize=12)
    ax.set_ylabel("订单量", fontsize=12)
    ax.set_title("年度订单量趋势分析", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.set_xticks(df["year"])

    plt.tight_layout()
    save_fig(fig, "ch02/trend_analysis.png")
    plt.close(fig)

    save_df(df, "ch02/trend_data.csv")
    return df


def comparison_analysis():
    """对比分析"""
    print("\n" + "=" * 60)
    print("2.2.2 对比分析")
    print("=" * 60)

    xlsx = chapter(2) / "2、由基础分析范式引申出的分析方法" / "data-有答案" / "2对比分析-参考.xlsx"
    df = pd.read_excel(xlsx, sheet_name="对比分析", engine="openpyxl", header=None)
    df = df.iloc[2:, 1:3].copy()
    df.columns = ["产品类型", "订单量"]
    df = df.dropna()
    df["订单量"] = pd.to_numeric(df["订单量"], errors="coerce")
    df = df.dropna()
    df["订单量"] = df["订单量"].astype(int)

    print(f"\n数据: {df.shape}")
    print(df.to_string(index=False))

    # 可视化
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 左图: 柱状图
    colors = plt.cm.Set2(np.linspace(0, 1, len(df)))
    axes[0].bar(df["产品类型"], df["订单量"], color=colors, edgecolor="black", linewidth=1)
    axes[0].set_xlabel("产品类型", fontsize=12)
    axes[0].set_ylabel("订单量", fontsize=12)
    axes[0].set_title("各产品类型订单量对比", fontsize=14, fontweight="bold")
    axes[0].grid(True, alpha=0.3, axis="y")
    for i, v in enumerate(df["订单量"]):
        axes[0].text(i, v + v * 0.01, str(v), ha="center", fontsize=10)

    # 右图: 雷达图
    categories = df["产品类型"].tolist()
    values = df["订单量"].tolist()
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    values += values[:1]

    axes[1] = fig.add_subplot(122, polar=True)
    axes[1].plot(angles, values, "o-", linewidth=2, color="steelblue")
    axes[1].fill(angles, values, alpha=0.25, color="steelblue")
    axes[1].set_xticks(angles[:-1])
    axes[1].set_xticklabels(categories)
    axes[1].set_title("产品类型订单量雷达图", fontsize=14, fontweight="bold", pad=20)

    plt.tight_layout()
    save_fig(fig, "ch02/comparison_analysis.png")
    plt.close(fig)

    save_df(df, "ch02/comparison_data.csv")
    return df


def composition_analysis():
    """构成分析"""
    print("\n" + "=" * 60)
    print("2.2.3 构成分析")
    print("=" * 60)

    xlsx = chapter(2) / "2、由基础分析范式引申出的分析方法" / "data-有答案" / "4构成分析-参考.xlsx"
    df = pd.read_excel(xlsx, sheet_name="构成分析", engine="openpyxl", header=None)
    df = df.iloc[3:, 1:3].copy()
    df.columns = ["产品类型", "销售量"]
    df = df.dropna()
    df["销售量"] = pd.to_numeric(df["销售量"], errors="coerce")
    df = df.dropna()
    df["销售量"] = df["销售量"].astype(int)

    # 计算占比
    total = df["销售量"].sum()
    df["占比"] = df["销售量"] / total
    df["累计占比"] = df["占比"].cumsum()

    print(f"\n数据: {df.shape}")
    print(df.to_string(index=False))

    # 可视化
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 左图: 饼图
    colors = plt.cm.Pastel1(np.linspace(0, 1, len(df)))
    wedges, texts, autotexts = axes[0].pie(
        df["销售量"],
        labels=df["产品类型"],
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        wedgeprops=dict(width=0.7, edgecolor="white"),
    )
    axes[0].set_title("各产品销售占比", fontsize=14, fontweight="bold")

    # 右图: 帕累托图
    df_sorted = df.sort_values("销售量", ascending=False)
    axes[1].bar(df_sorted["产品类型"], df_sorted["销售量"], color="steelblue", edgecolor="black")
    ax2 = axes[1].twinx()
    ax2.plot(df_sorted["产品类型"], df_sorted["累计占比"] * 100, marker="o", color="red", linewidth=2, markersize=8)
    ax2.axhline(y=80, color="gray", linestyle="--", alpha=0.5)
    ax2.set_ylabel("累计占比 (%)", fontsize=12, color="red")
    ax2.set_ylim(0, 105)
    axes[1].set_xlabel("产品类型", fontsize=12)
    axes[1].set_ylabel("销售量", fontsize=12)
    axes[1].set_title("帕累托分析(80/20法则)", fontsize=14, fontweight="bold")
    axes[1].grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    save_fig(fig, "ch02/composition_analysis.png")
    plt.close(fig)

    save_df(df, "ch02/composition_data.csv")
    return df


def distribution_analysis():
    """分布分析"""
    print("\n" + "=" * 60)
    print("2.2.4 分布分析")
    print("=" * 60)

    xlsx = chapter(2) / "2、由基础分析范式引申出的分析方法" / "data-有答案" / "3分布分析-参考.xlsx"
    df = pd.read_excel(xlsx, sheet_name="分布分析", engine="openpyxl")
    # 提取客单价数据
    price_data = df.iloc[1:, 19:21].copy()
    price_data.columns = ["用户id", "客单价"]
    price_data = price_data.dropna()
    price_data["客单价"] = price_data["客单价"].astype(float)

    print(f"\n数据: {price_data.shape}")
    print(price_data.describe().to_string())

    # 可视化
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 左上: 直方图
    axes[0, 0].hist(price_data["客单价"], bins=20, color="steelblue", edgecolor="black", alpha=0.7)
    axes[0, 0].axvline(price_data["客单价"].mean(), color="red", linestyle="--", linewidth=2, label=f'均值={price_data["客单价"].mean():.2f}')
    axes[0, 0].axvline(price_data["客单价"].median(), color="green", linestyle="--", linewidth=2, label=f'中位数={price_data["客单价"].median():.2f}')
    axes[0, 0].set_xlabel("客单价", fontsize=12)
    axes[0, 0].set_ylabel("频数", fontsize=12)
    axes[0, 0].set_title("客单价分布直方图", fontsize=14, fontweight="bold")
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # 右上: 箱线图
    axes[0, 1].boxplot(price_data["客单价"], vert=True, patch_artist=True, boxprops=dict(facecolor="lightblue"))
    axes[0, 1].set_ylabel("客单价", fontsize=12)
    axes[0, 1].set_title("客单价箱线图", fontsize=14, fontweight="bold")
    axes[0, 1].grid(True, alpha=0.3, axis="y")

    # 左下: QQ图
    from scipy import stats
    stats.probplot(price_data["客单价"], dist="norm", plot=axes[1, 0])
    axes[1, 0].set_title("Q-Q图(正态分布检验)", fontsize=14, fontweight="bold")
    axes[1, 0].grid(True, alpha=0.3)

    # 右下: 核密度估计
    price_data["客单价"].plot(kind="kde", ax=axes[1, 1], color="steelblue", linewidth=2)
    axes[1, 1].set_xlabel("客单价", fontsize=12)
    axes[1, 1].set_ylabel("密度", fontsize=12)
    axes[1, 1].set_title("客单价核密度估计", fontsize=14, fontweight="bold")
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    save_fig(fig, "ch02/distribution_analysis.png")
    plt.close(fig)

    save_df(price_data, "ch02/distribution_data.csv")
    return price_data


def relationship_analysis():
    """关系分析"""
    print("\n" + "=" * 60)
    print("2.2.5 关系分析")
    print("=" * 60)

    xlsx = chapter(2) / "2、由基础分析范式引申出的分析方法" / "data-有答案" / "5关系分析-参考.xlsx"
    df = pd.read_excel(xlsx, sheet_name="关系图", engine="openpyxl")
    # 提取两个连续变量的关系
    relation_data = df.iloc[1:, [23, 24]].copy()
    relation_data.columns = ["产出收益", "投入成本"]
    relation_data = relation_data.dropna()
    relation_data["产出收益"] = relation_data["产出收益"].astype(float)
    relation_data["投入成本"] = relation_data["投入成本"].astype(float)

    print(f"\n数据: {relation_data.shape}")
    print(relation_data.describe().to_string())

    # 计算相关系数
    from scipy import stats
    corr, p_value = stats.pearsonr(relation_data["投入成本"], relation_data["产出收益"])
    print(f"\nPearson相关系数: {corr:.4f}, P值: {p_value:.6f}")

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 8))

    scatter = ax.scatter(
        relation_data["投入成本"],
        relation_data["产出收益"],
        s=100,
        c=relation_data["产出收益"] / relation_data["投入成本"],
        cmap="RdYlGn",
        alpha=0.7,
        edgecolors="black",
        linewidth=1,
    )

    # 添加回归线
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        relation_data["投入成本"], relation_data["产出收益"]
    )
    x_line = np.linspace(relation_data["投入成本"].min(), relation_data["投入成本"].max(), 100)
    y_line = slope * x_line + intercept
    ax.plot(x_line, y_line, color="red", linewidth=2, linestyle="--", label=f"回归线: y={slope:.2f}x+{intercept:.2f}")

    # 添加颜色条
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("收益/成本比", fontsize=12)

    ax.set_xlabel("投入成本", fontsize=12)
    ax.set_ylabel("产出收益", fontsize=12)
    ax.set_title(f"投入产出关系分析 (r={corr:.3f})", fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    save_fig(fig, "ch02/relationship_analysis.png")
    plt.close(fig)

    save_df(relation_data, "ch02/relationship_data.csv")
    return relation_data


def sankey_diagram():
    """桑基图"""
    print("\n" + "=" * 60)
    print("2.2.6 桑基图")
    print("=" * 60)

    xlsx = chapter(2) / "2、由基础分析范式引申出的分析方法" / "data-有答案" / "6桑基图.xlsx"
    df = pd.read_excel(xlsx, sheet_name="Sheet1", engine="openpyxl")

    print(f"\n数据: {df.shape}")
    print(df.head(10).to_string(index=False))

    # 简单的桑基图数据准备
    # 假设数据包含: 来源, 目标, 流量
    if len(df.columns) >= 3:
        source = df.iloc[:, 0].dropna().tolist()
        target = df.iloc[:, 1].dropna().tolist()
        value = df.iloc[:, 2].dropna().astype(int).tolist()

        print(f"\n桑基图数据: {len(source)} 条流")

        # 使用plotly绘制桑基图
        try:
            import plotly.graph_objects as go

            fig = go.Figure(
                data=[
                    go.Sankey(
                        node=dict(
                            pad=15,
                            thickness=20,
                            line=dict(color="black", width=0.5),
                            label=[str(i) for i in range(max(max(source), max(target)) + 1)],
                            color="blue",
                        ),
                        link=dict(
                            source=source,
                            target=target,
                            value=value,
                        ),
                    )
                ]
            )

            fig.update_layout(title_text="桑基图", font_size=12)
            fig.write_html(str(Path(__file__).parent.parent / "output" / "ch02" / "sankey_diagram.html"))
            print("  -> saved output/ch02/sankey_diagram.html")

        except ImportError:
            print("Plotly未安装, 跳过桑基图可视化")

    return df


def main():
    trend_analysis()
    comparison_analysis()
    composition_analysis()
    distribution_analysis()
    relationship_analysis()
    sankey_diagram()

    print("\n" + "=" * 60)
    print("6种引申分析方法全部完成!")
    print("=" * 60)


if __name__ == "__main__":
    from common import run_main

    sys.exit(run_main(main))
