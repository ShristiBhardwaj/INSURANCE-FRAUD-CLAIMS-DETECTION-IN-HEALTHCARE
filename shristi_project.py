# -*- coding: utf-8 -*-
"""SHRISTI_PROJECT.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VYaR6IB3ASYFEd7dxl37hBfhv8hQUcIy

# **INSURANCE FRAUD CLAIM DETECTION IN HEALTHCARE**

### **IMPORTING THE LIBRARIES**
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import  confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score, recall_score, f1_score, precision_recall_curve
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings('ignore')

"""### **LOAD THE DATASET**"""

df=pd.read_csv('/content/Insurance Dataset.csv')

"""### **UNDERSTAND THE DATASET**"""

df.head()

df.tail()

df.shape

"""**Shape displays the number of rows and columns of the dataset**"""

df.describe()

df['Result'].value_counts()

"""**The describe() function provides summary statistics of the DataFrame's numerical columns**"""

df.info()

"""**Converting Days_spent_hsptl and age column to numeric**"""

df['Days_spend_hsptl']=pd.to_numeric(df['Days_spend_hsptl'],errors='coerce')

#Verifying the conversions
df.info()

"""**The info() function provides a concise summary of the DataFrame, including the number of non-null entries, column data types, and memory usage.**"""

df.duplicated()

"""**Duplicate() finds duplicate entries if any**"""

df.columns

"""**Columns gives name of all the columns in the dataset**

**ATTRIBUTES INFORMATION :**
- Area_Service: Where the service was provided.
- Hospital: The hospital where the treatment was given.
- County: County of the hospital.
- Hospital Id: Unique identifier for the hospital.
- Age, Gender, Cultural_group, Ethnicity: Patient demographics.
- Days_spend_hsptl: Duration of hospital stay.
- Admission_type: Type of hospital admission (emergency, elective, etc.).
- Home or self care: Whether the patient was discharged to home or needed further care.
- ccs_diagnosis_code, ccs_procedure_code: Codes for diagnosis and procedures.
- apr_drg_description: Description of the diagnosis-related group.
- Code_illness: Severity of illness.
- Mortality risk: Risk of patient death.
- Surg_Description: Details of any surgery performed.
- Weight_baby: Birth weight (if applicable).
- Abortion: Indicator of whether abortion was involved.
- Emergency_dept_yes/No: Whether the patient visited the emergency department.
- Tot_charg: Total charges for the visit.
- Tot_cost: Total costs incurred.
- ratio_of_total_costs_to_total_charges: Ratio of total costs to charges.
- Result: Outcome of the hospital visit (recovered, deceased, etc.).
- Payment_Typology: Type of payment (insurance, self-pay, etc.).

### **DATA CLEANING**

### CHECKING FOR MISSING VALUES IN EACH COLUMN
"""

print(df.isnull().sum())

"""**Missing values in 5 columns:**
* Area_Service                     
* Hospital County                          
* Hospital Id
* Mortality risk
* Days_spend_hsptl
"""

#Displaying the total number of rows
print(f"Total number of rows: {len(df)}")

#Finding the proportion of null values in each column
columns_with_missing_values = ['Area_Service','Hospital County','Hospital Id', 'Mortality risk','Days_spend_hsptl']
proportion_of_missing = df[columns_with_missing_values].isnull().sum() / len(df) * 100

proportion_of_missing

"""**As the proportion of missing values is less than 1% of the data ,it does not makes much impact to drop(delete) the rows with null values**"""

#DROPPING THE ROWS WITH NULL VALUES
df.dropna(subset=columns_with_missing_values, inplace=True)

"""**CHECKING FOR MISSING VALUES AGAIN TO ENSURE CLEAN DATA**"""

df.isnull().sum()

#NUMBER OF ROWS AFTER DROPING THE ROWS WITH NULL VALUES
print(f"\nNumber of rows after dropping rows with missing values in specified columns: {len(df)}")

"""# **DATA VISUALIZATION**

VISUALIZING THE AGE DISTRIBUTION USING HISTOGRAM
"""

