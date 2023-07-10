import pandas as pd

df = pd.read_csv("../../Data/one_animal_training_data_all.csv", index_col=False)

day_df = df[df["photoperiod"] == 1]
night_df = df[df["photoperiod"] == 0]

day_df.to_csv("../../Data/one_animal_training_data_day.csv", index=False)
night_df.to_csv("../../Data/one_animal_training_data_night.csv", index=False)