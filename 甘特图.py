import matplotlib.pyplot as plt

plt.close('all')

date_positions = {
    "2022/3/1": 0,
    "2022/3/16": 1,
    "2022/3/31": 2,
    "2022/4/15": 3,
    "2022/4/30": 4,
    "2022/5/15": 5,
    "2022/5/30": 6,
    "2022/6/14": 7,
}

task_data = [
    {"name": "制定计划", "start_x": 0,    "width": 0.8,  "pct": 51},
    {"name": "方案设计", "start_x": 0.9,  "width": 0.7,  "pct": 32},
    {"name": "资源调配", "start_x": 1.8,  "width": 0.65, "pct": 21},
    {"name": "第一阶段", "start_x": 2.4,  "width": 0.85, "pct": 85},
   {"name": "第二阶段", "start_x": 3.65, "width": 1.2,  "pct": 36},
    {"name": "第三阶段", "start_x": 5.05, "width": 0.65, "pct": 68},
    {"name": "项目总结", "start_x": 6.1,  "width": 0.6,  "pct": 68},
]

c1 = "#00b8f2"
c2 = "#0066cc"
bg_color = "#192040"

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(14, 8), dpi=120)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

y_ticks = list(range(len(task_data)))

# ---------------------- 关键：条形长度整体缩短一倍，但高度不变 ----------------------
scale = 0.5

for y, task in enumerate(task_data):
    s = task["start_x"] * scale
    w = task["width"] * scale
    pct = task["pct"]
    done_w = w * pct / 100

    ax.barh(y, done_w, left=s, height=0.6, color=c1)
    ax.barh(y, w - done_w, left=s + done_w, height=0.6, color=c2)

    # 百分比写在每个彩条中间
    cx = s + w / 2
    ax.text(cx, y, f"{pct}%", color="white", ha="center", va="center", fontsize=22)

ax.set_yticks(y_ticks)
ax.set_yticklabels([item["name"] for item in task_data], color="white", fontsize=26)
ax.invert_yaxis()

# x轴同步缩小，保证条形不会被挤变形
ax.set_xlim(-0.1, 3.7)

# ---------------------- 顶部日期放大一倍，对准虚线 ----------------------
for date_str, x_pos in date_positions.items():
    ax.text(x_pos * scale, -0.42, date_str, color="white", ha="center", fontsize=22)

ax.set_xticks([])
ax.tick_params(axis='x', bottom=False, labelbottom=False)

# 垂直虚线同步缩小
for _, x_pos in date_positions.items():
    ax.axvline(x=x_pos * scale, linestyle="--", color="#606880", lw=0.8)

for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(axis="y", length=0)

# 标题字号放大一倍
fig.suptitle("2022年化妆品类目采购项目进度", color="white", fontsize=44, weight="bold", y=0.96)

plt.subplots_adjust(left=0.07, bottom=0.12, right=0.96, top=0.88)

plt.show()
