import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as PathEffects
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import matplotlib.cm as cm

# Set the style
plt.style.use('ggplot')
sns.set_palette("deep")
sns.set_context("talk")

# Common colors
primary_color = "#1f77b4"  # Blue
secondary_color = "#ff7f0e"  # Orange
tertiary_color = "#2ca02c"  # Green
highlight_color = "#d62728"  # Red
purple_color = "#9467bd"  # Purple
brown_color = "#8c564b"  # Brown
pink_color = "#e377c2"  # Pink
gray_color = "#7f7f7f"  # Gray

# Create custom color maps
colors_swot = ["#2ca02c", "#d62728", "#1f77b4", "#ff7f0e"]  # Green, Red, Blue, Orange
cmap_swot = LinearSegmentedColormap.from_list("SWOT", colors_swot, N=4)

# Utility functions
def save_figure(fig, filename, dpi=300):
    fig.tight_layout()
    fig.savefig(filename, dpi=dpi, bbox_inches="tight")
    plt.close(fig)

def add_fancy_title(ax, title, subtitle=None):
    ax.text(0.5, 1.05, title, ha='center', va='bottom', fontsize=20, 
            fontweight='bold', transform=ax.transAxes)
    if subtitle:
        ax.text(0.5, 0.98, subtitle, ha='center', va='bottom', fontsize=14, 
                transform=ax.transAxes, fontstyle='italic', alpha=0.8)

def add_shadow_text(ax, x, y, text, fontsize=12, **kwargs):
    txt = ax.text(x, y, text, fontsize=fontsize, **kwargs)
    txt.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='white')])
    return txt

