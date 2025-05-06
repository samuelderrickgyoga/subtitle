import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle, Patch
import matplotlib.patheffects as path_effects

# Set style parameters
plt.style.use('fivethirtyeight')
sns.set_palette("deep")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14

# Create the main figure with a grid layout
fig = plt.figure(figsize=(20, 24), facecolor='#f9f9f9')
gs = GridSpec(5, 2, height_ratios=[1, 1, 1, 1, 1], width_ratios=[1.2, 0.8], hspace=0.4, wspace=0.3)

# Define some colors
main_color = '#3498db'  # Primary blue
secondary_color = '#2ecc71'  # Green
tertiary_color = '#9b59b6'  # Purple
accent_color = '#e74c3c'  # Red

# Add a title for the entire figure
fig.suptitle('Monetization & Scaling Strategy: Phonation-Aware AI for Music', 
             fontsize=26, fontweight='bold', y=0.995)
subtitle = fig.text(0.5, 0.975, 
                    'Pitch Deck Visualization for Investors', 
                    fontsize=18, ha='center', color='#555')

# 1. Commercialization Pathways - Bar chart
ax1 = fig.add_subplot(gs[0, :])

# Data for commercialization pathways
pathways = ['B2B SaaS', 'Mobile App', 'Music Schools', 'Dataset Licensing']
price_ranges = ['$20-100/mo', '$5/mo', '$1K-10K/yr', '$5K-50K']
potential_revenue = [200, 500, 50, 10]  # in millions

# Create the bar chart
bars = ax1.bar(pathways, potential_revenue, color=[main_color, secondary_color, tertiary_color, accent_color], alpha=0.7)

# Add price ranges as annotations on each bar
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax1.text(
        bar.get_x() + bar.get_width()/2, height + 10,
        price_ranges[i], ha='center', va='bottom',
        fontsize=12, fontweight='bold', color='#333'
    )
    ax1.text(
        bar.get_x() + bar.get_width()/2, height/2,
        f"${potential_revenue[i]}M", ha='center', va='center',
        fontsize=14, fontweight='bold', color='white'
    )

ax1.set_title('💰 Commercialization Pathways', fontsize=22, fontweight='bold', pad=20)
ax1.set_ylabel('Potential Revenue (Millions USD)', fontsize=16)
ax1.set_ylim(0, 550)

# Add key features as text boxes at the bottom
features = [
    'API/service for DAWs\nAbleton, FL Studio integration',
    'Real-time key detection\nVocal training exercises',
    'Institutions like Uganda\nNational Cultural Centre',
    'Unique phonation-annotated\nvocal dataset'
]

for i, feature in enumerate(pathways):
    ax1.text(
        i, -60, features[i],
        ha='center', va='center',
        fontsize=11, color='#333',
        bbox=dict(facecolor='#f0f0f0', alpha=0.6, boxstyle='round,pad=0.5')
    )

# 2. Market Size Potential - Horizontal bar chart
ax2 = fig.add_subplot(gs[1, :])

# Data for market segments
segments = ['Producers', 'Singers', 'Education', 'Data Buyers', 'Total (TAM)']
market_values = [200, 500, 50, 10, 760]  # in millions
users = ['5M+ DAW users', '50M+ hobbyists', '100K+ music schools', '500+ AI labs', '55.6M+ Total Users']
colors = [main_color, secondary_color, tertiary_color, accent_color, '#555555']

# Create horizontal bar chart
bars = ax2.barh(segments, market_values, color=colors, alpha=0.7)

# Add market value and user count annotations
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax2.text(
        width + 5, bar.get_y() + bar.get_height()/2,
        f"${market_values[i]}M", va='center',
        fontsize=14, fontweight='bold', color='#333'
    )
    ax2.text(
        width/2, bar.get_y() + bar.get_height()/2,
        users[i], va='center', ha='center',
        fontsize=12, fontweight='bold', color='white'
    )

