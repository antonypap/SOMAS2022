import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys, getopt

def main(filename, modelName):
    # import the data files
    data = pd.read_csv(filename)

    # extract the data
    selfish = data.iloc[:,[0]].to_numpy()
    selfless = data.iloc[:,[1]].to_numpy()
    collective = data.iloc[:,[2]].to_numpy()
    output = data.iloc[:,[3]].to_numpy()

    # create figure
    fig = plt.figure(figsize = (7.5,6))
    ax = fig.add_subplot(111, projection='3d')

    img = ax.scatter(selfish, selfless, collective, c=output, cmap='YlOrRd', alpha=1)
    ax.set_xlabel("Selfish")
    ax.set_ylabel("Selfless")
    ax.set_zlabel("Collective")
    fig.colorbar(img, shrink=0.5, pad=0.05, orientation = "horizontal")
    ax.view_init(-161,53)
    plt.title("Game Progress Using Prediction Model"+modelName+" Based On Population Constrution")
    plt.show()

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], ":f")
    filename=args[0]
    title_name=args[1]
    main(filename, title_name)
