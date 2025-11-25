import pandas as pd
from pandas.api.types import is_numeric_dtype

def nan_replace_t(t):
    assert isinstance(t, pd.DataFrame)
    for v in t.columns:
        if any(t[v].isna()):
            if is_numeric_dtype(t[v]):
                t[v].fillna(t[v].mean(), inplace=True)
            else:
                t[v].fillna(t[v].mode()[0], inplace=True)

# citire date
miscare = pd.read_csv("res/MiscareaNatLoc.csv", index_col=0)
populatie = pd.read_csv("res/PopulatieLocalitati.csv", index_col=0)
nan_replace_t(miscare)
nan_replace_t(populatie)

# Merge tabele
miscare = miscare.merge(populatie[["Populatie","Judet"]], left_index=True, right_index=True)

# 1. Localitati unde total decedati > nascuti vii
miscare["TotalDecedati"] = miscare["Decedati"] + miscare["DecedatiSub1An"]
cerinta1 = miscare[miscare["TotalDecedati"] > miscare["NascutiVii"]]
cerinta1 = cerinta1[["Siruta","Localitate","TotalDecedati","NascutiVii"]]
cerinta1.to_csv("Cerinta1.csv", index=False)

# 2. Rata mortalitatii infantile (RMI)
miscare["RMI"] = miscare["DecedatiSub1An"] * 1000 / miscare["NascutiVii"]
cerinta2 = miscare[["Siruta","Localitate","RMI"]].sort_values(by="RMI", ascending=False)
cerinta2.to_csv("Cerinta2.csv", index=False)

# 3. Rata sporului natural (RSN) la nivel de judet
# Rata natalitatii = (NascutiVii / Populatie) * 1000
# Rata mortalitatii = (TotalDecedati / Populatie) * 1000
miscare["RataNatalitate"] = miscare["NascutiVii"] / miscare["Populatie"] * 1000
miscare["RataMortalitate"] = miscare["TotalDecedati"] / miscare["Populatie"] * 1000
miscare["RSN"] = miscare["RataNatalitate"] - miscare["RataMortalitate"]
cerinta3 = miscare.groupby("Judet")["RSN"].mean().reset_index()
cerinta3.to_csv("Cerinta3.csv", index=False)

# 4. Localitati cu valori maxime la nivel de judet pentru fiecare indicator
def max_localitati(gr, cols):
    res = {}
    for c in cols:
        max_val = gr[c].max()
        res[c] = ",".join(gr[gr[c]==max_val]["Localitate"])
    return pd.Series(res)

indicatori = ["Casatorii","Decedati","DecedatiSub1An","Divorturi","NascutiMorti","NascutiVii"]
cerinta4 = miscare.groupby("Judet").apply(max_localitati, cols=indicatori)
cerinta4.reset_index(inplace=True)
cerinta4.to_csv("Cerinta4.csv", index=False)