df['Age'].hist(bins=30,color='purple')
plt.title('Age Distribution')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title("AGE DISTRIBUTION")
plt.show()

"""**MAXIMUM PEOPLE BELONG TO THE AGE GROUP "70 OR OLDER"**"""

df.groupby('Age')['Tot_charg'].mean().plot(color="orange")
plt.title('Average Total Charges by Age')
plt.xlabel('Age')
plt.ylabel('Average Total Charges')
plt.show()

"""**WE OBSERVE THAT AVERAGE TOTAL CHANGE CHANGES WITH INCREASE IN THE AGE**"""

df.groupby('Surg_Description')['Tot_cost'].mean().plot(color="teal")
plt.title('Average Total Cost by Surgery Description')
plt.xlabel('Surgery Description')
plt.ylabel('Average Total Cost')
plt.show()

"""**THERE IS A DIRECT RELATION BETWEEN AVERAGE TOTAL COST AND SURGERY DESCRIPTION**"""

df['ethnicity'].hist(bins=30,color="green")
plt.title('ethnicity Distribution')
plt.xlabel('ethnicity')
plt.ylabel('Frequency')
plt.title("ETHNICITY DISTRIBUTION")
plt.show()

"""**MAXIMUM PATIENTS BELONG TO THE ETHINICITY "Not Span/Hispanic**"""

df['Gender'].value_counts().plot.pie(autopct='%1.1f%%')
plt.title('Gender Distribution')
plt.show()

"""**THERE IS A MAJORITY OF MALE PATIENTS**"""

df['Emergency dept_yes/No'].value_counts().plot.pie(autopct='%1.1f%%')
plt.title('EMERGENCY DEPARTMENT')
plt.show()

"""**MAJORITY CASES BELONG TO THE EMERGENCY DEPARTMENT**"""

df['Surg_Description'].value_counts().plot.pie(autopct='%1.1f%%')
plt.title('Surgery Description Distribution')
plt.show()

df.groupby('Days_spend_hsptl')['Tot_charg'].mean().plot()
plt.title('Total Charges by Days Spent in Hospital')
plt.xlabel('Days Spent in Hospital')
plt.ylabel('Average Total Charges')
plt.show()

"""**WITH INCREASE IN NUMBER OF DAYS SPENT IN HOSPITAL, CHARGES ALSO INCREASES**"""

df.groupby('Age')['Mortality risk'].mean().plot()
plt.title('Mortality Risk by Age')
plt.xlabel('Age')
plt.ylabel('Average Mortality Risk')
plt.show()

"""**WE OBSERVE THAT MORTALITY RISK INCREASES WITH INCREASE IN THE AGE**

# **TRAINING THE MODELS**
"""

df=df.drop(columns=['Hospital Id','Age','Home or self care,','apr_drg_description','Weight_baby','Abortion','Emergency dept_yes/No',
'ratio_of_total_costs_to_total_charges','Payment_Typology','Area_Service'],axis=1)

df=df.drop(columns=['Cultural_group'	,'ethnicity'],axis=1)

df=df.drop(columns=['Days_spend_hsptl'],axis=1)

df.shape

y=df['Result']

x=df.drop(['Result'],axis=1)

x

y.head()

x=pd.get_dummies(x,columns=['Hospital County', 'Gender','Admission_type','Surg_Description'],dtype='int')

x.head()

x.info()

"""### **SPLITTING THE DATA FOR TRAINING AND TESTING**"""

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

"""**Splitting data into training and testing**

**test_size=0.3 tells that 70% of data is used for training and rest 30% for testing**

**Checking the shape of x_train,y_train and x_test,y_test**
"""

x_train.shape

x_test.shape

y_train.shape

y_test.shape

"""### **As our data in imbalnced, we use oversampling**"""

from imblearn.over_sampling import RandomOverSampler
ros = RandomOverSampler(random_state=0)
x_new, y_new = ros.fit_resample(x_train, y_train)

