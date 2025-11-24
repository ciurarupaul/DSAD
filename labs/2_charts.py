import numpy as np
import matplotlib.pyplot as plt

# explicatie a conceptelor de baza in matplotlib
# figure    - intreaga pagina/ecran sau echivalentul unui canvas din HTML
# axes      - o zona de desenare in interiorul figurii
# plot      - desenul propriu-zis compus din linii, puncte, histograme

# ------------------------------------------------------------------------
# 1. Scatter plot
# ------------------------------------------------------------------------
#   1.1. achizitie date
x = np.random.rand(50)
y = 3 * x + np.random.rand(50) * 0.2

#   1.2. definirea zonelor de desenare
plt.figure(figsize=(8, 6))

#   1.3. graficul propriu-zis
plt.scatter(x, y, color="royalblue", marker="o", edgecolors="black")

#   1.4. stilizarea graficului
plt.title("Relatia dintre X si Y")  # "Scatter plot of x vs y"
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)

#   1.5. afisare efectiva
# plt.show()

# alternativ pentru un scatter plot
# fig = plt.figure(figsize=(9, 6))
# ax1 = fig.add_subplot(1, 1, 1)
# ax2 = fig.add_subplot(1, 1, 1)  # |     ax1     |     ax2     |
# ax1.set_title("Scatter plot of x vs y", fontdict={"fontsize": 12, "color": "green"})
# ax1.set_xlabel("x_values")
# ax2.set_ylabel("y_values")
# ax1.scatter(x, y, color="royalblue", marker="o", edgecolors="black")
# for i in range(50):
#     ax1.text(x[i], y[i], "V" + str(i))

# ------------------------------------------------------------------------
# 2. Line plot
# ------------------------------------------------------------------------
# util pentru evolutia trendurilor in timp

#   2.1. achizitia de date
x = np.arange(0, 10, 0.1)
y1 = np.sin(x)
y2 = np.cos(x)

#   2.2. definirea zonelor de desenare
plt.figure(figsize=(8, 6))

#   2.3. graficul propriu-zis
plt.plot(x, y1, color="royalblue", label="sin(x)")
plt.plot(x, y2, color="red", label="cos(x)")

#   2.4. stilizare
plt.title(
    "Graficul functiilor sin si cos in intervalul [0, 10]",
    fontdict={"fontsize": 24, "color": "orange"},
)
plt.xlabel("t values", fontdict={"fontsize": 12, "color": "green"})
plt.ylabel("fc value", fontdict={"fontsize": 12, "color": "green"})
plt.grid(True)
plt.legend()

#   2.5. afisare efectiva
# plt.show()

# ------------------------------------------------------------------------
# 3. Histograma / BarChart
# ------------------------------------------------------------------------
# arata distributia unei variabile

#   3.1. ahizitie de date
x = np.random.normal(50, 10, 1000)

#   3.2. definirea zonelor de desenare
plt.figure(figsize=(8, 6))

#   3.3. grafic propriu-zis
plt.hist(x, bins=50, color="lightgreen", edgecolor="darkgreen", alpha=0.7)

#   3.4. stilizare
plt.title(
    "Distributia valorilor",
    fontdict={"fontsize": 24, "color": "orange"},
)
plt.xlabel("Interval de valori", fontdict={"fontsize": 12, "color": "green"})
plt.ylabel("Frecvente", fontdict={"fontsize": 12, "color": "green"})
plt.grid(True)

#   3.5. afisare efectiva
# plt.show()

# ------------------------------------------------------------------------
# Box plot (matplotlib si seaborn)
# ------------------------------------------------------------------------
# compara distributii sau pentru a identifica valorile outlier

# 1
departamente = ["HR", "IT", "Finance"]
salarii = [
    np.random.normal(4000, 300, 50),
    np.random.normal(6500, 500, 50),
    np.random.normal(4800, 300, 50),
]
# 2
plt.figure(figsize=(8, 6))
# 3
plt.boxplot(x=salarii, labels=departamente, patch_artist=True)
# 4
plt.title("Boxplot - salarii in functie de departament")
plt.ylabel("Salarii")
# 5
# plt.show()

# ------------------------------------------------------------------------
# Radar chart (spider chart)
# ------------------------------------------------------------------------
# date
labels = ["Speed", "Accuracy", "Stamina", "Skill", "Teamwork"]
data = np.array(
    [
        [5, 10, 6, 3, 10],
        [8, 5, 10, 5, 4],
        [9, 6, 4, 10, 7],
    ]
)
players = ["Player1", "Player2", "Player3"]
unghiuri = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
unghiuri += unghiuri[:1]

# definire zone
plt.subplots(subplot_kw=dict(polar=True), figsize=(8, 6))

# grafic proriu-zis
for i in range(len(players)):
    valori = data[i].tolist() + [data[i][0]]
    plt.plot(unghiuri, valori, label=players[i])
    plt.fill(unghiuri, valori, alpha=0.25)

# stilizare
plt.xticks(unghiuri[:-1], labels)
plt.title("Spider chart")
plt.legend()

#
# plt.show()

# ------------------------------------------------------------------------
# Area chart
# ------------------------------------------------------------------------
quarters = np.arange(1, 5)
hr_revenues = [10, 12, 6, 2]
it_revenues = [18, 20, 25, 27]
fin_revenues = [12, 14, 6, 17]

plt.figure(figsize=(8, 6))

plt.stackplot(
    quarters,
    hr_revenues,
    it_revenues,
    fin_revenues,
    labels=["HR", "IT", "Finance"],
    colors=["red", "green", "blue"],
    alpha=0.6,
)

plt.title("Revenue growth by department")
plt.xlabel("Quarters")
plt.ylabel("Revenue")
plt.legend(loc="upper left")

# plt.show()

# ------------------------------------------------------------------------
# Pie chart
# ------------------------------------------------------------------------
departamente = ["HR", "IT", "Finance", "Marketing"]
bugete = [150_000, 500_000, 300_000, 200_000]

plt.figure(figsize=(8, 6))

plt.pie(
    bugete,
    labels=departamente,
    shadow=True,  # 3d
    colors=["red", "green", "blue", "yellow"],
    explode=[0, 0.04, 0, 0],  # separare pie
    autopct="%1.1f%%",  # format procente (cu o zecimala)
)

plt.title("Distributia bugetelor departamentelor")

# plt.show()

# ------------------------------------------------------------------------
# Combine chart
# ------------------------------------------------------------------------
x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)
noise = np.random.randn(100) * 0.2
y_noise = y + noise

plt.figure(figsize=(8, 6))

plt.plot(x, y, label="sin(x)", color="green")
plt.scatter(x, y_noise, label="noise", color="red")

plt.title("Grafic combinat")
plt.legend()

plt.show()
