# Climate Visibility Project

[![Live Demo](https://img.shields.io/badge/Live%20Demo-climate--visibility--project.onrender.com-brightgreen)](https://climate-visibility-project.onrender.com/)
[![GitHub Repository](https://img.shields.io/badge/GitHub-tgarg535%2FClimate--Visibility--Project-blue)](https://github.com/tgarg535/Climate-Visibility-Project.git)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-red)](https://flask.palletsprojects.com/)
[![DVC](https://img.shields.io/badge/DVC-Pipeline-orange)](https://dvc.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A comprehensive machine learning web application for predicting atmospheric visibility based on meteorological data. This project combines advanced ML algorithms with real-time weather data integration to provide accurate visibility forecasting, which is crucial for aviation, transportation safety, and weather monitoring systems.

## 🌟 Features

- **🔮 Visibility Prediction**: ML models predict atmospheric visibility using current weather conditions
- **🌦️ Real-time Weather Integration**: Live weather data from OpenWeatherMap API
- **📊 Interactive Dashboard**: User-friendly web interface with weather visualizations
- **🌍 Location Services**: GPS-based location detection and manual city search
- **💨 Air Quality Monitoring**: Real-time air pollution data (AQI, PM2.5, PM10, etc.)
- **📈 5-Day Weather Forecast**: Extended weather predictions with hourly breakdowns
- **🔄 DVC Pipeline**: Automated ML pipeline for data processing and model training
- **🧪 Comprehensive Testing**: Unit tests for both ML models and Flask application
- **📰 Climate News Integration**: Latest climate and weather news updates

## 🚀 Live Demo

**🌐 Visit the deployed application: [https://climate-visibility-project.onrender.com/](https://climate-visibility-project.onrender.com/)**

## 📁 Project Structure

```
Climate-Visibility-Project/
├── .github/
│   └── workflows/
│       └── ci.yaml                 # GitHub Actions CI/CD pipeline
├── config/
│   ├── params.yaml                 # Model hyperparameters and configurations
│   ├── prediction_schema.yaml      # Schema for prediction input validation
│   └── schema.yaml                 # Data schema and column definitions
├── data/
│   ├── raw/                        # Raw data (train.csv, test.csv)
│   └── interim/                    # Processed data (pickle files)
├── flask_app/
│   ├── models/                     # Trained models for Flask app
│   ├── services/
│   │   ├── prediction_service.py   # ML prediction service
│   │   └── weather_service.py      # Weather API integration
│   ├── static/css/
│   │   └── main.css                # Frontend styling
│   ├── templates/
│   │   └── home.html               # Main web interface
│   ├── app.py                      # Flask application
│   └── requirements.txt            # Flask app dependencies
├── models/                         # Trained ML models and scalers
├── reports/                        # Model evaluation metrics
├── src/
│   ├── components/
│   │   ├── data_ingestion.py       # Data loading from MongoDB
│   │   ├── data_transformation.py  # Data preprocessing pipeline
│   │   ├── model_trainer.py        # Model training with GridSearch
│   │   └── model_evaluation.py     # Model performance evaluation
│   ├── configuration/
│   │   └── mongo_db_connection.py  # MongoDB connection handler
│   ├── data_access/
│   │   └── visibility_data.py      # Data access layer
│   ├── tests/
│   │   ├── test_flask_app.py       # Flask app unit tests
│   │   └── test_model.py           # ML model unit tests
│   ├── utils/
│   │   └── main_utils.py           # Utility functions
│   ├── constants/                  # Project constants
│   ├── exception/                  # Custom exception handling
│   └── logger/                     # Logging configuration
├── dvc.yaml                        # DVC pipeline definition
├── dvc.lock                        # DVC pipeline lock file
├── .dvcignore                      # DVC ignore patterns
├── requirements.txt                # Python dependencies
├── setup.py                        # Package setup
├── pyproject.toml                  # Project metadata
└── LICENSE                         # MIT License
```

## 🛠️ Technology Stack

### Machine Learning
- **Scikit-learn**: Multiple regression algorithms (Linear, Ridge, Lasso, Random Forest, Gradient Boosting, Decision Tree)
- **GridSearchCV**: Automated hyperparameter tuning
- **Pandas & NumPy**: Data manipulation and numerical computing
- **DVC**: Data version control and ML pipeline management

### Web Application
- **Flask**: Backend web framework
- **HTML5 & CSS3**: Frontend with responsive design
- **JavaScript**: Interactive UI components
- **Bootstrap**: UI component framework

### Data & APIs
- **MongoDB**: Primary database for storing weather data
- **OpenWeatherMap API**: Real-time weather and air quality data
- **NewsAPI**: Climate news integration

### DevOps & Testing
- **GitHub Actions**: CI/CD pipeline
- **pytest**: Unit testing framework
- **DVC**: Experiment tracking and reproducible pipelines
- **Render**: Cloud deployment platform

## 📊 Machine Learning Pipeline

The project uses a sophisticated ML pipeline managed by DVC with the following stages:

### 1. Data Ingestion (`data_ingestion.py`)
- Fetches weather data from MongoDB
- Splits data into training and testing sets
- Handles missing values and data validation

### 2. Data Transformation (`data_transformation.py`)
- Feature scaling using StandardScaler
- Data preprocessing and cleaning
- Outlier detection and handling

### 3. Model Training (`model_trainer.py`)
- Supports 6 different regression algorithms:
  - Linear Regression
  - Ridge Regression  
  - Lasso Regression
  - Random Forest Regression
  - Gradient Boosting Regression
  - Decision Tree Regression
- Automated hyperparameter tuning with GridSearchCV
- Model selection based on configuration

### 4. Model Evaluation (`model_evaluation.py`)
- Performance metrics: MSE, MAE, R² Score
- Model validation and testing
- Automated reporting in JSON format

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- MongoDB Atlas account (for data storage)
- OpenWeatherMap API key
- NewsAPI key

### 1. Clone Repository
```bash
git clone https://github.com/tgarg535/Climate-Visibility-Project.git
cd Climate-Visibility-Project
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory:
```env
MONGODB_URL=your_mongodb_connection_string
OPENWEATHER_API_KEY=your_openweather_api_key
NEWSAPI_KEY=your_newsapi_key
```

### 4. Run DVC Pipeline
```bash
# Initialize DVC (first time only)
dvc init

# Run the complete ML pipeline
dvc repro
```

### 5. Start Flask Application
```bash
cd flask_app
python app.py
```

The application will be available at `http://localhost:5000`

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run specific test modules
pytest src/tests/test_model.py
pytest src/tests/test_flask_app.py

# Run tests with coverage
pytest --cov=src
```

## 📈 Model Performance

The current best model is **Random Forest Regression** with the following performance:
- **Mean Squared Error**: [Value from reports/metrics.json]
- **Mean Absolute Error**: [Value from reports/metrics.json]  
- **R² Score**: [Value from reports/metrics.json]

*Note: Actual metrics are stored in `reports/metrics.json` after running the DVC pipeline.*

## 🌐 API Endpoints

### Weather Data
- `GET /weather` - Current weather for set location
- `GET /forecast` - 5-day weather forecast
- `GET /air_pollution` - Air quality data

### Location Services  
- `GET /set_location?lat={lat}&lon={lon}` - Set location coordinates
- `POST /manual_search` - Search location by city/state/country

### Predictions
- `GET /predicted_visibility?lat={lat}&lon={lon}` - ML visibility prediction

### News
- `GET /climate_news` - Latest climate news articles

## 📱 Web Application Features

### Interactive Dashboard
- **Real-time Weather Display**: Current conditions with weather icons
- **Detailed Weather Metrics**: Temperature, humidity, pressure, wind speed, etc.
- **Air Quality Index**: Comprehensive pollution data including PM2.5, PM10, CO, NO₂
- **Smart Weather Suggestions**: Context-aware recommendations based on conditions
- **5-Day Forecast**: Hourly weather predictions with interactive timeline
- **Climate News**: Latest environmental and weather news integration

### User Experience
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **GPS Location**: Automatic location detection with user permission
- **Manual Search**: City-based weather lookup
- **Dark Theme**: Modern UI with high contrast colors and animations

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for automated testing and deployment:

- **Continuous Integration**: Runs on every push
- **Automated Testing**: pytest execution for all test modules  
- **DVC Pipeline**: Automatic model retraining
- **Environment Management**: Secure handling of API keys and secrets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Tanush Garg**
- 🌐 Portfolio: [https://my-portfolio-9guz.onrender.com](https://my-portfolio-9guz.onrender.com)
- 💼 LinkedIn: [https://www.linkedin.com/in/tanushgargg/](https://www.linkedin.com/in/tanushgargg/)
- 🐙 GitHub: [https://github.com/tgarg535](https://github.com/tgarg535)

## 🙏 Acknowledgments

- OpenWeatherMap for providing comprehensive weather API
- MongoDB Atlas for database hosting
- Render for application deployment
- The open-source community for the amazing tools and libraries

---

⭐ **If you found this project helpful, please give it a star on GitHub!**
