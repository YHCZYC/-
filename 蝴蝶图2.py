import matplotlib.pyplot as plt
import numpy as np

# ---------------------- 数据 ----------------------
regions = ["华东", "西北", "东北", "华北", "华南"]
pct_2022 = np.array([0.36, 0.31, 0.18, 0.13, 0.09])
pct_2021 = np.array([0.42, 0.26, 0.19, 0.12, 0.05])

# 反转顺序，保证视觉从上到下为 华东、西北、东北、华北、华南
regions = regions[::-1]
pct_2022 = pct_2022[::-1]
pct_2021 = pct_2021[::-1]

y_pos = np.arange(len(regions))
bar_height = 0.55
gap = 0.08   # 蓝红之间间隔加大，容纳更大的地区文字

# ---------------------- 画布设置 ----------------------
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(12, 8), dpi=120)
fig.patch.set_facecolor('#192348')
ax.set_facecolor('#192348')

# ---------------------- 左上角标题：放大1.5倍 ----------------------
ax.text(-0.78, 5.2, "2022年第一季度销售目标完成情况",
        color='white', fontsize=33, weight='bold')
ax.text(-0.78, 4.8, "华东区域完成率最高达到36%，但是相比去年的42%有所下降",
        color='white', fontsize=21)

# ---------------------- 绘制蝴蝶图 ----------------------
bars_2022 = ax.barh(y_pos, -pct_2022, left=-gap,
                    height=bar_height, color="#2778d8")
bars_2021 = ax.barh(y_pos, pct_2021, left=gap,
                    height=bar_height, color="#dd4466")

# ---------------------- 中间地区名称：放大1倍 ----------------------
for i, region in enumerate(regions):
    ax.text(0, y_pos[i], region,
            color='white', fontsize=26, ha='center', va='center')

# ---------------------- 百分比数字：放大1倍 ----------------------
# 蓝色 2022：放在蓝色柱最左侧内部
for bar in bars_2022:
    bar_left = bar.get_x() + bar.get_width()
    val = abs(bar.get_width())
    ax.text(bar_left - 0.018, bar.get_y() + bar.get_height() / 2,
            f"{val:.0%}", color="white", va='center', ha='right', fontsize=24)

# 红色 2021：放在红色柱最右侧内部
for bar in bars_2021:
    bar_right = bar.get_x() + bar.get_width()
    val = bar.get_width()
    ax.text(bar_right + 0.018, bar.get_y() + bar.get_height() / 2,
            f"{val:.0%}", color="white", va='center', ha='left', fontsize=24)

# ---------------------- 蝴蝶图整体缩小约1.5倍 ----------------------
ax.set_xlim(-0.78, 0.78)
ax.set_ylim(-0.6, 4.6)

ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# ---------------------- 底部注释：放大1倍 ----------------------
ax.text(-0.78, -0.5,
        "*注: 数据来源于公司销售系统，统计日期截至2022.03.31",
        color='white', fontsize=20)

plt.tight_layout()
plt.show()
