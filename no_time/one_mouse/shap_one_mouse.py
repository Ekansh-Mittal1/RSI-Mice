import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model
import shap
import numpy as np
from sklearn.preprocessing import MinMaxScaler

pp_l = ["day", "night", "all"]
pp = pp_l[1]

#read data
x_df = pd.read_csv("../../Data/one_animal_training_data_"+pp+".csv", index_col=0)
x_df = x_df.drop(columns=['glucose', 'ee', 'exp.hour'])
y_df = pd.read_csv("../../Data/one_animal_training_data_"+pp+".csv", usecols=['glucose'])

print(x_df.head())
print(y_df.head())

x_scaler = MinMaxScaler()
y_scaler = MinMaxScaler()
scaled_x_np = x_scaler.fit_transform(x_df.values)
scaled_y_np = y_scaler.fit_transform(y_df.values)

scaled_x_df = pd.DataFrame(scaled_x_np, index=x_df.index, columns=x_df.columns)
scaled_y_df = pd.DataFrame(scaled_y_np, index=y_df.index, columns=y_df.columns)

x_train, x_rem, y_train, y_rem = train_test_split(scaled_x_df, scaled_y_df, train_size=0.8, random_state=42)

x_valid, x_test, y_valid, y_test = train_test_split(x_rem, y_rem, test_size=0.5, random_state=42)

model = load_model(pp+"/one_mouse_model_"+pp+".h5")

cols = column_names = list(x_df.columns)

x_train_np = x_train.to_numpy()
x_test_np = x_test.to_numpy()
x_valid_np = x_valid.to_numpy()

explainer = shap.GradientExplainer(model, x_train_np, features=cols)
shap_values = explainer.shap_values(x_valid_np)
shap.summary_plot(shap_values[0], plot_type='bar', feature_names=cols, max_display=20, show=False)
plt.savefig(pp+"/shap_importances.png")

feature_names = x_train.columns
rf_resultX = pd.DataFrame(shap_values[0], columns=feature_names)

print(rf_resultX)

vals = np.abs(rf_resultX.values).mean(0)

shap_importance = pd.DataFrame(list(zip(feature_names, vals)),
                               columns=['col_name', 'feature_importance_vals'])
shap_importance.sort_values(by=['feature_importance_vals'],
                            ascending=False, inplace=True)
print(shap_importance.head())

shap_importance.to_csv(pp+'/one_mouse_importances.tsv', sep='\t')
