import matplotlib.pyplot as plt
import numpy as np

# ---------------------- 数据 ----------------------
years = np.array([2017, 2018, 2019, 2020, 2021, 2022])
sales = np.array([1603, 2106, 2406, 3265, 3721, 3921])
growth = np.array([27, 31, 14, 36, 14, 5])

# ---------------------- 全局设置 ----------------------
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(figsize=(14, 9), dpi=120)
bg_color = "#192040"
fig.patch.set_facecolor(bg_color)

# ---------------------- 上方折线区：进一步缩短高度，ylim固定0~40，陡度不变 ----------------------
ax_top = fig.add_axes([0.08, 0.58, 0.84, 0.18])
ax_top.set_facecolor(bg_color)

line_color = "#e64458"
ax_top.plot(years, growth, color=line_color, marker='o', linewidth=2, markersize=6, zorder=3)
ax_top.set_ylim(0, 40)   # 关键：数值范围锁定，压缩画布高度，曲线相对斜率不变，波动不会放大
ax_top.set_xticks(years)
ax_top.set_xticklabels([])
ax_top.tick_params(axis='y', colors='white', labelsize=10)

# 折线百分比标注
for x, y in zip(years, growth):
    ax_top.text(x, y + 1.2, f"{y}%", ha="center", va="bottom", color="white", fontsize=11)

for spine in ax_top.spines.values():
    spine.set_visible(False)

# ---------------------- 下方柱形区：更窄、更高，柱间距缩小，X轴和折线严格对齐 ----------------------
ax_bottom = fig.add_axes([0.08, 0.14, 0.84, 0.38])
ax_bottom.set_facecolor(bg_color)

bar_color = "#007acc"
bars = ax_bottom.bar(years, sales, color=bar_color, width=0.32, zorder=2) # 宽度进一步收窄
ax_bottom.set_ylim(0, 4300)
ax_bottom.set_xticks(years)
ax_bottom.tick_params(axis='x', colors='white', labelsize=11)
ax_bottom.tick_params(axis='y', colors='white', labelsize=10)

# 柱子顶部销量标注
for bar in bars:
    h = bar.get_height()
    ax_bottom.text(
        bar.get_x() + bar.get_width() / 2,
        h + 70,
        f"{int(h)}",
        ha="center", va="bottom", color="white", fontsize=11
    )

for spine in ax_bottom.spines.values():
    spine.set_visible(False)

# ---------------------- 标题区：独立顶部靠左 ----------------------
fig.text(0.022, 0.945, "近六年销售量及增长率", color="white", fontsize=26, weight="bold")
fig.text(0.022, 0.912, "平台销量近6年持续增长，但近两年增长率有所放缓", color="white", fontsize=14)

# ---------------------- 右上角图例 ----------------------
from matplotlib.lines import Line2D
leg_items = [
    Line2D([0], [0], color=bar_color, lw=5, label="销售量"),
    Line2D([0], [0], color=line_color, marker="o", linestyle="-", label="同比")
]

ax_top.legend(
    handles=leg_items,
    loc="upper right",
    bbox_to_anchor=(1.0, 1.20),
    frameon=False,
    labelcolor="white",
    fontsize=11
)

# ---------------------- 底部注释 ----------------------
fig.text(0.022, 0.035, "*注：数据来源于公司销售系统", color="white", fontsize=10)

plt.show()
