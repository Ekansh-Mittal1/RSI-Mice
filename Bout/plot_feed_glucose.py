import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import cov
from scipy.stats import pearsonr

intake = pd.read_csv("../Data/full_food_intake_filtered.csv")
chow = pd.read_csv("../Data/chow_training_data_all.csv")
buffer = [x for x in range(0, 50, 5)]
thresh = 0.04

intake.dropna(inplace=True)
intake = intake[intake["In_g_min"] > thresh]

# TODO: FILTER BY NIGHT AND DAY

ids = chow["probe.id"].unique().tolist()
#ids = ["CGM_001"]
stats_df = pd.DataFrame(columns=["range_gl", "change", "max_fall", "max_rise", "feed", "lcm"])

correlation = {}

for id in ids:
    for buf in buffer:
        intake_id = intake[intake["Probe"] == id]
        chow_id = chow[chow["probe.id"] == id]
        for index, bout in intake.iterrows():
            s = bout["StartExpMinute"]
            e = bout["EndExpMinute"]

            gl = chow_id[(chow_id["exp.minute"] >= (s+buf)) & (chow_id["exp.minute"] <= (e+buf))]["glucose"].tolist()
            lcm = chow_id[(chow_id["exp.minute"] >= s) & (chow_id["exp.minute"] <= e)]["pedmeter"].mean()
            if len(gl) > 2:
                max_gl = max(gl)
                min_gl = min(gl)
                first = gl[0]
                last = gl[-1]
                range_gl = max_gl - min_gl
                change = last - first
                max_fall = min_gl - first
                max_rise = max_gl - first
                feed = bout["In_g_min"]

                stats_df.loc[len(stats_df.index)] = [range_gl, change, max_fall, max_rise, feed, lcm]

        cols = stats_df.columns.tolist()
        cols.remove("feed")
        cols.remove("lcm")

        cor = [id]

        for col in cols:
            sns.lmplot(data=stats_df, x="feed", y=col, hue="lcm")
            p = pearsonr(stats_df["feed"], stats_df[col])
            cor.append(p[0])
            plt.title(f"{id}/{col}_buffer{buf}_corr{round(p[0], 4)}")
            plt.savefig(f"feed_vs_glucose/{id}/{col}_buffer{buf}.png")
            plt.close()
            print(id, buf, col)
        stats_df.drop(stats_df.index, inplace=True)

        correlation[buf] = cor

        #print(correlation)