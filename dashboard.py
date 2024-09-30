import streamlit as st
import io
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

def about_dataset(data):
     
    data_sample = data.sample(10)
    print("Data Sample", data_sample)
    
    data_shape = data.shape
    print("\nData Shape", data_shape)
    
    buffer = io.StringIO()
    data.info(buf=buffer)
    info = buffer.getvalue()
    print(info)
    
    datatypes = data.dtypes
    print("\nData Columns", datatypes)
    

    misvalue = data.isnull().sum()
    print("\nCheck Missing Values", misvalue)
    
    # Get statistics for numerical columns
    data_statics = data.describe(include = 'all') ## Include 'all' to get stats for non-numerical columns as well
    print("\nCheck statistic", data_statics)

    return data_sample, data_shape, info, datatypes, misvalue, data_statics


def Dataset_statistics(data):
    
     #Calculate the relevant statistics 
     #Extract column vise inforamtion by Index location
     
    avr_age = data.iloc[:, 1].mean()
    avr_tenure = data.iloc[:, 3].mean()
    total_spend = data.iloc[:, 9].sum()
    avr_support_calls = data.iloc[:, 5].mean()
    churn_rate = data.iloc[:, 11].mean() * 100
    payment_delay_std_dev = data.iloc[:, 6].std()
    
    # Create a dictionary to store the statistics
    Customer_statistics = {
        'Average Age': avr_age,
        'Average Tenure': avr_tenure,
        'Total Spend': total_spend,
        'Average Support Calls': avr_support_calls,
        'Churn Rate (%)': churn_rate,
        'Payment Delay Std Dev': payment_delay_std_dev
    }
    
    return Customer_statistics




def future_insights(data):
    # 1. Projected Total Spend for next year assuming similar behavior
   
    average_monthly_spend = data.iloc[:, 9].mean()
    projected_total_spend_next_year = average_monthly_spend * 12 * len(data)

    churn_rate = data.iloc[:, 11].mean()
    projected_churn_next_year = churn_rate * len(data)
    
    average_support_calls = data.iloc[:, 5].mean()
    projected_support_calls_increase = average_support_calls * 1.1  # Assuming a 10% increase
    
    average_payment_delay = data.iloc[:, 6].mean()
    projected_payment_delay_increase = average_payment_delay * 1.05  # Assuming a 5% increase
    

    standard_and_basic_users = data[(data.iloc[:, 7] == 'Standard') | (data.iloc[:, 7] == 'Basic')]
    projected_upgrades = len(standard_and_basic_users) * 0.15  # Assuming 15% might upgrade
    

    average_tenure = data.iloc[:, 3].mean()
    projected_tenure_growth = average_tenure * 1.2  # Assuming a 20% improvement in retention
    
    
    #Storing Insights


    insights = {
        'Projected Total Spend Next Year': projected_total_spend_next_year,
        'Projected Churn Next Year': projected_churn_next_year,
        'Projected Support Calls Increase': projected_support_calls_increase,
        'Projected Payment Delay Increase': projected_payment_delay_increase,
        'Projected Subscription Upgrades': projected_upgrades,
        'Projected Tenure Growth': projected_tenure_growth
        }
    
    return insights

def age_distribution_graph(df):
    fig, ax = plt.subplots()
    df['Age'].plot(kind='hist', bins=10, color='skyblue', edgecolor='black', ax=ax)
    ax.set_title('Distribution of Age')
    ax.set_xlabel('Age')
    ax.set_ylabel('Frequency')
    return fig

# Average Total Spend by Subscription Type
def avg_total_spend_subscription_type(df):
    fig, ax = plt.subplots()
    df.groupby('Subscription Type')['Total Spend'].mean().plot(kind='bar', color='lightgreen', ax=ax)
    ax.set_title('Average Total Spend by Subscription Type')
    ax.set_xlabel('Subscription Type')
    ax.set_ylabel('Average Total Spend')
    return fig

