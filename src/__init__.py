"""Integration tests for weather dashboard."""
import pytest
from unittest.mock import patch, MagicMock
import datetime
from src.weatherdashboard import fetch_weather_data, filter_by_date, plot_weather


class TestIntegration:
    """Integration test suite for complete workflow."""

    @patch('src.weatherdashboard.requests.get')
    @patch('src.weatherdashboard.plt.show')
    def test_end_to_end_workflow(self, mock_show, mock_get):
        """Test complete workflow: fetch -> filter -> plot."""
        now = datetime.datetime.now()
        unix_time = int(now.timestamp())

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'list': [
                {'dt': unix_time + (i * 3600), 'main': {'temp': 20.0 + i, 'humidity': 50 + (i % 20)}}
                for i in range(8)
            ],
            'city': {'name': 'Mumbai'}
        }
        mock_get.return_value = mock_response

        times, temps, humidity, city = fetch_weather_data('Mumbai')
        assert len(times) == 8
        assert city == 'Mumbai'

        f_times, f_temps, f_humidity = filter_by_date(times, temps, humidity, 'today')
        assert len(f_times) > 0
        assert len(f_times) == len(f_temps) == len(f_humidity)

        plot_weather(f_times, f_temps, f_humidity, city, 'today')
        mock_show.assert_called_once()

    @patch('src.weatherdashboard.requests.get')
    def test_data_consistency_throughout_pipeline(self, mock_get):
        """Test that data remains consistent through pipeline."""
        now = datetime.datetime.now()
        unix_time = int(now.timestamp())
        original_temps = [20.0, 21.0, 22.0]
        original_humidity = [50, 55, 60]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'list': [
                {'dt': unix_time + (i * 3600), 'main': {'temp': original_temps[i], 'humidity': original_humidity[i]}}
                for i in range(3)
            ],
            'city': {'name': 'London'}
        }
        mock_get.return_value = mock_response

        times, temps, humidity, city = fetch_weather_data('London')
        assert temps == original_temps
        assert humidity == original_humidity

        f_times, f_temps, f_humidity = filter_by_date(times, temps, humidity, 'today')
        assert f_temps == original_temps
        assert f_humidity == original_humidity

    @patch('src.weatherdashboard.requests.get')
    def test_error_handling_in_pipeline(self, mock_get):
        """Test error handling at each stage of pipeline."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'message': 'city not found'}
        mock_get.return_value = mock_response

        times, temps, humidity, city = fetch_weather_data('InvalidCity')
        assert times == []
        assert temps == []
        assert humidity == []

        f_times, f_temps, f_humidity = filter_by_date(times, temps, humidity, 'today')
        assert f_times == []
        assert f_temps == []
        assert f_humidity == []

    @patch('src.weatherdashboard.requests.get')
    @patch('src.weatherdashboard.plt.show')
    def test_multiple_cities_workflow(self, mock_show, mock_get):
        """Test workflow with different cities."""
        cities = ['Mumbai', 'London', 'Tokyo']

        for city in cities:
            now = datetime.datetime.now()
            unix_time = int(now.timestamp())

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'list': [
                    {'dt': unix_time + (i * 3600), 'main': {'temp': 20.0 + i, 'humidity': 50 + i}}
                    for i in range(4)
                ],
                'city': {'name': city}
            }
            mock_get.return_value = mock_response

            times, temps, humidity, returned_city = fetch_weather_data(city)
            assert returned_city == city
            assert len(times) == 4

            f_times, f_temps, f_humidity = filter_by_date(times, temps, humidity, 'today')
            if f_times:
                plot_weather(f_times, f_temps, f_humidity, city, 'today')

            assert mock_show.called
