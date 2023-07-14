# -*- coding: utf-8 -*-
"""finalclaiminsurancecode.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Hf8gPIQ3kce0JfSIlb-dOGCMg3CmWAXL

# **DATA SCIENCE AND PATTERN RECOGNITION**
**Final Project (*Vehicle Insurance Claim Fraud Detection*)** 

Hitesh Vilas Sakhare

Insurers can use data science techniques to accurately identify fraudulent claims by implementing analytical tools. 
These tools can predict whether a claim is fraudulent or not by analyzing historical claim data and policyholder information.

# Importing Libraries
"""

import pandas as pd
import re
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

"""# Data Procurement"""

df = pd.read_csv('fraud_oracle.csv') # Loading the dataset into pandas dataframe
df

# This generates a statistical summary of the dataframe 'df' using the describe() method.
df.describe()

"""# Exploratory Data Analysis"""

# Create a new figure with a size of 12 by 8 inches
plt.figure(figsize=(12, 8))

# Create a count plot using Seaborn's `countplot()` function,
# where the x-axis shows the "Make" column of the given DataFrame.
# The order of the bars on the x-axis is set based on the number of
# occurrences of each "Make" value in the DataFrame, in descending order.
# The data used for the plot is the given DataFrame `df`.
ax3 = sns.countplot(x="Make", order=df['Make'].value_counts().index, data=df)

# Set the x-label of the plot to "Class" and the y-label to "Count"
ax3.set(xlabel='Class', ylabel='Count')

# Display the plot
plt.show()

# set the style of the plot
sns.set(style="whitegrid")

# set the size of the plot
plt.figure(figsize=(15,4))

# create a bar plot using seaborn's barplot function
# x = 'Make': the column in the dataframe to use as the x-axis
# y = 'FraudFound_P': the column in the dataframe to use as the y-axis
# data = df: the dataframe to use as the data source
# palette = 'hls': the color palette to use for the bars
# capsize = 0.05: the size of the caps on the error bars
# saturation = 8: the saturation of the colors
# errcolor = 'gray': the color of the error bars
# errwidth = 2: the width of the error bars
# order = df['Make'].value_counts().index: the order to use for the bars, based on the frequency of each value in the 'Make' column
# ci = 'sd': the method to use for calculating the confidence interval (standard deviation)
ax=sns.barplot(x = 'Make', y = 'FraudFound_P', data = df,
            palette = 'hls',
            capsize = 0.05,             
            saturation = 8,             
            errcolor = 'gray', errwidth = 2,
            order=df['Make'].value_counts().index,
            ci = 'sd'   
            )

# print the mean fraud found percentage for each make of car
print(df.groupby(['Make']).mean()['FraudFound_P'])

# print the standard deviation of the fraud found percentage for each make of car
print(df.groupby(['Make']).std()['FraudFound_P'])

# adjust the spacing of the subplots to prevent overlap
plt.tight_layout()

# display the plot
plt.show()

df.describe()

# Set the size of the figure to 10 by 10 inches
plt.figure(figsize=(10, 10))

# Create a heatmap of the correlation matrix for the DataFrame `df`,
# with annotations displaying the correlation coefficients.
sns.heatmap(df.corr(), annot=True)

# Display the plot
plt.show()

# This line of code creates a bar chart using Matplotlib's pyplot library.
# The bar chart will have the age values from the 'Age' column on the x-axis and 
# the corresponding year values from the 'Year' column on the y-axis.
# The chart will be created using data from the pandas DataFrame object 'df'.
plt.bar(df['Age'], df['Year'])

# This line creates a histogram for all columns in the dataframe `df`
# The `figsize` parameter sets the size of the histogram figure to (15, 10) inches
df.hist(figsize=(15,10))

# This line adjusts the spacing between the subplots in the figure
# The `hspace` parameter sets the height space between the subplots to 0.7 inches
plt.subplots_adjust(hspace=0.7);

"""# Data Cleaning"""

# Remove duplicates
df.drop_duplicates(inplace=True)

# Drop rows with missing values
df.dropna(inplace=True)

