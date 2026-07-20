import pandas as pd
import numpy as np
import sys
import os

def parse_time_to_minutes(time_str):
    if pd.isna(time_str) or time_str == 'NP' or ':' not in str(time_str):
        return None
    try:
        parts = str(time_str).split(':')
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 60 + int(parts[1]) + int(parts[2]) / 60
    except:
        return None
    return None

def format_minutes_to_time(minutes):
    if pd.isna(minutes) or minutes == "" or minutes is np.nan:
        return ""
    h = int(minutes // 60)
    m = int(round(minutes % 60))
    if m == 60:
        h += 1
        m = 0
    return f"{h:02d}:{m:02d}"

# Input validation, check for required argument (input file, output file)
def analyze_pbp():
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_csv> <output_xlsx>")
        return

    input_csv = sys.argv[1]
    output_xlsx = sys.argv[2]

    if not os.path.exists(input_csv):
        print(f"Error: Input file {input_csv} not found.")
        return

    # Load and clean headers
    df = pd.read_csv(input_csv)
    
    # 1. Enrollment Numbers
    enrollment = df.groupby('Year').size().reset_index(name='Total Participants')

    # 2. Female Participation
    df['is_female'] = df['Gender'].apply(lambda x: 1 if str(x).strip().upper() == 'F' else 0)
    female_stats = df.groupby('Year').agg(
        Female_Count=('is_female', 'sum'),
        Total_Count=('Year', 'count')
    ).reset_index()
    female_stats['Percentage (%)'] = (female_stats['Female_Count'] / female_stats['Total_Count'] * 100).round(2)
    female_participation = female_stats[['Year', 'Female_Count', 'Percentage (%)']]

    # 3. Time Statistics (Updated with 25th Percentile)
    df['Minutes'] = df['Time'].apply(parse_time_to_minutes)
    time_df = df.dropna(subset=['Minutes'])

    def get_mode(x):
        m = x.mode()
        return m.iloc[0] if not m.empty else np.nan

    # Added 'quantile' to the aggregation to capture the 25th percentile
    time_stats = time_df.groupby('Year')['Minutes'].agg(
        Fastest='min',
        Percentile_25=lambda x: x.quantile(0.25),
        Mean='mean',
        Median='median',
        Mode=get_mode,
        Slowest='max'
    ).reset_index()

    # Convert minutes back to HH:MM strings
    time_display = time_stats.copy()
    for col in ['Fastest', 'Percentile_25', 'Mean', 'Median', 'Mode', 'Slowest']:
        time_display[col] = time_display[col].apply(format_minutes_to_time)

    # Output to Excel with multiple tabs
    with pd.ExcelWriter(output_xlsx, engine='openpyxl') as writer:
        enrollment.to_excel(writer, sheet_name='Enrollment Trends', index=False)
        female_participation.to_excel(writer, sheet_name='Female Participation', index=False)
        time_display.to_excel(writer, sheet_name='Time Statistics', index=False)

    print(f"Analysis complete. Results saved to {output_xlsx}")

if __name__ == "__main__":
    analyze_pbp()
