"""Unit tests for weather data filtering functionality."""
import pytest
from unittest.mock import patch
import datetime
from src.weatherdashboard import filter_by_date


class TestFilterByDate:
    """Test suite for filter_by_date function."""

    def test_filter_by_date_today(self):
        """Test filtering data for today's date."""
        now = datetime.datetime.now()
        times = [
            now,
            now + datetime.timedelta(hours=1),
            now + datetime.timedelta(hours=2),
            now + datetime.timedelta(days=1),
        ]
        temps = [20.0, 21.0, 22.0, 23.0]
        humidity = [50, 55, 60, 65]

        f_times, f_temps, f_humidity = filter_by_date(times, temps, humidity, 'today')

        assert len(f_times) == 3
        assert len(f_temps) == 3
        assert len(f_humidity) == 3
        assert f_temps == [20.0, 21.0, 22.0]
        assert f_humidity == [50, 55, 60]

    def test_filter_by_date_tomorrow(self):
        """Test filtering data for tomorrow's date."""
        now = datetime.datetime.now()
        tomorrow = now + datetime.timedelta(days=1)
        times = [now, tomorrow, tomorrow + datetime.timedelta(hours=1)]
        temps = [20.0, 21.0, 22.0]
        humidity = [50, 55, 60]

        f_times, f_temps, f_humidity = filter_by_date(times, temps, humidity, 'tomorrow')

        assert len(f_times) == 2
        assert f_temps == [21.0, 22.0]
        assert f_humidity == [55, 60]

    def test_filter_by_date_specific_date_format(self):
        """Test filtering with specific date format (YYYY-MM-DD)."""
        date1 = datetime.datetime(2025, 5, 27, 10, 0, 0)
        date2 = datetime.datetime(2025, 5, 27, 11, 0, 0)
        date3 = datetime.datetime(2025, 5, 28, 10, 0, 0)
        times = [date1, date2, date3]
        temps = [20.0, 21.0, 22.0]
        humidity = [50, 55, 60]

        f_times, f_temps, f_humidity = filter_by_date(times, temps, humidity, '2025-05-27')

        assert len(f_times) == 2
        assert f_temps == [20.0, 21.0]
        assert f_humidity == [50, 55]

    def test_filter_by_date_invalid_date(self):
        """Test with invalid date format."""
        now = datetime.datetime.now()
        times = [now]
        temps = [20.0]
        humidity = [50]

        f_times, f_temps, f_humidity = filter_by_date(times, temps, humidity, 'invalid-date-xyz')

        assert f_times == []
        assert f_temps == []
        assert f_humidity == []

    def test_filter_by_date_no_matching_data(self):
        """Test when no data matches the filter date."""
        now = datetime.datetime.now()
        times = [now]
        temps = [20.0]
        humidity = [50]

        f_times, f_temps, f_humidity = filter_by_date(times, temps, humidity, 'tomorrow')

        assert f_times == []
        assert f_temps == []
        assert f_humidity == []

    def test_filter_by_date_preserves_data_order(self):
        """Test that filtered data maintains chronological order."""
        now = datetime.datetime.now()
        times = [
            now + datetime.timedelta(hours=3),
            now,
            now + datetime.timedelta(hours=1),
            now + datetime.timedelta(hours=2),
        ]
        temps = [23.0, 20.0, 21.0, 22.0]
        humidity = [65, 50, 55, 60]

        f_times, f_temps, f_humidity = filter_by_date(times, temps, humidity, 'today')

        assert len(f_times) == 4
        assert f_temps == [23.0, 20.0, 21.0, 22.0]
        assert f_humidity == [65, 50, 55, 60]

    def test_filter_by_date_empty_input(self):
        """Test with empty input lists."""
        f_times, f_temps, f_humidity = filter_by_date([], [], [], 'today')

        assert f_times == []
        assert f_temps == []
        assert f_humidity == []

    def test_filter_by_date_boundary_cases(self):
        """Test boundary case: data at midnight."""
        date1 = datetime.datetime(2025, 5, 27, 23, 59, 59)
        date2 = datetime.datetime(2025, 5, 28, 0, 0, 0)
        times = [date1, date2]
        temps = [20.0, 21.0]
        humidity = [50, 55]

        f_times, f_temps, f_humidity = filter_by_date(times, temps, humidity, '2025-05-27')

        assert len(f_times) == 1
        assert f_temps == [20.0]
        assert f_humidity == [50]
