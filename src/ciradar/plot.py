import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, linregress
import statsmodels.api as sm
from statsmodels.formula.api import ols

def execute(csv_file_path):
    if not os.path.exists(csv_file_path):
        print("CSV file not found. Please load data first.")
        return

    df = pd.read_csv(csv_file_path)
    if 'Merge Date' not in df.columns:
        print("Error: 'Merge Date' column not found in the CSV file.")
        return

    df['Merge Date'] = pd.to_datetime(df['Merge Date'])
    df['Time to Integration (days)'] = pd.to_numeric(df['Time to Integration (days)'], errors='coerce')
    df.sort_values('Merge Date', inplace=True)  # Ensure data is sorted by 'Merge Date'
    df.drop_duplicates(subset='Merge Date', inplace=True)  # Ensure no duplicate dates

    plot_rolling_stats(df.copy())
    plot_total_changes_vs_cycle_time_with_regression(df.copy())
    plot_monthly_merged_prs(df.copy())
    plot_monthly_total_lines_changed(df.copy())
    plot_monthly_proportion_under_24h(df.copy())

def plot_rolling_stats(df):
    df.set_index('Merge Date', inplace=True)
    rolling_avg = df['Time to Integration (days)'].rolling('30D').mean()
    rolling_std = df['Time to Integration (days)'].rolling('30D').std()
    plt.figure(figsize=(14, 7))
    plt.scatter(df.index, df['Time to Integration (days)'], alpha=0.5, label='Daily Data')
    plt.plot(rolling_avg.index, rolling_avg, color='red', label='Rolling Monthly Average')
    plt.fill_between(rolling_std.index, rolling_avg - rolling_std, rolling_avg + rolling_std, color='red', alpha=0.3)
    plt.title('Time to Integration for Pull Requests')
    plt.xlabel('Merge Date')
    plt.ylabel('Time to Integration (days)')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_total_changes_vs_cycle_time_with_regression(df):
    df.set_index('Merge Date', inplace=True)  # Set 'Merge Date' as index if not already
    df['Total Lines Changed'] = df['Total Additions'] + df['Total Deletions']
    df['Merge Year'] = df.index.year

    plt.figure(figsize=(14, 7))
    scatter = plt.scatter(df['Total Lines Changed'], df['Time to Integration (days)'],
                          c=df['Merge Year'], alpha=0.5, cmap='viridis')
    plt.colorbar(scatter, label='Merge Year')

    slope, intercept, r_value, p_value, std_err = linregress(df['Total Lines Changed'], df['Time to Integration (days)'])
    regression_line = slope * df['Total Lines Changed'] + intercept
    plt.plot(df['Total Lines Changed'], regression_line, 'r-', label=f'Linear fit: $R^2$ = {r_value ** 2:.2f}')

    plt.title(f'Total Changes vs. PR Cycle Time')
    plt.xlabel('Total Changes (Additions + Deletions)')
    plt.ylabel('PR Cycle Time (days)')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_monthly_total_lines_changed(df):
    if 'Total Additions' in df.columns and 'Total Deletions' in df.columns:
        df['Total Lines Changed'] = df['Total Additions'] + df['Total Deletions']
    else:
        print("Error: 'Total Additions' or 'Total Deletions' columns not found.")
        return

    df.set_index('Merge Date', inplace=True)  # Set 'Merge Date' as index if not already
    monthly_total_lines = df['Total Lines Changed'].resample('M').sum()
    plt.figure(figsize=(14, 7))
    plt.plot(monthly_total_lines.index, monthly_total_lines, label='Monthly Total Lines Changed', marker='o', linestyle='-')
    plt.title('Monthly Total Lines Changed')
    plt.xlabel('Month')
    plt.ylabel('Total Lines Changed')
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_monthly_merged_prs(df):
    df.set_index('Merge Date', inplace=True)  # Set 'Merge Date' as index if not already
    monthly_counts = df.resample('M').size()
    plt.figure(figsize=(14, 7))
    plt.plot(monthly_counts.index, monthly_counts, label='Monthly Merged PRs', marker='o', linestyle='-')
    plt.title('Monthly Merged PRs')
    plt.xlabel('Month')
    plt.ylabel('Number of Merged PRs')
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_monthly_proportion_under_24h(df):
    df.set_index('Merge Date', inplace=True)
    df['Under 24h'] = df['Time to Integration (days)'] < 1
    monthly_counts = df.resample('M').size()
    monthly_under_24h_counts = df.resample('M')['Under 24h'].sum()
    monthly_proportion = monthly_under_24h_counts / monthly_counts

    plt.figure(figsize=(14, 7))
    plt.plot(monthly_proportion.index, monthly_proportion, label='Proportion of Integrations under 24 hours', marker='o', linestyle='-')
    plt.title('Monthly Proportion of Integration Cycles under 24 Hours')
    plt.xlabel('Month')
    plt.ylabel('Proportion')
    plt.grid(True)
    plt.legend()
    plt.show()
