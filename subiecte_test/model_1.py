import pandas as pd

# 1. Să se salveze în fișierul Cerinta1.csv localitățile în care numărul de total de decedați (Decedați + DecedatiSub1An) este mai mare decât numărul de născuți vii. Se va salva pentru fiecare localitate, codul Siruta, denumirea localității, total decedați și născuți vii.

# 2. Să se salveze în fișierul Cerinta2.csv rata mortalității infantile la nivel de localitate, în ordine descrescătoare. Rata mortalității infantile se calculează ca număr de decedați sub un an la 1000 de născuți vii: DecedatiSub1An*1000/ NascutiVii. Pentru fiecare localitate se va salva codul Siruta, numele localității și rata mortalității infantile, în ordine descrescătoare după rata mortalității infantile.

# 3. Să se salveze în fișierul Cerinta3.csv rata sporului natural la nivel de județ. Rata sporului natural este diferența dintre rata natalității (născuți vii la 1000 locuitori) și rata mortalității (decedați la 1000 locuitori). Pentru fiecare județ se va salva indicativul de județ și rata sporului natural.

# 4. Să se calculeze și să se salveze în fișierul Cerinta4.csv pentru fiecare județ, localitățile în care ratele (valorile indicatorilor la 1000 locuitori) sunt cele mai mari. Pentru fiecare județ se va afișa indicativul de județ și numele localităților cu valorile maxime.

# citire date
miscare = pd.read_csv("res/MiscareaNatLoc.csv", index_col=0)
populatie = pd.read_csv("res/PopulatieLocalitati.csv", index_col=0)

# merge tabele - overwrite miscare
miscare = miscare.merge(
    populatie[["Populatie", "Judet"]], left_index=True, right_index=True
)

# left_index=True si right_index=True - aligns the data where the Index of miscare matches the Index of populatie
# nu poate fi folosit left/right_index independent! ori in pereche cu celalalt ori cu righ_on pentru a specifica o coloana anume

# cerinta 1 unde decedati > nascuti vii
miscare["TotalDecedati"] = miscare["Decedati"] + miscare["DecedatiSub1An"]

cerinta1 = miscare[miscare["TotalDecedati"] > miscare["NascutiVii"]]
cerinta1 = cerinta1.reset_index()  # reset Siruta as a normal column
# the merge was made on Siruta as an ID, and it became an 'index/ID column' and could no longer be selected normally. reset remakes it a normal column
cerinta1 = cerinta1[["Siruta", "Localitate", "TotalDecedati", "NascutiVii"]]

cerinta1.to_csv("output/cerinta1.csv", index=False)

# 2. rata mortalitatii infnatile
miscare["RMI"] = miscare["DecedatiSub1An"] * 1000 / miscare["NascutiVii"]
temp_df = miscare.reset_index()

cerinta2 = temp_df[["Siruta", "Localitate", "RMI"]].sort_values(
    by="RMI", ascending=False
)
# optional formatting
cerinta2["RMI"] = cerinta2["RMI"].apply(lambda item: "{:.2f}".format(item))

cerinta2.to_csv("output/cerinta2.csv", index=False)

# 3. RSN la nivel de judet
# Rata Natalitatii = (Nascuti/Populatie) * 1000
# Rata Mortalitatii = (TotalDecedati/Populatie) * 1000
miscare["RataNatalitate"] = miscare["NascutiVii"] / miscare["Populatie"] * 1000
miscare["RataMortalitate"] = miscare["TotalDecedati"] / miscare["Populatie"] * 1000

miscare["RSN"] = miscare["RataNatalitate"] - miscare["RataMortalitate"]

cerinta3 = miscare.groupby("Judet")["RSN"].mean().reset_index()
cerinta3.to_csv("output/cerinta3.csv", index=False)


# 4 localitati cu valori maxime la nivel de judet pentru fiecare indicator
def max_localitati(gr, cols):
    res = {}
    for c in cols:
        max_val = gr[c].max()
        res[c] = ",".join(gr[gr[c] == max_val]["Localitate"])
    return pd.Series(res)


indicatori = [
    "Casatorii",
    "Decedati",
    "DecedatiSub1An",
    "Divorturi",
    "NascutiMorti",
    "NascutiVii",
]

cerinta4 = miscare.groupby("Judet").apply(max_localitati, cols=indicatori)
cerinta4.reset_index(inplace=True)

cerinta4.to_csv("output/cerinta4.csv", index=False)