# 1. Commercialization Pathways (Bar Chart)
def create_commercialization_pathways():
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Data
    revenue_streams = ['B2B SaaS\nfor Music Tech', 'Mobile App\nfor Singers', 
                       'Licensing to\nMusic Schools', 'Dataset\nLicensing']
    revenue_values = [250000, 180000, 120000, 85000]
    
    # Features for each stream
    features = [
        "• API integration\n• Cloud deployment\n• Custom training\n• $499/month",
        "• Vocal key analysis\n• Practice tools\n• Voice journal\n• $4.99/month",
        "• Bulk educational licenses\n• Teaching analytics\n• $249/seat/year",
        "• Vocal dataset access\n• ML training data\n• $10K-50K per license"
    ]
    
    # Colors for each bar
    colors = [primary_color, secondary_color, tertiary_color, highlight_color]
    
    # Create the bar chart
    bars = ax.bar(revenue_streams, revenue_values, color=colors, alpha=0.8, width=0.6)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 5000,
                f'${height:,}',
                ha='center', va='bottom', fontweight='bold')
    
    # Add features text below each bar
    for i, (bar, feature) in enumerate(zip(bars, features)):
        y_pos = -25000  # Position below x-axis
        ax.text(bar.get_x() + bar.get_width()/2., y_pos, feature,
                ha='center', va='top', fontsize=10, 
                bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.8))
    
    # Customize the chart
    ax.set_ylabel('Annual Revenue Potential ($)', fontweight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Set y-axis limits to accommodate the feature text boxes
    ax.set_ylim(-70000, 280000)
    
    add_fancy_title(ax, "AI Vocal Key Detection System - Commercialization Pathways", 
                    "Projected Annual Revenue by Stream")
    
    # Add a watermark logo in the background (placeholder)
    fig.text(0.5, 0.5, "VOCAL AI", fontsize=100, color='gray', 
             ha='center', va='center', alpha=0.1, rotation=30)
    
    save_figure(fig, "commercialization_pathways.png")

# 2. Market Size Potential (Horizontal Bar Chart)
def create_market_size_potential():
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Data
    segments = ['Music Producers', 'Amateur/Pro Singers', 'Music Education', 'AI Data Buyers']
    tam_values = [1200, 3800, 950, 75]  # in millions $
    est_users = ['380,000+', '12.5 million+', '25,000+ institutions', '150+ companies']
    
    # Colors for each segment with gradient effect
    colors = [cm.Blues(0.6), cm.Blues(0.7), cm.Blues(0.8), cm.Blues(0.9)]
    
    # Create horizontal bar chart
    bars = ax.barh(segments, tam_values, color=colors, alpha=0.9)
    
    # Add value labels and user counts
    for i, (bar, users) in enumerate(zip(bars, est_users)):
        width = bar.get_width()
        ax.text(width + 50, bar.get_y() + bar.get_height()/2,
                f'${width:,}M', ha='left', va='center', fontweight='bold')
        
        # Add user count in the middle of the bar
        ax.text(width/2, bar.get_y() + bar.get_height()/2,
                f"{users}", ha='center', va='center', 
                color='white', fontweight='bold', fontsize=10)
    
    # Customize chart
    ax.set_xlabel('Total Addressable Market ($ Millions)', fontweight='bold')
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    add_fancy_title(ax, "Market Size Potential", 
                    "Total Addressable Market by Segment with Estimated User Base")
    
    # Add a total TAM annotation
    total_tam = sum(tam_values)
    ax.text(0.98, 0.05, f"Total TAM: ${total_tam:,}M",
            transform=ax.transAxes, ha='right', va='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor=primary_color, alpha=0.1),
            fontsize=14, fontweight='bold')
    
    save_figure(fig, "market_size_potential.png")

# 3. SWOT Analysis (Quadrant Visualization)
def create_swot_analysis():
    fig, ax = plt.subplots(figsize=(14, 12))
    
    # Remove axes
    ax.axis('off')
    
    # SWOT items
    strengths = [
        "Proprietary vocal analysis algorithm",
        "95% accuracy in real-time key detection",
        "Low latency (15ms) processing",
        "Cross-cultural vocal sample database",
        "Plug-and-play API integration"
    ]
    
    weaknesses = [
        "Higher compute requirements vs competitors",
        "Limited language support (8 languages)",
        "Requires initial calibration period",
        "Early-stage brand recognition",
        "Dependency on cloud infrastructure"
    ]
    
    opportunities = [
        "Emerging market for AI vocal tech",
        "Growing online music education sector",
        "Integration with major DAW platforms",
        "Expansion into speech therapy applications",
        "Partnership with streaming platforms"
    ]
    
    threats = [
        "Established competitors (Melodyne, iZotope)",
        "Potential ML vocal analysis patents",
        "Rapid evolution of competing technologies",
        "Data privacy regulations",
        "Open-source alternatives"
    ]
    
    # Define the quadrants
    quadrant_data = [
        {"title": "STRENGTHS", "items": strengths, "color": colors_swot[0], "position": (0, 0.5)},
        {"title": "WEAKNESSES", "items": weaknesses, "color": colors_swot[1], "position": (0.5, 0.5)},
        {"title": "OPPORTUNITIES", "items": opportunities, "color": colors_swot[2], "position": (0, 0)},
        {"title": "THREATS", "items": threats, "color": colors_swot[3], "position": (0.5, 0)}
    ]
    
    # Draw the quadrants
    for quad in quadrant_data:
        rect = Rectangle(quad["position"], 0.5, 0.5, transform=ax.transAxes,
                         facecolor=quad["color"], alpha=0.2, edgecolor='black')
        ax.add_patch(rect)
        
        # Add quadrant title
        ax.text(quad["position"][0] + 0.25, quad["position"][1] + 0.45, 
                quad["title"], transform=ax.transAxes,
                ha='center', va='center', fontsize=18, fontweight='bold')
        
        # Add items as bullet points
        for i, item in enumerate(quad["items"]):
            ax.text(quad["position"][0] + 0.05, quad["position"][1] + 0.35 - i*0.06, 
                    f"• {item}", transform=ax.transAxes,
                    ha='left', va='center', fontsize=12)
    
    # Add title
    fig.text(0.5, 0.95, "SWOT ANALYSIS: AI VOCAL KEY DETECTION SYSTEM", 
             ha='center', fontsize=22, fontweight='bold')
    fig.text(0.5, 0.92, "Strategic Evaluation of Market Position and Growth Potential", 
             ha='center', fontsize=16, fontstyle='italic')
    
    # Add a subtle background graphic
    ax.text(0.5, 0.5, "SWOT", fontsize=150, alpha=0.05, 
            ha='center', va='center', transform=ax.transAxes)
    
    save_figure(fig, "swot_analysis.png")

# 4. Competitor Analysis (Table-Style Comparison)
def create_competitor_analysis():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.axis('off')
    
    # Data structure for competitor analysis
    features = [
        "Real-time Analysis", 
        "Accuracy", 
        "Latency", 
        "Price Point",
        "Integration Options",
        "AI Training",
        "Cultural Adaptability",
        "Mobile Support"
    ]
    
    competitors = ["Our Solution", "Melodyne", "iZotope VocalSynth", "CREPE"]
    
    # Ratings data (0-5 scale where 5 is best)
    ratings = np.array([
        [5, 3, 4, 4],  # Real-time Analysis
        [5, 4, 3, 4],  # Accuracy
        [4, 3, 3, 5],  # Latency
        [4, 2, 3, 5],  # Price Point (5 means better/lower price)
        [5, 3, 4, 2],  # Integration Options
        [5, 2, 4, 3],  # AI Training
        [5, 2, 2, 3],  # Cultural Adaptability
        [4, 1, 2, 3]   # Mobile Support
    ])
    
    # Create a table-like structure
    cell_width = 0.19
    cell_height = 0.09
    start_x = 0.1
    start_y = 0.85
    
    # Draw header row with competitor names
    for i, comp in enumerate(competitors):
        x = start_x + i * cell_width
        color = primary_color if i == 0 else 'lightgray'
        rect = FancyBboxPatch((x, start_y), cell_width, cell_height, 
                             boxstyle="round,pad=0.03", transform=ax.transAxes,
                             facecolor=color, alpha=0.3)
        ax.add_patch(rect)
        ax.text(x + cell_width/2, start_y + cell_height/2, comp,
                transform=ax.transAxes, ha='center', va='center', 
                fontweight='bold' if i == 0 else 'normal')
    
    # Draw feature column
    for j, feature in enumerate(features):
        y = start_y - (j+1) * cell_height
        rect = FancyBboxPatch((start_x - cell_width, y), cell_width, cell_height, 
                             boxstyle="round,pad=0.03", transform=ax.transAxes,
                             facecolor='lightgray', alpha=0.3)
        ax.add_patch(rect)
        ax.text(start_x - cell_width/2, y + cell_height/2, feature,
                transform=ax.transAxes, ha='center', va='center', fontweight='bold')
    
    # Draw rating cells with colored indicators
    colors = ['#f8696b', '#ffeb84', '#63be7b']  # Red to Green
    for i in range(ratings.shape[1]):  # Competitors
        for j in range(ratings.shape[0]):  # Features
            x = start_x + i * cell_width
            y = start_y - (j+1) * cell_height
            
            # Determine color based on rating value
            rating = ratings[j, i]
            norm_rating = (rating - 1) / 4  # Normalize to 0-1 range
            color_idx = int(norm_rating * 2)  # Map to our 3 colors
            color_idx = min(color_idx, 2)  # Ensure it's within bounds
            
            highlight = (i == 0)  # Highlight our solution
            
            rect = FancyBboxPatch((x, y), cell_width, cell_height, 
                                 boxstyle="round,pad=0.03", transform=ax.transAxes,
                                 facecolor=colors[color_idx], alpha=0.7 if highlight else 0.5,
                                 linewidth=2 if highlight else 1,
                                 edgecolor='black' if highlight else 'gray')
            ax.add_patch(rect)
            
            # Add rating stars
            stars = "★" * int(rating) + "☆" * (5 - int(rating))
            ax.text(x + cell_width/2, y + cell_height/2, stars,
                    transform=ax.transAxes, ha='center', va='center',
                    color='black', fontsize=10)
    
    # Add title
    fig.text(0.5, 0.95, "COMPETITIVE ANALYSIS", 
             ha='center', fontsize=22, fontweight='bold')
    fig.text(0.5, 0.92, "Comparing Our AI Vocal Key Detection System Against Market Leaders", 
             ha='center', fontsize=16, fontstyle='italic')
    
    # Add legend
    legend_x = 0.1
    legend_y = 0.05
    for i, (text, color) in enumerate([("Poor", colors[0]), ("Average", colors[1]), ("Excellent", colors[2])]):
        rect = FancyBboxPatch((legend_x + i*0.1, legend_y), 0.05, 0.03, 
                             boxstyle="round,pad=0.01", transform=ax.transAxes,
                             facecolor=color, alpha=0.7)
        ax.add_patch(rect)
        ax.text(legend_x + i*0.1 + 0.025, legend_y - 0.015, text,
                transform=ax.transAxes, ha='center', va='top', fontsize=10)
    
    save_figure(fig, "competitor_analysis.png")

# 5. Scaling Plan (Interactive Timeline)
def create_scaling_timeline():
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Define timeline dates
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2030, 1, 1)
    
    # Phase markers
    phase1_end = datetime(2026, 1, 1)
    phase2_end = datetime(2028, 1, 1)
    
    # Set up the timeline
    ax.set_xlim([start_date, end_date])
    ax.set_ylim([0, 10])
    
    # Format x-axis as dates
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=(1, 4, 7, 10)))
    
    # Remove y-axis ticks and labels
    ax.set_yticks([])
    ax.set_yticklabels([])
    
    # Draw phase backgrounds
    phase_colors = [primary_color, secondary_color, tertiary_color]
    phase_alpha = 0.15
    
    # Phase 1 background
    ax.axvspan(start_date, phase1_end, ymin=0, ymax=1, 
               alpha=phase_alpha, color=phase_colors[0])
    
    # Phase 2 background
    ax.axvspan(phase1_end, phase2_end, ymin=0, ymax=1, 
               alpha=phase_alpha, color=phase_colors[1])
    
    # Phase 3 background
    ax.axvspan(phase2_end, end_date, ymin=0, ymax=1, 
               alpha=phase_alpha, color=phase_colors[2])
    
    # Add phase labels
    ax.text(start_date + timedelta(days=30), 9.5, "PHASE 1: LAUNCH (0-12 months)", 
            fontsize=14, fontweight='bold', ha='left', va='top', 
            color=phase_colors[0])
    
    ax.text(phase1_end + timedelta(days=30), 9.5, "PHASE 2: EXPANSION (1-3 years)", 
            fontsize=14, fontweight='bold', ha='left', va='top', 
            color=phase_colors[1])
    
    ax.text(phase2_end + timedelta(days=30), 9.5, "PHASE 3: SCALE (3-5 years)", 
            fontsize=14, fontweight='bold', ha='left', va='top', 
            color=phase_colors[2])
    
    # Define milestones with dates and descriptions
    milestones = [
        {"date": datetime(2025, 3, 1), "label": "MVP API Launch", 
         "desc": "Initial API release with core vocal key detection", "phase": 1},
        {"date": datetime(2025, 6, 1), "label": "Uganda Pilot", 
         "desc": "Pilot testing with Ugandan artists for cultural adaptation", "phase": 1},
        {"date": datetime(2025, 9, 1), "label": "Mobile App Beta", 
         "desc": "Launch beta version of mobile app for singers", "phase": 1},
        
        {"date": datetime(2026, 3, 1), "label": "DAW Integration", 
         "desc": "First plugin integration with major DAWs", "phase": 2},
        {"date": datetime(2026, 9, 1), "label": "Dataset Expansion", 
         "desc": "10x increase in vocal dataset with cultural diversity", "phase": 2},
        {"date": datetime(2027, 6, 1), "label": "Education Platform", 
         "desc": "Launch of specialized platform for music education", "phase": 2},
        
        {"date": datetime(2028, 6, 1), "label": "On-device AI", 
         "desc": "Release of lightweight on-device processing capabilities", "phase": 3},
        {"date": datetime(2029, 3, 1), "label": "Personalized Key Recommendation", 
         "desc": "AI-driven personalized vocal range optimization", "phase": 3},
        {"date": datetime(2029, 12, 1), "label": "Enterprise Solution", 
         "desc": "Full-scale enterprise solution for music production companies", "phase": 3}
    ]
    
    # Plot milestones
    for i, milestone in enumerate(milestones):
        y_pos = 7 - (i % 3) * 2  # Stagger vertically
        color = phase_colors[milestone["phase"]-1]
        
        # Draw milestone marker
        ax.scatter(milestone["date"], y_pos, s=120, color=color, zorder=10)
        
        # Draw milestone label
        ax.text(milestone["date"], y_pos + 0.4, milestone["label"], 
                ha='center', va='bottom', fontweight='bold', color='black',
                bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.3))
        
        # Draw milestone description
        ax.text(milestone["date"], y_pos - 0.4, milestone["desc"], 
                ha='center', va='top', fontsize=10, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # Connect milestones with lines
    for phase in [1, 2, 3]:
        phase_milestones = [m for m in milestones if m["phase"] == phase]
        if len(phase_milestones) > 1:
            dates = [m["date"] for m in phase_milestones]
            y_positions = [7 - (i % 3) * 2 for i in range(len(dates))]
            
            # Draw connecting line
            ax.plot(dates, y_positions, 'o-', color=phase_colors[phase-1], 
                    alpha=0.6, linewidth=2, markersize=0)
    
    # Add title
    fig.text(0.5, 0.95, "SCALING STRATEGY: 5-YEAR GROWTH PLAN", 
             ha='center', fontsize=22, fontweight='bold')
    fig.text(0.5, 0.92, "Timeline of Key Milestones and Development Phases", 
             ha='center', fontsize=16, fontstyle='italic')
    
    # Add key metrics projections along bottom
    metrics = [
        {"date": datetime(2025, 6, 1), "metric": "Users: 5K", "revenue": "$250K ARR"},
        {"date": datetime(2026, 6, 1), "metric": "Users: 50K", "revenue": "$1.2M ARR"},
        {"date": datetime(2027, 6, 1), "metric": "Users: 250K", "revenue": "$3.8M ARR"},
        {"date": datetime(2028, 6, 1), "metric": "Users: 1M", "revenue": "$8.5M ARR"},
        {"date": datetime(2029, 6, 1), "metric": "Users: 2.5M", "revenue": "$15M ARR"}
    ]
    
    for metric in metrics:
        ax.text(metric["date"], 0.5, f"{metric['metric']}\n{metric['revenue']}", 
                ha='center', va='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lavender', alpha=0.8))
    
    # Make grid subtle
    ax.grid(True, linestyle='--', alpha=0.3)
    
    save_figure(fig, "scaling_timeline.png")

# Create all visualizations
def create_all_visualizations():
    print("Creating Commercialization Pathways visualization...")
    create_commercialization_pathways()
    
    print("Creating Market Size Potential visualization...")
    create_market_size_potential()
    
    print("Creating SWOT Analysis visualization...")
    create_swot_analysis()
    
    print("Creating Competitor Analysis visualization...")
    create_competitor_analysis()
    
    print("Creating Scaling Timeline visualization...")
    create_scaling_timeline()
    
    print("All visualizations created successfully!")

# Run the script
if __name__ == "__main__":
    create_all_visualizations()