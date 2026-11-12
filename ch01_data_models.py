"""第1章 数据分析思维 - 关系模型与维度模型演示

本脚本迁移自教材第1章的两个演示案例:
1. 关系模型演示: 8张CSV表(accounts/card/clients/disp/district/loans/order/trans)
   展示关系型数据库中表与表之间的关联关系
2. 维度模型演示: 商场销售数据表.xlsx
   展示星型模型(Star Schema)中事实表与维度表的组织方式

迁移目标: 用pandas演示关系模型的JOIN操作与维度模型的聚合分析
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# 添加项目根目录到path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import GBK_CSV, save_df, save_fig
from paths import chapter


def demo_relational_model():
    """关系模型演示: 银行数据库的8张表及其关联"""
    print("=" * 60)
    print("1.1 关系模型演示 - 银行数据库")
    print("=" * 60)

    base = chapter(1) / "关系模型演示-不建议用poweBI操作关系型数据模型"

    # 加载8张表
    district = pd.read_csv(base / "district.csv", **GBK_CSV)
    accounts = pd.read_csv(base / "accounts.csv", **GBK_CSV)
    clients = pd.read_csv(base / "clients.csv", **GBK_CSV)
    disp = pd.read_csv(base / "disp.csv", **GBK_CSV)
    card = pd.read_csv(base / "card.csv", **GBK_CSV)
    loans = pd.read_csv(base / "loans.csv", **GBK_CSV)
    order = pd.read_csv(base / "order.csv", **GBK_CSV)
    trans = pd.read_csv(base / "trans.csv", **GBK_CSV)

    print(f"\n各表规模:")
    for name, df in [
        ("district", district),
        ("accounts", accounts),
        ("clients", clients),
        ("disp", disp),
        ("card", card),
        ("loans", loans),
        ("order", order),
        ("trans", trans),
    ]:
        print(f"  {name:10s}: {df.shape[0]:6d} rows x {df.shape[1]:2d} cols")

    # 演示关系模型的JOIN操作: 查询"每个客户的账户交易总额"
    # 需要关联: clients -> disp -> accounts -> trans
    print("\n\n关系模型的优势: 通过外键关联实现灵活查询")
    print("示例: 查询每个客户的账户交易总额")

    # Step 1: 客户 + 账户关联 (通过disp表)
    client_account = clients.merge(disp, on="client_id").merge(
        accounts, on="account_id"
    )
    print(f"\n  客户-账户关联表: {client_account.shape}")

    # Step 2: 关联交易表, 计算每个客户的交易总额
    client_trans = client_account.merge(trans, on="account_id")
    # trans表的amount列有千分位逗号, 需要清洗
    client_trans["amount_clean"] = (
        client_trans["amount"].astype(str).str.replace(",", "").astype(float)
    )
    result = (
        client_trans.groupby(["client_id", "sex", "birth_date"])["amount_clean"]
        .sum()
        .reset_index()
        .rename(columns={"amount_clean": "total_amount"})
        .sort_values("total_amount", ascending=False)
    )
    print(f"  客户交易汇总: {result.shape}")
    print(result.head(10).to_string(index=False))

    # 保存结果
    save_df(result, "ch01/relational_model_client_transactions.csv")

    # 对比: 如果用一张大宽表(反范式)存储, 会是什么样子?
    print("\n\n反例: 如果用一张大宽表存储(不推荐)")
    wide_table = client_trans[
        [
            "client_id",
            "sex",
            "birth_date",
            "account_id",
            "trans_id",
            "amount_clean",
        ]
    ].copy()
    print(f"  宽表规模: {wide_table.shape}")
    print("  问题: 数据冗余度高, 更新异常风险大")

    return result


def demo_star_schema():
    """维度模型演示: 商场销售数据的星型模型"""
    print("\n" + "=" * 60)
    print("1.2 维度模型演示 - 商场销售数据星型模型")
    print("=" * 60)

    xlsx = chapter(1) / "维度模型演示" / "商场销售数据表.xlsx"

    # 读取事实表(已包含部分维度信息)
    fact = pd.read_excel(xlsx, sheet_name="产品销售数据表", engine="openpyxl")
    # 清理列名(去除前后空格)
    fact.columns = fact.columns.str.strip()
    print(f"\n事实表(产品销售数据表): {fact.shape}")
    print(f"  列: {fact.columns.tolist()}")
    print(fact.head(3).to_string(index=False))

    # 读取维度表
    dim_brand = pd.read_excel(xlsx, sheet_name="品牌", engine="openpyxl")
    dim_category = pd.read_excel(xlsx, sheet_name="类别", engine="openpyxl")
    dim_city = pd.read_excel(xlsx, sheet_name="商铺城市", engine="openpyxl")
    dim_product = pd.read_excel(xlsx, sheet_name="产品信息表", engine="openpyxl")
    dim_date = pd.read_excel(xlsx, sheet_name="日期表", engine="openpyxl")

    print(f"\n维度表:")
    print(f"  品牌: {dim_brand.shape}")
    print(f"  类别: {dim_category.shape}")
    print(f"  商铺城市: {dim_city.shape}")
    print(f"  产品信息表: {dim_product.shape}")
    print(f"  日期表: {dim_date.shape}")

    # 星型模型的优势: 灵活的多维分析
    print("\n\n星型模型的优势: 支持灵活的多维分析(OLAP)")
    print("示例1: 按品牌和产品类别汇总销售额")

    # 事实表已经包含品牌名称和产品类别, 可以直接聚合
    brand_category_sales = (
        fact.groupby(["品牌名称", "产品类别"])["销售额"]
        .sum()
        .reset_index()
        .pivot(index="品牌名称", columns="产品类别", values="销售额")
        .fillna(0)
    )
    print(brand_category_sales.to_string())

    # 示例2: 按城市和月份分析销售趋势
    print("\n\n示例2: 按城市和月份分析销售趋势")
    fact["订单日期"] = pd.to_datetime(fact["订单日期"])
    fact["月份"] = fact["订单日期"].dt.to_period("M")
    city_month_sales = (
        fact.groupby(["商铺城市", "月份"])["销售额"].sum().reset_index()
    )
    print(city_month_sales.head(10).to_string(index=False))

    # 可视化: 各品牌销售额占比
    fig, ax = plt.subplots(figsize=(10, 6))
    brand_sales = fact.groupby("品牌名称")["销售额"].sum().sort_values(ascending=False)
    brand_sales.plot(kind="bar", ax=ax, color="steelblue")
    ax.set_title("各品牌销售额对比", fontsize=14)
    ax.set_xlabel("品牌")
    ax.set_ylabel("销售额")
    ax.tick_params(axis="x", rotation=0)
    for i, v in enumerate(brand_sales.values):
        ax.text(i, v + v * 0.01, f"{v:,.0f}", ha="center", fontsize=9)
    plt.tight_layout()
    save_fig(fig, "ch01/star_schema_brand_sales.png")
    plt.close(fig)

    # 保存汇总结果
    save_df(
        fact.groupby(["品牌名称", "产品类别"])["销售额"].sum().reset_index(),
        "ch01/star_schema_brand_category_sales.csv",
    )

    return brand_category_sales


def main():
    """运行第1章两个演示"""
    demo_relational_model()
    demo_star_schema()
    print("\n" + "=" * 60)
    print("第1章演示完成! 输出文件保存在 output/ch01/")
    print("=" * 60)


if __name__ == "__main__":
    from common import run_main

    sys.exit(run_main(main))