# Gender Distribution
def gender_distribution(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    df['Gender'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_title('Gender Distribution')
    ax.set_ylabel('')
    return fig

# Total Spend Distribution by Contract Length
def total_spend_distribution_by_contract_length(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    df.groupby('Contract Length')['Total Spend'].sum().plot(kind='pie', autopct='%1.1f%%', colors=['#ff9999', '#66b3ff', '#99ff99'], ax=ax)
    ax.set_title('Total Spend Distribution by Contract Length')
    ax.set_ylabel('')
    return fig

# Churn Rate by Gender
def churn_rate_by_gender(df):
    fig, ax = plt.subplots()
    churn_rate_by_gender = df.groupby('Gender')['Churn'].mean() * 100
    churn_rate_by_gender.plot(kind='bar', color='coral', ax=ax)
    ax.set_title('Churn Rate by Gender')
    ax.set_xlabel('Gender')
    ax.set_ylabel('Churn Rate (%)')
    return fig

# Age Distribution by Gender
def age_distribution_by_gender(df):
    fig, ax = plt.subplots()
    df[df['Gender'] == 'Male']['Age'].plot(kind='hist', bins=10, alpha=0.5, color='blue', label='Male', ax=ax)
    df[df['Gender'] == 'Female']['Age'].plot(kind='hist', bins=10, alpha=0.5, color='red', label='Female', ax=ax)
    ax.set_title('Age Distribution by Gender')
    ax.set_xlabel('Age')
    ax.set_ylabel('Frequency')
    ax.legend()
    return fig


if __name__=="__main__":

    
    st.title("Customer Drop-off analysis Dashboard")
    st.subheader("Customer support data analysis with visualization & future insighgts dashboard")
    st.sidebar.title("Drop your data file for analysis")

    file_upload = st.sidebar.file_uploader("Only csv file", type='csv')

    data = pd.DataFrame()
    if file_upload is not None:
        data = pd.read_csv(file_upload)

    
    if st.sidebar.button("Data Overview"):
        st.subheader("About Dataset")

        data_sample, data_shape,info, datatypes,misvalue, data_statics = about_dataset(data)

        st.subheader("Data Sample")
        st.write(data_sample)


        st.subheader("Dataset Size")
        st.write(data_shape)


        st.subheader("Dataset Information")
        st.write(info)


        st.subheader("Columns Names & Dtype")
        st.write(datatypes)

        st.subheader("Missing Values")
        st.write(misvalue)


        st.subheader("Check statistic")
        st.write(data_statics)


        #create a button of about Statistic for extraxtion of statistical information from data
    if st.sidebar.button("Data Trends"):
        st.subheader("Statistic")

        # Get the statistics
        stats = Dataset_statistics(data)
        
        # Print the statistics
        for key, value in stats.items():

            st.write(f'{key}: {round(value,2)}')



    #create a button of about Statistic
    if st.sidebar.button("Future Trends"):
        st.subheader("Dataset Future Trends")

        # Get the statistics

        future_stats = future_insights(data)

        # Print the future insights
        for key, value in future_stats.items():
                st.write(f'{key}: {value}')

        # dashboard 
    if st.sidebar.button("Data visualization"):
        st.subheader("Future Trends Visualization")
        col1,col2 = st.columns(2)
        with col1:
            st.subheader("Age Distribution")
            fig = age_distribution_graph(data)
            st.pyplot(fig)
        with col2:
            st.subheader("Avg Spend Sub Type")
            fig = avg_total_spend_subscription_type(data)
            st.pyplot(fig)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Gender Distribution")
            fig = gender_distribution(data)
            st.pyplot(fig)
        with col2:
            st.subheader("T/Spend Contact Length")
            fig = total_spend_distribution_by_contract_length(data)
            st.pyplot(fig)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Churn Rate By Gender")
            fig = churn_rate_by_gender(data)
            st.pyplot(fig)
        with col2:
            st.subheader("Age Dist By Gender")
            fig = age_distribution_by_gender(data)
            st.pyplot(fig)
            