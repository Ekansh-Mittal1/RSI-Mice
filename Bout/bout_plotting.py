import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from functions import *

full_data = pd.read_csv("../Data/chow_training_data_all.csv")
thresh = 0.03
overlays = ["none", "average", "other_days"]
o = overlays[1]

ids = full_data["probe.id"].unique().tolist()
ids = ["CGM_001"]
full_data["eating.bool"] = np.where(full_data['feed'] > thresh, True, False)
buffer = 20

# full_data.to_csv("full_data_test.csv")

start_end_all = {}

for id in ids:
    boutmins = full_data[(full_data["probe.id"] == id)]["exp.minute"].tolist()
    boutbool = full_data[(full_data["probe.id"] == id)]["eating.bool"].tolist()
    start_end_mouse = []
    prev = False
    for i in range(len(boutmins)):
        if not prev and boutbool[i] == 1:
            start = boutmins[i]
            prev = True
        if prev and boutbool[i] == 0:
            end = boutmins[i]
            prev = False
            center = int((start + end) / 2)
            bout = [center - buffer, start, end, center + buffer + 1]
            start_end_mouse.append(bout)

    start_end_all[id] = start_end_mouse

for id in ids:
    for bout in start_end_all[id]:
        if o == "other_days":
            plot_other_days(full_data, bout, id, True, True)
        elif o == "none":
            plot_bout(full_data, bout, id, True, True)
        elif o == "average":
            plot_average(full_data, bout, id)
