import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge

# ---------------------- 数据 ----------------------
labels = ["销售部", "采购部", "工程部", "财务部", "行政部", "人力部"]
percent = np.array([29.2, 22.7, 17.5, 13.6, 10.3, 5.0])
colors = ['#e64c65', '#f6c356', '#13b0ac', '#339ed8', '#0066cc', '#7b42bc']
total = 100

# ---------------------- 画布 ----------------------
fig, ax = plt.subplots(figsize=(10, 10), dpi=120, facecolor='#191938')
ax.set_facecolor('#191938')
ax.set_aspect('equal')
ax.axis('off')

# ---------------------- 标题（和样图位置匹配） ----------------------
fig.text(0.5, 0.95, "2021年各部门人数分布",
         color='white', fontsize=26, weight='bold', ha='center')
fig.text(0.5, 0.89, "公司总人数1664，销售部人数最多451，占比29.2%",
         color='white', fontsize=14, ha='center')

# ---------------------- roseType=radius玫瑰图：从圆心0向外绘制 ----------------------
start_angle = 90   # 起始角度，顶部
max_radius = 1.0
anno = []

for p, c, lab in zip(percent, colors, labels):
    span = p / total * 360
    end_angle = start_angle - span
    mid_angle = (start_angle + end_angle) / 2
    # 半径正比于占比
    r = (p / percent.max()) * max_radius

    # 重点！width=r，从0到r，根部汇聚圆心，没有内圈
    wedge = Wedge(
        center=(0, 0),
        r=r,
        theta1=end_angle,
        theta2=start_angle,
        width=r,
        color=c
    )
    ax.add_patch(wedge)

    anno.append({
        "mid": mid_angle,
        "r": r,
        "color": c,
        "label": lab,
        "pct": p
    })
    start_angle = end_angle

# ---------------------- L型引导线、圆点、标签文字 ----------------------
for item in anno:
    deg = item["mid"]
    r = item["r"]
    c = item["color"]
    lab = item["label"]
    pct = item["pct"]
    rad = np.radians(deg)

    # 引线起点：花瓣最外沿
    x0 = r * np.cos(rad)
    y0 = r * np.sin(rad)
    # 第一段径向延伸
    x1 = (r + 0.09) * np.cos(rad)
    y1 = (r + 0.09) * np.sin(rad)
    # 第二段水平
    if np.cos(rad) >= 0:
        x2 = x1 + 0.26
        align = 'left'
        tx = x2 + 0.02
    else:
        x2 = x1 - 0.26
        align = 'right'
        tx = x2 - 0.02
    y2 = y1

    ax.plot([x0, x1, x2], [y0, y1, y2], color=c, lw=1.1)
    ax.scatter(x1, y1, color=c, s=28, zorder=10)
    ax.text(tx, y2, f"{lab}\n{pct}%", color="white", fontsize=9, ha=align, va="center")


# ---------------------- 底部备注 ----------------------
fig.text(0.5, 0.04, "*注: 数据来源于公司人力资源系统，统计日期截至2022.01.01",
         color='white', fontsize=9, ha='center')

ax.set_xlim(-1.4, 1.4)
ax.set_ylim(-1.4, 1.4)
plt.tight_layout()
plt.show()
