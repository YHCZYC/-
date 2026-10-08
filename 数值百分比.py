import matplotlib.pyplot as plt
import numpy as np

# ---------------------- 数据 ----------------------
regions = ["华东", "西南", "西北", "东北", "华南", "华北"]
sales_raw = np.array([2109, 1369, 1872, 1536, 1946, 4321])
pct_text = np.array(["-5.8%", "-17.9%", "-15.9%", "-9.3%", "-20.8%", "-13.6%"])

total_length = 100
red_width = 10
sales_norm = sales_raw / sales_raw.max() * (total_length - red_width)
light_blue_width = (total_length - red_width) - sales_norm

# 反转顺序，保证视觉从上到下为华东、西南、西北、东北、华南、华北
regions = regions[::-1]
sales_norm = sales_norm[::-1]
light_blue_width = light_blue_width[::-1]
pct_text = pct_text[::-1]

y_pos = np.arange(len(regions))
bar_height = 0.6

# ---------------------- 画布设置 ----------------------
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig, ax = plt.subplots(figsize=(14, 8), dpi=120)
bg_color = "#192348"
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# ---------------------- 标题：放大1.5倍 ----------------------
ax.text(-12, 6.4, "2021年各区域销量及同比情况",
        color='white', fontsize=39, weight='bold')
ax.text(-12, 5.85, "各区域商品销量同比去年均有下降，其中华南下降最多，同比下降20.8%",
        color='white', fontsize=21)

# ---------------------- 绘制三段水平条形 ----------------------
bar_dark = ax.barh(y_pos, sales_norm, height=bar_height, color="#143470")
bar_light = ax.barh(y_pos, light_blue_width, left=sales_norm,
                    height=bar_height, color="#82a8d6")
bar_red = ax.barh(y_pos, red_width, left=sales_norm + light_blue_width,
                  height=bar_height, color="#923b4b")

# ---------------------- 地区名称：放大1倍 ----------------------
for i, region in enumerate(regions):
    ax.text(-3, y_pos[i], region,
            color="white", fontsize=28, va="center", ha="right")

# ---------------------- 深蓝销量数字：放大1倍，放在深蓝最右侧 ----------------------
for i, bar in enumerate(bar_dark):
    w = bar.get_width()
    y = bar.get_y() + bar.get_height() / 2
    ax.text(w - 1.2, y, f"{sales_raw[::-1][i]}",
            color="white", fontsize=26, va="center", ha="right")

# ---------------------- 红色百分比：放大1倍，红色块内居中 ----------------------
for i in range(len(y_pos)):
    x_start = sales_norm[i] + light_blue_width[i]
    x_center = x_start + red_width / 2
    ax.text(x_center, y_pos[i], pct_text[i],
            color="white", fontsize=26, va="center", ha="center")

# ---------------------- 底部注释：放大1倍 ----------------------
ax.text(-12, -0.65,
        "*注: 数据来源于公司销售系统，统计日期截至2022.01.01",
        color="white", fontsize=22)

# ---------------------- 整体缩小约1.5倍：扩大xlim和ylim给图表更多留白 ----------------------
ax.set_xlim(-12, total_length + 8)
ax.set_ylim(-0.7, 5.7)

ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.show()
