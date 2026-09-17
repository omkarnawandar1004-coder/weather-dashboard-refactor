"""Unit tests for weather data fetching functionality."""
import pytest
from unittest.mock import patch, MagicMock
import datetime
from src.weatherdashboard import fetch_weather_data


class TestFetchWeatherData:
    """Test suite for fetch_weather_data function."""

    @patch('src.weatherdashboard.requests.get')
    def test_fetch_weather_data_success(self, mock_get):
        """Test successful weather data fetch."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'list': [
                {'dt': 1625097600, 'main': {'temp': 25.0, 'humidity': 60}},
                {'dt': 1625101200, 'main': {'temp': 26.0, 'humidity': 55}}
            ],
            'city': {'name': 'Mumbai'}
        }
        mock_get.return_value = mock_response

        times, temps, humidity, city = fetch_weather_data('Mumbai')

        assert len(times) == 2
        assert len(temps) == 2
        assert len(humidity) == 2
        assert city == 'Mumbai'
        assert temps == [25.0, 26.0]
        assert humidity == [60, 55]
        mock_get.assert_called_once()

    @patch('src.weatherdashboard.requests.get')
    def test_fetch_weather_data_api_error(self, mock_get):
        """Test API error handling."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'message': 'city not found'}
        mock_get.return_value = mock_response

        times, temps, humidity, city = fetch_weather_data('InvalidCity')

        assert times == []
        assert temps == []
        assert humidity == []
        assert city == 'InvalidCity'

    @patch('src.weatherdashboard.requests.get')
    def test_fetch_weather_data_missing_list(self, mock_get):
        """Test when 'list' key is missing in response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'city': {'name': 'Mumbai'}}
        mock_get.return_value = mock_response

        times, temps, humidity, city = fetch_weather_data('Mumbai')

        assert times == []
        assert temps == []
        assert humidity == []

    @patch('src.weatherdashboard.requests.get')
    def test_fetch_weather_data_empty_list(self, mock_get):
        """Test when forecast list is empty."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'list': [], 'city': {'name': 'Mumbai'}}
        mock_get.return_value = mock_response

        times, temps, humidity, city = fetch_weather_data('Mumbai')

        assert times == []
        assert temps == []
        assert humidity == []
        assert city == 'Mumbai'

    @patch('src.weatherdashboard.requests.get')
    def test_fetch_weather_data_large_dataset(self, mock_get):
        """Test with larger dataset (5-day forecast)."""
        forecast_list = [
            {'dt': 1625097600 + (i * 3600), 'main': {'temp': 20.0 + i, 'humidity': 50 + (i % 20)}}
            for i in range(40)
        ]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'list': forecast_list, 'city': {'name': 'London'}}
        mock_get.return_value = mock_response

        times, temps, humidity, city = fetch_weather_data('London')

        assert len(times) == 40
        assert len(temps) == 40
        assert len(humidity) == 40
        assert city == 'London'
        assert temps[0] == 20.0
        assert temps[-1] == 59.0

    @patch('src.weatherdashboard.requests.get')
    def test_fetch_weather_data_timestamp_conversion(self, mock_get):
        """Test Unix timestamp conversion to datetime."""
        unix_timestamp = 1625097600
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'list': [{'dt': unix_timestamp, 'main': {'temp': 25.0, 'humidity': 60}}],
            'city': {'name': 'Mumbai'}
        }
        mock_get.return_value = mock_response

        times, temps, humidity, city = fetch_weather_data('Mumbai')

        assert len(times) == 1
        assert isinstance(times[0], datetime.datetime)
        assert times[0].year == 2021
        assert times[0].month == 7
        assert times[0].day == 1