ax2.set_title('📊 Market Size Potential', fontsize=22, fontweight='bold', pad=20)
ax2.set_xlabel('Market Value (Millions USD)', fontsize=16)
ax2.invert_yaxis()  # To have the largest segment at the top
ax2.set_xlim(0, 800)

# 3. SWOT Analysis - Quadrant visualization
ax3 = fig.add_subplot(gs[2, 0])

# Define the quadrants
strengths = [
    "✅ Novel phonation-aware AI",
    "✅ Works with minimal data",
    "✅ Real-time (<50ms latency)"
]

weaknesses = [
    "⚠️ Limited brand recognition",
    "⚠️ Dependency on GPU for training",
    "⚠️ Niche vocal focus"
]

opportunities = [
    "🌍 Africa's booming music industry",
    "📈 Rising DIY music production trend"
]

threats = [
    "🚫 Melodyne/iZotope adding AI features",
    "🚫 Open-source alternatives (CREPE)"
]

# Create a SWOT quadrant plot
ax3.axis('off')
ax3.set_title('🔍 SWOT Analysis', fontsize=22, fontweight='bold', pad=20)

# Draw the quadrants
rect_kw = dict(ec="black", lw=2, alpha=0.7)
strength_rect = Rectangle((0, 0.5), 0.5, 0.5, fc="#2ecc71", **rect_kw)  # Green
weakness_rect = Rectangle((0.5, 0.5), 0.5, 0.5, fc="#e74c3c", **rect_kw)  # Red
opportunity_rect = Rectangle((0, 0), 0.5, 0.5, fc="#3498db", **rect_kw)  # Blue
threat_rect = Rectangle((0.5, 0), 0.5, 0.5, fc="#f39c12", **rect_kw)  # Orange

ax3.add_patch(strength_rect)
ax3.add_patch(weakness_rect)
ax3.add_patch(opportunity_rect)
ax3.add_patch(threat_rect)

# Add quadrant titles
ax3.text(0.25, 0.95, "STRENGTHS", ha="center", va="top", fontsize=16, fontweight="bold", color="white")
ax3.text(0.75, 0.95, "WEAKNESSES", ha="center", va="top", fontsize=16, fontweight="bold", color="white")
ax3.text(0.25, 0.45, "OPPORTUNITIES", ha="center", va="top", fontsize=16, fontweight="bold", color="white")
ax3.text(0.75, 0.45, "THREATS", ha="center", va="top", fontsize=16, fontweight="bold", color="white")

# Add the SWOT text
for i, item in enumerate(strengths):
    ax3.text(0.05, 0.9 - i*0.1, item, va="top", fontsize=12, color="white")

for i, item in enumerate(weaknesses):
    ax3.text(0.55, 0.9 - i*0.1, item, va="top", fontsize=12, color="white")

for i, item in enumerate(opportunities):
    ax3.text(0.05, 0.4 - i*0.1, item, va="top", fontsize=12, color="white")

for i, item in enumerate(threats):
    ax3.text(0.55, 0.4 - i*0.1, item, va="top", fontsize=12, color="white")

# 4. Competitor Analysis - Comparison table
ax4 = fig.add_subplot(gs[2, 1])
ax4.axis('off')
ax4.set_title('🎯 Competitor Analysis', fontsize=22, fontweight='bold', pad=20)

# Create a table-style comparison
competitors = ['Melodyne', 'iZotope VocalSynth', 'CREPE (Open Source)']
differentiators = ['Industry-standard pitch correction', 'Vocal effects rack', 'Free pitch tracking']
our_edge = ['Real-time + phonation-aware', 'Key detection (not just FX)', 'SSL-trained for accuracy']

# Draw the table headers
ax4.text(0.05, 0.85, "Tool", fontsize=14, fontweight='bold')
ax4.text(0.4, 0.85, "Differentiator", fontsize=14, fontweight='bold')
ax4.text(0.75, 0.85, "Our Edge", fontsize=14, fontweight='bold')

