import os
import datetime
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# To import & display the csv file:
dataset = pd.read_csv("C:\\Users\\Ziad\\Downloads\\Downloads\\Just Study!\\Data Science Mehtology\\Project\\Dataset\\walmartSales.csv")

# To display the first 5 rows of the data:
dataset.head()

# To find and rename the unnamed coulumns:
unnamed_cols = dataset.columns[dataset.columns.str.contains('Unnamed')]

if len(unnamed_cols) > 0:
    print("Unnamed columns found:", unnamed_cols.tolist())
else:
    print("No unnamed columns found.")

# No unnamed columns so, we won't change anything.

# To check the data types & change it if we need:
dataset.dtypes

# From the previous we need to change date column from object type to datetime type:
dataset['Date'] = pd.to_datetime(dataset['Date'], dayfirst = True)
dataset.dtypes
# We have changed the type of date column so we can use it.

# To check the null values & drop or filling them if we need:
dataset.isnull().sum()
# no null values :)

# To check the duplicates and drop them:
dataset.duplicated().sum()
# no duplicated rows :)

# Adding month and year column to dataset we will need: 
dataset['year'] = pd.DatetimeIndex(dataset['Date']).year # year column 
dataset['month'] = dataset['Date'].dt.month_name() # month column
dataset.head()

# To visualize the data: 

# The sales over the year with area chart:
year_array = np.array(dataset['year'])
year_array = np.sort(year_array)
dataset['year'] = year_array
fig = px.area(dataset, x = 'year', y = 'Weekly_Sales', title = 'Sales over the years', labels = {'Year':'Year', 'Weekly_Sales':'Weekly_Sales'})
fig.update_layout(width = 1100, height = 600)
fig.show()

# To find the total sales per monthe & visualize it:
month_sales = dataset.groupby('month')[['Weekly_Sales']].sum()
month_sales
fig = px.bar(x = dataset['month'], y = dataset['Weekly_Sales'], title = 'Monthly Sales', color_discrete_sequence = ['red'])
fig.update_xaxes(title_text = 'Month')
fig.update_yaxes(title_text = 'Weekly_Sales')
fig.update_layout(width = 1100, height = 600)
fig.show()

# To find the hiehest sales in which year and visualize it: 
year_sales = dataset.groupby('year')[['Weekly_Sales']].sum()
year_sales
fig = px.line(year_sales, x = year_sales.index, y = year_sales['Weekly_Sales'], title = 'Total Sales per years')
fig.show()
# The highest years in sales are [2011].

# Visualoze the outliers data: 
features = ['CPI', 'Temperature', 'Fuel_Price', 'Unemployment']
fig, axs = plt.subplots(1,  len(features), figsize = (5 * len(features), 6))
for i , features in enumerate(features) :
    axs[i].boxplot(dataset[features])
    axs[i].set_title(f'{features}')
    axs[i].set_xlabel(f'{features} Values')
    axs[i].set_ylabel(features)
    axs[i].grid(True)

plt.tight_layout()
plt.show()

# A. To find the highst sales in which store: 
total_sales_by_store = dataset.groupby("Store")["Weekly_Sales"].sum()
pd.DataFrame(total_sales_by_store)
plt.figure(figsize = (13, 5))
total_sales_by_store.plot(kind ="bar" ,edgecolor = "black")
plt.xlabel("Store ID")
plt.ylabel("Total Weekly Sales")
plt.title("Total Sales in each store")
max_sales = total_sales_by_store.max()
store_with_max_sales = total_sales_by_store.idxmax()
print(str(max_sales) + 'B ' + 'in store: ' + str(store_with_max_sales))

