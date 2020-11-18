import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pickle
from sklearn.model_selection import RandomizedSearchCV


df = pd.read_csv('WindData_Model.csv')


x1, x2 = df.iloc[0:4055,2:], df.iloc[5740:,2:]
X_train = pd.concat([x1, x2])
X_test = df.iloc[4055:5740,2:]
print(X_train.head())
print(X_test.head())
y1, y2 = df.iloc[0:4055,1], df.iloc[5740:,1]
y_train = pd.concat([y1, y2])

y_test = df.iloc[4055:5740,1]
print(y_train.head())
print(y_test.head())
# RandomForestRegressor
rf = RandomForestRegressor()


# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 1200, num = 12)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(5, 30, num = 6)]

# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10, 15, 100]

# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 5, 10]

random_grid_rf = {  'n_estimators': n_estimators,
                    'max_features': max_features,
                    'max_depth': max_depth,
                    'min_samples_split': min_samples_split,
                    'min_samples_leaf': min_samples_leaf}


rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid_rf, scoring='neg_mean_squared_error', n_iter = 10, cv = 5, verbose = 2, random_state = 42, n_jobs = 1)
rf_random.fit(X_train, y_train)

preds_rf2 = rf_random.predict(X_test)

file = open('Power_Model.pkl', 'wb')
pickle.dump(rf_random, file)

model = pickle.load(open('Power_Model.pkl', 'rb'))
print(model.predict([[557.3723632902248, 5.79300785064697]]))