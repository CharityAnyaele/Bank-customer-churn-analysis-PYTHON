import pandas as pd
#Load the csv file (from your documents folder)
df = pd.read_csv(r"C:\Users\user\Documents\Bank Customer Churn Prediction.csv")
# show the first 5 rows
print(df.head())
#Show basic info about the dataset
print(df.info())
#show summary statistics for thr numerical columns
print(df.describe())
#check for missing values
print(df.isnull().sum())
#check the first few rows
print(df.head())
#check for duplicates
duplicates = df.duplicated().sum()
print(f"\n--- Duplicates Rows: {duplicates}---")
#standardize column names(remove spaces, make lowercase)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print("\n---New column Names---")
print(df.columns)
#Handle missing values (if any)
#If there are numeric columns with missing values, fill them with the column mean
nums_cols = df.select_dtypes(include=['float64', 'int64']).columns
df[nums_cols] = df[nums_cols]. fillna(df[nums_cols].mean())
#clean categorical values
df['gender'] = df['gender'].str.lower().str.strip()
df['country'] = df['country'].str.title().str.strip() # e.g., France, Germany, Spain
#check unique values to verify cleaning
print("\n---Unique values---")
for cols in ['country', 'gender', 'credit_card', 'active_member', 'churn']:
    print(f"{cols}: {df[cols].unique()}")
#save cleaned version
df.to_csv("Cleaned_Bank_Churn.csv", index=False)
print("\n Data cleaning complete! Cleaned file save as 'Cleaned_Bank_Churn.csv'")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#Load cleaned dataset
df = pd.read_csv('Cleaned_Bank_Churn.csv') #my cleaned data file
#Total number of customers
total_customers = len(df)
print("Total_customers:", total_customers)
#Average credit score, balance, and estimated salary
avg_credit_score = df["credit_score"].mean()
avg_balance = df['balance'].mean()
avg_salary = df['estimated_salary'].mean()
print(f"average Credit Score: {avg_credit_score:.2f}")
print(f"Average Balance: ${avg_balance: .2f}")
print(f"Average Estimated Salary: ${avg_salary: .2f}")

#Gender distribution
gender_dist = df['gender'].value_counts()
print("\nGender distribution:")
print(gender_dist)

#visualize gender distribution
sns.countplot(x='gender', data=df)
plt.show()

#country distribution
country_dist = df['country'].value_counts()
print("\nNumber of customers per country:")
print(country_dist)

#percentage of churned vs retained customers
churn_dist = df['churn'].value_counts(normalize=True)*100
print(churn_dist)

#Balance vs churn
import seaborn as sns
import matplotlib.pyplot as plt
#set the size of the plot
plt.figure(figsize=(10, 8))
#create the box plot
#x='churn': The categorical variable
#(0: stayed, 1: left)
#y ='balance':The numerical variable you want to compare
sns.boxplot(x='churn', y='balance',
data=df)
#Add a title and labels for clarity
plt.title('Account Balance vs Customer Churn')
plt.xlabel('churn (0: stayed, 1:left)')
plt.ylabel('Account Balance')
#Display the plot
plt.show()

#churn rate by country
#calculate the churn rate and immediately round it to 1 decimal place
churn_by_country = (df.groupby('country')['churn'].mean() * 100).round(1)
print("\nchurn rate by country (%):")
print(churn_by_country)

#Average balance and estimated salary of churned vs retained customers
financial_summary = df.groupby('churn') [['balance', 'estimated_salary']].mean()
print("\nAverage Balance and estimated_salary by churn status:")
print(financial_summary)

#Correlation between Credit score and Balance
correlation = df['credit_score'].corr(df['balance'])
print(f"\ncorrelation between Credit score and Balance: {correlation:.2f}")
sns.scatterplot(x='credit_score', y='balance', data=df)
plt.title("Credit Score vs Balance")
plt.show()
#Top 3 customer profiles likely to churn
#create a profile with multiple features
profile_cols = ['customer_id', 'gender', 'credit_score', 'tenure', 'products_number', 'active_member']
top_churn_profiles = df[df['churn'] ==1].groupby(profile_cols).size().sort_values(ascending=False).head(3)
print("\ntop 3 customer profiles most likely to churn:")
print(top_churn_profiles)

gender_country_churn = df.groupby(['country', 'gender'])['churn'].mean() * 100
highest_churn_group = gender_country_churn.idxmax()
print(f"\gender-country combination with highest churnrate:{highest_churn_group}")

#segement contributing most to total balance or salary
segment_value = df.groupby(['country', 'gender'])[['balance']].sum()
highest_balance_segment = segment_value['balance'].idxmax()
print(f"\nsegment with highest total balance: {highest_balance_segment}")
df.to_csv('cleaned_data.csv', index=False)

