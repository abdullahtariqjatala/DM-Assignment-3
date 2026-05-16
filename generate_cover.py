"""Generate a professional portfolio cover image."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.lines import Line2D

fig, ax = plt.subplots(figsize=(12, 8), facecolor='#0a0e1a')
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis('off')

# ── Background gradient panels ────────────────────────────────────────────────
for i in range(80):
    alpha = 0.03 + i * 0.002
    rect = patches.Rectangle((0, i*0.1), 12, 0.12,
                               color='#0f3460', alpha=alpha, zorder=0)
    ax.add_patch(rect)

# ── Decorative ECG / heartbeat line ──────────────────────────────────────────
np.random.seed(42)
x = np.linspace(0, 12, 1200)
ecg = np.zeros_like(x)

def ecg_beat(center, x):
    y = np.zeros_like(x)
    y += 0.08 * np.exp(-((x - center + 0.25)**2) / 0.003)
    y -= 0.12 * np.exp(-((x - center + 0.05)**2) / 0.001)
    y += 0.55 * np.exp(-((x - center)**2) / 0.0005)
    y -= 0.30 * np.exp(-((x - center + 0.12)**2) / 0.001)
    y += 0.10 * np.exp(-((x - center - 0.25)**2) / 0.004)
    return y

for beat_x in [1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.5]:
    ecg += ecg_beat(beat_x, x)

ecg_y = 1.1 + ecg * 0.7
ax.plot(x, ecg_y, color='#e94560', linewidth=1.4, alpha=0.85, zorder=2)

# Glow effect on ECG
ax.plot(x, ecg_y, color='#ff6b8a', linewidth=4, alpha=0.15, zorder=1)
ax.plot(x, ecg_y, color='#ff6b8a', linewidth=8, alpha=0.06, zorder=1)

# ── Horizontal divider lines ──────────────────────────────────────────────────
ax.axhline(y=2.1, color='#0f3460', linewidth=1.5, alpha=0.8, zorder=3)
ax.axhline(y=2.05, color='#e94560', linewidth=0.6, alpha=0.6, zorder=3)

# ── Accent bar left ───────────────────────────────────────────────────────────
rect_accent = patches.Rectangle((0, 0), 0.35, 8,
                                  color='#e94560', alpha=0.9, zorder=4)
ax.add_patch(rect_accent)

# ── Small decorative dots ─────────────────────────────────────────────────────
for xi, yi in [(0.7, 7.3), (0.7, 7.0), (0.7, 6.7)]:
    c = Circle((xi, yi), 0.06, color='#e94560', alpha=0.9, zorder=5)
    ax.add_patch(c)

# ── Main title ────────────────────────────────────────────────────────────────
ax.text(0.65, 6.85, "PULSE TO PREDICTION",
        fontsize=38, fontweight='bold', color='white',
        fontfamily='DejaVu Sans', va='center', zorder=6,
        transform=ax.transData)

# ── Subtitle ──────────────────────────────────────────────────────────────────
ax.text(0.65, 6.05,
        "A Patient Intelligence Pipeline for Clinical Decision Support",
        fontsize=14, color='#a0b4d0', fontfamily='DejaVu Sans',
        va='center', zorder=6)

# ── Divider under subtitle ────────────────────────────────────────────────────
ax.plot([0.65, 11.5], [5.65, 5.65], color='#e94560',
        linewidth=1.5, alpha=0.7, zorder=6)

# ── Tag pills ─────────────────────────────────────────────────────────────────
tags = [
    "Time Series Analysis", "Anomaly Detection", "Similarity Search",
    "DTW", "Decision Tree", "SVM", "kNN", "Naïve Bayes", "Rule-Based"
]
tag_colors = [
    '#1a4a7a', '#1a4a7a', '#1a4a7a',
    '#7a1a3a', '#1a6a4a', '#1a6a4a', '#1a6a4a', '#1a6a4a', '#1a6a4a'
]

x_pos, y_pos = 0.65, 5.25
for tag, tc in zip(tags, tag_colors):
    tw = len(tag) * 0.115 + 0.3
    if x_pos + tw > 11.6:
        x_pos = 0.65
        y_pos -= 0.52
    pill = FancyBboxPatch((x_pos, y_pos - 0.17), tw, 0.34,
                           boxstyle="round,pad=0.05",
                           facecolor=tc, edgecolor='#ffffff22',
                           linewidth=0.5, zorder=6)
    ax.add_patch(pill)
    ax.text(x_pos + tw/2, y_pos, tag,
            fontsize=8.5, color='white', ha='center', va='center',
            fontweight='bold', zorder=7)
    x_pos += tw + 0.18

# ── Stats row ─────────────────────────────────────────────────────────────────
stats = [
    ("500", "Patients"),
    ("60K+", "Readings"),
    ("5", "Diagnosis Classes"),
    ("5", "ML Classifiers"),
    ("4", "Analysis Phases"),
]
stat_x = 0.65
stat_y = 3.55
box_w  = 2.1

for val, label in stats:
    box = FancyBboxPatch((stat_x, stat_y - 0.55), box_w, 1.0,
                          boxstyle="round,pad=0.08",
                          facecolor='#0f1e3a', edgecolor='#0f3460',
                          linewidth=1.2, zorder=6)
    ax.add_patch(box)
    ax.text(stat_x + box_w/2, stat_y + 0.12, val,
            fontsize=20, fontweight='bold', color='#e94560',
            ha='center', va='center', zorder=7)
    ax.text(stat_x + box_w/2, stat_y - 0.28, label,
            fontsize=8, color='#a0b4d0',
            ha='center', va='center', zorder=7)
    stat_x += box_w + 0.22

# ── Tech stack line ───────────────────────────────────────────────────────────
ax.plot([0.65, 11.5], [2.55, 2.55], color='#0f3460',
        linewidth=1, alpha=0.8, zorder=6)
ax.text(0.65, 2.3,
        "Python  ·  Pandas  ·  NumPy  ·  Scikit-learn  ·  Statsmodels  ·  Matplotlib  ·  Seaborn",
        fontsize=9.5, color='#6a8aaa', va='center', zorder=6)

# ── Bottom bar ────────────────────────────────────────────────────────────────
bottom = patches.Rectangle((0, 0), 12, 0.55,
                             color='#0f3460', alpha=0.95, zorder=5)
ax.add_patch(bottom)
ax.text(0.65, 0.27, "Data Mining  ·  Healthcare Analytics  ·  Predictive Modelling",
        fontsize=9, color='#a0b4d0', va='center', zorder=6)
ax.text(11.5, 0.27, "2024",
        fontsize=9, color='#e94560', va='center', ha='right',
        fontweight='bold', zorder=6)

# ── Subtle grid dots in background ───────────────────────────────────────────
for gx in np.arange(0.8, 12, 0.6):
    for gy in np.arange(0.7, 8, 0.6):
        ax.plot(gx, gy, '.', color='#1a2a4a', markersize=1.5,
                alpha=0.5, zorder=0)

plt.tight_layout(pad=0)
out = "/Users/Abdullah/Desktop/semester 6/Data mining/Assignment 3/portfolio_cover.png"
plt.savefig(out, dpi=200, bbox_inches='tight',
            facecolor='#0a0e1a', edgecolor='none')
plt.close()
print(f"Cover saved: {out}")
