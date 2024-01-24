import pickle
import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import streamlit_authenticator as stauth

st.set_page_config(page_title="Electricity Bill Analysis and Power Consumption Prediction",
                   page_icon=":zap:",
                   layout="wide")

# user authentication
names = ["Peter Parker", "Rebecca Miller", "shane watson", "Arun vijay"]
usernames = ["pparker", "rmiller", "Swatson", "Avijay"]

# Load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)
    
authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "Electricity Bill Analysis and Power Consumption Prediction", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login","main")

if authentication_status == False:
    st.error("Username/password is incorrect")
    
if authentication_status == None:
    st.warning("Please enter your username and password")
    
if authentication_status:
     
    df = pd.read_csv("C:/Users/DELL/OneDrive/Desktop/Electricity_bill/electricitydatasetlatest.csv",parse_dates=['time'])
    
    # Create sidebar options
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    st.sidebar.header("NAVIGATION BAR:")
    menu = ["Home","Power Consumption Analysis","Power Consumption Prediction"]
    choice = st.sidebar.selectbox("Select Option", menu)
    
    #df = pd.read_csv('D:/Users/immah/Downloads/electricityuse.csv')
# Load the electricity bill data
#df = pd.read_csv("C:/Users/AASHISH KUMAR/Downloads/AEP_hourly.csv",parse_dates=['time']) 
df = pd.read_csv("C:/Users/DELL/OneDrive/Desktop/Electricity_bill/electricitydatasetlatest.csv",parse_dates=['time']) 

if choice == "Home":
    # Set page title and header
    st.title("Electricity Bill Data Analysis")
    st.header("About")

    # Display the loaded data
    st.write("""      The conventional approach requires an operator to give details in order to decide the amount of power consumed. The manual technique of evaluating consumption is time-consuming. Also, we are unable to predict our future consumption. 
         The proposed system also includes a website where customers can view their electricity usage and generated bill. The website displays graphs for daily, hourly, weekly, monthly, and yearly electricity usage. This project aims to provide an efficient and accurate system for electricity bill analysis and future power consumption prediction.
The results of the project show that the system can accurately predict future power consumption. The system also provides an efficient and user-friendly website for customers to view their electricity usage and generated bill. Overall, this project proposes a practical solution to the problem of electricity billing and can be implemented on a larger scale for more significant benefits.
The project also includes the development of a website for customers to check their electricity usage and generated bills.
The CT sensor is used to measure the current flowing in the main supply line, which is then fed to the Esp32 microcontroller for processing and analysis. The microcontroller is programmed to send the collected data to Google sheets for storing and further analysis using machine learning algorithms.
Supervised machine learning techniques such as LSTM are used to predict future power consumption based on historical data. The generated predictions are then used to generate bills for customers. The website provides customers with a user-friendly interface to check their electricity usage and generated bills.
Overall, this project provides a cost-effective and efficient solution for automating electricity bill analysis and prediction, which can be beneficial for both customers and utility companies.
""")
    
