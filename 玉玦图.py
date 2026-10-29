import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

labels = ["[20,30)", "[30,40)", "[40,50)", ">=50"]
percents = [37.5, 29.2, 20.8, 12.5]
colors = ["#e84b67", "#f9c254", "#17b1b0", "#3498db"]
bg_color = "#1b2040"

fig, ax = plt.subplots(figsize=(13, 9), dpi=120)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 玉玦整体放大 0.5 倍：在原来缩小版基础上恢复为 1.5 倍
base_radii = [0.90, 0.74, 0.58, 0.42]
radii = [r * 1.5 for r in base_radii]
ring_width = 0.16 * 1.5

# 50% 对应 360° 整圆
scale = 360 / 50

for r, pct, c in zip(radii, percents, colors):
    ax.pie(
        [pct * scale / 360, 1 - (pct * scale / 360)],
        radius=r,
        colors=[c, bg_color],
        startangle=90,
        counterclock=False,
        wedgeprops={
            "width": ring_width,
            "edgecolor": bg_color
        }
    )

# 百分比放在每根玉玦末端，全部独立以90°作为起点，不接力
start_angle_fixed = 80
for r, pct, c in zip(radii, percents, colors):
    sweep = pct * scale
    end_angle = start_angle_fixed - sweep
    ang_rad = np.radians(end_angle)
    txt_r = r - ring_width / 2
    tx = txt_r * np.cos(ang_rad)
    ty = txt_r * np.sin(ang_rad)
    ax.text(tx, ty, f"{pct}%", color="white", ha="center", va="center", fontsize=30)


# 分类标签：放到环起点附近，竖直并列排列
# 注意：这里不再跟随角度，只做文字位置调整
label_x = -0.53
label_y_start = 1.20
label_dy = 0.22

for i, lab in enumerate(labels):
    ax.text(
        label_x,
        label_y_start - i * label_dy,
        lab,
        color="white",
        va="center",
        fontsize=30
    )


fig.text(-0.03, 1.20, "2022年上半年年龄分布", fontsize=40, color="white", weight="bold")
fig.text(-0.03, 1.12, "公司平均年龄32.5，23-30员工比例最高", fontsize=35, color="white")
fig.text(-0.03,-0.11, "*注: 数据来源于公司人力资源系统，统计日期截至2022.06.30",
         fontsize=25, color="#dddddd")

ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect("equal")
ax.axis("off")
plt.tight_layout()
plt.show()
