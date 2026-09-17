"""Unit tests for weather visualization functionality."""
import pytest
from unittest.mock import patch
import datetime
from src.weatherdashboard import plot_weather


class TestPlotWeather:
    """Test suite for plot_weather function."""

    @patch('src.weatherdashboard.plt.show')
    @patch('src.weatherdashboard.sns.lineplot')
    @patch('src.weatherdashboard.plt.figure')
    @patch('src.weatherdashboard.plt.subplot')
    @patch('src.weatherdashboard.plt.title')
    @patch('src.weatherdashboard.plt.xlabel')
    @patch('src.weatherdashboard.plt.ylabel')
    @patch('src.weatherdashboard.plt.tight_layout')
    def test_plot_weather_success(
        self,
        mock_tight_layout,
        mock_ylabel,
        mock_xlabel,
        mock_title,
        mock_subplot,
        mock_figure,
        mock_lineplot,
        mock_show,
    ):
        """Test successful weather plot creation."""
        now = datetime.datetime.now()
        times = [now, now + datetime.timedelta(hours=1)]
        temps = [20.0, 21.0]
        humidity = [50, 55]
        city = 'Mumbai'
        date_label = 'today'

        plot_weather(times, temps, humidity, city, date_label)

        mock_figure.assert_called_once()
        mock_subplot.assert_called()
        mock_lineplot.assert_called()
        mock_tight_layout.assert_called_once()
        mock_show.assert_called_once()

    @patch('src.weatherdashboard.plt.show')
    def test_plot_weather_empty_data(self, mock_show):
        """Test plotting with empty data."""
        plot_weather([], [], [], 'Mumbai', 'today')
        mock_show.assert_not_called()

    @patch('src.weatherdashboard.plt.show')
    @patch('src.weatherdashboard.plt.figure')
    def test_plot_weather_single_datapoint(self, mock_figure, mock_show):
        """Test plotting with single data point."""
        now = datetime.datetime.now()
        times = [now]
        temps = [20.0]
        humidity = [50]
        city = 'London'
        date_label = 'today'

        plot_weather(times, temps, humidity, city, date_label)

        mock_figure.assert_called_once()
        mock_show.assert_called_once()

    @patch('src.weatherdashboard.plt.show')
    @patch('src.weatherdashboard.sns.set_style')
    @patch('src.weatherdashboard.plt.figure')
    def test_plot_weather_large_dataset(self, mock_figure, mock_set_style, mock_show):
        """Test plotting with large dataset."""
        now = datetime.datetime.now()
        times = [now + datetime.timedelta(hours=i) for i in range(40)]
        temps = [20.0 + i for i in range(40)]
        humidity = [50 + (i % 20) for i in range(40)]
        city = 'Tokyo'
        date_label = '2025-05-27'

        plot_weather(times, temps, humidity, city, date_label)

        mock_figure.assert_called_once()
        mock_set_style.assert_called_once()
        mock_show.assert_called_once()

    @patch('src.weatherdashboard.plt.show')
    @patch('src.weatherdashboard.plt.title')
    @patch('src.weatherdashboard.plt.figure')
    def test_plot_weather_title_formatting(self, mock_figure, mock_title, mock_show):
        """Test that plot titles are formatted correctly."""
        now = datetime.datetime.now()
        times = [now]
        temps = [20.0]
        humidity = [50]
        city = 'Mumbai'
        date_label = 'today'

        plot_weather(times, temps, humidity, city, date_label)

        title_calls = [str(call) for call in mock_title.call_args_list]
        title_str = ' '.join(title_calls)
        assert 'Mumbai' in title_str or city in title_str

    @patch('src.weatherdashboard.plt.show')
    @patch('src.weatherdashboard.plt.figure')
    def test_plot_weather_mismatched_lengths(self, mock_figure, mock_show):
        """Test behavior with mismatched data lengths."""
        now = datetime.datetime.now()
        times = [now, now + datetime.timedelta(hours=1)]
        temps = [20.0, 21.0, 22.0]
        humidity = [50]
        city = 'Delhi'
        date_label = 'today'

        try:
            plot_weather(times, temps, humidity, city, date_label)
        except (ValueError, IndexError):
            pass

    @patch('src.weatherdashboard.plt.show')
    @patch('src.weatherdashboard.plt.figure')
    def test_plot_weather_extreme_temperatures(self, mock_figure, mock_show):
        """Test plotting with extreme temperature values."""
        now = datetime.datetime.now()
        times = [now, now + datetime.timedelta(hours=1)]
        temps = [-40.0, 50.0]
        humidity = [0, 100]
        city = 'Siberia'
        date_label = 'today'

        plot_weather(times, temps, humidity, city, date_label)

        mock_figure.assert_called_once()
        mock_show.assert_called_once()
