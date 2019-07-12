import urllib.request, json
from urllib.request import Request, urlopen
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot
import warnings

def get_area(data):
    earthquake_data = json.loads(data)
    df = pd.DataFrame(earthquake_data["features"])
    for data in earthquake_data["features"]:
      place = data["properties"]["place"].split(",")
      place = place[-1]
  
def main():
  with open('earthquakes_2019_worldwide.json') as json_file:  
    data = json.load(json_file)
    df = pd.DataFrame(data["features"])
    df["Area"] = df["properties"].apply(lambda x: x.get("place").split(",")[-1])
    bins = np.array([0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0])
    group_names = ['Minor', 'Light', 'Moderate', 'Strong', 'Major', 'Great']
    df['Magnitude-binned'] = pd.cut(df["properties"]["mag"], bins,labels=group_names, include_lowest=True)

    place = data["properties"]["place"].split(",")
    print(df.columns)
#     plt.bar(group_names,height=df["Magnitude-binned"].value_counts(sort=False).head(20))
#     plt.xlabel("Magnitude")
#     plt.ylabel("Count")
#     plt.title("Magnitude bins")
#     plt.show()

if __name__ == "__main__":
  main()
