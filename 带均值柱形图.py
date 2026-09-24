import matplotlib.pyplot as plt

# ---------------------- 1. 数据 ----------------------
regions = ["华北", "华南", "东北", "西北", "西南", "华东"]
sales = [2354, 1902, 3524, 2698, 2896, 2563]
avg_value = 2656  # 平均值

# ---------------------- 2. 全局中文设置 ----------------------
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# ---------------------- 3. 创建画布、背景颜色 ----------------------
fig, ax = plt.subplots(figsize=(13, 8), dpi=120)
bg_color = "#192040"
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# ---------------------- 4. 绘制柱状图 ----------------------
bar_color = "#0077dd"
bars = ax.bar(regions, sales, color=bar_color, width=0.55)

# 在每个柱子上方标注数值
for bar in bars:
    h = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width()/2,
        h + 45,
        str(h),
        ha="center", va="bottom", color="white", fontsize=11
    )

# ---------------------- 5. 绘制黄色平均值水平线 + 文字标注 ----------------------
ax.axhline(y=avg_value, color="#ffdd00", linewidth=2)
# 在最右侧标注平均值文字
ax.text(5.15, avg_value + 45, f"平均值：{avg_value}", color="#ffdd00", fontsize=11)

# ---------------------- 6. 坐标轴样式 ----------------------
ax.set_ylim(0, 4100)
ax.set_yticks([0, 1000, 2000, 3000, 4000])
ax.tick_params(axis="x", colors="white", labelsize=11)
ax.tick_params(axis="y", colors="white", labelsize=11)

# 水平虚线网格
ax.yaxis.grid(True, linestyle="--", alpha=0.35, color="#cccccc")
ax.set_axisbelow(True)

# 隐藏所有边框
for spine in ax.spines.values():
    spine.set_visible(False)
# 保留底部白色基线（和原图一致）
ax.spines["bottom"].set_visible(True)
ax.spines["bottom"].set_color("white")

# ---------------------- 7. 标题、副标题、底部注释 ----------------------
ax.text(0.02, 0.94, "3月各区域销量分布", transform=ax.transAxes,
        fontsize=24, color="white", weight="bold")
ax.text(0.02, 0.87, "东北销量最多占比总销量的22%，华南销量最低", transform=ax.transAxes,
        fontsize=16, color="white")

plt.figtext(0.03, 0.06, "*注：数据来源于公司销售系统，统计日期截至2022.03.31",
            color="#dddddd", fontsize=9.5)

plt.tight_layout()
plt.show()
