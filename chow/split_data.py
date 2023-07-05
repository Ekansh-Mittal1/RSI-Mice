import pandas as pd

df = pd.read_csv("../Data/chow_training_data_all.csv", index_col=False)

day_df = df[df["photoperiod"] == "light"]
night_df = df[df["photoperiod"] == "dark"]

day_df.to_csv("../Data/chow_training_data_day.csv", index=False)
night_df.to_csv("../Data/chow_training_data_night.csv", index=False)