import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Set seaborn style
sns.set_theme(style="whitegrid")

# Load all dataframes
Gender = pd.read_excel('HDFC_modified.xlsx', sheet_name='Gender')
Education = pd.read_excel('HDFC_modified.xlsx', sheet_name='Education')
Experience = pd.read_excel('HDFC_modified.xlsx', sheet_name='Experience')
Age = pd.read_excel('HDFC_modified.xlsx', sheet_name='Age')

# Create list of dataframes with their display names
dataframes = [
    {"df": Gender, "name": "Gender"},
    {"df": Education, "name": "Education"},
    {"df": Experience, "name": "Experience"},
    {"df": Age, "name": "Age"}
]

# Process each dataframe
for data in dataframes:
    df = data["df"]
    name = data["name"]
    
    print(f"Creating dashboard for {name}...")
    
    # Create a figure with a 3x3 grid of subplots
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))

    # Add a main title to the entire figure
    fig.suptitle(f'HDFC {name} Analysis Dashboard', fontsize=16, fontweight='bold', y=0.98)

    # Initialize all subplots with empty charts and labels
    for row in range(3):
        for col in range(3):
            ax = axes[row, col]
            ax.set_title(f'Plot {row+1},{col+1}')
            ax.grid(True)
            
    # Chart 1: Distribution (first 3 columns) using Seaborn
    ax = axes[0, 0]

    # Extract the first 3 columns
    first_cols = df.columns[:3]
    # Reshape data for seaborn
    df_melted = pd.melt(df, 
                        id_vars=[first_cols[0]], 
                        value_vars=[first_cols[1], first_cols[2]], 
                        var_name='Metric', 
                        value_name='Count')

    # Calculate percentages for each cohort
    for metric in [first_cols[1], first_cols[2]]:
        total = df[metric].sum()
        df_melted.loc[df_melted['Metric'] == metric, 'Percentage'] = df_melted.loc[df_melted['Metric'] == metric, 'Count'] / total * 100

    # Using seaborn barplot with grouped bars
    bars = sns.barplot(x='Category', y='Count', hue='Metric', 
                      data=df_melted, 
                      palette=['blue', 'lightblue'], 
                      ax=ax)

    ax.set_title(f'{name} Distribution by Cohort')
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('Head Count')    # Increased font size by 20% (from base to 1.2x larger)
    base_fontsize = 12
    enlarged_fontsize = int(base_fontsize * 1.2)
    
    # Adding value labels and percentages INSIDE the bars with larger font
    for container_idx, container in enumerate(ax.containers):
        for bar_idx, bar in enumerate(container):
            count = bar.get_height()
            percentage = df_melted.iloc[container_idx*2+bar_idx if container_idx < 2 else bar_idx]['Percentage']
            
            # Calculate position for text inside the bar
            x_pos = bar_idx
            y_pos = count/2  # Mid-point of bar
            
            # Add the label inside the bar
            label_text = f'{int(count)}\n({percentage:.1f}%)'
            color = 'white' if count > 30 else 'black'  # White text for tall bars, black for short ones
            
            ax.text(x_pos, y_pos, label_text, 
                   ha='center', va='center', 
                   color=color, 
                   fontsize=enlarged_fontsize,
                   fontweight='bold',
                   linespacing=1.3)

    # Adjust legend
    ax.legend(title='Cohort Type')    # Chart 2: KPI Performance (top-middle)
    ax = axes[0, 1]

    # Get the 4th and 8th columns (indices 3 and 7)
    col4 = df.columns[3]
    col8 = df.columns[7]

    # Create shorter column names for display
    col4_short = "Cumulative Combined KPI"
    col8_short = "Cumulative KPI 1"

    # Create a DataFrame with the data and specified columns
    kpi_data = pd.DataFrame({
        'Category': df['Category'],
        col4_short: df[col4],
        col8_short: df[col8]
    })

    # Reshape data for seaborn
    kpi_melted = pd.melt(kpi_data, 
                         id_vars=['Category'], 
                         value_vars=[col4_short, col8_short],
                         var_name='KPI Type', 
                         value_name='Achievement %')    # Preparing custom colors to highlight Female category in Gender dashboard
    if name == "Gender":
        # Custom palette to make Female category bars stand out
        palette = []
        for category in kpi_melted['Category'].unique():
            if category == 'Female':
                palette.extend(['#ff5500', '#ff7733'])  # Brighter orange for Female
            else:
                palette.extend(['orange', 'coral'])  # Regular colors for other categories
        
        # Using seaborn barplot with custom colors
        bars = sns.barplot(x='Category', y='Achievement %', hue='KPI Type', 
                          data=kpi_melted, 
                          palette=palette, 
                          ax=ax)
    else:
        # Regular coloring for non-Gender dashboards
        bars = sns.barplot(x='Category', y='Achievement %', hue='KPI Type', 
                          data=kpi_melted, 
                          palette=['orange', 'coral'], 
                          ax=ax)

    ax.set_title(f'KPI Performance by {name} CAP LRM')
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('Achievement %')

    # Increased font size by 20% (from base to 1.2x larger)
    base_fontsize = 12
    enlarged_fontsize = int(base_fontsize * 1.2)
    
    # Adding value labels INSIDE the bars with larger font
    for container_idx, container in enumerate(ax.containers):
        for bar_idx, bar in enumerate(container):
            height = bar.get_height()
            
            # Calculate position for text inside the bar
            x_pos = bar_idx
            y_pos = height/2  # Mid-point of bar
            
            # Add the label inside the bar
            label_text = f'{height:.2f}%'
            color = 'white' if height > 0.3 else 'black'  # White text for tall bars, black for short ones
            
            ax.text(x_pos, y_pos, label_text, 
                   ha='center', va='center', 
                   color=color, 
                   fontsize=enlarged_fontsize,
                   fontweight='bold')
    
    # Add highlight rectangle around Female category if this is the Gender dashboard
    if name == "Gender":
        # Find the index of Female category from the melted data
        female_indices = [i for i, cat in enumerate(kpi_melted['Category']) if cat == 'Female']
        
        if female_indices:  # If Female category exists in the data
            female_idx = female_indices[0]
            
            # Add a rectangular highlight around the Female bar
            for container_idx, container in enumerate(ax.containers):
                bar = container[female_idx]  # Female bar
                
                # Get bar position and dimensions
                height = bar.get_height()
                
                # Draw a rectangle around the Female bar
                rect = plt.Rectangle((female_idx - 0.4, 0), 
                                    0.8, height,
                                    fill=False, linestyle='--', 
                                    linewidth=2, edgecolor='red', alpha=0.8, zorder=5)
                ax.add_patch(rect)
                  # Add a "Female" text label above the bar for the first container only (without arrow)
                if container_idx == 0:
                    ax.text(female_idx, height + height*0.1, 'Female',
                           ha='center', fontsize=enlarged_fontsize, fontweight='bold',
                           color='darkred',
                           bbox=dict(boxstyle='round,pad=0.3', 
                                    fc='white', ec='red', alpha=0.8))

    # Adjust legend
    ax.legend(title='Performance Metric')

    # Chart 3: Performance Multiple (top-right)
    ax = axes[0, 2]

    # Get the 7th and 11th columns (indices 6 and 10)
    col7 = df.columns[6]
    col11 = df.columns[10]

    # Create shorter column names for display
    col7_short = "Performance Multiple KPI Combined"
    col11_short = "Performance Multiple KPI 1"

    # Create a DataFrame with the data and specified columns
    perf_data = pd.DataFrame({
        'Category': df['Category'],
        col7_short: df[col7],
        col11_short: df[col11]
    })

    # Reshape data for seaborn
    perf_melted = pd.melt(perf_data, 
                          id_vars=['Category'], 
                          value_vars=[col7_short, col11_short],
                          var_name='Performance Type', 
                          value_name='Multiple')

    # Using seaborn barplot with grouped bars
    bars = sns.barplot(x='Category', y='Multiple', hue='Performance Type', 
                      data=perf_melted, 
                      palette=['green', 'lightgreen'], 
                      ax=ax)

    ax.set_title(f'Performance Multiple by {name}')
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('Multiple Value')

    # Adding value labels on top of each bar
    for container_idx, container in enumerate(ax.containers):
        labels = []
        for bar in container:
            height = bar.get_height()
            labels.append(f'{height:.1f}x')
        ax.bar_label(container, labels=labels, padding=5)

    # Adjust legend
    ax.legend(title='Multiple Type')

    # Chart 4: Top and Bottom Performers (middle-left) using Seaborn
    ax = axes[1, 0]

    # Get the 5th, 6th, 9th and 10th columns (indices 4, 5, 8, 9)
    col5 = df.columns[4]  # Top performers Combined KPI
    col6 = df.columns[5]  # Bottom performers Combined KPI
    col9 = df.columns[8]  # Top performers KPI 1
    col10 = df.columns[9]  # Bottom performers KPI 1

    # Create shorter column names for display
    col5_short = "Top 10% (Combined)"
    col6_short = "Bottom 10% (Combined)" 
    col9_short = "Top 10% (KPI 1)"
    col10_short = "Bottom 10% (KPI 1)"

    # Create a DataFrame with the data and specified columns
    performer_data = pd.DataFrame({
        'Category': df['Category'],
        col5_short: df[col5],
        col6_short: df[col6],
        col9_short: df[col9],
        col10_short: df[col10]
    })

    # Reshape data for seaborn - first combine top performers
    top_performers = pd.melt(performer_data, 
                         id_vars=['Category'], 
                         value_vars=[col5_short, col9_short],
                         var_name='KPI Type', 
                         value_name='Value')
    top_performers['Performance'] = 'Top 10%'

    # Then combine bottom performers
    bottom_performers = pd.melt(performer_data, 
                         id_vars=['Category'], 
                         value_vars=[col6_short, col10_short],
                         var_name='KPI Type', 
                         value_name='Value')
    bottom_performers['Performance'] = 'Bottom 10%'

    # Combine both datasets
    all_performers = pd.concat([top_performers, bottom_performers])

    # Using seaborn barplot with grouped bars
    bars = sns.barplot(x='Category', y='Value', hue='Performance', 
                      data=all_performers, 
                      palette=['purple', 'lavender'],
                      ax=ax)

    ax.set_title(f'Top vs Bottom Performers by {name}')
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('CAP Value')

    # Adding value labels on top of each bar
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f', padding=5)

    # Adjust legend
    ax.legend(title='Performance Group')

    # Chart 5: Time to First Sale (middle-center) using Seaborn
    ax = axes[1, 1]

    # Get the 12th column (index 11)
    col12 = df.columns[11]

    # Create a DataFrame for the chart
    first_sale_data = pd.DataFrame({
        'Category': df['Category'],
        'Time to First Sale': df[col12]
    })

    # Using seaborn barplot (fixed deprecation warning)
    bars = sns.barplot(x='Category', y='Time to First Sale', data=first_sale_data, 
                      hue='Category', palette=['teal', 'lightseagreen'], legend=False, ax=ax)

    ax.set_title(f'Time to Make First Sale by {name}')
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('Time (months)')

    # Adding value labels on top of each bar
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f months', padding=5)    # Add a horizontal line for the average
    avg_time = df[col12].mean()
    ax.axhline(y=avg_time, color='red', linestyle='--', alpha=0.7)
    
    # Find appropriate empty space for the average label
    right_edge = ax.get_xlim()[1]
    y_min, y_max = ax.get_ylim()
    y_position = y_max * 0.9  # Position at 90% of chart height
    
    ax.text(right_edge * 0.8, y_position, f'Average: {avg_time:.2f} months', 
            color='red', ha='right', va='center', fontsize=14, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='red', alpha=0.7, pad=5, boxstyle='round'))

    # Chart 6: CAR2CATPO Ratio (middle-right)
    ax = axes[1, 2]

    # Get the 13th column (index 12)
    col13 = df.columns[12]

    # Create a DataFrame for the chart
    ratio_data = pd.DataFrame({
        'Category': df['Category'],
        'CAR2CATPO Ratio': df[col13]
    })

    # Using seaborn barplot (fixed deprecation warning)
    bars = sns.barplot(x='Category', y='CAR2CATPO Ratio', data=ratio_data, 
                      hue='Category', palette=['darkgreen', 'mediumseagreen'], legend=False, ax=ax)

    ax.set_title(f'CAR2CATPO Ratio by {name}')
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('Ratio Value')

    # Adding value labels on top of each bar
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', padding=5)    # Add a horizontal line for the average
    avg_ratio = df[col13].mean()
    ax.axhline(y=avg_ratio, color='red', linestyle='--', alpha=0.7)
    
    # Find appropriate empty space for the average label
    right_edge = ax.get_xlim()[1]
    y_min, y_max = ax.get_ylim()
    y_position = y_max * 0.9  # Position at 90% of chart height
    
    ax.text(right_edge * 0.8, y_position, f'Average: {avg_ratio:.2f}', 
            color='red', ha='right', va='center', fontsize=14, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='red', alpha=0.7, pad=5, boxstyle='round'))

    # Chart 7: Attrition Count (bottom-left) using Seaborn
    ax = axes[2, 0]

    # Get the 14th column (index 13)
    col14 = df.columns[13]

    # Create a DataFrame for the chart
    attrition_data = pd.DataFrame({
        'Category': df['Category'],
        'Attrited Employees': df[col14]
    })

    # Using seaborn barplot (fixed deprecation warning)
    bars = sns.barplot(x='Category', y='Attrited Employees', data=attrition_data, 
                      hue='Category', palette=['crimson', 'lightcoral'], legend=False, ax=ax)

    ax.set_title(f'Employee Attrition by {name}')
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('Number of Attrited Employees')

    # Adding value labels on top of each bar
    for container in ax.containers:
        ax.bar_label(container, fmt='%d', padding=5)

    # Calculate and display attrition percentages
    total_per_category = df['CAP LRM cohort'].values
    attrition_per_category = df[col14].values
    attrition_rates = attrition_per_category / total_per_category * 100

    # Add percentage annotations
    for ann_idx, (count, rate) in enumerate(zip(attrition_per_category, attrition_rates)):
        ax.text(ann_idx, count/2, f'{rate:.1f}%', 
                ha='center', va='center', color='white', fontweight='bold')

    # Chart 8: Average Residency (bottom-middle) using Seaborn
    ax = axes[2, 1]

    # Get the 15th and 16th columns (indices 14 and 15)
    col15 = df.columns[14]  # Average Residency of all employees
    col16 = df.columns[15]  # Average Residency of TOP 100 employees

    # Create shorter column names for display
    col15_short = "All Employees"
    col16_short = "Top 100 Performers"

    # Create a DataFrame for the chart
    residency_data = pd.DataFrame({
        'Category': df['Category'],
        col15_short: df[col15],
        col16_short: df[col16]
    })

    # Calculate the percentage differences between Top 100 and All employees
    for idx, row in residency_data.iterrows():
        residency_data.loc[idx, 'Percentage Diff'] = ((row[col16_short] - row[col15_short]) / row[col15_short]) * 100

    # Reshape data for seaborn
    residency_melted = pd.melt(residency_data, 
                             id_vars=['Category'], 
                             value_vars=[col15_short, col16_short],
                             var_name='Employee Group', 
                             value_name='Average Residency')

    # Using seaborn barplot with grouped bars - improved color palette
    bars = sns.barplot(x='Category', y='Average Residency', hue='Employee Group', 
                      data=residency_melted, 
                      palette=['#4472C4', '#8FAADC'], 
                      ax=ax)

    ax.set_title(f'Employment Tenure by {name}', fontsize=11, fontweight='bold')
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('Average Tenure (months)')

    # Adding value labels on top of each bar
    for container_idx, container in enumerate(ax.containers):
        labels = []
        for bar_idx, bar in enumerate(container):
            height = bar.get_height()
            labels.append(f'{height:.2f}')
        ax.bar_label(container, labels=labels, padding=5)    # Add horizontal line for overall average tenure for all employees
    overall_avg = df[col15].mean()
    ax.axhline(y=overall_avg, color='red', linestyle='--', alpha=0.7)
    
    # Find appropriate empty space for the average label
    right_edge = ax.get_xlim()[1]
    y_min, y_max = ax.get_ylim()
    y_position = y_max * 0.9  # Position at 90% of chart height
    
    ax.text(right_edge * 0.8, y_position, f'Average: {overall_avg:.2f}', 
            color='red', ha='right', va='center', fontsize=14, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='red', alpha=0.7, pad=5, boxstyle='round'))

    # Add percentage difference annotations with improved styling
    for point_idx, category_value in enumerate(residency_data['Category']):
        diff_pct = residency_data.loc[residency_data['Category'] == category_value, 'Percentage Diff'].values[0]
        top_val = residency_data.loc[residency_data['Category'] == category_value, col16_short].values[0]
        # Add an arrow showing the increase from general to top performers
        ax.annotate(f'+{diff_pct:.1f}%', 
                    xy=(point_idx, top_val), 
                    xytext=(point_idx, top_val + 0.6),
                    ha='center', 
                    va='bottom',
                    color='darkgreen', 
                    fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', fc='honeydew', ec='green', alpha=0.7))

    # Add business insight annotation
    if len(residency_data) >= 2:  # Make sure there are at least 2 categories to compare
        # Find the category with highest tenure
        max_idx = residency_data[col15_short].idxmax()
        min_idx = residency_data[col15_short].idxmin()
        
        if max_idx != min_idx:  # Make sure there are different values
            higher_category = residency_data.loc[max_idx, 'Category'] 
            lower_category = residency_data.loc[min_idx, 'Category']
            cat_diff = residency_data.loc[max_idx, col15_short] - residency_data.loc[min_idx, col15_short]
            cat_diff_pct = (cat_diff / residency_data.loc[min_idx, col15_short]) * 100
            
            ax.text(0.5, 0.02, 
                    f"{higher_category}s stay {cat_diff_pct:.1f}% longer than {lower_category}s",
                    transform=ax.transAxes, ha='center', fontsize=9, fontstyle='italic', 
                    bbox=dict(facecolor='lightyellow', alpha=0.5, boxstyle='round,pad=0.5'))

    # Adjust legend with better positioning
    ax.legend(title='Employee Group', loc='upper right')

    # Chart 9: Infant Attrition (bottom-right) using Seaborn
    ax = axes[2, 2]

    # Get the last column (index 17)
    last_col = df.columns[-1]  # Using -1 to access the last column

    # Create a DataFrame for the chart with a shorter column name for display
    infant_attrition_data = pd.DataFrame({
        'Category': df['Category'],
        'Infant Attrition': df[last_col] * 100  # Convert to percentage
    })

    # Using seaborn barplot (fixed deprecation warning)
    bars = sns.barplot(x='Category', y='Infant Attrition', data=infant_attrition_data, 
                      hue='Category', palette=['darkblue', 'royalblue'], legend=False, ax=ax)

    ax.set_title(f'Infant Attrition Rate by {name}')
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('Attrition Rate (%)')

    # Adding value labels on top of each bar
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', padding=5)    # Add a horizontal line for the average
    avg_attrition = infant_attrition_data['Infant Attrition'].mean()
    ax.axhline(y=avg_attrition, color='red', linestyle='--', alpha=0.7)
    
    # Find appropriate empty space for the average label
    right_edge = ax.get_xlim()[1]
    y_min, y_max = ax.get_ylim()
    y_position = y_max * 0.9  # Position at 90% of chart height
    
    ax.text(right_edge * 0.8, y_position, f'Average: {avg_attrition:.1f}%', 
            color='red', ha='right', va='center', fontsize=14, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='red', alpha=0.7, pad=5, boxstyle='round'))

    # Adjust layout to prevent overlapping with more space for the title
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Add a subtle watermark with the date
    fig.text(0.99, 0.01, f'Generated: May 31, 2025', fontsize=8, color='gray', 
             ha='right', va='bottom', alpha=0.7)

    # Save the figure with higher resolution
    output_filename = f'{name.lower()}_dashboard.png'
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Dashboard saved as '{output_filename}'")
    
    # Show the plot (comment this out if you don't want to display each plot)
    plt.show()

print("All dashboards created successfully!")
