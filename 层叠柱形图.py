import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

quarters = ['2021Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6']
sales = [3121, 4086, 4321, 4601, 4936, 4231]
profit = [1020, 1421, 1502, 1623, 1781, 1432]

bar_width = 0.35
overlap = bar_width / 5
x = np.arange(len(quarters))

fig, ax = plt.subplots(figsize=(14, 9), dpi=120)
bg_color = "#191e44"
color_sales = "#027acc"
color_profit = "#e6374e"

fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

ax.bar(x, sales, width=bar_width, color=color_sales)
ax.bar(x + bar_width - overlap, profit, width=bar_width, color=color_profit)

for i, val in enumerate(sales):
    ax.text(x[i], val + 45, f"{val}", ha="center", va="bottom", color="white", fontsize=11)

for i, val in enumerate(profit):
    ax.text(x[i] + bar_width - overlap, val + 35, f"{val}",
            ha="center", va="bottom", color="white", fontsize=11)

ax.text(2.5, 7200, "2021年至今季度销售额(万)和利润额(万)",
        ha="center", va="bottom", color="white", fontsize=48, weight="bold")
ax.text(2.5, 6600, "2022年第二季度销售额首次出现下降，降幅达到15%",
        ha="center", va="bottom", color="white", fontsize=32)

ax.set_ylim(0, 8000)
ax.set_xticks(x)
ax.set_xticklabels(quarters, color="white", fontsize=11)
ax.set_yticks([])

for spine in ax.spines.values():
    spine.set_visible(False)

plt.subplots_adjust(bottom=0.18)
plt.figtext(0.02, 0.08, "*注：数据来源于公司销售系统，统计日期截至2022.06.30",
            color="#dddddd", fontsize=9.5)

# ========== 放到蓝色柱中部：按 4231 柱高估算，约在 2100 附近 ==========
last_x = x[-1]

ax.text(last_x, 2300, "销售额",
        ha="center", va="center", color="white", fontsize=13, weight="bold",
        bbox=dict(boxstyle="square,pad=0.45",
                  edgecolor=color_sales,
                  facecolor=bg_color,
                  alpha=1))

ax.text(last_x, 1850, "利润额",
        ha="center", va="center", color="white", fontsize=13, weight="bold",
        bbox=dict(boxstyle="square,pad=0.45",
                  edgecolor=color_profit,
                  facecolor=bg_color,
                  alpha=1))

plt.show()
