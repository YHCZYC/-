import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 配色和参数
bg_color = "#162042"
line_color = "#0078d4"
fill_color = "#0078d4"
percent = 0.65
# 水球放大一倍
r = 0.7 * 1.25
inner_r = r - 0.05
cx, cy = 0, -0.22

fig, ax = plt.subplots(figsize=(12, 9), dpi=120)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 双层圆环
outer_ring = Circle((cx, cy), r, edgecolor=line_color, facecolor="none", lw=2)
inner_ring = Circle((cx, cy), inner_r, edgecolor=line_color, facecolor="none", lw=2)
ax.add_patch(outer_ring)
ax.add_patch(inner_ring)

# 内层圆水平填充
y = np.linspace(cy - inner_r, cy + inner_r, 600)
dy = y - cy
x_radius = np.sqrt(np.clip(inner_r ** 2 - dy ** 2, 0, None))
water_level = cy - inner_r + 2 * inner_r * percent
mask = y <= water_level
ax.fill_betweenx(y[mask], cx - x_radius[mask], cx + x_radius[mask], color=fill_color)

#水球内百分比
ax.text(cx, cy, f"{int(percent*100)}%",
        fontname="Calibri",
        fontsize=90,
        color="white",
        ha="center", va="center")

# 顶部标题
fig.text(0.05, 0.87, "2022年上半年目标完成率", fontsize=40, color="white", weight="bold")
fig.text(0.05, 0.79, "截至6月30日销售目标总体完成率达到65%", fontsize=28, color="white")

# 底部注释
fig.text(0.05, 0.06, "*注: 数据来源于公司销售系统", fontsize=18, color="#dddddd")

ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect("equal")
ax.axis("off")

plt.tight_layout()
plt.show()
