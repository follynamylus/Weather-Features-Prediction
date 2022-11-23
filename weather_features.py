#***************************************IMPORT PACKAGES*************************************************

import streamlit as st #<-----------------------Import Streamlit for building the web application
import statsmodels.api as sm #<-----------------Import Stats model for making the statistical forecast
import pandas as pd #<--------------------------Import Pandas for data preprocessing
import plotly.express as px  #<-----------------Import  Plotly Express for data visualization

#***************************************BUILDING THE INPUT WIDGETS, TABS AND SIDEBAR***************************************
tab_1, tab_2,tab_3 = st.tabs(['VISUALIZATION','PREDICTION AND DOWNLOAD','ABOUT APPLICATION'])#<--- Creation of three tabs

tab_1.title("WEATHER FEATURES VISUALIZATION") #<------ Title for First Tab
tab_2.title("WEATHER FEATURES PREDICTION") #<--------- Title for Second Tab
tab_3.title("ABOUT APPLICATION") #<--------------------Title for Third Tab
start = st.sidebar.date_input("Input the start date from 2016") #<---------- Input Widget for the start date
start_date = pd.to_datetime(start) # <-------------------------------------- Convert Start date to a date time format
end = st.sidebar.date_input("Input the end date later than the start date") #<---------- Input widget for the end date
if end == start_date : # <---------------------- Conditional Statement to check if the end date is equal to start date
    option = st.sidebar.selectbox("Tick how you want to forecast", ('forward','backward')) # Code to select prediction option.
    if option == 'forward' : # <---------------- Condition for forward prediction.
        steps = int(st.sidebar.number_input("Input The days to extend to", 0)) # <----- Number of days to predict forward
        end_date = start_date + pd.DateOffset(days = steps) # <----- Set end date for forward prediction
    elif option == 'backward' : # <-------------- Condition for backward prediction
        steps = int(st.sidebar.number_input("Input The days to extend from, not later than 2000 days", 0)) # Days to predict backward
        start_date = start_date - pd.DateOffset(days = steps) # Start date for backward prediction
        end_date = pd.to_datetime(end) # <------------------- End date for backward prediction
else : # <------------------------- If end and start date are not the same
    end_date = pd.to_datetime(end) # <------------------ Set end date
choice = st.sidebar.multiselect("Which Weather Factors Do you Select ?",["Temperature","Humidity","Wind Speed",'Pressure'],['Temperature'])# Choose weather factors

# ************************************************ BACKEND CODES ******************************************

def load_model(file_name) : # <---------- Define the function.
    '''
    The Load model function loads pickled statistical models in the script. 
    It takes in file name as parameter.
    It returns the loaded model.
    '''
    return sm.iolib.smpickle.load_pickle(file_name) # <------------- Function return

temp = load_model('model_temp') # <-------------------- Load the temperature model
humidity = load_model('model_humidity') # <------------ Load Humidity model
wind = load_model('model_wind') # <-------------------- Load Wind Speed model
pressure = load_model('model_pressure') # <------------ Load Pressure model

