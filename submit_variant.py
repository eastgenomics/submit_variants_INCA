import argparse
import numpy as np
import pyodbc
import pandas as pd


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments

    Returns
    -------
    args : Namespace
        Namespace of passed command line argument inputs
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", "-i", required=True, help="input csv file name"
    )
    parser.add_argument("-uid", required=True, help="uid to connect server")
    parser.add_argument(
        "--password", "-pw", required=True, help="password to connect server"
    )

    return parser.parse_args()


def insert(csv_file, conn) -> None:
    """
    Insert the variants in csv file into INCA table

    Parameters
    ----------
    str input csv file name
    """
    cursor = conn.cursor()
    df = pd.read_csv(csv_file)

    # remove some cols as they don't exist in db table atm
    df.drop(["R code", "Organisation ID"], axis=1, inplace=True)

    # rename col to match with col in INCA
    df.rename(columns={"Ref genome": "Ref_genome"}, inplace=True)

    # loop for each row in df
    for i in range(df.shape[0]):
        temp_df = df.loc[[i]]
        temp_df = temp_df[temp_df.columns[~temp_df.isnull().all()]]
        cols = [f"[{x}]" for x in temp_df.columns]
        columns = ", ".join(cols)
        qmarks = ", ".join("?" * temp_df.shape[1])
        qry = "Insert Into [Shiredata].[dbo].[INCA] (%s) Values (%s)" % (
            columns,
            qmarks
        )
        # convert int64 to int
        item_to_insert = []
        for item in list(temp_df.iloc[0]):
            if isinstance(item, np.int64):
                item = int(item)
            item_to_insert.append(item)
        cursor.execute(qry, item_to_insert)
        conn.commit()


def main():
    args = parse_args()
    conn_str = (
        f"DSN=gemini;DRIVER={{SQL Server Native Client 11.0}};"
        f"UID={args.uid};PWD={args.password}"
    )

    # establish connection
    conn = pyodbc.connect(conn_str)

    # insert
    insert(args.input, conn)

    # close
    conn.close


if __name__ == "__main__":
    main()
