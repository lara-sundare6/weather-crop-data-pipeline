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