import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import urllib.request 
import json

def coordinates_to_address(data, url):
    for lat, long in enumerate(zip(data["latitude"], data["longitude"]), start=1):
        print(str(lat) + str(long))
        url = "&lon=" + str(long) + "&lat=" + lat
        webUrl = urllib.request.urlopen(url)
        #print ("result code: " + str(webUrl.getcode()) + "\n")
        if (webUrl.getcode() == 200):
            data = webUrl.read()
            theJSON = json.loads(data)
            df = pd.DataFrame(theJSON["display_name"])
            print(df)
        else:
            print ("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))
    

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
    print(df[["mag","Magnitude-binned"]].head())
    print(df["Magnitude-binned"].value_counts())
    plt.bar(group_names,height=df["Magnitude-binned"].value_counts(sort=False))
    plt.show()
    # plt.bar(group_names, df["Magnitude-binned"].value_counts())

    # # set x/y labels and plot title
    # plt.xlabel("Magnitude")
    # plt.ylabel("count")
    # plt.title("Magnitude bins")
    # plt.show()


if __name__== "__main__":
    main()
# print(df.head().columns)

# set x/y labels and plot title
# plt.pyplot.xlabel("Magnitude")
# plt.pyplot.ylabel("count")
# plt.pyplot.title("Magnitude bins")

# print(bins)

# x=df["mag"]
# y=df["place"].rsplit(",",1)
# plt.pyplot.scatter(x,y)
# plt.pyplot.title("Scatter Plot - Magnitude vs Country")
# plt.pyplot.xlabel("Magnitude")
# plt.pyplot.ylabel("Country")
# plt.pyplot.show()
