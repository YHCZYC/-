import matplotlib.pyplot as plt
import numpy as np

# ---------------------- 数据 ----------------------
regions = ["华北", "华南", "东北", "西北", "西南", "华东"]
sales = np.array([2354, 1902, 3524, 2698, 2896, 2563])
yoy_rate = np.array([12, 25, 16, 21, 18, 25])

# ---------------------- 配色 ----------------------
bar_color = "#e0445c"
circle_color = "#007acc"
bg_color = "#191c40"

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(14, 9), dpi=120)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

x = np.arange(len(regions))
bar_width = 0.25  # 柱子收窄一倍

# 红色柱形
bars = ax.bar(x, sales, width=bar_width, color=bar_color, zorder=2)

# 柱顶销量文字
for bar in bars:
    h = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        h + 80,
        f"{int(h)}",
        ha="center", va="bottom", color="white", fontsize=12
    )

# 圆圈：横坐标和柱子一一对应，统一在同一高度，大小由百分比决定
circle_y = 4000
for i, rate in enumerate(yoy_rate):
    ax.scatter(x[i], circle_y, s=rate * 35, c=circle_color, zorder=3)
    ax.text(x[i], circle_y, f"{rate}%", ha="center", va="center", color="white", fontsize=11)

# ---------------------- 坐标轴 ----------------------
ax.set_xticks(x)
ax.set_xticklabels(regions, color="white", fontsize=14)
ax.set_ylim(0, 4300)
ax.set_yticks([])

ax.spines["bottom"].set_color("#666677")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.grid(False)

# ---------------------- 标题、副标题、注释 ----------------------
fig.text(0.04, 0.93, "各区域上半年销量以同比", color="white", fontsize=28, weight="bold")
fig.text(0.04, 0.87, "东北区域销量持续保持第一，华东和华南同比去年增长最多", color="white", fontsize=16)
fig.text(0.04, 0.06, "*注：数据来源于公司销售系统，统计日期截至2022.06.30", color="white", fontsize=10)

plt.subplots_adjust(top=0.82, bottom=0.14, left=0.07, right=0.96)
plt.show()
