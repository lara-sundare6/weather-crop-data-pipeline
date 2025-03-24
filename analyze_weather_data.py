import pandas as pd
import matplotlib.pyplot as plt

def load_weather_data(file_path):
    """Load weather data from a CSV file."""
    return pd.read_csv(file_path)

def check_missing_values(df):
    """Check for missing values in the DataFrame."""
    return df.isnull().sum()

def summary_statistics(df):
    """Generate summary statistics for the DataFrame."""
    return df.describe()

def plot_temperature_trends(df):
    """Plot temperature trends."""
    df['temperature'].plot(kind='line', figsize=(10, 6))
    plt.title('Temperature Trends')
    plt.xlabel('Time (Index)')
    plt.ylabel('Temperature (°F)')
    plt.grid()
    plt.show()

def plot_humidity_distribution(df):
    """Plot humidity distribution."""
    df['humidity'].plot(kind='hist', bins=20, figsize=(10, 6), color='skyblue', edgecolor='black')
    plt.title('Humidity Distribution')
    plt.xlabel('Humidity (%)')
    plt.ylabel('Frequency')
    plt.grid()
    plt.show()

def scatter_temperature_vs_humidity(df):
    """Scatter plot of temperature vs. humidity."""
    plt.figure(figsize=(8, 6))
    plt.scatter(df['temperature'], df['humidity'], alpha=0.7, color='orange')
    plt.title('Temperature vs. Humidity')
    plt.xlabel('Temperature (°F)')
    plt.ylabel('Humidity (%)')
    plt.grid()
    plt.show()

def filter_ideal_corn_growth_conditions(df):
    """Filter data for ideal conditions for corn growth."""
    return df[(df['temperature'] >= 60) & (df['temperature'] <= 95)]

def save_to_csv(df, file_path):
    """Save DataFrame to a CSV file."""
    df.to_csv(file_path, index=False)



def plot_growth_conditions(historical_data, crop_name, ideal_temp_range, ideal_precipitation, ideal_sunlight):
    """Plot growth conditions for a specific crop."""
    # Load historical data
    df = pd.read_csv(historical_data)
    
    # Plot temperature
    plt.figure(figsize=(12, 8))
    plt.plot(df['date'], df['temperature'], label='Actual Temperature (°F)', color='orange')
    plt.fill_between(df['date'], ideal_temp_range[0], ideal_temp_range[1], color='orange', alpha=0.2, label='Ideal Temperature Range')
    
    # Plot precipitation
    plt.bar(df['date'], df['precipitation'], label='Actual Precipitation (in)', color='blue', alpha=0.6)
    plt.axhline(y=ideal_precipitation, color='blue', linestyle='--', label='Ideal Precipitation')
    
    # Plot sunlight (estimated from cloud cover)
    sunlight_hours = 24 * (1 - df['cloud_cover'] / 100)
    plt.plot(df['date'], sunlight_hours, label='Estimated Sunlight Hours', color='yellow')
    plt.axhline(y=ideal_sunlight, color='yellow', linestyle='--', label='Ideal Sunlight Hours')
    
    # Add labels, title, and legend
    plt.title(f"Chicago Urban Farm Growth Conditions: {crop_name}")
    plt.xlabel("Date")
    plt.ylabel("Environmental Factors")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # Load the weather data
    df = load_weather_data('weather_data.csv')

    # Check for missing values
    print("Missing Values:\n", check_missing_values(df))

    # Summary statistics
    print("Summary Statistics:\n", summary_statistics(df))

    # Plot temperature trends
    plot_temperature_trends(df)

    # Plot humidity distribution
    plot_humidity_distribution(df)

    # Scatter plot of temperature vs. humidity
    scatter_temperature_vs_humidity(df)

    # Filter data for ideal conditions for corn growth
    ideal_corn_growth_conditions = filter_ideal_corn_growth_conditions(df)
    print("Ideal Conditions for Corn Growth:\n", ideal_corn_growth_conditions)

    # Save ideal conditions to a new CSV file
    save_to_csv(ideal_corn_growth_conditions, 'ideal_conditions.csv')
    print("Ideal conditions saved to 'ideal_conditions.csv'")

    # Plot growth conditions for a specific crop
    crop_name = "Tomatoes"
    ideal_temp_range = (70, 85)  # Ideal temperature range in °F
    ideal_precipitation = 0.5  # Ideal daily precipitation in inches
    ideal_sunlight = 10  # Ideal daily sunlight hours
    
    plot_growth_conditions('historical_weather_data.csv', crop_name, ideal_temp_range, ideal_precipitation, ideal_sunlight)