from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import glob
import os


def merge_file():
    root = './WISDM'
    filenames = []
    for path, _, files in os.walk(root):
        for name in files:
            filenames.append(os.path.join(path, name))

    cnt = 0
    with open('./WISDM/merged_file.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    cnt += 1
                    line = line.replace(';', '')
                    outfile.write(line)
    print("cnt", cnt)


def preprocess():
    scaler = MinMaxScaler(feature_range=(0, 100000))
    fname = './WISDM/merged_file.txt'
    wfname = './WISDM/wisdm_preprocessed.txt'
    with open(fname) as infile, open(wfname, 'w') as outfile:
        df = pd.read_csv(infile, header=None, delimiter=',')
        # sort based on the timestamp.
        df = df.sort_values(df.columns[2], ascending=True)
        print("Sorting done.")

        # get timestamp column and drop first 3 columns.
        time = df.iloc[:, 2].values
        df = df.drop(columns=[0, 1, 2])

        # normalize to [0, 1e5].
        df = scaler.fit_transform(df)
        df = df.astype(int)
        print("Normalization done.")

        # add time as first column.
        data_cols = np.array(df, dtype=float)
        res = np.insert(data_cols, 0, time, axis=1)
        # add weight 1 as second column.
        res = np.insert(res, 1, 1, axis=1)
        # write to file.
        for row in res:
            format_row = str(row[0])
            for i in range(1, len(row)):
                format_row += "," + str(int(row[i]))
            outfile.write(format_row + "\n")
        print("Writing to file done.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    merge_file()
    preprocess()