# to check if there are any null values in the dataset
df.isnull().sum()

# Get the number of unique values in each column of the DataFrame `df`
# `df.nunique()` returns a new Series object with the number of unique values in each column
# The result is indexed by column name, with the number of unique values as the corresponding value
df.nunique()

"""# Convert values of different types to floats

* This Python function that takes in a value and converts it to a float. The function first checks if the input is already an integer or a float, and if so, simply returns the input as a float.

* If the input contains the phrase 'more than', the function extracts the first integer value found in the string using regular expressions and returns it as a float.

* If the input contains the word 'to', the function extracts all integer values found in the string using regular expressions, calculates the average of the values, and returns it as a float.

* If the input contains the word 'years', the function extracts the first integer value found in the string using regular expressions and returns it as a float.

* If none of these conditions are met, the function returns None.
"""

# define a function named convert_to_float that takes a single argument val
def convert_to_float(val):
    # check if val is already an integer, and if so, convert it to a float and return it
    if isinstance(val, int):
        return float(val)
    # check if val is already a float, and if so, return it
    elif isinstance(val, float):
        return val
    # check if val contains the string "more than"
    elif 'more than' in val:
        # extract the first number found in val using regular expressions, convert it to a float, and return it
        return float(re.findall(r'\d+', val)[0])
    # check if val contains the string "to"
    elif 'to' in val:
        # extract both numbers found in val using regular expressions, convert them to floats, take their average, and return it
        return sum(map(float, re.findall(r'\d+', val))) / 2
    # check if val contains the string "years"
    elif 'years' in val:
        # extract the first number found in val using regular expressions, convert it to a float, and return it
        return float(re.findall(r'\d+', val)[0])
    # if none of the above rules apply, return None
    else:
        return None

# Applying the above function 
df['Days_Policy_Accident'] = df['Days_Policy_Accident'].apply(convert_to_float)
df['Days_Policy_Claim'] = df['Days_Policy_Claim'].apply(convert_to_float)
df['PastNumberOfClaims'] = df['PastNumberOfClaims'].apply(convert_to_float)
df['AgeOfVehicle'] = df['AgeOfVehicle'].apply(convert_to_float)
df['AgeOfPolicyHolder'] = df['AgeOfPolicyHolder'].apply(convert_to_float)
df['NumberOfSuppliments'] = df['NumberOfSuppliments'].apply(convert_to_float)
df['NumberOfCars'] = df['NumberOfCars'].apply(convert_to_float)
df['VehiclePrice'] = df['VehiclePrice'].apply(convert_to_float)
# Convert the Following columns to float
df['Days_Policy_Accident'] = df['Days_Policy_Accident'].astype(float)
df['Days_Policy_Claim'] = df['Days_Policy_Claim'].astype(float)
df['PastNumberOfClaims'] = df['PastNumberOfClaims'].astype(float)
df['AgeOfVehicle'] = df['AgeOfVehicle'].astype(float)
df['AgeOfPolicyHolder'] = df['AgeOfPolicyHolder'].astype(float)
df['NumberOfSuppliments'] = df['NumberOfSuppliments'].astype(float)
df['NumberOfCars'] = df['NumberOfCars'].astype(float)
df['VehiclePrice'] = df['VehiclePrice'].astype(float)

"""# Data Transformation"""

# Create a LabelEncoder object
le = LabelEncoder()
# Encode the column of the DataFrame and store the result in a new column
df['Month']= le.fit_transform(df['Month'])
df['DayOfWeek']= le.fit_transform(df['DayOfWeek'])
df['DayOfWeekClaimed'] = le.fit_transform(df['DayOfWeekClaimed'])
df['MonthClaimed'] = le.fit_transform(df['MonthClaimed'])
df['Make'] = le.fit_transform(df['Make'])
df['AccidentArea'] = le.fit_transform(df['AccidentArea'])
df['Sex'] = le.fit_transform(df['Sex'])
df['MaritalStatus'] = le.fit_transform(df['MaritalStatus'])
df['Fault'] = le.fit_transform(df['Fault'])
df['PolicyType'] = le.fit_transform(df['PolicyType'])
df['VehicleCategory'] = le.fit_transform(df['VehicleCategory'])
df['PoliceReportFiled'] = le.fit_transform(df['PoliceReportFiled'])
df['WitnessPresent'] = le.fit_transform(df['WitnessPresent'])
df['AgentType'] = le.fit_transform(df['AgentType'])
df['AddressChange_Claim'] = le.fit_transform(df['AddressChange_Claim'])
df['BasePolicy'] = le.fit_transform(df['BasePolicy'])

