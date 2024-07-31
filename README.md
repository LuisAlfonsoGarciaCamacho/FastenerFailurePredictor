# FastenerFailurePredictor
![Project Demonstration](https://github.com/LuisAlfonsoGarciaCamacho/FastenerFailurePredictor/blob/20d003d3b2911a9bceb1ffc467c46f2feb447238/img/demostration.gif)
This is an advanced monitoring solution for bolt fastening processes. It employs machine learning techniques to detect potential failures by analyzing torque and angle measurements in real-time. This project aims to enhance quality control and reduce failures in manufacturing processes involving bolt tightening.

## Key Features

- Real-time data processing from sensors and historical Excel files
- Advanced anomaly detection using machine learning models
- Interactive visualizations for torque and angle data
- Alerting system for detected anomalies

## Technology Stack

- **Python**: The core programming language (version 3.8+)
- **Pandas**: For efficient data manipulation and analysis
- **Scikit-learn**: For data preprocessing and model evaluation
- **XGBoost & LightGBM**: The primary machine learning algorithms used for anomaly detection
- **FastAPI**: For creating robust API services
- **Streamlit**: For building the interactive web application
- **Matplotlib/Plotly**: For generating visualizations

## Model Architecture

The final predictive model is an ensemble combining XGBoost and LightGBM. This hybrid approach leverages the strengths of both algorithms:

- **XGBoost**: Provides excellent performance and handles complex feature interactions
- **LightGBM**: Offers fast training speed and high efficiency with large datasets

The ensemble model aims to achieve superior predictive performance and robustness compared to single-algorithm approaches.

## Project Structure

- `src/`: Source code for data processing and model training
- `app/`: Application code for the web interface and API services
- `models/`: Trained models and scalers
- `data/`: Input data files (Excel format)
- `output/`: Generated visualizations and reports

## Setup and Usage

1. Install Python 3.8 or higher
2. Install required libraries: `pip install -r requirements.txt`
3. Configure file paths in the respective scripts
4. Run the model training script
5. Start the services using `main.py` or individual service scripts

For detailed instructions, refer to the user guide in the documentation.

## Contributing

Contributions to improve TorqueAngleSentry are welcome. Please refer to our contributing guidelines for more information.
