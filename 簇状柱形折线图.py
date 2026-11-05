import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# ---------------------- 数据 ----------------------
regions = ["华北", "华南", "东北", "西北", "西南", "华东"]
sale_2022 = np.array([2354, 1902, 3524, 2698, 2896, 2563])
sale_2021 = np.array([2021, 1563, 3213, 2531, 2631, 2361])
yoy = np.array([16, 22, 10, 7, 10, 9])

# ---------------------- 配色 ----------------------
c2022 = "#007acc"
c2021 = "#e0445c"
cline = "#ffcc00"
bg_color = "#191c40"

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 上下两个子图：上折线，下簇状柱
fig, (ax1, ax2) = plt.subplots(
    nrows=2, ncols=1,
    figsize=(14, 9),
    dpi=120,
    gridspec_kw={'height_ratios': [1, 3.5], 'hspace': 0.32}
)
fig.patch.set_facecolor(bg_color)
ax1.set_facecolor(bg_color)
ax2.set_facecolor(bg_color)

x = np.arange(len(regions))

# ========== 上方子图：同比折线图 ==========
ax1.plot(x, yoy, color=cline, marker='o', linewidth=2.5, markersize=8, zorder=4)
for i, rate in enumerate(yoy):
    ax1.text(x[i], rate + 0.6, f"{rate}%", ha="center", va="bottom", color="white", fontsize=12)

ax1.set_ylim(0, 26)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.spines[:].set_visible(False)
ax1.grid(False)

# ========== 下方子图：簇状柱形图 ==========
bar_width = 0.18
bar1 = ax2.bar(x - bar_width/2 - 0.02, sale_2022, width=bar_width, color=c2022, zorder=2)
bar2 = ax2.bar(x + bar_width/2 + 0.02, sale_2021, width=bar_width, color=c2021, zorder=2)

# 柱顶标注数值
for b in bar1:
    h = b.get_height()
    ax2.text(b.get_x() + b.get_width() / 2, h + 60, f"{int(h)}",
             ha="center", va="bottom", color="white", fontsize=11)
for b in bar2:
    h = b.get_height()
    ax2.text(b.get_x() + b.get_width() / 2, h + 60, f"{int(h)}",
             ha="center", va="bottom", color="white", fontsize=11)

ax2.set_xticks(x)
ax2.set_xticklabels(regions, color="white", fontsize=13)
ax2.set_ylim(0, 3800)
ax2.set_yticks([])
ax2.spines["bottom"].set_color("#666677")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.grid(False)

# ========== 手动绘制右上角方框图例（重点！） ==========
# 坐标是 ax2 的归一化坐标 (0,0左下角，1,1右上角)
box_w = 0.11
box_h = 0.06
x_pos = 0.86
y1 = 0.50
y2 = 0.41



# 2022方框
rect22 = Rectangle((x_pos, y1), box_w, box_h, facecolor=bg_color, edgecolor=c2022, lw=2, transform=ax2.transAxes)
ax2.add_patch(rect22)
ax2.text(x_pos + box_w/2, y1 + box_h/2, "2022", color="white", fontsize=16, ha="center", va="center", transform=ax2.transAxes)

# 2021方框
rect21 = Rectangle((x_pos, y2), box_w, box_h, facecolor=bg_color, edgecolor=c2021, lw=2, transform=ax2.transAxes)
ax2.add_patch(rect21)
ax2.text(x_pos + box_w/2, y2 + box_h/2, "2021", color="white", fontsize=16, ha="center", va="center", transform=ax2.transAxes)

# 标题、副标题、底部注释
fig.text(0.04, 0.94, "上半年各月商品销量同比去年情况", color="white", fontsize=28, weight="bold")
fig.text(0.04, 0.88, "2022年相比于2021年销量都有提升，半年整体提升17%", color="white", fontsize=16)
fig.text(0.04, 0.04, "*注：数据来源于公司销售系统，统计日期截至2022.06.30", color="white", fontsize=10)

plt.subplots_adjust(top=0.83, bottom=0.10, left=0.07, right=0.96)
plt.show()