"""# Converting categorical variables to numerical values and Scaling the data"""

# Convert categorical variables to numerical values
cat_cols = ['Make', 'Sex', 'MaritalStatus', 'Fault', 'PolicyType', 'VehicleCategory', 'VehiclePrice',
            'PoliceReportFiled', 'WitnessPresent', 'AgentType', 'AddressChange_Claim', 'BasePolicy']
le = LabelEncoder()
for col in cat_cols:
    df[col] = le.fit_transform(df[col])

# Scale the data
num_cols = ['Age', 'Deductible', 'DriverRating', 'Days_Policy_Accident', 'Days_Policy_Claim',
            'PastNumberOfClaims', 'AgeOfVehicle', 'AgeOfPolicyHolder', 'NumberOfSuppliments',
            'NumberOfCars', 'Year']
scaler = MinMaxScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

# Identify outliers
sns.boxplot(x=df['Age'])

"""# Feature Engineering"""

# Feature Engineering
df['TotalNumberOfClaims'] = df['PastNumberOfClaims'] + df['Days_Policy_Accident']
df['PolicyAge'] = 2023 - df['Year']

"""# Model Building"""

X = df.drop(['FraudFound_P', 'PolicyNumber','DayOfWeek','DayOfWeekClaimed','MonthClaimed'], axis=1)
y = df['FraudFound_P']
# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fill in missing values with mean
imputer = SimpleImputer(strategy='mean')
X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)

"""# AdaBoost Classifier"""

# Train AdaBoostClassifier model
abc = AdaBoostClassifier()
abc.fit(X_train, y_train)

# Make predictions on test set
y_pred_abc = abc.predict(X_test)

"""# Decision Tree Classifier"""

# Decision Tree Classifier
# Train Decision Tree model
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)
# Make predictions on test set
y_pred_dt = dt_model.predict(X_test)

"""# Random Forest Classifier"""

#Train Random Forest Classifier
rf = RandomForestClassifier()
rf.fit(X_train, y_train)

# Make predictions on test set
y_pred_rf = rf.predict(X_test)

"""# Model Evaluation

**AdaBoost Classifier**
"""

# Calculate various evaluation metrics for the AdaBoost classifier's predictions on the test set
accuracy_abc = accuracy_score(y_test, y_pred_abc)
precision_abc = precision_score(y_test, y_pred_abc)
recall_abc = recall_score(y_test, y_pred_abc)
f1_abc = f1_score(y_test, y_pred_abc)
confusion_abc = confusion_matrix(y_test, y_pred_abc)
# Print the evaluation metrics
print('AdaBoost Classifier: ')
print('Accuracy:', accuracy_abc*100)
print('Precision:', precision_abc*100)
print('Recall:', recall_abc*100)
print('F1 score:', f1_abc*100)
print('Confusion matrix:')
print(confusion_abc)
# Visualize the confusion matrix using a heatmap
sns.set(font_scale=1.4)
sns.heatmap(confusion_abc, annot=True, fmt='g', cmap='autumn')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix AdaBoost')
plt.show()

"""**Decision Tree Classifier**"""

