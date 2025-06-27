# Surf Condition Forecasting Using XGBoost

## Overview
Taiwan is surrounded by ocean and hosts many world-famous surf spots such as Jinzun and Wushi Harbor. However, surfers often need to go to the beach in person to check for good waves. This project aims to build predictive models for wave conditions using publicly accessible weather and ocean data, providing surfers a tool to save time and make better surfing decisions.

## Data Collection

We used the [Surfline API](https://www.surfline.com/) via the `pysurfline` Python package to collect surf-related data for multiple international surf spots. Data was saved as CSV files for further analysis.

Main script: [`surfline_crawl.ipynb`](https://github.com/mellamochiao/Datascience_final_project/blob/main/surfline_crawl.ipynb)

## Model Building

We focused on predicting three key aspects of swell conditions:
1. **Swell Height**
2. **Swell Period**
3. **Swell Power**

Each target variable was predicted using both Linear Regression (for baseline evaluation) and XGBoost (for optimized performance).

### Highlights:

- **Swell height (XGBoost):**  
  MSE = 0.065  
  R² = 0.893
  ![Image](https://github.com/user-attachments/assets/12bd94d7-fbda-43a1-80c6-80cbedfa1857)

- **Swell period (XGBoost):**  
  MSE = 1.145  
  R² = 0.770
  ![Image](https://github.com/user-attachments/assets/3e70f64d-bc7d-4b15-994f-455e1987c687)

- **Swell power (XGBoost):**  
  MSE = 2618.05  
  R² = 0.927
  ![Image](https://github.com/user-attachments/assets/cf737796-41e0-4f34-9242-24fd3dedac27)

Model script: [`xgb_model.ipynb`](https://github.com/mellamochiao/Datascience_final_project/blob/main/xgb_model.ipynb)

## Surf Condition Predictor

We developed a terminal-based application to predict surf conditions using the trained models. The program allows users to input basic weather data and outputs predicted swell height, period, power, and a surf suitability suggestion.

### Key Features:
Surf suitability assessment:
  - Good: Swell period between 8–16 sec
  - Acceptable: Swell period 6–8 sec with offshore wind


Warnings:
  - High wind alert: wind speed > 19 m/s
  - Low temperature alert: temperature < 20°C

### How to Run the Predictor Script

To run the interactive surf condition predictor in your terminal:

Make sure you have Python installed. 

Then run:
```bash
pip install xgboost pandas numpy
git clone https://github.com/mellamochiao/Datascience_final_project.git
cd Datascience_final_project
python surf_predict.py
```
Example output:
<img width="926" alt="Image" src="https://github.com/user-attachments/assets/78a28855-80a3-4f6d-9b91-e4e7bc79919f" />


## References

1. [Surfline API Spot Forecast Example](https://giocaizzi.github.io/pysurfline/examples/SpotForecasts.html)
2. [Surf Forecasting API Tutorial ](https://medium.com/@williamChen0832/...)
3. [Surf Forecast Interpretation Guide ](https://www.awamemo.com/blog/outdoors/surfing/...)