elif choice=="Power Consumption Analysis":
    st.title("Power Consumption Analysis")
    submenu=["Hourly Consumption","Day VS Night","Monthly analysis","Date to date consumption"]
    select=st.selectbox("Select Analysis",submenu)
    if select=="Hourly Consumption":
        st.title("Hourly Consumption")
       
        
        # Load dataset
          # Replace 'dataset.csv' with the path to your own dataset
        df['time'] = pd.to_datetime(df['time'], errors='coerce')

        

        # Extract date from 'time' column
        df['date'] = df['time'].dt.date
        # Convert 'time' column to datetime object
        #df['time'] = pd.to_datetime(df['time'])
        #to particular date
        # Extract date from 'time' column
        #df['date'] = df['time'].dt.date
        
        # Specify the date you want to extract
        target_date = st.date_input("Enter required date")
        
        # Filter dataset for the target date
        filtered_df = df[df['date'] == pd.to_datetime(target_date).date()]
        
        # Print the filtered dataset
        #print(filtered_df)
        col=['time','consumption']
        st.write(filtered_df[col])
        # Set 'time' column as the index
        filtered_df.set_index('time', inplace=True)
        
        # Resample the data at hourly frequency
        df_hourly = filtered_df.resample('H').mean()
        
        # Plot the graph
        fig, ax = plt.subplots()
        ax.plot(df_hourly.index, df_hourly['consumption'])
        
        # Set the x-axis label to show only hours and minutes
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        
        # Set the x-axis label to rotate for better readability
        plt.xticks(rotation=45)
        
        # Set the y-axis label
        ax.set_ylabel('Consumption')
        
        # Set the title of the graph
        ax.set_title('Hourly Consumption Plot')
        
        # Display the plot
        #plt.show()
        st.write(fig)
        
    elif select=="Day VS Night":
        st.title("Day vs Night")
        
        #extract parcticular date
        df['time'] = pd.to_datetime(df['time'], errors='coerce')
        df['date'] = df['time'].dt.date
        
        # Specify the date you want to extract
        target_date = st.date_input("Enter requierd date")
        
        # Filter dataset for the target date
        filtered_df = df[df['date'] == pd.to_datetime(target_date).date()]
        
       # Extract hour from 'time' column
        filtered_df['hour'] = filtered_df['time'].dt.hour
        
        # Calculate total consumption for day and night time periods
        day_consumption = filtered_df[filtered_df['hour'].between(6, 22)]['consumption'].sum()
        night_consumption = filtered_df[(filtered_df['hour'] < 6) | (filtered_df['hour'] > 22)]['consumption'].sum()
        
        # Create pie chart
        labels = ['Day', 'Night']
        sizes = [day_consumption, night_consumption]
        colors = ['#ff9999', '#66b3ff']
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.set_title('Day vs Night Consumption for {}'.format(target_date))
        st.pyplot(fig)  # Display the pie chart in Streamlit
        
    elif select=="Monthly analysis":
         st.title("Monthly analysis")
         #extract parcticular date
         targetdf=df
         

         # Convert 'time' column to datetime type
         df['time'] = pd.to_datetime(df['time'], errors='coerce')
         targetdf['time'] = pd.to_datetime(df['time'], format='%d-%m-%Y %H:%M:%S')

        
         # Extract year from 'time' column
         targetdf['year'] = targetdf['time'].dt.year
        
         # Filter data for a particular year
         target_year = int(st.text_input("Enter the Year"))
         targetdf = targetdf[targetdf['year'] == target_year]
        
         # Group by month and calculate sum of consumption
         monthly_sum = targetdf.groupby(targetdf['time'].dt.month)['consumption'].sum()
        
         # Convert the result to a dataframe
         monthly_sum_df = pd.DataFrame({'Month': monthly_sum.index, 'Monthly Sum': monthly_sum.values})
        
         # Plot the monthly sum of consumption in a bar graph
         fig, ax = plt.subplots()
         ax.bar(monthly_sum_df['Month'], monthly_sum_df['Monthly Sum'])
         ax.set_xlabel('Month')
         ax.set_ylabel('Monthly Sum of Consumption')
         ax.set_title(f'Monthly Sum of Consumption for Year {target_year}')
         plt.xticks(monthly_sum_df['Month'])
         plt.tight_layout()
        
         # Display the bar graph in Streamlit
         st.pyplot(fig)
    elif select=="Date to date consumption":
        st.title("Date to date ")
        
        targetdf=df
        # Convert 'time' column to datetime type
        df['time'] = pd.to_datetime(df['time'], errors='coerce')
        targetdf['timestamp'] = pd.to_datetime(df['time'], format='%d-%m-%Y %H:%M:%S')
        targetdf.set_index('timestamp',inplace=True)
        

        # Input start date
        df['time'] = pd.to_datetime(df['time'], errors='coerce')
        start_date = st.date_input('Start Date')# value=targetdf.index.min()
    
        # Input end date
        df['time'] = pd.to_datetime(df['time'], errors='coerce')
        end_date = st.date_input('End Date')# value=targetdf.index.max()
    
        # Calculate usage
        filtered_data = targetdf.loc[start_date:end_date]

        # Calculate sum of consumption column for filtered data
        usage = filtered_data['consumption'].sum()

    
        # Display result
        st.write('Total usage:',usage)
elif choice=="Power Consumption Prediction":
    st.title("Power Consumption Prediction")    
    st.write("The power consumption of next week is forecasted.")
    consumption=[5.19, 7.18, 10.12, 9.89, 9.97, 11.12, 10.22, 8.12, 9.91, 12.12, 11.17, 10.12, 9.98, 10.95] 
    forecast=[11.224321,10.12134,11.0123,11.8432,11.9789,10.51,10.83633,10.2708883,12.0907454,5.955956 ,5.847149 , 5.748282 , 5.728899,
     5.7161865 ,5.7079206 ,5.7028036, 5.6999736 ,5.698904 , 5.698259,  5.697883,
     5.6976776 ,5.6975718]
    # Number of vertices
    num_vertices = 10
    
    # Number of vertices to be colored blue and red
    num_blue = num_vertices // 2
    num_red = num_vertices // 2
    
    # If the number of vertices is odd, color one extra vertex red
    if num_vertices % 2 != 0:
        num_red += 1
    
    # Generating vertex coordinates
    x = [i for i in range(num_vertices)]
    y = [0 for _ in range(num_vertices)]
    
    # Plotting the blue vertices with blue line
    plt.plot([1,2,3,4,5,6,7], consumption[-7:], color='blue', marker='o', markersize=8, label='Past week')
    
    # Plotting the red vertices with red line
    plt.plot([8,9,10,11,12,13,14], forecast[:7], color='red', marker='o', markersize=8, label='Upcoming week')
    # Adding labels and title
    plt.xlabel('Days')
    plt.ylabel('Consumption in Kwh')
    plt.title('Power consumption plot.')
    
    # Adding a legend
    plt.legend()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    # Displaying the plot
    st.pyplot()

