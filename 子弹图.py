import matplotlib.pyplot as plt
import numpy as np

# ---------------------- 数据 ----------------------
goods = ["口红", "面膜", "隔离", "防晒", "精华", "面霜"]
actual = np.array([653, 523, 648, 856, 714, 785])
target = np.array([700, 500, 600, 900, 600, 600])
pass_val = np.array([600, 600, 600, 600, 600, 600])
good_val = np.array([200, 200, 200, 200, 200, 200])
excellent_val = np.array([200, 200, 200, 200, 200, 200])

# 配色（对齐样图）
color_pass = "#a0c4e8"
color_good = "#0099bb"
color_excel = "#0066bb"
color_actual = "#0066ff"
color_target = "#ffcc00"
bg_color = "#191c40"

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(14, 9), dpi=120)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

x = np.arange(len(goods))
bar_width = 0.35

# 分段背景条：及格、良好、优秀（堆叠）
ax.bar(x, pass_val, width=bar_width, color=color_pass, zorder=1)
ax.bar(x, good_val, width=bar_width, bottom=pass_val, color=color_good, zorder=1)
ax.bar(x, excellent_val, width=bar_width, bottom=pass_val+good_val, color=color_excel, zorder=1)

# 实际值蓝色柱（窄一点）
ax.bar(x, actual, width=bar_width*0.4, color=color_actual, zorder=3)

# 目标黄色短横线
ax.scatter(x, target, marker="_", s=600, c=color_target, zorder=4, linewidth=3)

# 坐标轴设置
ax.set_xticks(x)
ax.set_xticklabels(goods, color="white", fontsize=12)
ax.set_ylim(0, 1200)
ax.set_yticks([0,200,400,600,800,1000,1200])
ax.tick_params(axis='y', colors="white", labelsize=12)

# 隐藏边框
for spine in ax.spines.values():
    spine.set_visible(False)
ax.grid(False)

# 标题、副标题
fig.text(0.04, 0.93, "2022年上半年各商品销量完成情况", color="white", fontsize=28, weight="bold")
fig.text(0.04, 0.87, "防晒整体销量最好，达到856，面霜远超目标，超额完成30%", color="white", fontsize=14)

# 图例，正方形marker
from matplotlib.lines import Line2D
legend_items = [
    Line2D([], [], marker='s', linestyle='', markerfacecolor=color_pass, markersize=10, label="及格"),
    Line2D([], [], marker='s', linestyle='', markerfacecolor=color_good, markersize=10, label="良好"),
    Line2D([], [], marker='s', linestyle='', markerfacecolor=color_excel, markersize=10, label="优秀"),
    Line2D([], [], marker='s', linestyle='', markerfacecolor=color_actual, markersize=10, label="实际"),
    Line2D([], [], marker='_', linestyle='', markeredgecolor=color_target, markersize=14, markeredgewidth=3, label="目标")
]
ax.legend(handles=legend_items,
          loc="upper left",
          bbox_to_anchor=(0.00, 1.00),
          ncol=5,
          frameon=False,
          labelcolor="white",
          fontsize=11,
          handletextpad=0.4)

# 底部注释
fig.text(0.04, 0.06, "*注：数据来源于公司销售系统，统计日期截至2022.06.30", color="white", fontsize=9)

plt.subplots_adjust(top=0.82, bottom=0.14, left=0.07, right=0.96)
plt.show()
