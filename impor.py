import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Patch
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FuncFormatter

# Set the aesthetic style
plt.style.use('dark_background')
sns.set_style("darkgrid", {'axes.facecolor': '#1a1a1a', 'grid.color': '#444444'})

# Create the figure with a specific size
fig = plt.figure(figsize=(20, 24))
fig.suptitle("Monetization & Scaling Strategy", fontsize=26, fontweight='bold', color='white', y=0.995)

# Create a grid layout
gs = gridspec.GridSpec(6, 2, height_ratios=[1, 1.5, 1, 1.5, 1, 1])

# Define colors
colors = {
    'primary': '#3498db',    # Blue
    'secondary': '#2ecc71',  # Green
    'accent': '#e74c3c',     # Red
    'highlight': '#f39c12',  # Orange
    'neutral': '#95a5a6'     # Grey
}

# Create segments for the commercialization pathways
segments = ['B2B SaaS for Music Tech', 'Mobile App for Singers', 'Licensing to Music Schools', 'Dataset Licensing']
prices = ['$20-100/month', '$5/month PRO tier', '$1K-10K/year', '$5K-50K dataset']
features = ['API for DAWs', 'Real-time key detection', 'Educational tools', 'Phonation-annotated data']

# 1. Commercialization Pathways
ax1 = fig.add_subplot(gs[0, :])
x = np.arange(len(segments))
ax1.bar(x, [0.6, 0.8, 0.4, 0.3], color=[colors['primary'], colors['secondary'], colors['highlight'], colors['accent']], alpha=0.7, width=0.6)
ax1.set_xticks(x)
ax1.set_xticklabels(segments, fontsize=12)
ax1.set_title('💰 Commercialization Pathways', fontsize=18, pad=15)
ax1.set_ylim(0, 1)
ax1.set_yticks([])

# Add price labels
for i, j in enumerate(x):
    ax1.text(j, 0.05, prices[i], ha='center', va='bottom', color='white', fontsize=10, fontweight='bold')
    ax1.text(j, 0.9, features[i], ha='center', va='bottom', color='white', fontsize=10)

# 2. Market Size Potential
ax2 = fig.add_subplot(gs[1, :])
market_segments = ['Producers', 'Singers', 'Education', 'Data Buyers']
market_sizes = [200, 500, 50, 10]  # in $M
users = ['5M+ DAW users', '50M+ hobbyists', '100K+ music schools', '500+ AI labs']

# Horizontal bars with gradient color
for i, (size, color) in enumerate(zip(market_sizes, [colors['primary'], colors['secondary'], colors['highlight'], colors['accent']])):
    ax2.barh(i, size, color=color, alpha=0.7)
    # Add text labels for market size and user count
    ax2.text(size + 5, i, f"${size}M+", va='center', fontsize=10, fontweight='bold')
    ax2.text(size/2, i, users[i], va='center', ha='center', fontsize=9, color='white')

ax2.set_yticks(range(len(market_segments)))
ax2.set_yticklabels(market_segments, fontsize=12)
ax2.set_title('📊 Market Size Potential', fontsize=18, pad=15)
ax2.set_xlabel('Market Value ($M)', fontsize=10)
total_market = sum(market_sizes)
ax2.text(0.5, -0.2, f"Total Addressable Market (TAM): ${total_market}M+", 
         transform=ax2.transAxes, ha='center', fontsize=14, fontweight='bold', color=colors['secondary'])

# 3. SWOT Analysis
ax3 = fig.add_subplot(gs[2, 0])
ax4 = fig.add_subplot(gs[2, 1])

# SWOT data
strengths = ['Novel phonation-aware AI', 'Works with minimal data', 'Real-time (<50ms latency)']
weaknesses = ['Limited brand recognition', 'Dependency on GPU for training', 'Niche vocal focus']
opportunities = ['Africa\'s booming music industry', 'Rising DIY music production trend']
threats = ['Melodyne/iZotope adding AI features', 'Open-source alternatives']

# Create SWOT quadrants
for i, strength in enumerate(strengths):
    ax3.text(0.1, 0.85 - i*0.2, f"✅ {strength}", fontsize=10, color='white')
for i, weakness in enumerate(weaknesses):
    ax3.text(0.1, 0.25 - i*0.2, f"⚠️ {weakness}", fontsize=10, color='white')
    
for i, opportunity in enumerate(opportunities):
    ax4.text(0.1, 0.85 - i*0.2, f"🌍 {opportunity}", fontsize=10, color='white')
for i, threat in enumerate(threats):
    ax4.text(0.1, 0.45 - i*0.2, f"🚫 {threat}", fontsize=10, color='white')

# Configure SWOT panels
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.set_title('🔍 SWOT Analysis - Strengths & Weaknesses', fontsize=14)
ax3.axis('off')

ax4.set_xlim(0, 1)
ax4.set_ylim(0, 1)
ax4.set_title('🔍 SWOT Analysis - Opportunities & Threats', fontsize=14)
ax4.axis('off')

# Add colored backgrounds for SWOT quadrants
ax3.add_patch(plt.Rectangle((0, 0.5), 1, 0.5, fill=True, alpha=0.1, color=colors['secondary']))
ax3.add_patch(plt.Rectangle((0, 0), 1, 0.5, fill=True, alpha=0.1, color=colors['accent']))
ax4.add_patch(plt.Rectangle((0, 0.5), 1, 0.5, fill=True, alpha=0.1, color=colors['primary']))
ax4.add_patch(plt.Rectangle((0, 0), 1, 0.5, fill=True, alpha=0.1, color=colors['highlight']))

