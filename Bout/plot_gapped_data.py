import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../Data/Chow_Bout_filtered_all.csv")
ids = df["probe.id"].unique().tolist()
for id in ids:

    df_m = df[df["probe.id"] == id]

    sns.lineplot(data=df_m, x="exp.minute", y="feed")
    plt.savefig("graphs/"+id+"_threshold_feed.png")
    #plt.show()
    plt.clf()
    sns.lineplot(data=df_m, x="exp.minute", y="glucose")
    plt.savefig("graphs/"+id+"_threshold_glucose.png")
    #plt.show()
    plt.clf()

#df_2 = pd.read_csv("../Data/Chow_Bout_filtered_all.csv")
#df_2 = df_2[df_2["probe.id"] == "CGM_001"]
#sns.lmplot(data=df_2, x="feed", y="glucose")
#plt.show()