# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

labels = ['[20,30)', '[30,40)', '[40,50)', '≥50']
values = [37.5, 29.2, 20.8, 12.5]
colors = ['#8B3FCF', '#4A6FD9', '#2CC5C3', '#F5C842']

fig, ax = plt.subplots(figsize=(12, 9), dpi=100)
bg_color = '#0D1A3A'
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)
ax.set_xlim(-1.8, 1.8)
ax.set_ylim(-1.8, 1.8)
ax.set_aspect('equal')
ax.axis('off')

# ========== 绘制南丁格尔圆环扇区 ==========
inner_r = 0.20
max_outer = 0.85
N = len(values)
gap_deg = 4
sector_deg = (360 - N * gap_deg) / N  # 每个扇区86°

# 从12点方向（90°）顺时针
angles_start = [90 - i * (sector_deg + gap_deg) for i in range(N)]

for i in range(N):
    # 外半径按百分比值线性映射
    r_outer = inner_r + (values[i] / max(values)) * (max_outer - inner_r)

    t1 = angles_start[i]
    t2 = t1 - sector_deg

    wedge = Wedge(
        (0, 0), r_outer, t2, t1,
        width=r_outer - inner_r,
        facecolor=colors[i],
        edgecolor=bg_color,
        linewidth=2.5,
        alpha=0.92
    )
    ax.add_patch(wedge)

# ========== 引线 + 标签 ==========
for i in range(N):
    mid_deg = angles_start[i] - sector_deg / 2
    mid_rad = np.radians(mid_deg)

    r_outer = inner_r + (values[i] / max(values)) * (max_outer - inner_r)

    # 扇区外缘点
    x1 = r_outer * np.cos(mid_rad)
    y1 = r_outer * np.sin(mid_rad)

    # 引线终点
    lr = max_outer + 0.35
    x2 = lr * np.cos(mid_rad)
    y2 = lr * np.sin(mid_rad)

    # 水平延伸
    if np.cos(mid_rad) >= 0:
        ext = 0.35
        ha = 'left'
    else:
        ext = -0.35
        ha = 'right'

    x3 = x2 + ext
    y3 = y2

    # 引线
    ax.plot([x1, x2, x3], [y1, y2, y3], color=colors[i], lw=1.8, zorder=5)
    ax.plot(x1, y1, 'o', color=colors[i], markersize=6, zorder=6)

    # 文字
    tx = x3 + (0.08 if ha == 'left' else -0.08)
    ax.text(tx, y3 + 0.08, labels[i], fontsize=14, fontweight='bold',
            color='white', ha=ha, va='bottom')
    ax.text(tx, y3 - 0.08, f'{values[i]}%', fontsize=13,
            color=colors[i], ha=ha, va='top')

# ========== 标题和注释 ==========
ax.text(-1.65, 1.55, '2022年上半各年龄段人数分布', color='white', fontsize=28, weight='bold')
ax.text(-1.65, 1.38, '公司平均年龄32.5，20-30员工比例最高占比37.5%', color='#99AABB', fontsize=16)
ax.text(-1.65, -1.60, '*注：数据来源于公司人力资源系统，统计日期截至2022.06.30', color='#556677', fontsize=11)

plt.tight_layout()
plt.show()