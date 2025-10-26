import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from earthquakes import get_data


def extract_earthquake_data(data):
    """
    Extract year, magnitude data from earthquake features.
    
    Returns:
        years (numpy array): Array of years for each earthquake
        magnitudes (numpy array): Array of magnitudes for each earthquake
    """
    years = []
    magnitudes = []
    
    for earthquake in data["features"]:
        # Extract timestamp (in milliseconds since epoch)
        timestamp_ms = earthquake["properties"]["time"]
        # Convert to datetime and extract year
        year = datetime.fromtimestamp(timestamp_ms / 1000).year
        
        # Extract magnitude
        magnitude = earthquake["properties"]["mag"]
        
        years.append(year)
        magnitudes.append(magnitude)

    return np.array(years), np.array(magnitudes)


def analyze_earthquakes_by_year(years, magnitudes):
    """
    Analyze earthquake frequency and average magnitude by year.
    
    Returns:
        unique_years (numpy array): Sorted array of unique years
        frequency_per_year (numpy array): Number of earthquakes per year
        avg_magnitude_per_year (numpy array): Average magnitude per year
    """
    # Get unique years and sort them
    unique_years = np.unique(years)
    
    frequency_per_year = []
    avg_magnitude_per_year = []
    
    for year in unique_years:
        # Find earthquakes for this year
        year_mask = (years == year)
        year_magnitudes = magnitudes[year_mask]
        
        # Calculate frequency and average magnitude
        frequency = len(year_magnitudes)
        avg_magnitude = np.mean(year_magnitudes)
        
        frequency_per_year.append(frequency)
        avg_magnitude_per_year.append(avg_magnitude)
    
    return unique_years, np.array(frequency_per_year), np.array(avg_magnitude_per_year)


def create_plots(years, frequency, avg_magnitude):
    """
    Create and save a combined plot: frequency (bars) and average magnitude (line) on the same chart.
    """
    # Create figure with single subplot
    fig, ax1 = plt.subplots(1, 1, figsize=(14, 8))
    
    # Plot 1: Frequency of earthquakes per year (left y-axis)
    color1 = 'steelblue'
    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('Number of Earthquakes', color=color1, fontsize=12)
    bars = ax1.bar(years, frequency, color=color1, alpha=0.7, label='Earthquake Frequency')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_xlim(years[0] - 1, years[-1] + 1)
    
    # Force integer years on x-axis
    ax1.set_xticks(years)
    ax1.set_xticklabels([int(year) for year in years])
    
    ax1.grid(True, alpha=0.3)
    
    # Create second y-axis for magnitude
    ax2 = ax1.twinx()
    
    # Plot 2: Average magnitude per year (right y-axis)
    color2 = 'red'
    ax2.set_ylabel('Average Magnitude', color=color2, fontsize=12)
    line = ax2.plot(years, avg_magnitude, marker='o', linewidth=3, markersize=8, 
                    color=color2, label='Average Magnitude')
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # Add title
    plt.title('UK Earthquake Analysis: Frequency and Average Magnitude per Year (2000-2018)', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Add legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('earthquake_analysis_combined.png', dpi=300, bbox_inches='tight')
    print("Combined plot saved as 'earthquake_analysis_combined.png'")
    
    # Show the plot
    plt.show()


def print_summary_statistics(years, frequency, avg_magnitude):
    """
    Print summary statistics about the earthquake data.
    """
    print("\n" + "="*50)
    print("EARTHQUAKE ANALYSIS SUMMARY")
    print("="*50)
    print(f"Data period: {years[0]} - {years[-1]}")
    print(f"Total years analyzed: {len(years)}")
    print(f"Total earthquakes: {np.sum(frequency)}")
    print(f"Average earthquakes per year: {np.mean(frequency):.1f}")
    print(f"Year with most earthquakes: {years[np.argmax(frequency)]} ({np.max(frequency)} earthquakes)")
    print(f"Year with fewest earthquakes: {years[np.argmin(frequency)]} ({np.min(frequency)} earthquakes)")
    print(f"Overall average magnitude: {np.mean(avg_magnitude):.2f}")
    print(f"Highest average magnitude year: {years[np.argmax(avg_magnitude)]} (avg: {np.max(avg_magnitude):.2f})")
    print(f"Lowest average magnitude year: {years[np.argmin(avg_magnitude)]} (avg: {np.min(avg_magnitude):.2f})")


def main():
    """
    Main function to run the earthquake analysis.
    """
    print("Loading earthquake data...")
    
    # Load data (try local file first, then API if needed)
    data = get_data(use_local_file=True)
    
    print(f"Loaded {len(data['features'])} earthquakes")
    
    # Extract years and magnitudes
    years, magnitudes = extract_earthquake_data(data)
    
    # Analyze by year
    unique_years, frequency_per_year, avg_magnitude_per_year = analyze_earthquakes_by_year(years, magnitudes)
    
    # Print summary statistics
    print_summary_statistics(unique_years, frequency_per_year, avg_magnitude_per_year)
    
    # Create and save plots
    create_plots(unique_years, frequency_per_year, avg_magnitude_per_year)


if __name__ == "__main__":
    main()