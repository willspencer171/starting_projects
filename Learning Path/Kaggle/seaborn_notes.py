### Line charts
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

pd.set_option("display.max_rows", 12)

spot_data = pd.read_csv('Kaggle/data/spotify.csv', 
                        index_col='Date', 
                        parse_dates=True, 
                        engine="pyarrow") # faster than using the standard C engine
# The above is true because it delegates to spare cores for processing.
# Doesn't produce a change if you're already using all cores manually
# CSVs are slow af, apparently parquets are faster?

spot_data.index = pd.to_datetime(spot_data.index)
spot_data.style.format_index(lambda t: t.strftime('%d/%m/%Y'))

"""Seaborn is a nice, very simple way of plotting things onto pyplot figures

It does give you less control over the presentation of things, but it's a beginner-friendly
package to use in lieu of pyplot"""

def line():
    plt.figure(figsize=(14,6))

    print(spot_data.head())
    print(spot_data.tail())

    # These lines will add lineplots to the same figure, rather than create two figures
    sns.lineplot(data=spot_data['Shape of You'], label='Shape of You Streams')
    sns.lineplot(data=spot_data['Unforgettable'], label='Unforgettable Streams')

    plt.title("Spotify Streams 2017 - 2018")

    plt.show()

# Bar charts and heatmaps

def bar():
    plt.figure(figsize=(14,6))

    # Bar plots will aggregate the data in each column by averaging it
    # if you don't specify the x and y aesthetics. The below shows bars
    # of the averages of each song:

    sns.barplot(spot_data)

    plt.show()

    plt.figure(figsize=(14,6))

    # These two bars show a bar for each value at each date
    # this is the same as saying barplot(x=spot_data.index, y=spot_data[<song_name>])
    sns.barplot(spot_data['Shape of You'])
    sns.barplot(spot_data['Unforgettable'])
    # Slow, as each bar is actually a large patch to add

    plt.show()

    """
    I'm going to show a good way of grouping dates into months
    It's also worth looking into Groupers at some point to back this up
    """

    monthly_grouping = spot_data.groupby(pd.Grouper(freq='MS')).mean() # Groups the index by Month Start, then average the data in that group
    print(monthly_grouping)

    # Gonna get some more data up in this biyatch

    airline_data = pd.read_csv("Kaggle/data/flight_delays.csv", index_col='Month')

    # Heatmaps

    plt.figure(figsize=(14,6))

    # Simply put, this shows the average delay from different airlines as a heatmap
    # We could do this with others tbf let's have a quick look
    hm = sns.heatmap(monthly_grouping)
    # Oof not with the spotify raw data that sucked, but if I group by month that's not so bad
    ylabs = [date.strftime("%B %Y") if type(date) == pd.Timestamp else date for date in monthly_grouping.index]
    hm.set_yticks(range(len(ylabs)), ylabs)

    plt.show()

# Scatter Plots

def scatter():
    """Here's some cool stuff that we can create scatter
plots with including regression lines"""

    insurance_data = pd.read_csv("Kaggle/data/insurance.csv", engine="pyarrow")
    print(insurance_data)

    plt.figure(figsize=(14,6))

    sns.scatterplot(x=insurance_data['bmi'], y=insurance_data['charges'])

    plt.show()

    plt.figure(figsize=(14,6))

    # with linear regression
    sns.regplot(x=insurance_data['bmi'], y=insurance_data['charges'])

    plt.show()

    plt.figure(figsize=(14,6))

    sns.scatterplot(data=insurance_data, x='bmi', y='charges', hue='smoker')

    plt.show()

    plt.figure(figsize=(14,6))

    sns.lmplot(data=insurance_data, x='bmi', y='charges', hue='smoker')

    plt.show()

    plt.figure(figsize=(14,6))

    sns.swarmplot(data=insurance_data, x="smoker", y='bmi')

    plt.show()

def distributions():
    pass