# Calculate various evaluation metrics for the Decision Tree classifier's predictions on the test set
accuracy_dt = accuracy_score(y_test, y_pred_dt)
precision_dt = precision_score(y_test, y_pred_dt)
recall_dt = recall_score(y_test, y_pred_dt)
f1_dt = f1_score(y_test, y_pred_dt)
confusion_dt = confusion_matrix(y_test, y_pred_dt)
# Print the evaluation metrics
print('Decision Tree Classifier:')
print('Accuracy:', accuracy_dt*100)
print('Precision:', precision_dt*100)
print('Recall:', recall_dt*100)
print('F1 score:', f1_dt*100)
print('Confusion matrix:')
print(confusion_dt)
# Visualize the confusion matrix using a heatmap
sns.set(font_scale=1.4)
sns.heatmap(confusion_dt, annot=True, fmt='g', cmap='jet')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix Decision Tree')
plt.show()

"""**Random Forest Classifier**"""

# Calculate various evaluation metrics for the Random Forest classifier's predictions on the test set
accuracy_rf = accuracy_score(y_test, y_pred_rf)
precision_rf = precision_score(y_test, y_pred_rf)
recall_rf = recall_score(y_test, y_pred_rf)
f1_rf = f1_score(y_test, y_pred_rf)
confusion_rf = confusion_matrix(y_test, y_pred_rf)
# Print the evaluation metrics
print('Random Forest Classifier:')
print('Accuracy:', accuracy_rf*100)
print('Precision:', precision_rf*100)
print('Recall:', recall_rf*100)
print('F1 score:', f1_rf*100)
print('Confusion matrix:')
print(confusion_rf)
# Visualize the confusion matrix using a heatmap
sns.set(font_scale=1.4)
sns.heatmap(confusion_rf, annot=True, fmt='g', cmap='jet')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix RandomForest')
plt.show()

"""# Function to predict fraud

This is a Python function that takes in some data as input, uses it to make a prediction with a pre-trained machine learning model, and returns the predicted result. Here is a breakdown of the function:

1. First, the input data is converted to a Pandas DataFrame object with a single row and assigned to a variable called "new_data".

2. Next, the categorical features in "new_data" are converted to one-hot encoded features using the "pd.get_dummies()" function, which creates new columns for each unique value in the categorical features.

3. Then, the feature names in "new_data" are removed by assigning new column names that are simply integers from 0 to the number of columns in the DataFrame.

4. Finally, the pre-trained machine learning model "rf" is used to make a prediction on "new_data" and the predicted result is returned.
"""

def predict_fraud(data):
    # Convert the input data to a pandas DataFrame
    new_data = pd.DataFrame(data, index=[0])

    # Convert categorical features to one-hot encoded features
    new_data = pd.get_dummies(new_data)

    # Remove feature names
    new_data.columns = range(new_data.shape[1])

    # Make a prediction with the trained model
    prediction = rf.predict(new_data)

    return prediction[0]

"""# Real Time Prediction"""

# Example usage
new_data = { 'Month': 10, 'WeekOfMonth': 1, 'Make': 'Toyota', 'AccidentArea': 'Urban',
            'WeekOfMonthClaimed': 2, 'Sex': 'Female', 
            'MaritalStatus': 'Married', 'Age': 65, 'Fault': 'Third Party', 'PolicyType': 'Collison', 
            'VehicleCategory': 'Hatchback', 'VehiclePrice': 20000, 'RepNumber': 789, 
            'Deductible': 500, 'DriverRating': 3, 'Days_Policy_Accident': 10, 'Days_Policy_Claim': 30, 
            'PastNumberOfClaims': 1, 'AgeOfVehicle': 5, 'AgeOfPolicyHolder': '26-30', 'PoliceReportFiled': 
            'No', 'WitnessPresent': 'No', 'AgentType': 'External', 'NumberOfSuppliments': 0, 
            'AddressChange_Claim': 'no change', 'NumberOfCars': 1, 'Year': 2018, 'BasePolicy': 'All Perils'}

# Engineer new features based on domain knowledge or data exploration
new_data['TotalNumberOfClaims'] = new_data['PastNumberOfClaims'] + new_data['Days_Policy_Accident']
new_data['PolicyAge'] = 2023 - new_data['Year']

prediction = predict_fraud(new_data)

if prediction == 1:
    print("Potential fraud detected!")
else:
    print("No fraud detected.")