# 4. Competitor Analysis
ax5 = fig.add_subplot(gs[3, :])
competitors = ['Melodyne', 'iZotope VocalSynth', 'CREPE (Open Source)']
differentiators = ['Industry-standard pitch correction', 'Vocal effects rack', 'Free pitch tracking']
our_edge = ['Real-time + phonation-aware', 'Key detection (not just FX)', 'SSL-trained for accuracy']

# Create a table-like visualization
table_data = pd.DataFrame({
    'Competitor': competitors,
    'Their Differentiator': differentiators,
    'Our Edge': our_edge
})

y_positions = np.arange(len(competitors))
ax5.set_xlim(0, 1)
ax5.set_ylim(-0.5, len(competitors) - 0.5)

# Draw the table
for i, (comp, diff, edge) in enumerate(zip(competitors, differentiators, our_edge)):
    # Competitor name
    ax5.text(0.15, i, comp, ha='center', va='center', fontsize=12, fontweight='bold')
    # Differentiator
    ax5.text(0.5, i, diff, ha='center', va='center', fontsize=11)
    # Our edge
    ax5.text(0.85, i, edge, ha='center', va='center', fontsize=11, color=colors['secondary'], fontweight='bold')

# Add column headers
ax5.text(0.15, len(competitors), 'Tool', ha='center', va='center', fontsize=12, fontweight='bold')
ax5.text(0.5, len(competitors), 'Differentiator', ha='center', va='center', fontsize=12, fontweight='bold')
ax5.text(0.85, len(competitors), 'Our Edge', ha='center', va='center', fontsize=12, fontweight='bold')

# Add separation lines
for i in range(len(competitors) + 1):
    ax5.axhline(y=i-0.5, color='gray', linestyle='-', alpha=0.3, linewidth=1)
ax5.axvline(x=0.3, color='gray', linestyle='-', alpha=0.3, linewidth=1)
ax5.axvline(x=0.7, color='gray', linestyle='-', alpha=0.3, linewidth=1)

ax5.set_yticks([])
ax5.set_xticks([])
ax5.set_title('🎯 Competitor Analysis', fontsize=18, pad=15)

# 5. Scaling Plan Timeline
ax6 = fig.add_subplot(gs[4:, :])

# Create timeline data
phases = ['Phase 1 (0-12 months)', 'Phase 2 (1-3 years)', 'Phase 3 (3-5 years)']
phase_durations = [1, 2, 2]  # in years
milestones = [
    ['Launch MVP API', 'Partner with Ugandan artists'],
    ['Integrate with Ableton/Final Cut Pro', 'Expand dataset to cover African folk vocals'],
    ['Edge AI: On-device inference', 'Voice Cloning: Add personalized key recommendations']
]
icons = ['💻', '🌍', '📱']

# Create a horizontal timeline
start_positions = [0, 1, 3]
for i, (phase, duration) in enumerate(zip(phases, phase_durations)):
    # Phase bar
    ax6.broken_barh([(start_positions[i], duration)], (0.5, 1), 
                   facecolors=colors['primary'], alpha=0.7)
    # Phase label
    ax6.text(start_positions[i] + duration/2, 2, phase, ha='center', va='center', fontsize=14, fontweight='bold')
    # Add phase icon
    ax6.text(start_positions[i] + duration/2, 0.2, icons[i], ha='center', va='center', fontsize=20)
    
    # Add milestones
    for j, milestone in enumerate(milestones[i]):
        ax6.text(start_positions[i] + duration/2, -0.5 - j*0.5, f"• {milestone}", ha='center', va='center', fontsize=11)
        
# Configure timeline
ax6.set_ylim(-2, 3)
ax6.set_xlim(0, 5.5)
ax6.set_yticks([])
ax6.set_xticks([0, 1, 3, 5])
ax6.set_xticklabels(['Start', 'Year 1', 'Year 3', 'Year 5'], fontsize=12)
ax6.set_title('🚀 Scaling Plan', fontsize=18, pad=15)

# Add color-coded flags at the bottom
ax6.text(0.1, -3, "🇺🇬 Local first (Uganda)", fontsize=12)
ax6.text(0.6, -3, "🌐 Global expansion", fontsize=12)

# Add a key insight callout
ax6.text(4.5, -1.5, "💡 Key Insight:", fontsize=14, fontweight='bold', color=colors['highlight'])
ax6.text(4.5, -2, "Start with Ugandan music studios\nas early adopters, then scale globally", 
         fontsize=12, color='white', ha='center')

# Add a footer with icons reference
footer_text = "💻 SaaS | 📱 App | 🎓 Education | 📊 Data"
fig.text(0.5, 0.01, footer_text, fontsize=14, ha='center', color='white')

# Adjust layout
plt.tight_layout(rect=[0, 0.02, 1, 0.98])
plt.subplots_adjust(hspace=0.5)

# Save the figure
plt.savefig('monetization_strategy_visualization.png', dpi=300, bbox_inches='tight', pad_inches=0.5, facecolor='#121212')

# Show the plot
plt.show()