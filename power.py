from sklearn.preprocessing import MinMaxScaler
import pandas as pd


def preprocess():
    scaler = MinMaxScaler(feature_range=(0, 100000))
    fname = 'power/power_middle.txt'
    wfname = 'power/power_preprocessed.txt'
    with open(fname) as infile, open(wfname, 'w') as outfile:
        df = pd.read_csv(infile, header=None, delimiter=',')

        # create time column based on the first two columns.
        time = df.iloc[:, 0].values
        # drop the first timestamp column.
        df = df.drop(columns=[0])
        # normalize to [0, 1e5].
        df = pd.DataFrame(scaler.fit_transform(df.values))
        print("Normalization done.")
        # add time as the first column
        df.insert(loc=0, column='Timestamp', value=time)
        # add weight 1 as second column.
        df.insert(loc=1, column='Weight', value=1)
        # sort based on the timestamp.
        df = df.sort_values(df.columns[0], ascending=True)
        print("Adding timestamp and weight done.")

        # write to file.
        res = df.values
        for row in res:
            format_row = str(row[0])
            for i in range(1, len(row)):
                format_row += "," + str(int(row[i]))
            outfile.write(format_row + "\n")
        print("Writing to file done.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    preprocess()
