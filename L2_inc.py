import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

plt.style.use('_mpl-gallery')

incidents = pd.read_csv("incident.csv", encoding="utf-8", encoding_errors='ignore')
incidents.ndim

incidents["opened_at"] = pd.to_datetime(incidents["opened_at"]).dt.date
incidents.set_index("opened_at", inplace=True)

incidents.head()
print('')
incidents.tail()

incidents["u_cause_code"].copy().fillna("Not Applicable", inplace=True)
incidents["u_cause_source"].copy().fillna("Not Applicable", inplace=True)
incidents["description"].copy().fillna("No Description", inplace=True)
incidents.drop("calendar_stc", axis=1, inplace=True)

# Reporter names
incidents["caller_id"].unique()

# Sorted incident raised by reporter
print(incidents["caller_id"].value_counts())

#Sorted data per year
for year in incidents.index.year.unique():
    print('')
    print(year)
    print(incidents[incidents.index.year==year]["caller_id"].value_counts()[:10])


# helper function to plot horizontal bars
def plot_hbars(col_name, color):
    """
    Plots horizontal bars for categorical columns.
    """
    fig, ax = plt.subplots(2, 3, figsize=(15, 5))

    years = [2020, 2021, 2022, 2023, 2024, 2025]
    
    index=0
    for row in range(2):
        for col in range(3):
            incidents[incidents.index.year==years[index]][f"{col_name}"].value_counts(ascending=False)[:10].plot(kind='barh', ax=ax[row,col],
                                                                                                                 ylabel='', alpha=0.8, color=color)
            #ax[row,col].set_xlabel('')
            ax[row,col].set_title(years[index], size=10)
            index += 1
    
        sns.despine()
    plt.tight_layout()
    plt.show()


plot_hbars("caller_id", "orange")
plot_hbars("priority", "orange")


def plot_pie_charts(colname):
    """
    Plots pie charts for each year on specified columns.
    """
    fig, ax = plt.subplots(3, 2, figsize=(10, 10), subplot_kw=dict(aspect='equal'))
    index = 0
    
    for row in range(3):
        for col in range(2):
            wedges, text, pct = ax[row, col].pie(incidents[incidents.index.year==years[index]][f"{colname}"].value_counts()[:5],
                                                        autopct="%.1f%%",
                                                        wedgeprops=dict(width=0.5),
                                                        startangle=0,
                                                        pctdistance=0.8,
                                                        colors=sns.set_palette('tab10', len(incidents[incidents.index.year==years[index]][f"{colname}"].value_counts()[:5])),
                                                        textprops=dict(color='w', fontfamily='sans-serif', fontsize=8, fontweight='bold'))
            
            bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.5)
            kw = dict(arrowprops=dict(arrowstyle="-"),
                              bbox=bbox_props, zorder=0, va="center")

            for i, p in enumerate(wedges):
                ang = (p.theta2 - p.theta1)/2. + p.theta1
                if np.isclose(ang % 90, 0):
                    ang += 1e-4  # A very small angle in degrees

                y = np.sin(np.deg2rad(ang))
                x = np.cos(np.deg2rad(ang))
                hor_align = {-1: "right", 1: "left"}[int(np.sign(x))]
                conn_style = "angle, angleA=0, angleB={}".format(ang)
                kw["arrowprops"].update({"connectionstyle": conn_style})
                ax[row,col].annotate(incidents[incidents.index.year==years[index]][f"{colname}"].value_counts()[:5].index[i],
                                                xy=(x, y),
                                                xytext=(1.35 * np.sign(x), 1.3 * y),
                                                horizontalalignment=hor_align,
                                                fontfamily='sans-serif',
                                                fontsize=10, **kw)
            index += 1

    plt.show()