# B. To find the hightest S.D in store: 
weekly_sales_std_by_store = dataset.groupby('Store')['Weekly_Sales'].std()
pd.DataFrame(weekly_sales_std_by_store)
plt.figure(figsize = (13, 5))
weekly_sales_std_by_store.plot(kind = "bar" ,edgecolor = "black")
plt.xlabel("Store ID")
plt.ylabel("Standard Deviation")
plt.title("S.D in each store")
store_with_max_std = weekly_sales_std_by_store.idxmax()
max_std_value = weekly_sales_std_by_store.max()
print('the max S.D in store: ' + str(max_std_value) + ' in store ' + str(store_with_max_std))

# C&D.The holidays that have higher sales than the mean sales in the non-holiday season for all stores:
# To find all holidays in our date and delete the duplicates:
holidays = dataset.loc[dataset["Holiday_Flag"] == 1, 'Date']
holidays.duplicated().sum()
pd.DataFrame(holidays).drop_duplicates()

# The holidays in each month:
faburay_holidays = ['2010-02-12','2011-02-11','2012-02-10']
november_holidays = ['2010-11-26','2011-11-25']
september_holidays = ['2010-09-10','2011-09-09','2012-09-07']
december_holidays = ['2010-12-31','2011-12-30']

# To calculate the mean sales in this holidays:
feburayholidayes_mean_sales = dataset[dataset['Date'].isin(faburay_holidays)]['Weekly_Sales'].mean()
novemberholidayes_mean_sales = dataset[dataset['Date'].isin(november_holidays)]['Weekly_Sales'].mean()
septemberholidayes_mean_sales = dataset[dataset['Date'].isin(september_holidays)]['Weekly_Sales'].mean()
decemberholidayes_mean_sales = dataset[dataset['Date'].isin(december_holidays)]['Weekly_Sales'].mean()
holidays_mean_sales = [feburayholidayes_mean_sales,novemberholidayes_mean_sales,septemberholidayes_mean_sales,decemberholidayes_mean_sales]
holidays_mean_sales

# To calculate the mean sales in nonholidays:
notholidays_mean_sales = dataset[dataset["Holiday_Flag"] == 0]['Weekly_Sales'].mean()
notholidays_mean_sales

# The result:
sales = {
    'notholidays_mean_sales': notholidays_mean_sales,
    'feburayholidayes_mean_sales': feburayholidayes_mean_sales,
    'novemberholidayes_mean_sales': novemberholidayes_mean_sales,
    'septemberholidayes_mean_sales': septemberholidayes_mean_sales,
    'decemberholidayes_mean_sales': decemberholidayes_mean_sales
}

sorted_sales = dict(sorted(sales.items(), key = lambda item: item[1], reverse = True))
sortedsales = pd.DataFrame([sorted_sales]).T
sortedsales

# Seasons sales visualization: 
# Defining the seasons:
summer = dataset[dataset['month'].isin(['June', 'July', 'August'])]
winter = dataset[dataset['month'].isin(['December', 'January', 'February'])]
spring = dataset[dataset['month'].isin(['March', 'April', 'May'])]
autumn = dataset[dataset['month'].isin(['September', 'November', 'December'])]
seasons = ['Summer', 'Winter', 'Spring', 'Autumn']
total_sales = [summer['Weekly_Sales'].sum(), winter['Weekly_Sales'].sum(), spring['Weekly_Sales'].sum(), autumn['Weekly_Sales'].sum()]

# The visualization:
fig = px.bar(x = seasons, y = total_sales, color = seasons, title = 'Sales Of Each Season', orientation = 'v') 
fig.update_xaxes(title_text='Season')
fig.update_yaxes(title_text='Sales')
fig.update_layout(width=1100,height=600)
fig.show()

# The relation between the weekly sales and the numeric values: 

# We use the scatter blot cause the numeric values.
numeric_features = ['Temperature', 'Fuel_Price', 'CPI', 'Unemployment']
fig = px.scatter(dataset, x = 'Weekly_Sales', y = numeric_features, title = 'Numeric Values Vs Weekly Sales')
fig.update_layout(xaxis_title='Weekly Sales', yaxis_title ='Value', height = 1000)
fig.show()