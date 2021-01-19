import numpy as np
import pandas as pd


def preprocess():
    fname = './barcrawl/barcrawl_raw.csv'
    wfname = './barcrawl/barcrawl_preprocessed.txt'
    with open(fname) as infile, open(wfname, 'w') as outfile:
        df = pd.read_csv(infile, header=None, delimiter=',', skiprows=1)
        # sort based on the timestamp.
        df = df.sort_values(df.columns[0], ascending=True)
        print("Sorting done.")
        print(df.shape[0])

        # drop second column.
        df = df.drop(columns=[1])
        # add weight 1 as second column.
        res = np.insert(df.values, 1, 1, axis=1)
        print("Add weight complete.")

        # write to file.
        for row in res:
            format_row = str(row[0])
            for i in range(1, len(row)):
                format_row += "," + str(row[i])
            outfile.write(format_row + "\n")
        print("Writing to file done.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    preprocess()
