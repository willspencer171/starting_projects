import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from typing import Any
from os import path
from os import listdir
import re

PATH_TO_FILE = r"C:\Users\wills\Documents\Me\Self-Organisation\Money Stuff\Ins and Outs.xlsx"

january = pd.read_excel(PATH_TO_FILE, "January")
february = pd.read_excel(PATH_TO_FILE, "February")

def getMaxFileNo(path, filename):
    directory = listdir(path)
    max = 0
    for file in directory:
        count = 0
        if filename in file:
            count = re.search(r"\d+", file).group()
        if count and int(count) >= max:
            max = int(count)
    return max

def plotStem(data: pd.DataFrame, subplot: tuple[Figure, Any], x_axis: str, y_axis: str, exp_root=1, output_path="default"):

    if output_path == "default":
        output_path = path.relpath("data/graphs/")
    else:
        output_path = path.relpath(output_path)

    labeldict = {"Date": "Date",
                 "Time": "Time",
                 "Datetime": "Date",
                 "Account": "Account",
                 "Expenditure": "Expenditure",
                 "Amount Out": "Expenditure / £$^{\\frac{1}{" + str(exp_root) + "}}$",
                 "Amount In": "Expenditure / £$^{\\frac{1}{" + str(exp_root) + "}}$",
                 "Total": "Expenditure / £$^{\\frac{1}{" + str(exp_root) + "}}$",
                 "W/N/S/U": "Transaction Group",
                 "Category1": "Category 1",
                 "Category2": "Category 2",
                 "Balance": "Balance / £",
                 "For": "Transaction Profiteer"}

    if not x_axis in data.columns:
        raise Exception(x_axis + " not a valid column name")
    elif not y_axis in data.columns:
        raise Exception(y_axis + " not a valid column name")

    subplot[0].set_figwidth(20)

    def nonlinear_transform(y, root: int | float):
        return np.sign(y) * pow(np.abs(y), 1/root)

    subplot[1].stem(data[x_axis], data[y_axis].apply(nonlinear_transform, args=(exp_root,)))
    plt.ylabel(labeldict[y_axis], fontdict={"size": 18})
    plt.xlabel(labeldict[x_axis], fontdict={"size": 18})
    subplot[1].set_title(f"{x_axis} vs {y_axis}")

    filename = f"{x_axis}_vs_{y_axis}"

    max = getMaxFileNo(output_path, filename)

    filename = filename + f"_{max + 1}_stem"

    subplot[0].savefig(f"{output_path}/{filename}.png")

    return subplot

def plotPie(data: pd.DataFrame, subplot: tuple[Figure, Any], series_name: str, output_path="default", agg_func="count", **kwargs):
    """Takes categorical data and creates a pie chart based on a given aggregation function"""
    if output_path == "default":
        output_path = path.relpath("data/graphs/")
    else:
        output_path = path.relpath(output_path)
    
    if series_name not in data.columns:
        raise Exception(series_name + " not a valid column name")
    
    series = data[series_name] if "dropna" not in kwargs.keys() or kwargs["dropna"] != True else data[series_name].dropna()

    ### Determine aggregate function
    if agg_func == "counts":
        aggregated = (series.value_counts() if 
                      "dropna" not in kwargs.keys()
                      else series.value_counts(dropna=kwargs["dropna"]))
    elif agg_func == "sum":
        if "field" not in kwargs.keys():
            raise Exception("Aggregation function 'sum' must have secondary numerical field\nTry passing field=<column name>")
        aggregated = (data.groupby(series_name)[kwargs["field"]].sum().apply(lambda x: abs(x)) if
                      "dropna" not in kwargs.keys()
                      else data.groupby(series_name, dropna=kwargs["dropna"])[kwargs["field"]].sum()
                      .apply(lambda x: abs(x)))
    
    elif agg_func == "average":
        if "field" not in kwargs.keys():
            raise Exception("Aggregation function 'average' must have secondary numerical field\nTry passing field=<column name>")
        aggregated = data.groupby(series_name, dropna=True)[kwargs["field"]].mean().apply(lambda x: abs(x))
    else:
        raise Exception("Aggregate function not recognised: " + agg_func)

    aggregated = aggregated[aggregated > 0].sort_values(ascending=False).head(8)


    ### Pieing
    wedges, texts, autotexts = subplot[1].pie(aggregated.dropna(),
        colors=plt.get_cmap("Blues")(np.linspace(1, 0.4, len(aggregated))),
        radius=1.5, center=(3,4),
        wedgeprops={"width": 1, "linewidth": 1, "edgecolor": "white"},
        startangle=90,
        textprops=dict(color="w"),
        autopct= lambda pct: f"{pct:.1f}%")

    subplot[1].legend(wedges, aggregated.keys(),
              title="Groups",
              loc="center left",
              bbox_to_anchor=(-1, 0.5, 0.5, 0.5))
    
    plt.setp(autotexts, size=8, weight="bold")

    
    ### Naming and saving
    format_series_name = series_name.replace("/", "_")

    if "field" in kwargs.keys():
        format_series_name += f"_{kwargs['field']}"

    format_series_name += "_" + agg_func

    subplot[1].set_title(format_series_name.replace("_", " "))

    max = getMaxFileNo(output_path, format_series_name)

    format_series_name = format_series_name + f"_{max + 1}"

    subplot[0].savefig(f"{output_path}/{format_series_name}_pie.png")

    return subplot

plotPie(january, 
        plt.subplots(figsize=(6, 3),
                    layout="constrained", 
                    subplot_kw=dict(aspect="equal")), 
        "Time", 
        agg_func="average", field="AmountOut")
