import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

## wrriten by Guy Almog & Daniel Nachshoni 08/2022

# האם קיימת השפעה של גובה שחקני כדורסל על עמדותיהם במשחק כדורסל
# The question: Does height of basketball players impact their positions in Basketball game?
#האם שחקנים נמוכים יקלעו הרבה [שלא מעונשין]




def top_12(data, top_12_cols):

    X = sm.add_constant(data.loc[:, top_12_cols])  # adding the feature vectors
    Y = data.height  # target
    fit = sm.OLS(Y, X).fit()
    print(fit.summary())

    p = fit.params




def show_regline(x,y):


    # print(name12List[i])
    # print(y)



    plt.plot(x, y, 'o')
    idx = np.isfinite(x) & np.isfinite(y)
    a, b = np.polyfit(x[idx], y[idx], 1)

    plt.plot(x, a * x + b)


    plt.show()

    return


def prepare_df(season_stats_df):
    # ~~~~~~~~~~~~~ clean DF ~~~~~~~~~~~~~~ #

    season_stats_df = season_stats_df.drop(['blanl', 'blank2', 'Age', 'Year', 'Unnamed: 0', 'TOV', 'Player', 'Pos', 'Tm', 'GS','2P','FG','3PAr'], axis=1)
    season_stats_df = season_stats_df[season_stats_df['height'].notna()]
    season_stats_df = season_stats_df.fillna(0)
    season_stats_df = season_stats_df.rename(index={0: 'SavedIndex'})
    season_stats_df.to_csv("FINAL1.csv")
    season_stats_df.index.name = 'saved index' # in case needed to compare vs original table




    return season_stats_df

def simple_linear(data,str):

    # Height vs all other features correlatons
    indexes = list(data.columns)
    indexes.remove("height")
    pearson_data = {col: np.abs(pearsonr(data[col], data["height"])[0]) for col in indexes}
    pearson = pd.Series(data=pearson_data, index=indexes)
    pearson.sort_values(ascending=False, inplace=True)

    # plot correlations graph
    pearson.plot(kind='bar')
    plt.title("Correlation values (abs) with 'height'" + str)
    plt.show()

    # plotting reg lines
    top_12_cols = list(pearson.head(12).index)
    for i in range(12):
        plt.subplot(4, 3, i + 1)
        x, y = data[top_12_cols[i]].to_numpy(), data["height"]
        x = np.reshape(x, (x.shape[0], 1))
        print(x.shape)
        print(y.shape)
        print(y)

        plt.scatter(x, y, s=3)
        reg = LinearRegression().fit(x, y)
        y_pred = reg.predict(x)
        plt.plot(x, y_pred, 'black')
        r = pearson.head(12)[top_12_cols[i]]
        if reg.coef_ < 0:
            r *= -1
        plt.title("%s, %.3f" % (top_12_cols[i], r))
    plt.tight_layout()
    plt.suptitle("Top 12 correlation with 'height'" + str)
    plt.show()
    print("plotting...")
    return top_12_cols # returns 12 highest correlated features list


# ##################### organizing data ####################### #

players_data_df = pd.read_csv("player_data.csv")
players_df = pd.read_csv("Players.csv")
season_stats_df = pd.read_csv("Seasons_Stats.csv")
season_stats_df_copy = season_stats_df.copy()


# merging
# print(season_stats_df)
players_df = players_df[['Player', 'height', 'weight']]
height = players_df["height"]

season_stats_df["height"] = height



# #  generating DF for each position
#
sg_pos = season_stats_df.loc[season_stats_df["Pos"] == "SG"]
sg_pos = prepare_df(sg_pos)
sf_pos = season_stats_df.loc[season_stats_df["Pos"] == "SF"]
sf_pos = prepare_df(sf_pos)
pg_pos = season_stats_df.loc[season_stats_df["Pos"] == "PG"]
pg_pos = prepare_df(pg_pos)
pf_pos = season_stats_df.loc[season_stats_df["Pos"] == "PF"]
pf_pos = prepare_df(pf_pos)
center_pos = season_stats_df.loc[season_stats_df["Pos"] == "C"]
center_pos = prepare_df(center_pos)

print(sg_pos.shape)
print(sf_pos.shape)
print(pg_pos.shape)
print(pf_pos.shape)
print(center_pos.shape)

## getting most corelated cols with height for each position and ploting regression lines

# DO THIS OF EACH POS
SG_heightCorrs = simple_linear(sg_pos, " for SG position")# ploting 2 graphs, most correlated features and theyre regressions with height.
top_12(sg_pos, SG_heightCorrs) # prints summary of multy regression model of 12 most correlated features with height
                                # summary shows which features impacts the most on height prediction,
                                # therefore explains which features are most corelated with height of player




SF_heightCorrs = simple_linear(sf_pos, " for SF position")
top_12(sf_pos, SF_heightCorrs) # prints summary of multy regression of 12 most correlated features with height

PG_heightCorrs = simple_linear(pg_pos, " for PG position")
top_12(pg_pos, PG_heightCorrs) # prints summary of multy regression of 12 most correlated features with height

PF_heightCorrs = simple_linear(pf_pos, " for PF position")
top_12(pf_pos, PF_heightCorrs) # prints summary of multy regression of 12 most correlated features with height

C_heightCorrs = simple_linear(center_pos, " for Center position")
top_12(center_pos, C_heightCorrs) # prints summary of multy regression of 12 most correlated features with height

print("TOP Features Correlated to Height of player for SG position")
print(SG_heightCorrs)

print("TOP Features Correlated to Height of player for SF position")
print(SF_heightCorrs)
print("TOP Features Correlated to Height of player for PG position")
print(PG_heightCorrs)
print("TOP Features Correlated to Height of player for PF position")
print(PF_heightCorrs)
print("TOP Features Correlated to Height of player for Center position")
print(C_heightCorrs)




