import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# ---------------------- 数据 ----------------------
goods = ["口红", "面膜", "隔离", "防晒", "精华"]
sales_2021 = np.array([3568, 4135, 4436, 4106, 4936])
sales_2022 = np.array([2569, 3241, 2965, 3209, 3541])
diff = np.array([999, 894, 1471, 897, 1395])

bar_width = 0.35
x = np.arange(len(goods))

# ---------------------- 画布设置 ----------------------
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig, ax = plt.subplots(figsize=(14, 8), dpi=120)
bg_color = "#192348"
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# ---------------------- 绘制两组柱子 ----------------------
bar_21 = ax.bar(x - bar_width/2, sales_2021, width=bar_width, color="#1468c2", zorder=3)
bar_22 = ax.bar(x + bar_width/2, sales_2022, width=bar_width, color="#82a8d6", zorder=3)

# ---------------------- 深蓝色柱顶数值 ----------------------
for bar in bar_21:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 120,
            f"{h}", ha="center", va="bottom", color="white", fontsize=11, zorder=6)

# ---------------------- 浅蓝色柱数值：放在柱形内部靠上位置 ----------------------
for bar in bar_22:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h - 180,
            f"{h}", ha="center", va="top", color="white", fontsize=11, zorder=6)

# ---------------------- 蓝色水平连线 ----------------------
for i in range(len(x)):
    bar_right_x = x[i] - bar_width/2 + bar_width
    arrow_x = x[i] + bar_width/2
    y_level = sales_2021[i]
    ax.plot([bar_right_x, arrow_x], [y_level, y_level], color="#1468c2", lw=3, zorder=5)

# ---------------------- 白色箭头：自下往上指，差值数字放在箭头右侧 ----------------------
for i in range(len(x)):
    x_center = x[i] + bar_width / 2
    y_bottom = sales_2022[i]
    y_top = sales_2021[i]
    y_mid = (y_bottom + y_top) / 2

    ax.annotate("",
                xy=(x_center, y_top),
                xytext=(x_center, y_bottom),
                arrowprops=dict(arrowstyle="->", color="white", lw=2), zorder=6)

    ax.text(x_center + 0.045, y_mid, f"{diff[i]}",
            ha="left", va="center", color="white", fontsize=11, zorder=6)

# ---------------------- X轴设置，柱子紧贴y=0轴线 ----------------------
ax.set_xticks(x)
ax.set_xticklabels(goods, color="white", fontsize=12)
ax.set_xlim(-0.6, len(x)-0.4)
ax.set_ylim(0, 6000)
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color("white")

# ---------------------- 标题：拉大两行标题间距 ----------------------
ax.text(0, 1.18, "2022年商品对比去年销售情况",
        transform=ax.transAxes, color="white", fontsize=36, weight="bold")
ax.text(0, 1.08, "商品整体比去年销量有所下降，其中隔离下降最多，下降33%",
        transform=ax.transAxes, color="white", fontsize=20)

# ---------------------- 图例：横向并排两个小正方形 ----------------------
square_size = 0.013
base_y = 0.975
x0 = 0.003

rect1 = Rectangle((x0, base_y), width=square_size, height=square_size, color="#1468c2", transform=ax.transAxes)
ax.add_patch(rect1)
ax.text(x0 + square_size + 0.005, base_y + square_size/2, "2021销量",
        transform=ax.transAxes, color="white", fontsize=11, va="center")

x1 = x0 + square_size + 0.09
rect2 = Rectangle((x1, base_y), width=square_size, height=square_size, color="#82a8d6", transform=ax.transAxes)
ax.add_patch(rect2)
ax.text(x1 + square_size + 0.005, base_y + square_size/2, "2022销量",
        transform=ax.transAxes, color="white", fontsize=11, va="center")

# ---------------------- 底部注释：缩小一倍 ----------------------
ax.text(0, -0.14,
        "*注: 数据来源于公司销售系统，统计日期截至2022.01.01",
        transform=ax.transAxes, color="white", fontsize=11, va="top")

# ---------------------- 整体图表主体缩小1.5倍 ----------------------
ax.set_position([0.22, 0.22, 0.52, 0.52])

plt.show()
