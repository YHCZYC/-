import matplotlib.pyplot as plt
import numpy as np

# -------------------- 基础配置 --------------------
VAL = 76
V_MIN = 50
V_MAX = 150
START_DEG = 270
TOTAL_DEG = 270
TICKS = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
COLOR_BANDS = [
    (50, 80, "#008888"),
    (80, 120, "#ffc247"),
    (120, 150, "#f34b5b"),
]
BG = "#191d3a"
BLUE_RING = "#0073c7"

# 【核心】改成减号，顺时针铺开
def val2angle(v):
    ratio = (v - V_MIN) / (V_MAX - V_MIN)
    deg = START_DEG - ratio * TOTAL_DEG
    return np.radians(deg)

# -------------------- 创建画布 --------------------
fig, ax = plt.subplots(figsize=(10,10), subplot_kw={"projection":"polar"})
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_ylim(0, 1.4)
ax.set_yticks([])
ax.grid(False)
ax.spines["polar"].set_visible(False)

# 1. 外层完整蓝色圆环（整圆）
theta_full = np.linspace(0, 2*np.pi, 500)
r_full = np.ones_like(theta_full)
ax.plot(theta_full, r_full, color=BLUE_RING, lw=30, solid_capstyle="round", zorder=0)

# 2. 内层三色270°色带
r_band = 0.82
for v1, v2, c in COLOR_BANDS:
    a1 = val2angle(v1)
    a2 = val2angle(v2)
    theta_seg = np.linspace(a1, a2, 200)
    r_seg = np.full_like(theta_seg, r_band)
    ax.plot(theta_seg, r_seg, color=c, lw=20, solid_capstyle="butt", zorder=1)

# 3. 黑色刻度短线
tick_in_r = 0.70
tick_out_r = 0.93
for t in TICKS:
    ang = val2angle(t)
    ax.plot([ang, ang], [tick_in_r, tick_out_r], c="black", lw=3, zorder=2)

# 4. 刻度文字
text_r = 0.58
tick_angles = [val2angle(t) for t in TICKS]
ax.set_xticks(tick_angles)
ax.set_xticklabels([str(t) for t in TICKS], color="white", fontsize=14)
ax.tick_params(axis="x", pad=10)

# 5. 白色指针
ptr_ang = val2angle(VAL)
ax.plot([0, ptr_ang], [0, r_band], c="white", lw=2.3, solid_capstyle="round", zorder=4)

# 6. 中心数字
ax.text(0,0, f"{VAL}", color="white", fontsize=48, ha="center", va="center", zorder=5)

# 标题
plt.title("2022年6月29公司整体运营指数良好", color="white", fontsize=28, pad=40)
plt.tight_layout()
plt.show()
