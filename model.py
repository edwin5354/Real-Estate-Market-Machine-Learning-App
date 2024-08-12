import pandas as pd 

# Open csv file
df = pd.read_csv('excel_files/cleaned.csv')

# Drop some columns specifically for the ML model
model_df = df.drop(['address', 'district', 'sap', 'gfa', 'gfap', 'monthly'], axis=1)

# Wrong technique... Should be using One-Hot-Encoding to deal with categorical variables
convert_num = {
    'NT West': 1,
    'NT East': 2,
    'HK Island': 3,
    'Kowloon': 4
}

def get_num(region):
    for each_reg, num in convert_num.items():
        if each_reg in region:
            return num

model_df['region'] = model_df['region'].apply(get_num)

# Extract X & y variables 
X = model_df.drop(['price'], axis= 1)
y = model_df['price']

#  Split the test and train data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Decision Tree Regressor
from sklearn.tree import DecisionTreeRegressor
model_tree = DecisionTreeRegressor()
model_tree.fit(X_train, y_train)

# Save the tree model and scaler model
import pickle
with open('model/decision_tree_model.pkl', 'wb') as model_file:
    pickle.dump(model_tree, model_file)

with open('model/scaler.pkl', 'wb') as scaler_file:
    pickle.dump(sc, scaler_file)
