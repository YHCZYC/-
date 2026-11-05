import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# ---------------------- 数据 ----------------------
months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
month_sales = [2354, 1902, 3524, 2698, 2896, 2563, 3156, 2896, 3621, 2635, 2963, 2789]
quarter_sales = [7780, 8157, 9673, 8387]
# 季度背景色，和样图保持一致
quarter_colors = ["#242860", "#5c2c3c", "#4b3838", "#462850"]
# 每个季度内部月份柱子颜色
month_colors = [
    "#4455cc", "#4455cc", "#4455cc",
    "#ff6622", "#ff6622", "#ff6622",
    "#ffaa22", "#ffaa22", "#ffaa22",
    "#993377", "#993377", "#993377"
]
bg_color = "#191c40"

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(14, 8), dpi=120)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

x = np.arange(len(months))
bar_width = 0.22

# 月度小柱子
bars_month = ax.bar(x, month_sales, width=bar_width, color=month_colors, zorder=3)

# 月度柱子顶部标注数字
for b in bars_month:
    h = b.get_height()
    ax.text(b.get_x() + b.get_width()/2, h + 70, f"{int(h)}", color="white", ha="center", va="bottom", fontsize=10)

ax.set_xticks(x)
ax.set_xticklabels(months, color="white", fontsize=11)
ax.set_ylim(0, 10500)
ax.set_yticks([])
ax.spines["bottom"].set_color("#666677")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.grid(False)

# 四个季度背景色块 + 季度总量文字
q_info = [
    {"x_start": -0.4, "x_end": 2.4, "val":7780, "color":quarter_colors[0]},
    {"x_start": 2.6, "x_end": 5.4, "val":8157, "color":quarter_colors[1]},
    {"x_start": 5.6, "x_end": 8.4, "val":9673, "color":quarter_colors[2]},
    {"x_start": 8.6, "x_end": 11.4, "val":8387, "color":quarter_colors[3]},
]

for q in q_info:
    w = q["x_end"] - q["x_start"]
    rect = Rectangle((q["x_start"], 0), w, q["val"], color=q["color"], alpha=0.85, zorder=1)
    ax.add_patch(rect)
    cx = (q["x_start"] + q["x_end"]) / 2
    ax.text(cx, q["val"] + 120, f"{q['val']}", color="white", ha="center", va="bottom", fontsize=13)

# 标题、副标题、底部注释
fig.text(0.05, 0.92, "2021年各月化妆品销量走势", color="white", fontsize=30, weight="bold")
fig.text(0.05, 0.85, "2021年第三季度销量最多9673，9月单月销量最大3621", color="white", fontsize=20)
fig.text(0.05, 0.06, "*注：数据来源于公司销售系统，统计日期截至2021.12.31", color="white", fontsize=10)

plt.tight_layout()
plt.subplots_adjust(top=0.78, bottom=0.12, left=0.05, right=0.95)
plt.show()
