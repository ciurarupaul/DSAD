import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from indici_diversitate import diversitate

# pandas - biblioteca de functii construita pentru np pentru calcul tabelar
# pandas expune doua tipuri de obiecte:
#   1. Series = date unidimensionale (coloana intr-un tabel)
#   2. DataFrame = date bidimensionale (tabele propriu-zise)

s = pd.Series([10, 20, 30], index=["a", "b", "c"])
df = pd.DataFrame(
    {
        "Name": ["Alice", "Bob", "Carol"],
        "Age": [30, 32, 35],
        "Salary": [4000, 4500, 4700],
    }
)

df = pd.read_csv("res/employees.csv", index_col=1)
# index_col = 0     - organizeaza datele in functie de prima coloana (indexarea incepe de la 0)

# proprietati pe dataframe
print("\nDF head:\n", df.head())  # primele 5 randuri din df
print("\nDF tail:\n", df.tail())  # ultimele 5 randuri din df

print(
    "\nDF info:\n", df.info()
)  # structura informatiilor din df: tipuri de date, valori null, ..
print(
    "\nDF describe:\n", df.describe()
)  # statistici simple cu privire la datele din coloane

print("\nDF shape:\n", df.shape)  # (rows, cols)
print("\nDF columns:\n", df.columns)  # lista cu denumirile coloanelor
print("\nDF index:\n", df.columns)  # lista cu denumirile referinteor randurilor

# ------------------------------------------------------------------------
# accesarea datelor
# ------------------------------------------------------------------------

# citirea datelor

# accesul se face folosind operatorul de indexare [] (exact ca in np)
# singura diferenta este ca se pot folosi direct stringuri (numele coloanelor/liniilor)

ages = df["Age"]
# subset = df[["Name", "Salary"]] # err?

# citirea datelor pe randuri in functie de pozitie | iloc = index location
fr = df.iloc[0]  # primul rand
ftr = df.iloc[0:3]  # primele 3 randuri, exact ca in np

# citirea datelor pe randuri in functie de etichete (strings) | loc
l1 = df.loc["Bob"]
print(l1)
l2 = df.loc["Eva":"Ivy", ["Gender", "Salary"]]
print(l2)

# tl;dr
# iloc se refera la index-ul efectiv al randului: 0, 1, 2
# loc gaseste randurile dupa la continutul 'celulei index' a randului: Bob, Alice,..
# celula index e 'definita' prin index_col = 1, in cazul de fata numele angajatilor

# ------------------------------------------------------------------------
# transformari de date
# ------------------------------------------------------------------------

# adaugarea unei coloane noi
df["TaxedSalary"] = df["Salary"] * 0.9

# df.rename(columns={"Salary": "GrossSalary"}, inplace=True)
# inplace=True - se aplica direct pe setul de date. altfel intoarce o copie modificata

# drop pe randuri si coloane
df.drop(columns=["TaxedSalary"], inplace=True)  # drop coloana
df.drop(index=["Carol"], inplace=True)  # drop pe rand

# data sanitization
# in general, ne vom gasi intr-unul dint urmatoarele scenarii:
#  cand avem celule lipsa, de regula urmarim fie sa inlocuim valorile lipsa, fie sa stergem ori coloanele, ori randurile problematice
#   1. Date numerice
#       inlocuim cu media pe coloana sau cu o valoare convenabil aleasa
#   2. Date categorice (stringuri)
#       inlocuim cu modulul/valoarea cea mai desc intalnita

missing = df.isna().sum()

# drop
df.dropna()  # cand axis = 0, facem drop pe toate coloanele care au NaN
df.dropna(axis=1)  # cand axis = 1, facem drop pe toate randurile care au NaN

# replace
df.fillna(0)
df["Salary"].fillna(df["Salary"].mean(), inplace=True)

# alte transformari pe coloane

# vectorizare
df["AgeInMonths"] = df["Age"] * 12

# lambda si apply


def return_bracket(x):
    if x > 6000:
        return "High"
    else:
        return "Low"


df["IncomeBracket"] = df["Salary"].apply(return_bracket)

# functii pe clasa string
df["Gender"] = df["Gender"].str.lower()

# ------------------------------------------------------------------------
# statistici
# ------------------------------------------------------------------------

# centrarea datelor
# translatarea intregului set relativ la o valoare de referinta care va sta in centrul setului de date
df["SalaryCentered"] = df["Salary"] - df["Salary"].mean()

# scalarea datelor
# aducerea valorilor pe coloane la ordine de marime comparabile

#

# standardizarea = centrare + scalare
df["SalaryCentered"] = (df["Salary"] - df["Salary"].mean()) / df["Salary"].std()

# normalizarea datelor
# este un procedeu ce transforma datele folosind o formula de tipul: (xi - xmin) / (xmax - xmin)
# in urma normalizarii datelor, valorile obtinute vor if in intervalul [0:1]
# normalizarea datelor transforma reprezentarea acestora. in urma normalizarii, reprezentarea grafica difera
# normalizarea se utilizeaza in general in ML si in algoritmi unde datele au domenii de definitie finite

