import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import urllib.request
import json


def main():
    filename = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.csv"
    address_url = "https://nominatim.openstreetmap.org/reverse?format=json"

    df = pd.read_csv(filename, header=0)

    plt.hist(df["mag"])

    # set x/y labels and plot title
    plt.xlabel("Magnitude")
    plt.ylabel("count")
    plt.title("Magnitude bins")
    plt.show()

    bins = np.array([0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0])
    group_names = ['Minor', 'Light', 'Moderate', 'Strong', 'Major', 'Great']
    df['Magnitude-binned'] = pd.cut(df['mag'], bins,labels=group_names, include_lowest=True)
    plt.bar(group_names,height=df["Magnitude-binned"].value_counts(sort=False))
    plt.xlabel("Magnitude")
    plt.ylabel("Count")
    plt.title("Magnitude bins")
    plt.show()


if __name__ == "__main__":
    main()
