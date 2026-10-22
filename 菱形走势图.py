import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ---------------------- 数据 ----------------------
month_labels = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月"]
rate = np.array([0.536, 0.498, 0.527, 0.708, 0.609, 0.496, 0.586, 0.704])
rate_text = ["53.60%", "49.80%", "52.70%", "70.80%", "60.90%", "49.60%", "58.60%", "70.40%"]
x_raw = np.arange(len(month_labels))

# 配色
bg_color = "#1a1a40"
stem_color = "#ee6043"

fig, ax = plt.subplots(figsize=(13, 8), dpi=120)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# -------- 核心：手动画竖线 + 空心菱形，避免线条穿过菱形 --------
marker_size = 0.021  # 菱形对应的高度偏移，控制竖线截止位置
# 1. 画竖线：从y=0 画到 y=rate - marker_size（不到菱形中心）
ax.vlines(x=x_raw, ymin=0, ymax=rate - marker_size, color=stem_color, lw=2)
# 2. 单独绘制空心菱形
ax.scatter(x_raw, rate, marker="D", s=110, facecolor="none", edgecolor=stem_color, linewidth=2)

# 在菱形上方标注百分比文字
for xi, yi, txt in zip(x_raw, rate, rate_text):
    ax.text(xi, yi + 0.022, txt, color="white", ha="center", fontsize=14)

# X轴
ax.set_xticks(x_raw)
ax.set_xticklabels(month_labels, color="white", fontsize=14)

# Y轴：隐藏刻度
ax.set_ylim(0, 0.85)
ax.set_yticks([])

# 底部白色基线
ax.hlines(y=0, xmin=-0.5, xmax=7.5, color="white", lw=1.2)

# 隐藏所有边框
for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(axis="y", length=0)

# 标题、副标题
fig.text(0.045, 0.94, "2022年1-8月公司计划完成率", color="white", fontsize=32, weight="bold")
fig.text(0.045, 0.86, "公司整体完成率55%，4月和8月超过70%，2月和6月较低未过半", color="white", fontsize=20)

# 底部注释
fig.text(0.045, 0.008, "*注: 数据来源于公司销售系统，统计日期截至2022.08.31", color="white", fontsize=12)

plt.subplots_adjust(left=0.04, right=0.97, top=0.78, bottom=0.14)
plt.show()
