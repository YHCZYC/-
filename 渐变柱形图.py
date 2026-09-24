import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# ===================== 渐变绘图函数 =====================
def gradient_image(ax, extent, direction=0.3, cmap_range=(0, 1), **kwargs):
    phi = direction * np.pi / 2
    v = np.array([np.cos(phi), np.sin(phi)])
    X = np.array([[v @ [1, 0], v @ [1, 1]],
                  [v @ [0, 0], v @ [0, 1]]])
    a, b = cmap_range
    X = a + (b - a) / X.max() * X
    im = ax.imshow(X, interpolation='bicubic', extent=extent,
                   clim=(0, 1), aspect='auto', **kwargs)
    return im

def gradient_bar(ax, x, y, width=0.5):
    # 自定义蓝渐变：底部浅蓝 #00ccff → 顶部深蓝 #004499（匹配原图）
    cmap = LinearSegmentedColormap.from_list("bar_blue", ["#00ccff", "#004499"])
    for left, top in zip(x, y):
        right = left + width
        gradient_image(ax, extent=(left, right, 0, top),
                       cmap=cmap, cmap_range=(0.1,0.9))

# ===================== 数据准备 =====================
regions = ["华北", "华南", "东北", "西北", "西南", "华东"]
sales = [2354, 1902, 3524, 2698, 2896, 2563]
x_pos = np.arange(len(regions))
bar_width = 0.55

# ===================== 画布基础设置 =====================
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(figsize=(12,8), dpi=120)
bg_color = "#1a2040"
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 绘制渐变柱子
gradient_bar(ax, x_pos, sales, width=bar_width)

# ===================== 柱子顶部数字标注 =====================
for idx, val in enumerate(sales):
    ax.text(x_pos[idx], val + 48, str(val),
            ha="center", va="bottom", color="white", fontsize=11)

# ===================== 坐标轴、网格线 =====================
ax.set_xticks(x_pos)
ax.set_xticklabels(regions, color="white", fontsize=11)
ax.set_ylim(0,4100)
ax.set_yticks([0,1000,2000,3000,4000])
ax.tick_params(axis="y", colors="white", labelsize=11)

ax.yaxis.grid(True, linestyle="--", alpha=0.35, color="#cccccc")
ax.set_axisbelow(True)
# 隐藏边框
for spine in ax.spines.values():
    spine.set_visible(False)

# ===================== 标题、副标题、底部注释 =====================
ax.text(0.02,0.94,"3月各区域销量分布",transform=ax.transAxes,
        fontsize=24, weight="bold", color="white")
ax.text(0.02,0.87,"东北销量最多占比总销量的22%，华南销量最低",transform=ax.transAxes,
        fontsize=16, color="white")

plt.figtext(0.03,0.06,"*注：数据来源于公司销售系统，统计日期截至2022.03.31",
            color="#dddddd", fontsize=9.5)

plt.tight_layout()
plt.show()
