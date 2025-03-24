import pandas as pd
from analyze_weather_data import (
    check_missing_values,
    summary_statistics,
    filter_ideal_corn_growth_conditions,
)

def test_check_missing_values():
    """Test for missing values."""
    df = pd.DataFrame({
        'temperature': [55, 65, None],
        'humidity': [30, None, 50],
    })
    result = check_missing_values(df)
    expected = pd.Series([1, 1], index=['temperature', 'humidity'])
    pd.testing.assert_series_equal(result, expected)

def test_summary_statistics():
    """Test summary statistics."""
    df = pd.DataFrame({
        'temperature': [55, 65, 75],
        'humidity': [30, 40, 50],
    })
    result = summary_statistics(df)
    assert 'temperature' in result.columns
    assert 'humidity' in result.columns

def test_filter_ideal_corn_growth_conditions():
    """Test filtering for ideal corn growth conditions."""
    df = pd.DataFrame({
        'temperature': [55, 65, 75, 85, 95, 105],
        'humidity': [30, 40, 50, 60, 70, 80],
    })
    result = filter_ideal_corn_growth_conditions(df)
    expected = pd.DataFrame({
        'temperature': [65, 75, 85, 95],
        'humidity': [40, 50, 60, 70],
    })
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)