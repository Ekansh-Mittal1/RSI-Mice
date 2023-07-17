import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_bout(full_df, bout, id, show, save, bout_num):

    bout_df = full_df[(full_df["exp.minute"].isin(range(bout[0], bout[3])) & (full_df["probe.id"] == id))]

    mins = bout_df[bout_df["exp.minute"].isin(range(bout[1], bout[2]))]["exp.minute"]
    gl = bout_df[bout_df["exp.minute"].isin(range(bout[1], bout[2]))]["glucose"]
    f = bout_df[bout_df["exp.minute"].isin(range(bout[1], bout[2]))]["feed"]

    sns.lineplot(data=bout_df, x="exp.minute", y="glucose", linestyle="--")
    plt.plot(mins, gl, linestyle="-")

    if save:
        plt.savefig(f"graphs/{id}/bout_{bout_num}_glucose_none.png")
        plt.clf()
    if show:
        plt.show()

    sns.lineplot(data=bout_df, x="exp.minute", y="feed", linestyle="--")
    plt.plot(mins, f, linestyle="-")

    if save:
        plt.savefig(f"graphs/{id}/bout_{bout_num}_feed_none.png")
        plt.clf()
    if show:
        plt.show()

def plot_other_days(full_df, bout, id, show, save, bout_num):
    bout_day = bout[1] // 1440
    mouse_df = full_df[full_df["probe.id"] == id]
    mouse_df["minute"] = mouse_df["exp.minute"] % 1440

    # process glucose data
    pivoted_df_gl = mouse_df.pivot_table(index=["minute"], columns=["exp.day"], values=["glucose"])
    pivoted_df_gl.columns = [f"{col[0]}_{col[1]}" for col in pivoted_df_gl.columns]
    pivoted_df_gl.drop(columns=["glucose_5"], inplace=True)
    bout_df_gl = pivoted_df_gl.iloc[bout[0] % 1440:bout[3] % 1440]
    bout_df_gl.reset_index(inplace=True)

    # process feed data
    pivoted_df_f = mouse_df.pivot_table(index=["minute"], columns=["exp.day"], values=["feed"])
    pivoted_df_f.columns = [f"{col[0]}_{col[1]}" for col in pivoted_df_f.columns]
    pivoted_df_f.drop(columns=["feed_5"], inplace=True)
    bout_df_f = pivoted_df_f.iloc[bout[0] % 1440:bout[3] % 1440]
    bout_df_f.reset_index(inplace=True)

    # get bout data
    mins = pivoted_df_gl.loc[range(bout[1] % 1440, bout[2] % 1440)].index
    gl = pivoted_df_gl.loc[range(bout[1] % 1440, bout[2] % 1440)]["glucose_" + str(bout_day)]
    f = pivoted_df_f.loc[range(bout[1] % 1440, bout[2] % 1440)]["feed_" + str(bout_day)]

    # plot glucose data
    sns.lineplot(x="minute", y="value", hue="variable", data=pd.melt(bout_df_gl, ["minute"]), linestyle="--")
    plt.plot(mins, gl, linestyle="-")

    if save:
        plt.savefig(f"graphs/{id}/bout_{bout_num}_glucose_other_days.png")
        plt.clf()
    if show:
        plt.show()

    # plot feed data
    sns.lineplot(x="minute", y="value", hue="variable", data=pd.melt(bout_df_f, ["minute"]), linestyle="--")
    plt.plot(mins, f, linestyle="-")

    if save:
        plt.savefig(f"graphs/{id}/bout_{bout_num}_feed_other_days.png")
        plt.clf()
    if show:
        plt.show()

def plot_average(full_df, bout, id, show, save, bout_num):

    days = [0, 1, 2, 3, 4]
    bout_day = bout[1] // 1440
    days.remove(bout_day)
    days_gl = ["glucose_" + str(d) for d in days]
    days_f = ["feed_" + str(d) for d in days]

    mouse_df = full_df[full_df["probe.id"] == id]
    mouse_df["minute"] = mouse_df["exp.minute"] % 1440

    # process glucose data
    pivoted_df_gl = mouse_df.pivot_table(index=["minute"], columns=["exp.day"], values=["glucose"])
    pivoted_df_gl.columns = [f"{col[0]}_{col[1]}" for col in pivoted_df_gl.columns]
    pivoted_df_gl.drop(columns=["glucose_5"], inplace=True)
    bout_df_gl = pivoted_df_gl.iloc[bout[0] % 1440:bout[3] % 1440]
    bout_df_gl['average'] = bout_df_gl[days_gl].mean(axis=1)
    bout_df_gl.drop(days_gl, axis=1, inplace=True)
    bout_df_gl.reset_index(inplace=True)

    # process feed data
    pivoted_df_f = mouse_df.pivot_table(index=["minute"], columns=["exp.day"], values=["feed"])
    pivoted_df_f.columns = [f"{col[0]}_{col[1]}" for col in pivoted_df_f.columns]
    pivoted_df_f.drop(columns=["feed_5"], inplace=True)
    bout_df_f = pivoted_df_f.iloc[bout[0] % 1440:bout[3] % 1440]
    bout_df_f['average'] = bout_df_f[days_f].mean(axis=1)
    bout_df_f.drop(days_f, axis=1, inplace=True)
    bout_df_f.reset_index(inplace=True)

    # get bout data
    mins = pivoted_df_gl.loc[range(bout[1] % 1440, bout[2] % 1440)].index
    gl = pivoted_df_gl.loc[range(bout[1] % 1440, bout[2] % 1440)]["glucose_" + str(bout_day)]
    f = pivoted_df_f.loc[range(bout[1] % 1440, bout[2] % 1440)]["feed_" + str(bout_day)]

    # plot glucose data
    sns.lineplot(x="minute", y="value", hue="variable", data=pd.melt(bout_df_gl, ["minute"]), linestyle="--")
    plt.plot(mins, gl, linestyle="-")

    if save:
        plt.savefig(f"graphs/{id}/bout_{bout_num}_glucose_average.png")
        plt.clf()
    if show:
        plt.show()

    # plot feed data
    sns.lineplot(x="minute", y="value", hue="variable", data=pd.melt(bout_df_f, ["minute"]), linestyle="--")
    plt.plot(mins, f, linestyle="-")
    if save:
        plt.savefig(f"graphs/{id}/bout_{bout_num}_feed_average.png")
        plt.clf()
    if show:
        plt.show()



def plot_other_mice(full_df, bout, id, show, save, bout_num):
    pivoted_all_mice_gl = full_df.pivot_table(index="exp.minute", columns="probe.id", values="glucose")
    bout_df_gl = pivoted_all_mice_gl.iloc[bout[0]: bout[3]]
    bout_df_gl.reset_index(inplace=True)

    mins = pivoted_all_mice_gl.loc[range(bout[1], bout[2])].index
    gl = pivoted_all_mice_gl.loc[range(bout[1], bout[2])][id]

    sns.lineplot(x="exp.minute", y="value", hue="variable", data=pd.melt(bout_df_gl, ["exp.minute"]), linestyle="--")
    plt.plot(mins, gl, linestyle="-")

    #pivoted_all_mice_gl = full_df.pivot_table(index="exp.minute", columns="probe.id", values="glucose")
