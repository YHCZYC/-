import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.lines import Line2D
import numpy as np

# ===================== 数据 =====================
regions   = ["华南", "华北", "东北", "西北", "华东"]
rate2022  = [0.86, 0.74, 0.62, 0.51, 0.35]
rate2021  = [0.92, 0.69, 0.53, 0.39, 0.45]

bg_color      = "#191c40"
color_2022    = "#0077cc"
color_2021    = "#888890"
bar_bg_color  = "#606370"

bar_height    = 0.32
round_radius  = bar_height / 2
circle_r      = 0.022
core_ratio    = 0.72

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

for y, r22, r21 in zip(y_pos, rate2022, rate2021):

    # 灰色底层胶囊条
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

    # 蓝色2022进度胶囊条
    blue_bar = FancyBboxPatch(
        (0, y - bar_height / 2),
        r22,
        bar_height,
        boxstyle=f"round,pad=0,rounding_size={round_radius}",
        color=color_2022,
        zorder=2
    )
    ax.add_patch(blue_bar)

    # 2022 百分比文字
    ax.text(
        r22 + 0.018,
        y,
        f"{r22:.0%}",
        color="white",
        fontsize=11,
        ha="left",
        va="center",
        zorder=3
    )

    # 2022 滑珠：白外圈 + 蓝芯
    outer22 = Circle((r22, y), circle_r, color="white", zorder=4)
    inner22 = Circle((r22, y), circle_r * core_ratio, color=color_2022, zorder=5)
    ax.add_patch(outer22)
    ax.add_patch(inner22)

    # 2021 参考圆点：白外圈 + 灰芯
    outer21 = Circle((r21, y), circle_r, color="white", zorder=4)
    inner21 = Circle((r21, y), circle_r * core_ratio, color=color_2021, zorder=5)
    ax.add_patch(outer21)
    ax.add_patch(inner21)


# ===================== 顶部横向图例 =====================
legend_elements = [
    Line2D([0], [0], marker='o', color=bg_color, markerfacecolor=color_2022,
           markeredgecolor="white", markersize=11, label="2022完成率"),
    Line2D([0], [0], marker='o', color=bg_color, markerfacecolor=color_2021,
           markeredgecolor="white", markersize=11, label="2021完成率")
]

leg = ax.legend(
    handles=legend_elements,
    loc="upper center",
    bbox_to_anchor=(0.12, 1.02),
    ncol=2,
    frameon=False,
    labelcolor="white",
    fontsize=11
)

# ===================== 标题、注释 =====================
fig.text(0.11, 0.96, "2022年上半年销量目标达成率同比去年情况", color="white", fontsize=21, weight="bold")
fig.text(0.11, 0.91, "华南完成率最高达到86%，华东最低35%，其中华南和华东不及2021年", color="white", fontsize=12)
fig.text(0.11, 0.05, "*注：数据来源于公司销售系统，统计日期截至2022.06.30", color="white", fontsize=10)

plt.tight_layout()
plt.subplots_adjust(top=0.76, bottom=0.10, left=0.08, right=0.94)
plt.show()
