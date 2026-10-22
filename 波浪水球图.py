import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ========== 参数 ==========
percent = 0.65
bg_color = "#1b2040"
water_color = "#0088e0"
ring_color = "#0088e0"

cx, cy = 0, 0
water_r = 0.55
# 原来间隙：0.72 - 0.55 = 0.17；缩小两倍，间隙改为 0.085
outer_ring_r = water_r + 0.085

wave_amp = 0.035
wave_freq = 2.0

fig, ax = plt.subplots(figsize=(12, 9), dpi=120)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# ========== 内部波浪水球 ==========
x = np.linspace(-water_r, water_r, 1000)
base_y = cy - water_r + 2 * water_r * percent
wave_y = base_y + wave_amp * np.sin(wave_freq * np.pi * x / water_r)

fill = ax.fill_between(x, wave_y, cy - water_r, color=water_color)
water_circle = Circle((cx, cy), water_r, transform=ax.transData)
fill.set_clip_path(water_circle)

# ========== 外层蓝色圆环 ==========
outer_ring = Circle((cx, cy), outer_ring_r, edgecolor=ring_color, facecolor="none", lw=2)
ax.add_patch(outer_ring)

# ========== 中间文字 ==========
ax.text(cx, cy, f"{int(percent * 100)}%",
        fontname="Calibri",
        fontsize=80,
        color="white",
        ha="center",
        va="center")

# ========== 标题注释 ==========
fig.text(0.04, 0.88, "本科及以上学历员占比", fontsize=36, color="white", weight="bold")
fig.text(0.04, 0.80, "6月30日最新统计数据本科及以上员工占比65%", fontsize=22, color="white")
fig.text(0.04, 0.06, "*注: 数据来源于公司人力资源系统", fontsize=14, color="#dddddd")

ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect("equal")
ax.axis("off")

plt.tight_layout()
plt.show()
