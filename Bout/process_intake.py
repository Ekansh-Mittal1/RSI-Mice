import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

intake = pd.read_csv("../Data/full_food_intake.csv")
chow = pd.read_csv("../Data/chow_training_data_all.csv")

ids = chow["probe.id"].unique().tolist()

intake["StartDateTime"] = pd.to_datetime(intake["StartDate"] + ' ' + intake["StartTime"], format='%m/%d/%Y %H:%M:%S').dt.round("min")
intake["EndDateTime"] = pd.to_datetime(intake["EndDate"] + ' ' + intake["EndTime"], format='%m/%d/%Y %H:%M:%S').dt.round("min")

intake = intake[intake["Probe"].isin(ids)]
intake = intake[((intake["StartDateTime"] >= "2022-07-01 06:00:00") & (intake["EndDateTime"] <= "2022-07-06 06:00:00")
                & (intake["Cohort"] == 1)) | ((intake["StartDateTime"] >= "2022-07-08 06:00:00")
                & (intake["EndDateTime"] <= "2022-07-13 06:00:00") & (intake["Cohort"] == 2))]

chow["Date.Time"] = pd.to_datetime(chow["Date.Time"])

start_exp_min_l = []
end_exp_min_l = []

for id in ids:
    intake_id = intake[intake["Probe"] == id]
    for index, row in intake_id.iterrows():
        min_s = chow[(chow["Date.Time"] == row["StartDateTime"]) & (chow["probe.id"] == id)
                     & (chow["cohort"] == row["Cohort"])]["exp.minute"].tolist()
        min_e = chow[(chow["Date.Time"] == row["EndDateTime"]) & (chow["probe.id"] == id)
                     & (chow["cohort"] == row["Cohort"])]["exp.minute"].tolist()

        if len(min_s) == 1:
            start_exp_min_l.append(min_s[0])
        else:
            start_exp_min_l.append(None)
        if len(min_e) == 1:
            end_exp_min_l.append(min_e[0])
        else:
            end_exp_min_l.append(None)

        print(row['StartDateTime'], row['EndDateTime'], min_s, min_e, row["Probe"])

intake["StartExpMinute"] = start_exp_min_l
intake["EndExpMinute"] = end_exp_min_l

intake.to_csv("../Data/full_food_intake_filtered.csv")

