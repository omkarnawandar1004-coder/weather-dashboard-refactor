# Weather Dashboard Refactoring Project

## 📋 Assignment Overview

This is a **Code Refactoring Assignment** based on the original [Python-Weather-Dashboard](https://github.com/shitanshu15/Python-Weather-Dashboard) by shitanshu15.

The goal is to:
1. Identify code smells in the original implementation
2. Build a comprehensive test suite
3. Refactor using clean code principles
4. Measure improvements in code metrics

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/omkarnawandar1004-coder/weather-dashboard-refactor.git
cd weather-dashboard-refactor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure .env
cp .env.example .env
# Edit .env with your OpenWeatherMap API key
```

### Get API Key

Visit https://openweathermap.org/api and sign up for a free API key.

### Run the Application

```bash
python -m src.weatherdashboard
```

### Run Tests

```bash
pytest tests/ -v --cov=src --cov-report=html
```

## 📊 Project Structure

```
weather-dashboard-refactor/
├── src/
│   ├── __init__.py
│   └── weatherdashboard.py      # Main implementation
├── tests/
│   ├── __init__.py
│   ├── test_data_fetcher.py
│   ├── test_data_filter.py
│   └── test_visualization.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 📝 Assignment Progress

### Phase 1: Code Smell Audit ✅
- [ ] Identify 4+ code smells
- [ ] Document with line numbers
- [ ] Create baseline metrics

### Phase 2: Testing Safety Net ✅
- [ ] Write unit tests (70%+ coverage)
- [ ] Run baseline tests
- [ ] Document test strategy

### Phase 3: Refactoring ✅
- [ ] Apply 4+ refactoring techniques
- [ ] Commit each change separately
- [ ] Ensure tests pass after each refactor

### Phase 4: Analysis & Reporting ✅
- [ ] Compare before/after metrics
- [ ] Write reflection report
- [ ] Document trade-offs

## 🔗 References

- [Refactoring.guru](https://refactoring.guru/refactoring)
- [Original Repository](https://github.com/shitanshu15/Python-Weather-Dashboard)
- [OpenWeatherMap API](https://openweathermap.org/api)