def Forecast(model, start, end) : # <--------- Forecast function definition
    '''
    The Forecast function performs the tasks of making forecast/prediction.
    It create a dataframe from the predictions with flexible columns depending on the number of multiple choice with date as the index column.
    It creates four plots which include line plot, bar plot, area plot and density contour plot.
    It takes three input parameters which are a model for prediction, a start date and an end date.
    It returns a dataframe
    '''
    df = pd.DataFrame() # <------------ Create an empty dataframe
    for i in model : # <------------- Loop through the choices
        if i == 'Temperature' : # <------------- Condition for temperature
            pred = temp.get_prediction(start = pd.to_datetime(start), end = pd.to_datetime(end)) # Make prediction
            mean_disp = pred.predicted_mean # <---------- Create series from predicted values
            mean_df = mean_disp.to_frame() # <----------- Convert series to data frame
            mean_df.reset_index(inplace = True) # <------- Reset the data frame's index
            mean_df.columns = ['Date','Temperature'] # <-------- Rename the dataframe's column
            mean_df['Month'] = pd.to_datetime(mean_df['Date']).dt.month_name() # Create additional month column from the date column
            if df.empty == True : # <----------- Condition to check for empty dataframe
                mean_df['Month'] = pd.to_datetime(mean_df['Date']).dt.month_name() # <----- Create month column for empty dataframe
                df['Date'] = mean_df['Date'] # <-------- Add date column to the dataframe
                df['Temperature (degree C)'] = mean_df['Temperature'] # <--------- Add temperature column to the data frame
            else : # <----- Condition if dataframe is not empty
                df['Temperature (degree C)'] = mean_df['Temperature'] # <---------- Add temperature column to the data frame
        if i == 'Humidity' : # <----------- Condition for humidity 
            pred = humidity.get_prediction(start = pd.to_datetime(start), end = pd.to_datetime(end))
            mean_disp = pred.predicted_mean
            mean_df = mean_disp.to_frame()
            mean_df.reset_index(inplace = True)
            mean_df.columns = ['Date','Humidity']
            mean_df['Month'] = pd.to_datetime(mean_df['Date']).dt.month_name()
            if df.empty == True :
                mean_df['Month'] = pd.to_datetime(mean_df['Date']).dt.month_name()
                df['Date'] = mean_df['Date']
                df['Humidity (g/m3)'] = mean_df['Humidity'] # <----------- Add Humidity column to the dataframe
            else :
                df['Humidity (g/m3)'] = mean_df['Humidity'] # <----------- Add Humidity column to the dataframe
        if i == 'Wind Speed' : # <----------- Condition for wind speed
            pred = wind.get_prediction(start = start, end = end)
            mean_disp = pred.predicted_mean
            mean_df = mean_disp.to_frame()
            mean_df.reset_index(inplace = True)
            mean_df.columns = ['Date','wind']
            mean_df['Month'] = pd.to_datetime(mean_df['Date']).dt.month_name()
            if df.empty == True :
                mean_df['Month'] = pd.to_datetime(mean_df['Date']).dt.month_name()
                df['Date'] = mean_df['Date']
                df['wind (m/min)'] = mean_df['wind'] *16.6667 # Multiply the column by 16.6667 then add the column to the dataframe
            else :
                df['wind (m/min)'] = mean_df['wind'] * 16.6667 # Multiply the column by 16.6667 then add the column to the dataframe
        if i == 'Pressure' : # <-------------- Condition for pressure
            pred = pressure.get_prediction(start = pd.to_datetime(start), end = pd.to_datetime(end))
            mean_disp = pred.predicted_mean
            mean_df = mean_disp.to_frame()
            mean_df.reset_index(inplace = True)
            mean_df.columns = ['Date','pressure']
            mean_df['Month'] = pd.to_datetime(mean_df['Date']).dt.month_name()
            if df.empty == True :
                mean_df['Month'] = pd.to_datetime(mean_df['Date']).dt.month_name()
                df['Date'] = mean_df['Date']
                df['pressure (MPa)'] = mean_df['pressure'] * 0.1013 # Multiply column by 0.1013, then add column to the dataframe
            else :
                df['pressure (MPa)'] = mean_df['pressure'] * 0.1013 # Multiply column by 0.1013, then add column to the dataframe
    with st.expander("Click to view the line plot") : # <-------------- Create an expander for line plot
        st.write("The Line plot for the weather features") # <--------- Write in the created expander
        fig = px.line(df, x= 'Date', y= df.columns[1:]) # <--- Create a line plot of all weather features in the dataframe against the date
        st.plotly_chart(fig, use_container_width=True) # <------------- Fit the plot to the web page
    with st.expander("Click to view the grouped bar chart") : # <----------- Create an expander for grouped bar chart
        st.write("The Group bar chart for the weather features") # <--------- Write in the created expander
        fig1 = px.bar(df, x= 'Date', y= df.columns[1:], barmode= 'group') #Create a  bar plot of all weather features in the dataframe against the date
        st.plotly_chart(fig1, use_container_width=True) 
    with st.expander("Click to view the Area plot") : # <-------------- Create an expander for Area plot
        st.write("The Area plot for the weather features") # <--------- Write in the created expander
        fig = px.area(df, x= 'Date', y= df.columns[1:]) # <--- Create a Area plot of all weather features in the dataframe against the date
        st.plotly_chart(fig, use_container_width=True)
    with st.expander("Click to view the Density_Contour plot") : # <-------------- Create an expander for Density contour plot
        st.write("The Density Contour plot for the weather features") # <--------- Write in the created expander
        fig = px.density_contour(df, x= 'Date', y= df.columns[1:]) # Create a Density Contour plot of all weather features in the dataframe against the date
        st.plotly_chart(fig, use_container_width=True)
    
    return df # <------------------ Return the dataframe.

