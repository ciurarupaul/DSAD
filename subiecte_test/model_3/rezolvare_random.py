# În fișierul Agricultura.csv se află informații privind cifra de afaceri pentru activități agricole la nivel de localitate. Informațiile sunt următoarele:
# Siruta -  Codul Siruta al localității;
# Localitate - Denumirea localității;
# PlanteNepermanente, PlanteInmultire, CrestereaAnimalelor, FermeMixte, ActivitatiAuxiliare - Activitățile agricole cu cifra de afaceri.
# În fișierul PopulatieLocalitati.csv se află populația pe localități și indicativele de județ pentru fiecare localitate.

# -------------------------------------
# Cerințe
# -------------------------------------

# 1. Să se salveze în fișierul Cerinta1.csv valoarea totală a cifrei de afaceri (suma pentru activitățile menționate) la nivel de localitate. Pentru fiecare localitate se va salva codul Siruta, numele localității și cifra de afaceri.

# 2. Să se salveze în fișierul Cerinta2.csv activitatea agricolă cu cifra de afaceri cea mai mare la nivel de localitate. Se va salva pentru fiecare localitate codul Siruta, denumirea localității și activitatea agricolă cu cea mai mare cifră de afaceri (este vorba de denumirea activității: PlanteNepermanente sau PlanteInmultire șamd).

# 3. Să se calculeze și să se salveze în fișierul Cerinta3.csv cifra de afaceri pe locuitor la nivel de județ pentru fiecare activitate. Cifra de afaceri pe locuitor se calculează prin raportarea cifrei de afaceri la numărul locuitori. Se va salva indicativul de județ și cifra de afaceri pentru fiecare activitate.

# 4. Să se salveze în fișierul Cerinta4.csv valorile medii ale cifrei de afaceri pentru fiecare activitate la nivel de județ (media localităților). Se va calcula media ponderată, cu pondere populația la nivel de localitate.

# 5. Să se reprezinte într-un grafic la alegere valoarea totală a cifrei de afaceri (cerința 1), pentru primele 50 de localități în ordine descrescătoare a cifrei de afaceri.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================
# 1. CITIREA DATELOR
# ============================================

agri = pd.read_csv("Agricultura.csv")
pop = pd.read_csv("PopulatieLocalitati.csv")

# Coloanele activităților agricole
activitati = [
    "PlanteNepermanente",
    "PlanteInmultire",
    "CrestereaAnimalelor",
    "FermeMixte",
    "ActivitatiAuxiliare",
]

# ============================================
# 1. CERINȚA 1 — TOTAL CIFRĂ DE AFACERI / LOCALITATE
# ============================================

agri["Total"] = agri[activitati].sum(axis=1)

cerinta1 = agri[["Siruta", "Localitate", "Total"]]
cerinta1.to_csv("Cerinta1.csv", index=False)
print("Cerinta1.csv a fost generat.")


# ============================================
# 2. CERINȚA 2 — ACTIVITATEA CU CIFRA DE AFACERI MAXIMĂ
# ============================================

agri["ActivitateMax"] = agri[activitati].idxmax(axis=1)

cerinta2 = agri[["Siruta", "Localitate", "ActivitateMax"]]
cerinta2.to_csv("Cerinta2.csv", index=False)
print("Cerinta2.csv a fost generat.")


# ============================================
# 3. CERINȚA 3 — CIFRA DE AFACERI PE LOCUITOR / JUDEȚ
# ============================================

# Combinăm datele pe Siruta
merged = pd.merge(agri, pop, on="Siruta")

# Grupăm pe județ și însumăm activitățile + populația
sum_judete = merged.groupby("Judet")[activitati + ["Populatie"]].sum()

# Calculăm cifra de afaceri pe locuitor
for act in activitati:
    sum_judete[act] = sum_judete[act] / sum_judete["Populatie"]

cerinta3 = sum_judete[activitati].reset_index()
cerinta3.to_csv("Cerinta3.csv", index=False)
print("Cerinta3.csv a fost generat.")


# ============================================
# 4. CERINȚA 4 — MEDIA PONDERATĂ A CIFREI DE AFACERI PE JUDEȚ
# ============================================

# Formula: sum(CifraLocalitate * PopLocalitate) / sum(PopLocalitate)


def media_ponderata(df, nume_col):
    return np.average(df[nume_col], weights=df["Populatie"])


rezultate = []

for jud, df_jud in merged.groupby("Judet"):
    rand = {"Judet": jud}
    for act in activitati:
        rand[act] = media_ponderata(df_jud, act)
    rezultate.append(rand)

cerinta4 = pd.DataFrame(rezultate)
cerinta4.to_csv("Cerinta4.csv", index=False)
print("Cerinta4.csv a fost generat.")


# ============================================
# 5. CERINȚA 5 — GRAFIC CU PRIMELE 50 LOCALITĂȚI
# ============================================

top50 = cerinta1.sort_values("Total", ascending=False).head(50)

plt.figure(figsize=(12, 6))
plt.bar(top50["Localitate"], top50["Total"])
plt.xticks(rotation=90)
plt.title("Top 50 localități după cifra totală de afaceri")
plt.tight_layout()
plt.show()
