import tensorflow as tf
import pandas as pd
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
from tensorflow.keras import metrics
from sklearn.metrics import r2_score, mean_squared_error
import random
import numpy as np
import shap
import seaborn as sns

tf.random.set_seed(0)
random.seed(0)
np.random.seed(0)


pp_l = ["day", "night", "all"]
pp = pp_l[2]

# read data
x_df = pd.read_csv("../../Data/chow_training_data_" + pp + ".csv", index_col=0)
x_df = x_df.drop(columns=['glucose', 'exp.hour', 'ee', 'probe.id', 'Date.Time', 'photoperiod'])
y_df = pd.read_csv("../../Data/chow_training_data_" + pp + ".csv", usecols=['glucose'])

print(x_df.head())
print(y_df.head())

x_scaler = MinMaxScaler()
y_scaler = MinMaxScaler()
scaled_x_np = x_scaler.fit_transform(x_df.values)
scaled_y_np = y_scaler.fit_transform(y_df.values)

scaled_x_df = pd.DataFrame(scaled_x_np, index=x_df.index, columns=x_df.columns)
scaled_y_df = pd.DataFrame(scaled_y_np, index=y_df.index, columns=y_df.columns)

print(scaled_x_df.head())
print(scaled_y_df.head())

x_train, x_rem, y_train, y_rem = train_test_split(scaled_x_df, scaled_y_df, train_size=0.8, random_state=42)

x_valid, x_test, y_valid, y_test = train_test_split(x_rem, y_rem, test_size=0.5, random_state=42)

#
# set up model
#
inputs = tf.keras.Input(shape=(13))
x = layers.Dense(7, activation='relu')(inputs)
outputs = layers.Dense(1, activation="sigmoid")(x)
model = tf.keras.Model(inputs=inputs, outputs=outputs)
optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=optimizer,
              loss='mae', metrics=[metrics.MeanSquaredError()])
history = model.fit(x_train, y_train, batch_size=32, epochs=100, verbose=1,
                    validation_data=(x_valid, y_valid))

#
# Predict and evaluate
#
y_pred = model.predict(x_test)
y_pred_inverse = y_scaler.inverse_transform(y_pred)
y_test_inverse = y_scaler.inverse_transform(y_test)
print(y_pred_inverse)
print(y_test_inverse)

print(r2_score(y_test_inverse, y_pred_inverse))
print(mean_squared_error(y_test_inverse, y_pred_inverse))
pred_df = pd.DataFrame({"Test": list(y_test_inverse[:,0]), "Hat": list(y_pred_inverse[:,0])})
pred_df.to_csv(pp+"/PredictionsComparison_"+pp+".csv", index=False)

#
# save model
#
model.save(pp+"/chow_model_"+pp+".h5")
