"""第3章 商业数据分析框架 - 三个案例

迁移自:
- 案例1: 收入趋势分析
- 案例2: 财务费用分析
- 案例3: 电商平台精准营销

本脚本实现三个商业分析案例的Python版本
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import save_df, save_fig
from paths import chapter


def case1_revenue_trend():
    """案例1: 收入趋势分析"""
    print("=" * 60)
    print("3.1 收入趋势分析")
    print("=" * 60)

    xlsx = chapter(3) / "案例1：收入趋势分析" / "案例1：收入趋势分析原始数据.xlsx"
    df = pd.read_excel(xlsx, sheet_name="原始数据", engine="openpyxl")

    print(f"\n数据规模: {df.shape}")
    print(f"时间跨度: {df['订单年份'].min()}-{df['订单年份'].max()}")
    print(f"省份数: {df['销售省份'].nunique()}")

    # 1. 年度趋势
    yearly = df.groupby("订单年份")["销售额"].sum().reset_index()
    yearly["同比增长率"] = yearly["销售额"].pct_change() * 100

    print("\n年度销售额:")
    print(yearly.to_string(index=False))

    # 2. 月度趋势
    df["年月"] = df["订单年份"].astype(str) + "-" + df["订单月份"].astype(str).str.zfill(2)
    monthly = df.groupby("年月")["销售额"].sum().reset_index()
    monthly["环比增长率"] = monthly["销售额"].pct_change() * 100

    # 3. 省份分析
    province = df.groupby("销售省份")["销售额"].agg(["sum", "mean", "count"]).reset_index()
    province.columns = ["销售省份", "总销售额", "平均销售额", "订单数"]
    province = province.sort_values("总销售额", ascending=False)

    print("\n省份销售额TOP10:")
    print(province.head(10).to_string(index=False))

    # 可视化 - 简化为2个图
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 左: 年度趋势
    axes[0].bar(yearly["订单年份"], yearly["销售额"], color="steelblue", edgecolor="black")
    axes[0].set_xlabel("年份")
    axes[0].set_ylabel("销售额")
    axes[0].set_title("年度销售额趋势", fontweight="bold")
    axes[0].grid(True, alpha=0.3, axis="y")
    for i, v in enumerate(yearly["销售额"]):
        axes[0].text(i, v + v * 0.01, f"{v:,.0f}", ha="center", fontsize=9)

    # 右: 省份TOP10
    top10 = province.head(10)
    axes[1].barh(range(len(top10)), top10["总销售额"], color="coral", edgecolor="black")
    axes[1].set_yticks(range(len(top10)))
    axes[1].set_yticklabels(top10["销售省份"], fontsize=8)
    axes[1].set_xlabel("总销售额")
    axes[1].set_title("省份销售额TOP10", fontweight="bold")
    axes[1].grid(True, alpha=0.3, axis="x")

    plt.tight_layout()
    save_fig(fig, "ch03/case1_revenue_trend.png")
    plt.close(fig)

    # 保存结果
    save_df(yearly, "ch03/case1_yearly_trend.csv")
    save_df(monthly, "ch03/case1_monthly_trend.csv")
    save_df(province, "ch03/case1_province_analysis.csv")

    return df


def case2_financial_expense():
    """案例2: 财务费用分析"""
    print("\n" + "=" * 60)
    print("3.2 财务费用分析")
    print("=" * 60)

    xlsx = chapter(3) / "案例2：财务费用分析" / "案例2：财务费用分析-原始数据.xlsx"

    # 读取三个sheet
    total_expense = pd.read_excel(xlsx, sheet_name="总费用数据", engine="openpyxl")
    period_expense = pd.read_excel(xlsx, sheet_name="财务三大期间费用数据", engine="openpyxl")
    admin_expense = pd.read_excel(xlsx, sheet_name="管理费用数据", engine="openpyxl")

    print(f"\n总费用数据: {total_expense.shape}")
    print(f"期间费用数据: {period_expense.shape}")
    print(f"管理费用数据: {admin_expense.shape}")

    print("\n总费用数据:")
    print(total_expense.to_string(index=False))

    # 可视化
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 左上: 总费用趋势
    axes[0, 0].plot(total_expense["年"], total_expense["总费用"], marker="o", linewidth=2, markersize=8)
    axes[0, 0].set_xlabel("年份")
    axes[0, 0].set_ylabel("总费用")
    axes[0, 0].set_title("总费用趋势", fontweight="bold")
    axes[0, 0].grid(True, alpha=0.3)
    for i, v in enumerate(total_expense["总费用"]):
        axes[0, 0].text(i, v + v * 0.01, f"{v:,.0f}", ha="center", fontsize=9)

    # 右上: 三大期间费用对比
    period_melted = period_expense.melt(id_vars=["年"], var_name="费用类型", value_name="金额")
    sns.barplot(data=period_melted, x="年", y="金额", hue="费用类型", ax=axes[0, 1])
    axes[0, 1].set_title("三大期间费用对比", fontweight="bold")
    axes[0, 1].set_xlabel("年份")
    axes[0, 1].set_ylabel("金额")
    axes[0, 1].grid(True, alpha=0.3, axis="y")

    # 左下: 管理费用构成
    admin_melted = admin_expense.melt(id_vars=["年"], var_name="项目", value_name="金额")
    sns.lineplot(data=admin_melted, x="年", y="金额", hue="项目", marker="o", ax=axes[1, 0])
    axes[1, 0].set_title("管理费用构成趋势", fontweight="bold")
    axes[1, 0].set_xlabel("年份")
    axes[1, 0].set_ylabel("金额")
    axes[1, 0].grid(True, alpha=0.3)

    # 右下: 费用占比
    latest_year = total_expense["年"].max()
    latest_period = period_expense[period_expense["年"] == latest_year].iloc[0, 1:]
    axes[1, 1].pie(latest_period.values, labels=latest_period.index, autopct="%1.1f%%", startangle=90)
    axes[1, 1].set_title(f"{latest_year}年费用占比", fontweight="bold")

    plt.tight_layout()
    save_fig(fig, "ch03/case2_financial_expense.png")
    plt.close(fig)

    # 保存结果
    save_df(total_expense, "ch03/case2_total_expense.csv")
    save_df(period_expense, "ch03/case2_period_expense.csv")
    save_df(admin_expense, "ch03/case2_admin_expense.csv")

    return total_expense


def case3_ecommerce_marketing():
    """案例3: 电商平台精准营销"""
    print("\n" + "=" * 60)
    print("3.3 电商平台精准营销")
    print("=" * 60)

    xlsx = chapter(3) / "案例3：电商平台的精准营销" / "案例3：电商平台的精准营销-原始数据.xlsx"
    df = pd.read_excel(xlsx, sheet_name="原始数据", engine="openpyxl")

    print(f"\n数据规模: {df.shape}")
    print(f"客户数: {df['客户ID'].nunique()}")
    print(f"品类数: {df['品类'].nunique()}")

    # 1. 客户画像
    customer_profile = df.groupby("客户ID").agg(
        性别=("性别", "first"),
        年龄=("年龄", "first"),
        订单数=("品类", "count"),
        总数量=("数量", "sum"),
        主要品类=("品类", lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0]),
        主要支付方式=("支付方式", lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0]),
    ).reset_index()

    print("\n客户画像统计:")
    print(f"  性别分布:\n{customer_profile['性别'].value_counts()}")
    print(f"  年龄分布:\n{customer_profile['年龄'].describe()}")

    # 2. 品类分析
    category = df.groupby("品类").agg(
        订单数=("客户ID", "count"),
        总数量=("数量", "sum"),
        客户数=("客户ID", "nunique"),
    ).reset_index()
    category["平均购买量"] = category["总数量"] / category["订单数"]
    category = category.sort_values("订单数", ascending=False)

    print("\n品类销售分析:")
    print(category.to_string(index=False))

    # 3. 支付方式分析
    payment = df.groupby("支付方式").agg(
        订单数=("客户ID", "count"),
        总数量=("数量", "sum"),
    ).reset_index()
    payment["订单占比"] = payment["订单数"] / payment["订单数"].sum() * 100

    print("\n支付方式分析:")
    print(payment.to_string(index=False))

    # 可视化
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 左上: 年龄分布
    axes[0, 0].hist(customer_profile["年龄"], bins=20, color="steelblue", edgecolor="black", alpha=0.7)
    axes[0, 0].axvline(customer_profile["年龄"].mean(), color="red", linestyle="--", linewidth=2, label=f'均值={customer_profile["年龄"].mean():.1f}')
    axes[0, 0].set_xlabel("年龄")
    axes[0, 0].set_ylabel("人数")
    axes[0, 0].set_title("客户年龄分布", fontweight="bold")
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # 右上: 品类订单数
    top_categories = category.head(10)
    axes[0, 1].barh(top_categories["品类"], top_categories["订单数"], color="coral", edgecolor="black")
    axes[0, 1].set_xlabel("订单数")
    axes[0, 1].set_title("品类订单数TOP10", fontweight="bold")
    axes[0, 1].grid(True, alpha=0.3, axis="x")
    for i, v in enumerate(top_categories["订单数"]):
        axes[0, 1].text(v + v * 0.01, i, str(v), va="center", fontsize=9)

    # 左下: 支付方式占比
    axes[1, 0].pie(payment["订单数"], labels=payment["支付方式"], autopct="%1.1f%%", startangle=90, colors=["#FF6B6B", "#4ECDC4", "#45B7D1"])
    axes[1, 0].set_title("支付方式订单占比", fontweight="bold")

    # 右下: 性别×品类交叉分析
    gender_category = df.groupby(["性别", "品类"]).size().unstack(fill_value=0)
    gender_category.plot(kind="bar", ax=axes[1, 1])
    axes[1, 1].set_xlabel("性别")
    axes[1, 1].set_ylabel("订单数")
    axes[1, 1].set_title("性别×品类交叉分析", fontweight="bold")
    axes[1, 1].legend(title="品类", bbox_to_anchor=(1.05, 1), loc="upper left")
    axes[1, 1].tick_params(axis="x", rotation=0)

    plt.tight_layout()
    save_fig(fig, "ch03/case3_ecommerce_marketing.png")
    plt.close(fig)

    # 保存结果
    save_df(customer_profile, "ch03/case3_customer_profile.csv")
    save_df(category, "ch03/case3_category_analysis.csv")
    save_df(payment, "ch03/case3_payment_analysis.csv")

    return df


def main():
    case1_revenue_trend()
    case2_financial_expense()
    case3_ecommerce_marketing()

    print("\n" + "=" * 60)
    print("第3章三个案例全部完成!")
    print("=" * 60)


if __name__ == "__main__":
    from common import run_main

    sys.exit(run_main(main))
