"""
This is a script for precursor and peptide counting from DIA NN output
"""
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import scripts.config as conf
import scripts._utils as ut

# Settings
pd.set_option('expand_frame_repr', False)  # Single line print for pd.Dataframe

STR_PEPTIDE = "n Pep R0"
STR_PRECURSOR = "n Pre R0"


# I Helper Functions
def check_col_id_str(df=None, col_id=None):
    cols = list(df)
    if col_id not in cols:
        raise ValueError(f"'col_id' ('{col_id}' is not in 'df'. Chose from following: {cols}")


# II Main Functions
def _precursor_count(df=None, groups=None, col_id="Protein.Group"):
    """Get precursor count from Precursor File"""
    check_col_id_str(df=df, col_id=col_id)
    list_df = []
    for g in groups:
        df_g = df[[col_id, g]]
        df_g = df_g.dropna()
        list_df.append(df_g[col_id].value_counts())
    df_pre = pd.concat(list_df, axis=1)
    df_pre.columns = [f"{STR_PRECURSOR}{n+1}" for n in range(0, len(groups))]
    return df_pre


def _peptide_count(df=None, groups=None, col_id="Protein.Group", col_pep="Stripped.Sequence"):
    """Get peptide count from Precursor File"""
    check_col_id_str(df=df, col_id=col_id)
    list_df = []
    for g in groups[0:]:
        df_g = df[[col_id, col_pep, g]]
        df_g = df_g.dropna()
        df_g = df_g.drop_duplicates([col_id, col_pep], keep="last")
        list_df.append(df_g[col_id].value_counts())
    df_pep = pd.concat(list_df, axis=1)
    df_pep.columns = [f"{STR_PEPTIDE}{n+1}" for n in range(0, len(groups))]
    return df_pep


def get_counts(df=None, group_str="MS_data", col_id=None):
    """Get count for precursor and peptides"""
    groups = [x for x in list(df) if group_str in x]
    df_pre = _precursor_count(df=df, groups=groups, col_id=col_id)
    df_pep = _peptide_count(df=df, groups=groups, col_id=col_id)
    df_count = df_pre.join(df_pep)
    return df_count


def filter_pep(df=None, percent=90, n_pep_min=2):
    """Filter based on peptide count"""
    ut.check_non_negative_number(name="percent", val=percent, min_val=10, max_val=100)
    ut.check_non_negative_number(name="n_pep_min", val=n_pep_min, min_val=1, max_val=10)
    cols_pep = [x for x in list(df) if STR_PEPTIDE in x]
    n = int(len(cols_pep) * percent / 100)
    mask = (df[cols_pep] >= n_pep_min).sum(axis=1) >= n
    df_filtered = df[mask]
    return df_filtered


# III Test/Caller Functions
def ring_trial():
    """"""
    ut.plot_settings()
    col_id = "Protein.Group"
    group_str = "MS_data"
    file_pr = "report_CSF_ringtrial.pr_matrix.tsv"
    file_pg = "report_CSF_ringtrial.pg_matrix.tsv"
    df_pr = pd.read_csv(conf.folder_data + file_pr, sep="\t")
    df_pg = pd.read_csv(conf.folder_data + file_pg, sep="\t").set_index(col_id)
    df_count = get_counts(df=df_pr, col_id=col_id, group_str=group_str)
    cols = [x for x in list(df_pg) if group_str not in x]
    cols_group = ["Int " + x.split("timsproDIA_")[-1].split(".")[0] for x in list(df_pg) if group_str in x]
    df_pg.columns = cols + cols_group
    df_pg = df_pg.join(df_count)
    print(df_pg)
    array = []
    list_percent = list(range(50, 110, 10))
    list_n_pep_min = list(range(1, 10))
    for percent in list_percent:
        a = []
        for i in list_n_pep_min:
            df_filtered = filter_pep(df=df_pg, n_pep_min=i, percent=percent)
            a.append(len(df_filtered))
        array.append(a)
    df = pd.DataFrame(data=array, columns=list_n_pep_min, index=list_percent)
    df = df.sort_index(ascending=False)
    sns.heatmap(df, cmap="viridis")
    plt.yticks(rotation=0)
    plt.ylabel("Coverage [%]")
    plt.xlabel("min n peptides")
    plt.show()


# IV Main
def main():
    t0 = time.time()
    ring_trial()
    t1 = time.time()
    print("Time:", t1 - t0)


if __name__ == "__main__":
    main()
