import matplotlib.pyplot as plt
import numpy as np

# ---------------------- 数据 ----------------------
goods = ["口红", "面膜", "隔离", "防晒", "精华", "面霜"]
actual = np.array([653, 523, 648, 856, 714, 785])
target = np.array([700, 500, 600, 900, 600, 600])

# ---------------------- 全局字体设置 ----------------------
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(14, 9), dpi=120)
bg_color = "#191c40"
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

x = np.arange(len(goods))
bar_width_target = 0.35    # 空心目标框 保持原来宽度不变
bar_width_actual = 0.18   # 蓝色实柱 窄一半

# 目标销量：空心框
bar_target = ax.bar(x, target, width=bar_width_target, fill=False, edgecolor="#cccccc", linewidth=1.4, zorder=1)
# 实际销量：实心蓝色柱，居中
bar_actual = ax.bar(x, actual, width=bar_width_actual, color="#007acc", zorder=2)

# X轴商品名称
ax.set_xticks(x)
ax.set_xticklabels(goods, color="white", fontsize=12)
ax.tick_params(axis='y', colors="white", labelsize=10)
ax.set_ylim(0, 950)

# 标注实际销量数字
for bar in bar_actual:
    h = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        h + 18,
        f"{int(h)}",
        ha="center", va="bottom", color="white", fontsize=11
    )

# 隐藏边框
for spine in ax.spines.values():
    spine.set_visible(False)
    
ax.set_yticks([])        # 彻底隐藏左侧刻度数字
ax.tick_params(axis='y', left=False)   # 隐藏左侧刻度线
ax.grid(False)

# ---------------------- 标题、副标题（独立顶部靠左） ----------------------
fig.text(0.04, 0.93, "2022年上半年各商品销量完成情况", color="white", fontsize=28, weight="bold")
fig.text(0.04, 0.87, "防晒整体销量最好，达到856，面霜远超目标，超额完成30%", color="white", fontsize=14)

from matplotlib.lines import Line2D
legend_items = [
    Line2D([], [], marker='s', linestyle='', markerfacecolor=bg_color, markeredgecolor="#cccccc", markersize=12, label="目标销量"),
    Line2D([], [], marker='s', linestyle='', markerfacecolor="#007acc", markersize=12, label="实际销量")
]
ax.legend(handles=legend_items,
          loc="upper left",
          bbox_to_anchor=(0.00, 0.90),
          ncol=2,
          frameon=False,
          labelcolor="white",
          fontsize=11,
          handletextpad=0.6)



# 底部注释
fig.text(0.04, 0.06, "*注：数据来源于公司销售系统，统计日期截至2022.06.30", color="white", fontsize=11)

plt.subplots_adjust(top=0.82, bottom=0.14, left=0.07, right=0.96)
plt.show()
