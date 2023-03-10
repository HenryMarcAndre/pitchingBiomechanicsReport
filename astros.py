# -*- coding: utf-8 -*-
"""astros.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UflMYzm2OpoZljjJc5EGB_cKkDdl4cXC
"""

import pandas as pd
import numpy as np

df = pd.read_csv("/content/astrosNew.csv")

df = df.drop(df.index[72])
df = df.drop(columns=["plate_speed"])

df['hip_torso_separation_at_sit'] = df["hip_rotation_at_sit"] - df['torso_rotation_at_sit']

df['hip_torso_separation_at_footplant'] = df["hip_rotation_at_footplant"] - df['torso_rotation_at_footplant']

df['hip_torso_separation_at_release'] = df["hip_rotation_at_release"] - df['torso_rotation_at_release']

fastballs = df.loc[df['pitch_type'] == 'FF']

import seaborn as sns
import matplotlib.pyplot as plt

target_column = "release_speed"

correlations = df.corr()[target_column].sort_values()

print("Top 5 positive correlations with {}:".format(target_column))
print(correlations[-5:])

top_5_correlations = correlations[-5:].index

plt.matshow(df[top_5_correlations].corr())
plt.xticks(np.arange(len(top_5_correlations)), top_5_correlations, rotation=90)
plt.yticks(np.arange(len(top_5_correlations)), top_5_correlations)
plt.colorbar()
plt.show()

target_column = "release_speed"

correlations = df.corr()[target_column].sort_values()

print("Negative top 5 correlations with {}:".format(target_column))
print(correlations[0:4])

top_5_correlations = [target_column] + list(correlations[0:4].index)

corr_matrix = np.abs(df[top_5_correlations].corr())

plt.matshow(corr_matrix)
plt.xticks(np.arange(len(top_5_correlations)), top_5_correlations, rotation=90)
plt.yticks(np.arange(len(top_5_correlations)), top_5_correlations)
plt.colorbar()
plt.show()

import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, GridSearchCV, KFold
from sklearn.feature_selection import RFE
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

X = fastballs.iloc[:, 5:]
Y = fastballs["release_speed"]
features = X.columns

model = RandomForestRegressor()
rfe = RFE(estimator=model, n_features_to_select=5)
fit = rfe.fit(X, Y)
X = X.iloc[:, fit.support_]
features = features[fit.support_]

param_grid = {'n_estimators': [10, 50, 100],
              'max_depth': [None, 10, 20]}

kfold = KFold(n_splits=5, shuffle=True)
grid_search = GridSearchCV(model, param_grid, cv=kfold, scoring='neg_mean_squared_error')
grid_search.fit(X, Y)

best_model = grid_search.best_estimator_
best_model.fit(X, Y)

scores = cross_val_score(best_model, X, Y, cv=kfold, scoring='neg_mean_squared_error')
scores = -scores
print("Cross-validated MSE:", scores)
print("Average cross-validated MSE:", scores.mean())

y_pred = best_model.predict(X)
mae = mean_absolute_error(Y, y_pred)
print("Mean Absolute Error:", mae)

r2 = r2_score(Y, y_pred)
print("R^2:", r2)

plt.scatter(Y, y_pred)
plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.show()

importances = best_model.feature_importances_
for feature, importance in zip(features, importances):
    print(f"{feature}: {importance}")

X = df.iloc[:, 5:]
Y = df["release_speed"]
features = X.columns

model = RandomForestRegressor()
rfe = RFE(estimator=model, n_features_to_select=5)
fit = rfe.fit(X, Y)
X = X.iloc[:, fit.support_]
features = features[fit.support_]

param_grid = {'n_estimators': [10, 50, 100],
              'max_depth': [None, 10, 20]}

kfold = KFold(n_splits=5, shuffle=True)
grid_search = GridSearchCV(model, param_grid, cv=kfold, scoring='neg_mean_squared_error')
grid_search.fit(X, Y)

best_model = grid_search.best_estimator_
best_model.fit(X, Y)

scores = cross_val_score(best_model, X, Y, cv=kfold, scoring='neg_mean_squared_error')
scores = -scores
print("Cross-validated MSE:", scores)
print("Average cross-validated MSE:", scores.mean())

y_pred = best_model.predict(X)
mae = mean_absolute_error(Y, y_pred)
print("Mean Absolute Error:", mae)

r2 = r2_score(Y, y_pred)
print("R^2:", r2)

plt.scatter(Y, y_pred)
plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.show()

importances = best_model.feature_importances_
for feature, importance in zip(features, importances):
    print(f"{feature}: {importance}")