#******************************************************* OUTPUT FRONTEND CODES *********************************************************

with tab_1 : # <------------------------- Declare tab 1 container
    df = Forecast(choice, start_date, end_date) # <---------------- Call Forecast function in tab 1.  

tab_2.dataframe(df) # <--------------- Display the dataframe on tab2
@st.cache # <------------- IMPORTANT: Cache the conversion to prevent computation on every rerun

def convert_df(df): # <--------------- Function declaration
    '''
    Convert_df function converts the resulting dataframe to a CSV file.
    It takes in a data frame as a aprameter.
    It returns a CSV file
    '''
    
    return df.to_csv().encode('utf-8') # <--------------- Return dataframe as a CSV file
csv = convert_df(df) # <------------ Convert_df function calling and assigning to a variable.
tab_2.success("Print Result as CSV file") # <--------------- A widget as heading for the download option in tab 2
tab_2.download_button("Download",csv,"Prediction.csv",'text/csv') # <------------------ Download button widget in tab 2.

tab_3.write(
    """
    The Web Application is used for making weather forecasts / predictions of four weather factors which are Temperature, Pressure, Humidity 
    and wind.

    The web application makes use of statistical models trained using Delhi (India) weather data from 1st of January 2013 till 1st if January 2017.
    The data which are aggregated to the average monthly value for the weather features.

    The application consists of an adjustable Sidebar for Input widgets,
    Visualizations are provided on the first tab while data frame of the predictions and download option are provided on the second tabs of the application
    """
)
tab_3.subheader("ABOUT THE FEATURES")
tab_3.write(
    '''
    The columns includes, Temperature with degree celcius(degree C) as it unit ,
    
     Pressure with Mega Pascal (MPa) as its unit , 

    Wind Speed with unit of Meters per Minutes (M/min),

     and Humidity with unit of gram of water vapor per cubic meter volume of air (g/m3).
    '''
)
tab_3.subheader("ABOUT INPUT WIDGETS")
tab_3.write(
    """
    The Input widgets consist of date input type which is in a calender format with a drop down comprising the year, month and days in the months , 
    they are considered as the start date and end date , the date widgets have a default value of the day's date. 

     There is the number input widget that serves as an alternative when considering number of days to forecast / predict ,it is only provided
     when the start date and end date is the same ,it has a default value of zero.

    The option widget if a select box dropdown, with option to choose for either a forward or backward prediction. Its default is forward .
    The multi select widget drop down can select multiple choice, It selects for the prefered weather features to predict, visualize and
    download as a data frame at a time. Its default value is Temprature.
    
    All the input widgets are contained in the sidebar
    """
)
tab_3.subheader("ABOUT OUTPUT WIDGETS")
tab_3.write(
    """
    The Output widgets are in tabs .
    Tab 1 the VISUALIZATION tab contains graphs and plots of the predictions. The graphs are in expanders that include the Line plot , Bar chart ,
    stacked Area plot and stacked Density Contour plot . These variables are flexible and multiple can be selected at a time,
     it also can be activated or deactivated by clicking on their names by the top
    right corner of Visualization tab.


    Tab 2  the PREDICTION AND DOWNLOAD tab, It displays the prediction dataframe and a download button option for downloading the file in a 
    CSV format.


    Tab 3 ABOUT APPLICATION tab, contains information on the application widgets .
    """
)