import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ---------------------- 数据 ----------------------
month_labels = ["1月", "2月", "3月", "4月", "5月", "6月"]
x_raw = np.arange(len(month_labels))
data_2021 = [1686, 1345, 1934, 1658, 1865, 1936]
data_2022 = [1385, 1846, 1654, 1936, 2564, 2236]
color_2021 = "#ee4360"
color_2022 = "#2078d9"
bg_color = "#1a1a40"

fig, ax = plt.subplots(figsize=(13, 8), dpi=120)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 绘制两条折线 + 圆点标记
ax.plot(x_raw, data_2021, color=color_2021, marker="o", linewidth=2.5, markersize=8, label="2021年")
ax.plot(x_raw, data_2022, color=color_2022, marker="o", linewidth=2.5, markersize=8, label="2022年")

# 每个点上方标注数值
for xi, val in zip(x_raw, data_2021):
    ax.text(xi, val + 75, str(val), color="white", ha="center", fontsize=14)
for xi, val in zip(x_raw, data_2022):
    ax.text(xi, val + 75, str(val), color="white", ha="center", fontsize=14)

# X轴
ax.set_xticks(x_raw)
ax.set_xticklabels(month_labels, color="white", fontsize=14)

# Y轴
ax.set_ylim(0, 3100)
ax.set_yticks([0, 500, 1000, 1500, 2000, 2500, 3000])
ax.set_yticklabels(["0", "500", "1000", "1500", "2000", "2500", "3000"], color="white", fontsize=14)

# 横向网格虚线
ax.grid(axis='y', linestyle='--', color="#606080", linewidth=1)
ax.set_axisbelow(True)

# 隐藏边框
for spine in ax.spines.values():
    spine.set_visible(False)

# ========== 重点：ncol=2 横向并排，样式保持原样 ==========
leg = ax.legend(
    loc="upper right",
    frameon=False,
    labelcolor="white",
    fontsize=14,
    ncol=2,
    handlelength=1.8,
    handletextpad=0.7
)

# 标题、副标题
fig.text(0.045, 0.94, "2022年上半年各月同比去年销量", color="white", fontsize=32, weight="bold")
fig.text(0.045, 0.86, "上半年同比去年增长明显，5月份同比增长最多，增长近40%", color="white", fontsize=20)

# 底部注释
fig.text(0.045, 0.008, "*注: 数据来源于公司销售系统，统计日期截至2022.06.30", color="white", fontsize=12)

plt.subplots_adjust(left=0.04, right=0.97, top=0.78, bottom=0.14)
plt.show()
