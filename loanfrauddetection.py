import pandas as pd
from sklearn.preprocessing import LabelEncoder
df=pd.read_csv(r"C:\Users\DELL\OneDrive\Documents\GitHub\Mugilan\csv\loan_default_prediction_project (1).csv")
column111=['Age', 'Gender', 'Income', 'Employment_Status', 'Location',
       'Credit_Score', 'Debt_to_Income_Ratio', 'Existing_Loan_Balance',
       'Loan_Status', 'Loan_Amount', 'Interest_Rate', 'Loan_Duration_Months']
df['Gender'].fillna("Female",inplace=True)
Empsts=df['Employment_Status'].mode()[0]
df['Employment_Status'].fillna(Empsts,inplace=True)
label_encoder = LabelEncoder()
df['Gender']=label_encoder.fit_transform(df['Gender'])
df['Employment_Status']=label_encoder.fit_transform(df['Employment_Status'])
df['Location']=label_encoder.fit_transform(df['Location'])
df['Loan_Status']=label_encoder.fit_transform(df['Loan_Status'])
x=df[['Age', 'Gender', 'Income', 'Employment_Status', 'Location',
       'Credit_Score', 'Debt_to_Income_Ratio', 'Existing_Loan_Balance',
    'Loan_Amount', 'Interest_Rate', 'Loan_Duration_Months']]
y=df['Loan_Status']
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.1,random_state=0)
from sklearn.ensemble import GradientBoostingClassifier
Classifier=GradientBoostingClassifier(n_estimators=7, random_state=0)
Classifier.fit(x_train,y_train)
y_pred = Classifier.predict(x_test)

#### Confusion Matrix - study on error metrics
from sklearn.metrics import confusion_matrix
cm=confusion_matrix(y_test, y_pred)
print(cm)


### accuracy
from sklearn.metrics import accuracy_score, confusion_matrix
print(accuracy_score(y_test, y_pred))
