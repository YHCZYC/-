import matplotlib.pyplot as plt
import numpy as np

# ---------------------- 数据 ----------------------
regions = ["华东","西北", "东北", "华北", "华南"]
sales_2022 = np.array([1215, 1321, 1426, 1531, 2238])
sales_2021 = np.array([1003, 1256, 1531, 1436, 2066])
y_pos = np.arange(len(regions))
bar_height = 0.52
gap = 600

# ---------------------- 画布设置 ----------------------
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(14, 9), dpi=120)
fig.patch.set_facecolor('#171e3f')
ax.set_facecolor('#171e3f')

# ---------------------- 标题：放大1.5倍 ----------------------
ax.text(-4600, 5.42, "2022年上半年各区域对比去年销量",
        color='white', fontsize=27, weight='bold')
ax.text(-4600, 5.05, "2022年整体销量高于2021年，只有东北区域较2021有所下降",
        color='white', fontsize=19.5)

# ---------------------- 年份文字 ----------------------
ax.text(-1700, 4.72, "2022", color="#3478d8", fontsize=21, weight='bold', ha='center')
ax.text(1700, 4.72, "2021", color="#dd4466", fontsize=21, weight='bold', ha='center')

# ---------------------- 绘制柱子 ----------------------
bars_2022 = ax.barh(y_pos, -sales_2022, left=-gap, height=bar_height, color='#3478d8')
bars_2021 = ax.barh(y_pos, sales_2021, left=gap, height=bar_height, color='#dd4466')

# ---------------------- 中间地区名称：放大1倍 ----------------------
for i, region in enumerate(regions):
    ax.text(0, y_pos[i], region,
            color='white', fontsize=26, ha='center', va='center')

# ---------------------- 销量数字：放大1倍 ----------------------
# 蓝色柱：最左端内侧
for bar in bars_2022:
    bar_left = bar.get_x() + bar.get_width()
    ax.text(bar_left + 30, bar.get_y() + bar.get_height() / 2,
            f"{abs(bar.get_width())}",
            color="white", va='center', ha='left', fontsize=22)

# 红色柱：最右端内侧
for bar in bars_2021:
    bar_right = bar.get_x() + bar.get_width()
    ax.text(bar_right - 30, bar.get_y() + bar.get_height() / 2,
            f"{bar.get_width()}",
            color="white", va='center', ha='right', fontsize=22)

# ---------------------- 蝴蝶图整体缩小1.5倍 ----------------------
ax.set_xlim(-4600, 4600)
ax.set_ylim(-0.7, 4.55)

ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# ---------------------- 左下角注释：放大1倍 ----------------------
ax.text(-4600, -0.62,
        "*注: 数据来源于公司销售系统，统计日期截至2022.06.30",
        color='white', fontsize=18)

plt.tight_layout()
plt.show()
