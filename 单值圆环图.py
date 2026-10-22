import matplotlib.pyplot as plt
from matplotlib.patches import Wedge

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

bg_color = "#1a1a38"
complete_rate = 0.85
radius = 0.75
# 原ring_width=0.18，缩小两倍 → 0.09，外半径不变，整体大小不变
ring_width = 0.09

fig, ax = plt.subplots(figsize=(9, 8), dpi=120)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 15%灰色段 左上
gray_deg = 54
gray_t1 = 126
gray_t2 = gray_t1 + gray_deg

# 渐变：紫色（灰色上沿）顺时针往下过渡到紫红色
color_total_deg = 306
gradient_colors = [
    "#8c1fe3",
    "#9828d8",
    "#a432cd",
    "#b03cc2",
    "#bc46b7",
    "#c850ac",
    "#d45aa1",
    "#df6496",
    "#eb6e8b",
    "#f77880"
]
seg_num = len(gradient_colors)
seg_deg = color_total_deg / seg_num

current_theta = gray_t1
for c in gradient_colors:
    t1 = current_theta - seg_deg
    t2 = current_theta
    w = Wedge((0,0), r=radius, theta1=t1, theta2=t2, width=ring_width, color=c, zorder=2)
    ax.add_patch(w)
    current_theta = t1

# 灰色块
gray_wedge = Wedge((0,0), r=radius, theta1=gray_t1, theta2=gray_t2, width=ring_width, color="#5c607a", zorder=2)
ax.add_patch(gray_wedge)

# 中间文字，位置不变
ax.text(0, 0.12, "85%", fontsize=58, color="white", ha="center", va="center")
ax.text(0, -0.32, "目标完成率", fontsize=18, color="#ddddee", ha="center", va="center")

ax.set_xlim(-1.1,1.1)
ax.set_ylim(-1.1,1.1)
ax.set_aspect("equal")
ax.axis("off")

# 标题备注
fig.text(0.05, 0.92, "2022年上半年目标完成率", color="white", fontsize=30, weight="bold")
fig.text(0.05, 0.84, "截至6月30日销售目标总体完成率达到85%", color="white", fontsize=18)
fig.text(0.05, 0.04, "*注: 数据来源于公司销售系统", color="#ccccdd", fontsize=13)

plt.subplots_adjust(left=0.03, right=0.97, top=0.78, bottom=0.08)
plt.show()