print("original dataset shape:", y_train.value_counts())
print("resampled dataset shape:", y_new.value_counts())

"""## **1. LOGISTIC REGRESSION**"""

logreg = linear_model.LogisticRegression()
logreg.fit(x_new,y_new) #we always fit the training data
predicted_y_lreg = logreg.predict(x_test)
print(predicted_y_lreg)

"""### **CONFUSION MATRIX**"""

confusion_matrix(y_test,predicted_y_lreg)

"""### **HEATMAP**"""

conf_matrix = confusion_matrix(y_test,predicted_y_lreg)

plt.figure(figsize=(6, 4))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Logistic Regression Confusion Matrix')
plt.show()

"""## **2. KNN**

**KNN CAN ONLY BE USED FOR SMALL DATA SETS AND BECAUSE MY DATASET HAS 1MILLION+ ROWS I CAN'T APPLY IT TO MY DATASET**

## **3. DECISISON TREE CLASSIFIER**
"""

clf = tree.DecisionTreeClassifier(max_depth=5)
clf = clf.fit(x_new,y_new)
predicted_y_dt=clf.predict(x_test)

predicted_y_dt

"""**PLOTTING THE DECISION TREE**"""

tree.plot_tree(clf)
plt.show()

"""### **CONFUSION MATRIX**"""

confusion_matrix(y_test,predicted_y_dt)

"""### **HEATMAP**"""

conf_matrix = confusion_matrix(y_test,predicted_y_dt)

plt.figure(figsize=(6, 4))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Decision Tree Confusion Matrix')
plt.show()

"""## **4. RANDOM FOREST**"""

rf_mode = RandomForestClassifier(n_estimators=100, random_state=42)
rf_mode=rf_mode.fit(x_new,y_new)

predicted_y_rf = rf_mode.predict(x_test)

predicted_y_rf

"""### **CONFUSION MATRIX**"""

confusion_matrix(y_test,predicted_y_rf)

"""### **HEATMAP**"""

conf_matrix = confusion_matrix(y_test,predicted_y_rf)

plt.figure(figsize=(6, 4))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Random Forest Confusion Matrix')
plt.show()

"""## **5. SUPPORT VECTOR MACHINE (SVM)**

**SVM CAN ONLY BE USED FOR SMALL DATA SETS AND BECAUSE MY DATASET HAS 1MILLION+ ROWS I CAN'T APPLY IT TO MY DATASET**

# **MODEL COMPARISIONS**

### **COMPARING THE ACCURACY SCORES**
"""

score_LG =accuracy_score(y_test,predicted_y_lreg)
score_DT =accuracy_score(y_test,predicted_y_dt)
score_RF=accuracy_score(y_test,predicted_y_rf)

print("ACCURACY REPORT")
print("Accuracy score of Logistic Regression",score_LG)
print("Accuracy score of Decision Tree",score_DT)
print("Accuracy score of Random Forest",score_RF)

"""### **COMPARING THE CLASSIFICATION REPORTS**"""

report_LG=classification_report(y_test, predicted_y_lreg)

report_DT=classification_report(y_test, predicted_y_dt)

report_RF=classification_report(y_test,predicted_y_rf)

print("CLASSIFICATION REPORTS")
print("Classification report of Logistic Regression")
print(report_LG)
print("Classification report of Decision Tree")
print(report_DT)
print("Classification report of Random Forest")
print(report_RF)

"""### **PRECISION RECALL CURVE**"""

precision, recall, thresholds = precision_recall_curve(y_test,predicted_y_lreg)

plt.plot(recall, precision, marker='.')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Logistic Regression Precision-Recall Curve')
plt.show()

precision, recall, thresholds = precision_recall_curve(y_test,predicted_y_dt)

plt.plot(recall, precision, marker='.')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Decision Tree Precision-Recall Curve')
plt.show()

precision, recall, thresholds = precision_recall_curve(y_test,predicted_y_rf)

plt.plot(recall, precision, marker='.')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Random Forest Precision-Recall Curve')
plt.show()