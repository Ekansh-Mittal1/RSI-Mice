import pandas as pd
import numpy as np

df = pd.read_csv("..\Data\chow_training_data_all.csv")

ids = df["probe.id"].unique().tolist()
ids = ["CGM_001"]
filter_id_min = []
gaps_id_min = []

for id in ids:
    boutmins = df[(df["feed"] > 0.03) & (df["probe.id"] == id)]["exp.minute"].tolist()
    surroundmins = []
    print(boutmins)
    for i in range(len(boutmins)):
        if boutmins[i] < 5 & boutmins[i] > 7253:
            i += 1
        else:
            surroundmins = surroundmins + [x + boutmins[i] for x in range(-4, 5)]

    final_list = np.unique(np.array(surroundmins)).tolist()
    print(len(final_list))
    filter_id_min.append(df[(df["exp.minute"].isin(final_list)) & (df["probe.id"] == id)])

    gaps = df.copy()
    gaps = gaps[gaps["probe.id"] == id]
    gaps["glucose"] = np.where(gaps["exp.minute"].isin(final_list), gaps["glucose"], 0)
    gaps["feed"] = np.where(gaps["exp.minute"].isin(final_list), gaps["feed"], 0)

#    print(gaps)
    gaps_id_min.append(gaps)


filtered_df = pd.concat(filter_id_min)
filtered_df.to_csv("../Data/Chow_Bout_filtered_all.csv", index=False)

gap_df = pd.concat(gaps_id_min)
gap_df.to_csv("../Data/Chow_Bout_gapped_all.csv", index=False)