# statistici descriptive
df["Salary"].mean()
df[
    "Salary"
].median()  # mediana, valoarea care imparte setul de date in 2 jumatatie EGALE
df["Salary"].mode()  # modul, cea mai frecvent intalnita valoare pe coloana

# metrici privitoare la dispersia datelor
df["Salary"].std()
df["Salary"].var()

# relatia intre 2 variabile
# daca valoarea coeficientului este pozitiva, intre cele doua variabile exista o relatie de direct proportionalitate - atunci cand o variabila creste si cealalta creste, respectiv invers
# daca valoarea coeficientului este negativa, intre cele doua varibile exista o relatie de invers proportionalitate - atunci cand o variabila creste, cealalta scade, respectiv invers
# daca valoarea tinde sa fie apropiata de 0, cele doua variabile tind sa fie independente
df[["Age", "Salary"]].corr()

# desenare grafice direct din pandas
df["Age"].hist(bins=5, edgecolor="red")
plt.show()

# ------------------------------------------------------------------------
# merge
# ------------------------------------------------------------------------
# merge pe tabele (echivalentul unui join in SQL) si concatenare
df1 = pd.DataFrame({"ID": [1, 2, 3], "Name": ["Alice", "Bob", "Carol"]})

df2 = pd.DataFrame({"ID": [4, 5, 6], "Name": ["Mark", "Eva", "Ivy"]})

df3 = pd.DataFrame({"ID": [1, 2, 3], "Department": ["IT", "HR", "Finance"]})

merged = df1.merge(df3, on="ID")
print(merged)

concat = pd.concat([df1, df2])
print(concat)

# tipuri de merge - vom presupune ca operam cu 2 data frames: df1 si df2, iar operatiile de merge respecta formatul
# df1.merge(df2)
# inner - intersectia dintre df1 si df2, adica randurile comune celor 2 surse
# left - toate randurile din df1, chiar daca nu au un corespondent in df2
# right - toate randurile din df2, chiar daca nu au un corespondent in df1
# outer - reuniunea dintre df1 si df2 sau toate datele

employees = pd.read_csv("res/employees.csv")
departments = pd.read_csv("res/departments.csv")

# exemplele de mai jos sunt cazuri de merge pe baza coloanelor
# merge pe baza de coloane presupune ca in ambele data frames exista o coloana comuna (in df.columns, nu df.index!!!)

# inner
inner = employees.merge(departments, on="DepartmentID", how="inner")
print(inner)

# left
left = employees.merge(departments, on="DepartmentID", how="left")
print(left)

# right
right = employees.merge(departments, on="DepartmentID", how="right")
print(right)

# outer
outer = employees.merge(departments, on="DepartmentID", how="outer")
print(outer)

# merge pe baza de index
tabel_etnii = pd.read_csv("res/ethnicity.csv", index_col=0)
# nan_replace()

variabile_etnii = list(tabel_etnii.columns)[1:]

# calcul populatie pe etnii la nivel de judet
localitati = pd.read_excel(
    "res/CoduriRomania.xlsx", index_col=0, sheet_name="Localitati"
)

t1 = tabel_etnii.merge(right=localitati, right_index=True, left_index=True)
print(t1)

g1 = t1[variabile_etnii + ["County"]].groupby("County").agg("sum")
print(g1)

# calcul populatie pe etnii la nivel de regiune
judete = pd.read_excel("res/CoduriRomania.xlsx", index_col=0, sheet_name="Judete")

t2 = g1.merge(right=judete, right_index=True, left_index=True)
print(t2)

g2 = t2[variabile_etnii + ["Regiune"]].groupby("Regiune").agg("sum")
print(g2)

# calcul populatie pe etnii la nivel de macroregiune
regiuni = pd.read_excel("res/CoduriRomania.xlsx", index_col=0, sheet_name="Regiuni")

t3 = g2.merge(right=regiuni, right_index=True, left_index=True)
print(t3)

g3 = t3[variabile_etnii + ["MacroRegiune"]].groupby("MacroRegiune").agg("sum")
print(g3)

g1.to_csv("res/output_etnii_judete.csv")
g2.to_csv("res/output_etnii_regiuni.csv")
g3.to_csv("res/output_etnii_macroregiuni.csv")

# indici de diversitate la nivel de localitate
diversitate_loc = tabel_etnii.apply(
    func=diversitate, axis=1, denumire_coloana="Localitate"
)
diversitate_loc.to_csv("res/diversitate_etnii_localitati.csv")

# indici de diversitate la nivel de judet
diversitate_judet = g1.apply(func=diversitate, axis=1)
diversitate_judet.to_csv("res/diversitate_etnii_judet.csv")

# indici de diversitate la nivel de regiune
diversitate_regiune = g2.apply(func=diversitate, axis=1)
diversitate_regiune.to_csv("res/diversitate_etnii_regiune.csv")
