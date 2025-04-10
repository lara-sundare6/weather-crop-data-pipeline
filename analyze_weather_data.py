import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


CROP_CONDITIONS = {
    "Corn": {
        "temperature_range": (77, 91),  # Ideal temperature range in °F
        "precipitation": 0.2,  # Ideal daily precipitation in inches
        "sunlight": 8  # Ideal daily sunlight hours
    },
    "Tomatoes": {
        "temperature_range": (70, 80),
        "precipitation": 0.2,
        "sunlight": 8
    },
    "Arugula": {
        "temperature_range": (45, 65),
        "precipitation": 0.2,
        "sunlight": 6
    }
}

def load_weather_data(file_path):
    """Load weather data from a CSV file."""
    df = pd.read_csv(file_path)
    # Convert precipitation from mm to inches
    df['precipitation'] = df['precipitation'] / 25.4  # Convert mm to inches
    return df

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

def filter_ideal_growth_conditions(df, crop_name):
    """Filter data for ideal growth conditions for a specific crop."""
    conditions = CROP_CONDITIONS.get(crop_name)
    if not conditions:
        raise ValueError(f"Ideal conditions for crop '{crop_name}' are not defined.")
    
    temp_min, temp_max = conditions["temperature_range"]
    return df[(df['temperature'] >= temp_min) & (df['temperature'] <= temp_max)]

def save_to_csv(df, file_path):
    """Save DataFrame to a CSV file."""
    df.to_csv(file_path, index=False)



def plot_growth_conditions(historical_data, crop_name):
    """Plot growth conditions for a specific crop."""
    # Load historical data
    df = pd.read_csv(historical_data)
    
    # Convert 'date' column to datetime for better handling
    df['date'] = pd.to_datetime(df['date'])
    
    # Get ideal conditions for the crop
    conditions = CROP_CONDITIONS.get(crop_name)
    if not conditions:
        raise ValueError(f"Ideal conditions for crop '{crop_name}' are not defined.")
    
    ideal_temp_range = conditions["temperature_range"]
    ideal_precipitation = conditions["precipitation"]
    ideal_sunlight = conditions["sunlight"]
    
    # Calculate sunlight hours from cloud cover
    df['sunlight_hours'] = 24 * (1 - df['cloud_cover'] / 100)
    
    # Identify critical events
    frost_days = df[df['temperature'] < 32]  # Days with freezing temperatures
    heat_stress_days = df[df['temperature'] > ideal_temp_range[1]]  # Days above ideal range
    
    # Create subplots
    fig, axs = plt.subplots(3, 1, figsize=(12, 15), sharex=True)
    
    # Plot temperature
    axs[0].plot(df['date'], df['temperature'], label='Actual Temperature (°F)', color='orange')
    axs[0].fill_between(df['date'], ideal_temp_range[0], ideal_temp_range[1], color='orange', alpha=0.2, label='Ideal Temperature Range')
    axs[0].scatter(frost_days['date'], frost_days['temperature'], color='blue', label='Frost Days (<32°F)', zorder=5)
    axs[0].scatter(heat_stress_days['date'], heat_stress_days['temperature'], color='red', label='Heat Stress Days', zorder=5)
    axs[0].set_ylabel("Temperature (°F)")
    axs[0].set_title(f"Temperature Trends for {crop_name}")
    axs[0].legend()
    
    # Plot precipitation
    axs[1].bar(df['date'], df['precipitation'], label='Actual Precipitation (in)', color='blue', alpha=0.6)
    axs[1].axhline(y=ideal_precipitation, color='blue', linestyle='--', label='Ideal Precipitation')
    axs[1].set_ylabel("Precipitation (in)")
    axs[1].set_title(f"Precipitation Trends for {crop_name}")
    axs[1].legend()
    
    # Plot sunlight
    axs[2].plot(df['date'], df['sunlight_hours'], label='Estimated Sunlight Hours', color='yellow')
    axs[2].axhline(y=ideal_sunlight, color='yellow', linestyle='--', label='Ideal Sunlight Hours')
    axs[2].set_ylabel("Sunlight (hours)")
    axs[2].set_title(f"Sunlight Trends for {crop_name}")
    axs[2].legend()
    
    # Format the X-axis for better readability
    axs[2].xaxis.set_major_locator(mdates.MonthLocator())  # Show one tick per month
    axs[2].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Format as "Month Year"
    fig.autofmt_xdate()  # Rotate and align date labels
    
    # Save the graph to a file
    output_dir = "graphs"
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
    output_file = os.path.join(output_dir, f"{crop_name}_growth_conditions.png")
    plt.tight_layout()
    plt.savefig(output_file)  # Save the graph as a PNG file
    print(f"Graph saved to {output_file}")

if __name__ == '__main__':
    # Load the weather data
    df = load_weather_data('historical_weather_data.csv')

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

    # Specify the crop name
    crop_name = "Tomatoes"  # Change this to the desired crop (e.g., "Corn", "Lettuce")

    # Filter data for ideal growth conditions for the specified crop
    ideal_growth_conditions = filter_ideal_growth_conditions(df, crop_name)
    print(f"Ideal Conditions for {crop_name} Growth:\n", ideal_growth_conditions)

    # Save ideal conditions to a new CSV file
    save_to_csv(ideal_growth_conditions, f'ideal_conditions_{crop_name.lower()}.csv')
    print(f"Ideal conditions saved to 'ideal_conditions_{crop_name.lower()}.csv'")

    # Plot growth conditions for the specified crop
    plot_growth_conditions('historical_weather_data.csv', crop_name)