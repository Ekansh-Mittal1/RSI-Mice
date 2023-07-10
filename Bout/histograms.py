import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../Data/chow_training_data_all.csv")

ids = df["probe.id"].unique().tolist()
for id in ids:
    df_m = df[df["probe.id"] == id]

    sns.histplot(data=df_m, x="feed", bins=30)
    plt.savefig("graphs/" + id + "_histogram_feed.png")
    plt.clf()
    # plt.show()

    sns.histplot(data=df_m, x="glucose")
    plt.savefig("graphs/" + id + "_histogram_glucose.png")
    # plt.show()
    plt.clf()
