# WEATHER FEATURES PREDICTION

### ABOUT APPLICATION
Weather feature application is a web application that predict/forecast weather features using a statistical model.

### REQUIREMENTS
- The programing language used is Python
- Two Integrated Development Environment (IDE) were used, these are Jupyter notebook and Visual Studio Code .
- All the python packages used can be installed through python's pip.
- The application built was deployed on heroku.

### DATA USED
The data used to train the statistical model is Delhi Climate Time Series from Kaggle, It consists of Weather Data from 01-01-2013 till 01-01-2017. The features included are mean_temp, humidity, wind_speed and meanpressure. The linkto the data is provided here [Kaggle](https://www.kaggle.com/datasets/sumanthvrao/daily-climate-time-series-data).

### DATA PREPROCESSES
- There was check for missing values.
- The date column was converted to a datetime data.
- The data column was set as the index column.
- The monthly average aggregate of each weather features were derived
### EXPLORATORY ANALYSIS AND VISUALIZATION
- Line plot was plottled
- Decomposition plot was conducted to check for Trend, Seasonality and Noise.
### PRE TRAINING 
Best SARIMAX parameters were searched for each features to forecast.
### TRAINING
SARIMAX statistical algorithm was trained on the average monthly aggregate of data and the trained model was saved as a pickled file .
### EVALUATION
Diagnostis plots and the use of Root Mean Squared Error was used to evaluate the model.

### WEB APPLICATION BUILDING
- Streamlit python package was used to build the web application
- Plotly was used to plot graphs and charts
### APPLICATION FRONT END.
- The front end consists of three tabs and a side bar.
- The side bar contains the input widgets.
- The first tab contains the the Visualization.
- The second tab displays the data frame and an option to download
- The Third tab contains all the information about the web application.