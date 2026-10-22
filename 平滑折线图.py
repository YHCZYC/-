import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from matplotlib.patches import Rectangle

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ---------------------- 原始数据 ----------------------
month_labels = ["5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月", "1月", "2月", "3月"]
x_raw = np.arange(len(month_labels))
# 根据图走势拟合销量数据，峰值1月=3782
y_raw = np.array([150, 220, 310, 400, 490, 600, 780, 760, 3782, 3300, 2950])

# 平滑插值
x_smooth = np.linspace(x_raw.min(), x_raw.max(), 300)
spl = make_interp_spline(x_raw, y_raw, k=3)
y_smooth = spl(x_smooth)

# 配色
bg_color = "#1a1a40"
line_color = "#ee6043"
color_2021 = "#62c8dd"
color_2022 = "#f6bc46"

fig, ax = plt.subplots(figsize=(13, 8), dpi=120)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 绘制平滑曲线
ax.plot(x_smooth, y_smooth, color=line_color, linewidth=2.8)

# 峰值标注 + 垂直虚线
peak_x = 8
peak_y = 3782
ax.text(peak_x, peak_y + 120, "3782", color="white", ha="center", fontsize=14)
ax.vlines(x=peak_x, ymin=0, ymax=peak_y, linestyle="--", color=line_color, lw=1.2)

# X轴
ax.set_xticks(x_raw)
ax.set_xticklabels(month_labels, color="white", fontsize=13)

# ========== 在这里插入基线刻度代码 ==========
trans = ax.get_xaxis_transform()
ax.hlines(y=0, xmin=0, xmax=10, color="white", lw=1.2, transform=trans)
ax.vlines(x=x_raw, ymin=-0.06, ymax=0, color="white", lw=1.4, transform=trans)
mid_points = (x_raw[:-1] + x_raw[1:]) / 2
ax.vlines(x=mid_points, ymin=-0.03, ymax=0, color="white", lw=0.8, transform=trans)
# ==========================================

# Y轴
ax.set_ylim(0, 4200)
ax.set_yticks([0,1000,2000,3000,4000])
ax.set_yticklabels(["0","1,000","2,000","3,000","4,000"], color="#ff8866", fontsize=13)

# 隐藏边框
for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(axis="x", length=0)

# 标题、副标题
fig.text(0.045, 0.94, "化妆品品类月度销量走势", color="white", fontsize=32, weight="bold")
fig.text(0.045, 0.86, "2022年销量迅速增加，1月最高，销量达到3782", color="white", fontsize=20)

# ---------- 底部色块图例（2021 / 2022） ----------
# 2021色块
rect1 = Rectangle((0.072, 0.045), 0.66, 0.055, transform=fig.transFigure, facecolor=color_2021, ec="none")
fig.patches.append(rect1)
fig.text(0.39, 0.053, "2021", color="white", fontsize=16, ha="center")
# 2022色块
rect2 = Rectangle((0.745, 0.045), 0.205, 0.055, transform=fig.transFigure, facecolor=color_2022, ec="none")
fig.patches.append(rect2)
fig.text(0.848, 0.053, "2022", color="white", fontsize=16, ha="center")

# 底部注释
fig.text(0.045, 0.008, "*注: 数据来源于公司销售系统，统计日期截至2022.03.31", color="white", fontsize=12)

plt.subplots_adjust(left=0.04, right=0.97, top=0.78, bottom=0.14)
plt.show()
