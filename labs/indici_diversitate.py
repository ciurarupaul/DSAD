import numpy as np
import pandas as pd


def diversitate(tabel, denumire_coloana=None):
    if denumire_coloana is not None:
        date = np.array(tabel.iloc[1:], dtype=float)
    else:
        date = np.array(tabel.values, dtype=float)

    suma = np.sum(date)
    proportii = date / suma

    # validare necesara dpdv matematic intrucat evitam calcularea de logaritmi din 0.
    # codul de mai jos identifica acele pozitii pentru care avem valoarea 0 si le inlocuiest cu 1
    indici_nuli = proportii == 0
    proportii[indici_nuli] = 1

    # definire indice de diversitate Shannon
    shannon = -np.sum(proportii * np.log(proportii))

    # definire indice de diversitate Simspon
    # dpdv matematic pentru indicele Simpson nu e avantajos sa refolosim proportii, intrucat acestea au fost alterate
    # prin inlocuirea indicilor nuli
    simpson = 1 - np.sum(date / suma * date / suma)

    if denumire_coloana is not None:
        results = pd.Series(
            data=[tabel.iloc[0], shannon, simpson],
            index=["denumire_coloana", "Shannon", "Simpson"],
        )
    else:
        results = pd.Series(data=[shannon, simpson], index=["Shannon", "Simpson"])

    return results
