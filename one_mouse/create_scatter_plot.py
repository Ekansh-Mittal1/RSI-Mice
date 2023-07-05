import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

pp_l = ["day", "night", "all"]
pp = pp_l[2]

pred_df = pd.read_csv(pp+"/PredictionsComparison_"+pp+".csv")
sns.lmplot(data=pred_df, x="Test", y="Hat")
plt.show()
plt.savefig(pp+"/PredictionsScatter_"+pp+".png")