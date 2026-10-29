import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

departments = ["销售部", "采购部", "工程部", "财务部", "行政部", "人力部"]
nums = [451, 326, 293, 238, 226, 130]
colors = ["#e84855", "#f9c74f", "#2bbbad", "#4392f1", "#0066cc", "#7b2cbf"]
total = sum(nums)

# 规则：50% 对应360°
pcts = [v / total * 100 for v in nums]
scale = 360 / 50

fig, ax = plt.subplots(figsize=(12, 9), dpi=100)
bg_color = "#1a1e40"
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect("equal")
ax.axis("off")

base_radii = [0.90, 0.78, 0.66, 0.54, 0.42, 0.30]
ring_width = 0.06

for r, pct, c in zip(base_radii, pcts, colors):
    angle = pct * scale
    ratio = angle / 360
    ax.pie(
        [ratio, 1 - ratio],
        radius=r,
        colors=[c, bg_color],
        startangle=90,
        counterclock=False,
        wedgeprops={
            "width": ring_width,
            "edgecolor": bg_color
        }
    )

# ========== 全部标签统一左侧纵向并列对齐：部门+数值 ==========
label_x = -0.3
label_y_start = 0.85
label_dy = 0.12
for name, v in zip(departments, nums):
    ax.text(label_x, label_y_start, f"{name} {v}", color="white", va="center", fontsize=13)
    label_y_start -= label_dy

ax.text(-1.35, 1.22, "2022年上半年各部门人数", color="white", fontsize=32, weight="bold")
ax.text(-1.35, 1.10, f"公司总人数{total}，销售部人数最多451，占比27%", color="white", fontsize=22)
ax.text(-1.35, -1.22, "*注：数据来源于公司人力资源系统，统计日期截止2022.06.30", color="#dddddd", fontsize=15)

plt.tight_layout()
plt.show()
