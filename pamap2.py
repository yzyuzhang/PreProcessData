from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd


def merge_file():
    """
        Merge all the files in subdirectories of PAMAP2.
    """
    cnt = 0
    filenames_protocol = ['subject101.dat', 'subject102.dat', 'subject103.dat', 'subject104.dat', 'subject105.dat',
                          'subject106.dat', 'subject107.dat', 'subject108.dat', 'subject109.dat']
    filenames_optional = ['subject101.dat', 'subject105.dat', 'subject106.dat', 'subject108.dat', 'subject109.dat']
    filenames = ['PAMAP2/protocol/' + f for f in filenames_protocol] + \
                ['PAMAP2/optional/' + f for f in filenames_optional]
    with open('./PAMAP2/merged_file.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    cnt += 1
                    outfile.write(line)
    print("cnt", cnt)


def preprocess():
    """
        Do the preprocessing including normalization and PCA by myself.
    """
    pca = PCA(n_components=4)
    imp_most = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
    scaler = MinMaxScaler(feature_range=(0, 100000))
    fname = './PAMAP2/merged_file.txt'
    wfname = './PAMAP2/PAMAP2_my_preprocessed.txt'
    with open(fname) as infile, open(wfname, 'w') as outfile:
        df = pd.read_csv(infile, header=None, delimiter=' ')
        # sort based on the timestamp.
        df = df.sort_values(df.columns[0], ascending=True)
        print("Sorting done.")
        # take all the 52 columns and fill in the NaN values.
        t = np.array(df.iloc[:, 0].values)
        x = df.iloc[:, 2:].values
        x = imp_most.fit_transform(x)
        print("Fill missing values done.")
        # PCA.
        p_comp = pca.fit_transform(x)
        print(pca.explained_variance_ratio_)
        print("PCA done.")
        # normalize to [0, 1e5].
        norm = scaler.fit_transform(p_comp)
        norm = norm.astype(int)
        print("Normalization done.")
        # add time as first column.
        data_cols = np.array(norm, dtype=float)
        res = np.insert(data_cols, 0, t, axis=1)
        # add weight 1 as second column.
        res = np.insert(res, 1, 1, axis=1)
        # write to file.
        for row in res:
            format_row = str(row[0])
            for i in range(1, len(row)):
                format_row += "," + str(int(row[i]))
            outfile.write(format_row + "\n")
        print("Writing to file done.")


def combine():
    """
        Merge the timestamp column from the orginal data with the downloaded processed data columns.
    """
    fname_merged = './PAMAP2/merged_file.txt'
    fname_download = './PAMAP2/PAMAP2_d=4.ds'
    wfname = './PAMAP2/PAMAP2_preprocessed.txt'
    with open(fname_merged) as infile_merged, open(fname_download) as infile_download, open(wfname, 'w') as outfile:
        df_merged = pd.read_csv(infile_merged, header=None, delimiter=' ')
        df_download = pd.read_csv(infile_download, header=None, delimiter=' ', skiprows=1)

        # sort based on the timestamp, take the timestamp column.
        df_merged = df_merged.sort_values(df_merged.columns[0], ascending=True)
        time = np.array(df_merged.iloc[:, 0].values)
        print("Sorting merged file done and take the timestamp column.")

        # remove the first index column of downloaded file.
        df_download = df_download.iloc[:, 1:]

        # add time as first column.
        data_cols = np.array(df_download, dtype=float)
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
    # preprocess()
    combine()
