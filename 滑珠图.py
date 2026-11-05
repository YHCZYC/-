import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np

# ---------------------- 数据 ----------------------
regions = ["华南", "华北", "东北", "西北", "华东"]
rates = [0.86, 0.74, 0.62, 0.51, 0.35]

bg_color = "#191c40"
fill_color = "#0077cc"
bar_bg_color = "#66697c"

bar_height = 0.34
round_radius = bar_height / 2          # 标准胶囊半圆端头
circle_r = 0.023                       # 珠子在x轴单位中的半径
core_ratio = 0.72

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(14, 7), dpi=120)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

y_pos = np.arange(len(regions))

ax.set_ylim(-0.5, len(regions) - 0.5)
ax.set_yticks(y_pos)
ax.set_yticklabels(regions, color="white", fontsize=13)
ax.set_xlim(0, 1.08)
ax.set_xticks([])
ax.spines[:].set_visible(False)

# 不使用 set_aspect("equal")，也不使用 blended_transform
# 珠子正圆靠固定 xlim + Circle 在 transData 中按 x 单位绘制

for y, rate in zip(y_pos, rates):

    # ---------- 灰色底层胶囊条 ----------
    gray_bar = FancyBboxPatch(
        (0, y - bar_height / 2),
        1.0,
        bar_height,
        boxstyle=f"round,pad=0,rounding_size={round_radius}",
        color=bar_bg_color,
        alpha=0.7,
        zorder=1
    )
    ax.add_patch(gray_bar)

    # ---------- 蓝色进度胶囊条 ----------
    blue_bar = FancyBboxPatch(
        (0, y - bar_height / 2),
        rate,
        bar_height,
        boxstyle=f"round,pad=0,rounding_size={round_radius}",
        color=fill_color,
        zorder=2
    )
    ax.add_patch(blue_bar)

    # ---------- 百分比文字 ----------
    ax.text(
        rate - 0.042,
        y,
        f"{rate:.0%}",
        color="white",
        fontsize=11,
        ha="right",
        va="center",
        zorder=3
    )

    # ---------- 滑珠：白外圈 + 蓝内芯 ----------
    outer_circle = Circle(
        (rate, y),
        circle_r,
        color="white",
        zorder=4
    )
    inner_circle = Circle(
        (rate, y),
        circle_r * core_ratio,
        color=fill_color,
        zorder=5
    )

    ax.add_patch(outer_circle)
    ax.add_patch(inner_circle)

# ---------- 标题与注释 ----------
fig.text(0.11, 0.93, "2022年上半年产品销量目标达成率情况", color="white", fontsize=21, weight="bold")
fig.text(0.11, 0.87, "华南完成率最高达到86%，华东最低35%", color="white", fontsize=13)
fig.text(0.11, 0.05, "*注：数据来源于公司销售系统，统计日期截至2022.06.30", color="white", fontsize=10)

plt.tight_layout()
plt.subplots_adjust(top=0.80, bottom=0.10, left=0.08, right=0.94)
plt.show()
