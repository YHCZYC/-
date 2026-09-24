import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

products = ["口红", "面膜", "隔离", "防晒", "精华", "面霜", "眼影", "气垫"]
sales = [9221, 5102, 6571, 5760, 6321, 8612, 2645, 5321]
bar_colors = [
    "#82bbc8",
    "#4e8c84",
    "#e06b4e",
    "#f7bc2c",
    "#0099dd",
    "#0066bb",
    "#5555bb",
    "#444499"
]

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(13, 7.5), dpi=130)
bg_color = "#202940"
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

bars = ax.bar(products, sales, color=bar_colors, width=0.62)

for bar, value, color in zip(bars, sales, bar_colors):
    height = bar.get_height()
    x_pos = bar.get_x() + bar.get_width() / 2

    box_y = height + 320

    txt = ax.text(
        x_pos,
        box_y,
        f"{value}",
        ha="center",
        va="center",
        color="white",
        fontsize=9,
        fontweight="bold",
        bbox=dict(
            boxstyle="round,pad=0.32",
            fc=color,
            ec="none"
        )
    )

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bbox = txt.get_window_extent(renderer)

    inv = ax.transData.inverted()
    left, bottom = inv.transform((bbox.x0, bbox.y0))
    right, top = inv.transform((bbox.x1, bbox.y1))

    # 小倒三角：只在标签框底部中心出现一次
    tri_x = [x_pos - 0.06, x_pos + 0.06, x_pos]
    tri_y = [bottom, bottom, bottom - 0.35]

    triangle = Polygon(
        list(zip(tri_x, tri_y)),
        closed=True,
        facecolor=color,
        edgecolor="none"
    )
    ax.add_patch(triangle)

ax.set_ylim(0, 10800)
ax.set_yticks([0, 2000, 4000, 6000, 8000, 10000])
ax.tick_params(axis='both', colors='white', labelsize=10)
ax.grid(axis='y', linestyle='--', alpha=0.3, color="#cccccc")
ax.set_axisbelow(True)
for spine in ax.spines.values():
    spine.set_visible(False)

plt.figtext(0.042, 0.97, "2021年商品销量情况", fontsize=24, weight="bold", color="white", ha="left")
plt.figtext(0.042, 0.922, "口红销量最好达9221，是眼影最低值2645近3.5倍", fontsize=14, color="white", ha="left")
plt.figtext(0.5, 0.032, "*注：数据来源于公司销售系统，统计日期截至2022.08.31", fontsize=9, color="#cccccc", ha="center")

plt.tight_layout()
plt.subplots_adjust(top=0.85, bottom=0.11, left=0.05, right=0.97)

plt.show()
