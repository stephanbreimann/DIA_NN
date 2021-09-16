"""
This is a script for ...
"""
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import scripts.config as conf

# Settings
pd.set_option('expand_frame_repr', False)  # Single line print for pd.Dataframe


# I Helper Functions
def check_prot_id_str(df=None, prot_id=None):
    cols = list(df)
    if prot_id not in cols:
        raise ValueError(f"'prot_id' ('{prot_id}' is not in 'df'. Chose from following: {cols}")


# II Main Functions
def precursor_count(df=None, group_str="MS_data", prot_id="Protein.Group"):
    """Get precursor count from Precursor File"""
    check_prot_id_str(df=df, prot_id=prot_id)
    groups = [x for x in list(df) if group_str in x]
    for g in groups:
        df_g = df[[prot_id, g]]
        print(df_g.sort_values(by=prot_id))


# III Test/Caller Functions
def get_counts():
    """"""
    file = "report_CSF_ringtrial.pr_matrix.tsv"
    df = pd.read_csv(conf.folder_data + file, sep="\t")
    precursor_count(df=df)

# IV Main
def main():
    t0 = time.time()
    get_counts()
    t1 = time.time()
    print("Time:", t1 - t0)


if __name__ == "__main__":
    main()
