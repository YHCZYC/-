import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

departments = ["销售部", "采购部", "工程部", "财务部", "行政部", "人力部"]
nums = [451, 326, 293, 238, 226, 130]
colors = ["#e84855", "#f9c74f", "#2bbbad", "#4392f1", "#0066cc", "#7b2cbf"]
total = sum(nums)

fig, ax = plt.subplots(figsize=(12, 9), dpi=100)
bg_color = "#1a1e40"
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)
ax.set_aspect("equal")
ax.axis("off")

wedges, texts = ax.pie(
    nums,
    colors=colors,
    startangle=90,
    counterclock=False,
    wedgeprops={"edgecolor": bg_color}
)

# 修复：循环变量 w
for w in wedges:
    ang = (w.theta1 + w.theta2) / 2
    r0 = 1.02
    r1 = 1.2
    r2 = 1.5
    theta = np.radians(ang)

    x0 = r0 * np.cos(theta)
    y0 = r0 * np.sin(theta)
    x1 = r1 * np.cos(theta)
    y1 = r1 * np.sin(theta)

    if x0 > 0:
        x2 = r2
    else:
        x2 = -r2
    y2 = y1

    line_color = w.get_facecolor()

    ax.plot([x0, x1, x2], [y0, y1, y2], color=line_color, lw=1.2)
    ax.scatter(x0, y0, color=line_color, s=40, zorder=5)

ax.text(-2.0, 1.60, "2021年各部门人数分布", color="white", fontsize=36, weight="bold")
ax.text(-2.0, 1.48, f"公司总人数{total}，销售部人数最多451，占比29.2%", color="white", fontsize=25)
ax.text(-2.0, -1.55, "*注：数据来源于公司人力资源系统，统计日期截至2022.01.01", color="#dddddd", fontsize=22)

plt.tight_layout()
plt.show()
