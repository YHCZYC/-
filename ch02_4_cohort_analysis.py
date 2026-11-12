"""第2章 1、分析的基础范式 - 同期群分析(Cohort Analysis)

迁移自: 1-4同期群分析-参考.xlsx

同期群分析按用户注册日期分组, 追踪各组用户在后续时间段的留存情况。
核心指标: 留存率 = 某注册批次在后续时间段活跃的用户数 / 该批次总用户数
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import save_df, save_fig
from paths import chapter


def load_data():
    """加载用户登录明细"""
    xlsx = chapter(2) / "1、分析的基础范式" / "data-有答案" / "1-4同期群分析-参考.xlsx"
    data = pd.read_excel(xlsx, sheet_name="用户登录明细", engine="openpyxl")
    # 清理空列
    data = data[["用户编号", "注册日期", "登录日期"]]
    data["注册日期"] = pd.to_datetime(data["注册日期"])
    data["登录日期"] = pd.to_datetime(data["登录日期"])
    return data


def calculate_cohort_retention(data: pd.DataFrame):
    """计算同期群留存率"""
    # 1. 提取注册周(按周分组)
    data["注册周"] = data["注册日期"].dt.to_period("W")

    # 2. 计算每个用户的注册周
    user_cohort = (
        data.groupby("用户编号")["注册周"].min().reset_index(name="用户注册周")
    )

    # 3. 合并登录数据, 计算登录周
    data = data.merge(user_cohort, on="用户编号")
    data["登录周"] = data["登录日期"].dt.to_period("W")

    # 4. 计算周次差(登录周 - 注册周)
    data["周次差"] = (data["登录周"] - data["用户注册周"]).apply(lambda x: x.n)

    # 5. 去重: 每个用户在每个周次只计一次
    data_unique = data.drop_duplicates(subset=["用户编号", "周次差"])

    # 6. 构建留存表
    cohort_data = data_unique.groupby(["用户注册周", "周次差"])["用户编号"].nunique().reset_index(name="活跃用户数")

    # 7. 计算每个注册周的总用户数
    cohort_size = (
        data_unique.groupby("用户注册周")["用户编号"].nunique().reset_index(name="注册用户数")
    )

    # 8. 合并并计算留存率
    cohort_data = cohort_data.merge(cohort_size, on="用户注册周")
    cohort_data["留存率"] = cohort_data["活跃用户数"] / cohort_data["注册用户数"]

    # 9. 构建留存矩阵
    retention_matrix = cohort_data.pivot(
        index="用户注册周", columns="周次差", values="留存率"
    ).fillna(0)

    return retention_matrix, cohort_size, cohort_data


def visualize_cohort(retention_matrix, cohort_size):
    """可视化同期群留存"""
    # 1. 留存率热力图
    fig, ax = plt.subplots(figsize=(14, 10))

    # 转换为百分比显示
    retention_pct = retention_matrix * 100

    sns.heatmap(
        retention_pct,
        annot=True,
        fmt=".1f",
        cmap="YlGnBu",
        ax=ax,
        cbar_kws={"label": "留存率 (%)"},
        linewidths=0.5,
    )

    ax.set_xlabel("周次(相对于注册周)", fontsize=12)
    ax.set_ylabel("注册周", fontsize=12)
    ax.set_title("同期群留存率热力图", fontsize=14, fontweight="bold")

    # 添加注册用户数标注
    for i, (idx, row) in enumerate(retention_matrix.iterrows()):
        size = cohort_size[cohort_size["用户注册周"] == idx]["注册用户数"].values[0]
        ax.text(-0.5, i + 0.5, f"n={size}", ha="right", va="center", fontsize=9)

    plt.tight_layout()
    save_fig(fig, "ch02/cohort_retention_heatmap.png")
    plt.close(fig)

    # 2. 留存曲线
    fig, ax = plt.subplots(figsize=(12, 6))

    # 选择前5个注册周展示
    cohorts_to_plot = retention_matrix.index[:5]
    for cohort in cohorts_to_plot:
        retention_values = retention_matrix.loc[cohort]
        ax.plot(
            retention_values.index,
            retention_values.values * 100,
            marker="o",
            label=str(cohort),
            linewidth=2,
        )

    ax.set_xlabel("周次", fontsize=12)
    ax.set_ylabel("留存率 (%)", fontsize=12)
    ax.set_title("各注册周留存曲线", fontsize=14, fontweight="bold")
    ax.legend(title="注册周")
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color="gray", linestyle="--", alpha=0.5)

    plt.tight_layout()
    save_fig(fig, "ch02/cohort_retention_curves.png")
    plt.close(fig)


def main():
    print("=" * 60)
    print("2.4 同期群分析(Cohort Analysis)")
    print("=" * 60)

    data = load_data()
    print(f"\n用户登录明细: {data.shape}")
    print(f"  用户数: {data['用户编号'].nunique()}")
    print(f"  注册日期范围: {data['注册日期'].min().date()} ~ {data['注册日期'].max().date()}")
    print(f"  登录日期范围: {data['登录日期'].min().date()} ~ {data['登录日期'].max().date()}")

    retention_matrix, cohort_size, cohort_data = calculate_cohort_retention(data)

    print(f"\n注册周数: {len(cohort_size)}")
    print(f"留存矩阵形状: {retention_matrix.shape}")
    print(f"\n前5周注册用户数:")
    print(cohort_size.head().to_string(index=False))

    print(f"\n留存率矩阵(前5行 x 前8列):")
    print((retention_matrix.iloc[:5, :8] * 100).round(1).to_string())

    # 保存结果
    save_df(cohort_size, "ch02/cohort_size.csv")
    save_df(cohort_data, "ch02/cohort_retention_detail.csv")
    retention_matrix.to_csv(
        Path(__file__).parent.parent / "output" / "ch02" / "cohort_retention_matrix.csv"
    )

    # 可视化
    visualize_cohort(retention_matrix, cohort_size)

    # 关键洞察
    print("\n" + "=" * 60)
    print("关键洞察:")
    week0_retention = retention_matrix[0] if 0 in retention_matrix.columns else None
    if week0_retention is not None:
        print(f"  第0周留存率(基准): {week0_retention.mean()*100:.1f}%")
    if 1 in retention_matrix.columns:
        week1_retention = retention_matrix[1]
        print(f"  第1周留存率: {week1_retention.mean()*100:.1f}%")
    if 4 in retention_matrix.columns:
        week4_retention = retention_matrix[4]
        print(f"  第4周留存率: {week4_retention.mean()*100:.1f}%")
    print("=" * 60)


if __name__ == "__main__":
    from common import run_main

    sys.exit(run_main(main))
