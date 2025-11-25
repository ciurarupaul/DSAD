import pandas as pd
import numpy as np
from pandas.core.dtypes.common import is_numeric_dtype


# -----------------------------------------
# cerinte
# -----------------------------------------

# 1. Salvarea în fișierul Cerinta1.csv a consumului mediu pe cei cinci ani la nivel de țară, în ordine descrescătoare după consum. Se va salva pentru fiecare țară, codul de țară, numele țării și consumul mediu.

# 2. Salvarea în fișierul Cerinta2.csv a anului cu cel mai mare consum pentru fiecare țară. Se va salva codul de țară, numele țării și anul cu cel mai mare consum.

# 3. Salvarea în fișierul Cerinta3.csv a coeficienților de variație pentru fiecare an la nivel de continent. Coeficientul de variație se calculează prin raportarea abaterii standard a indicatorului respectiv la media sa. Se va salva numele continentului și coeficienții de variație pe fiecare an.

# 4. Salvarea în fișierul Cerinta4.csv a țărilor la care se înregistrează cel mai mare consum, la nivel de continent, pe ani. Pentru fiecare județ se va afișa codul țării cu consumul maxim la fiecare an.


# -----------------------------------------
# rezolvare
# -----------------------------------------
def nan_replace_t(t):
    assert isinstance(t, pd.DataFrame)
    for v in t.columns:
        if any(t[v].isna()):
            if is_numeric_dtype(t[v]):
                t[v].fillna(t[v].mean(), inplace=True)
            else:
                t[v].fillna(t[v].mode()[0], inplace=True)


alcool = pd.read_csv("res/alcohol.csv", index_col=1)
ani = list(alcool)[1:]
nan_replace_t(alcool)

coduri = pd.read_csv("res/CoduriTariExtins.csv", index_col=2)
nan_replace_t(coduri)

# data = alcool.merge(
#     coduri[["Country_Name", "Two_Letter_Country_Code"]],
#     left_index=True,
#     right_index=True,
# )
# data.reset_index(inplace=True, names="Three_Letter_Country_Code")

# 1.
cerinta1 = alcool.apply(
    lambda x: pd.Series([x["Country"], x.iloc[1:].mean()], ["Country", "Consum Mediu"]),
    axis=1,
)
cerinta1.sort_values(by="Consum Mediu", ascending=False, inplace=True)
cerinta1.to_csv("output/cerinta1.csv", index=False)

# 2. anul cu cel mai mare consum pentru fiecare tara
cerinta2 = alcool.apply(
    lambda x: pd.Series(
        [x["Country"], x.index[x.iloc[1:].argmax() + 1]], ["Country", "Anul"]
    ),
    axis=1,
)
cerinta2.to_csv("output/cerinta2.csv")

# 3.
alcool_ = alcool[ani].merge(
    coduri[["Continent_Name"]], left_index=True, right_index=True
)

cerinta3 = (
    alcool_[["Continent_Name"] + ani]
    .groupby(by="Continent_Name")
    .agg(lambda x: x.std() / x.mean())
)
cerinta3.round(5).to_csv("Cerinta3_1.csv")

# 4.
cerinta4 = alcool_.groupby(by="Continent_Name").apply(func=f, ani=ani)
cerinta4.to_csv("Cerinta4_1.csv")