# Draw horizontal lines
ax4.axhline(y=0.82, xmin=0.05, xmax=0.95, color='black', alpha=0.3)
ax4.axhline(y=0.45, xmin=0.05, xmax=0.95, color='black', alpha=0.3)
ax4.axhline(y=0.55, xmin=0.05, xmax=0.95, color='black', alpha=0.3)
ax4.axhline(y=0.65, xmin=0.05, xmax=0.95, color='black', alpha=0.3)

# Draw vertical lines
ax4.axvline(x=0.35, ymin=0.45, ymax=0.85, color='black', alpha=0.3)
ax4.axvline(x=0.7, ymin=0.45, ymax=0.85, color='black', alpha=0.3)

# Fill in the table data
for i, (comp, diff, edge) in enumerate(zip(competitors, differentiators, our_edge)):
    y_pos = 0.75 - i * 0.1
    ax4.text(0.05, y_pos, comp, fontsize=12)
    ax4.text(0.4, y_pos, diff, fontsize=12)
    ax4.text(0.75, y_pos, edge, fontsize=12, color=accent_color, fontweight='bold')

# 5. Scaling Plan - Timeline
ax5 = fig.add_subplot(gs[3:, :])
ax5.axis('off')
ax5.set_title('🚀 Scaling Plan', fontsize=22, fontweight='bold', pad=20)

# Create a timeline visualization
phases = ['Phase 1 (0-12 months)', 'Phase 2 (1-3 years)', 'Phase 3 (3-5 years)']
milestones = [
    ['Launch MVP API (FastAPI + AWS)', 'Partner with Ugandan artists for pilot testing'],
    ['Integrate with Ableton/Final Cut Pro', 'Expand dataset to cover African folk vocals'],
    ['Edge AI: On-device inference (TensorFlow Lite)', 'Voice Cloning: Add personalized key recommendations']
]

colors = [main_color, secondary_color, tertiary_color]
arrows = ['→', '↔', '↗']

# Draw the timeline
line_y = 0.7
start_x = 0.1
end_x = 0.9
line_length = end_x - start_x

ax5.plot([start_x, end_x], [line_y, line_y], 'k-', lw=3, alpha=0.6)

# Add phase markers
for i, phase in enumerate(phases):
    x_pos = start_x + (i * line_length / (len(phases) - 0.5))
    
    # Draw circles on the timeline
    circle = plt.Circle((x_pos, line_y), 0.02, color=colors[i], alpha=0.8)
    ax5.add_patch(circle)
    
    # Phase titles
    text = ax5.text(x_pos, line_y + 0.1, phase, 
             ha='center', va='center', fontsize=16, fontweight='bold',
             bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5', edgecolor=colors[i], linewidth=2))
    
    # Add outline to make text more readable
    text.set_path_effects([path_effects.withStroke(linewidth=3, foreground='white')])
    
    # Milestones
    for j, milestone in enumerate(milestones[i]):
        y_offset = -0.1 - j * 0.15
        ax5.text(x_pos, line_y + y_offset, f"{arrows[i]} {milestone}", 
                 ha='center', va='center', fontsize=13,
                 bbox=dict(facecolor=colors[i], alpha=0.2, boxstyle='round,pad=0.3'))

# Add key insight box
insight_text = "💡 Key Insight: Start with Ugandan music studios as early adopters, then scale globally."
insight_box = ax5.text(0.5, 0.15, insight_text, 
                      ha='center', va='center', fontsize=16, fontweight='bold',
                      bbox=dict(facecolor='#f0f0f0', alpha=0.8, boxstyle='round,pad=1', edgecolor='#555'))

# Add flags
ax5.text(0.3, 0.05, '🇺🇬 Local first approach', fontsize=14)
ax5.text(0.7, 0.05, '🌐 Global expansion strategy', fontsize=14)

# Footer with icons legend
footer = fig.text(0.5, 0.01, 
                 '💻 SaaS    📱 App    🎓 Education    📊 Data', 
                 fontsize=16, ha='center', color='#555', fontweight='bold')

plt.tight_layout(rect=[0, 0.02, 1, 0.97])
plt.savefig('monetization_strategy_visualization.png', dpi=300, bbox_inches='tight')
plt.show()