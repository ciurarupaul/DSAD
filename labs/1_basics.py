from functools import reduce
import numpy as np
import time

#
# lists, sets, tuples and dictionaries
#

print()
# list comprehensions
# bloc in alte limbaje (ish)
numere = []
for each in range(
    20
):  # metoda built in care intoarce un set de numere intregi cuprins intre [0:19]
    if each % 2 == 0:
        numere.append(each**3)
print(numere)

print()
# acelasi bloc in python (w/ list comprehensions)
numere = [x**3 for x in range(20) if x % 2 == 0]
# un comprehension este compus din 3 blocuri:
#   1. blocul iterativ: for each in range(20)
#   2. (dreapta for) (optional) blocul de filtrare: if x % 2 == 0
#   3. (stanga for) blocul de transformare: x ** 3
# [actiune filtrare iteratie]

# map values with list comprehensions
celsius = [10, -5, 3, 17, 0, 20, 19]
fahrenheit = [round(c * 9 / 5 + 32, 1) for c in celsius]  # f = c * 9/5 + 32
print("Celsius: ", celsius)
print("Fahrenheit: ", fahrenheit)

# filtrare cu list comprehensions
temp_pozitive = [c for c in celsius if c >= 0]
print(temp_pozitive)

print()
note = [3, 6, 7, 5, 4, 10, 9]
status = [
    "promovat" if n >= 5 else "restant" for n in note
]  # diferit de un list comprehension clasic
print(note)
print(status)

print()
# dict comprehensios
nume = ["Ana", "Andreea", "Alin"]
note_dict = [10, 9.2, 9.6]
catalog = {
    key + " procesat": value for key, value in zip(nume, note_dict) if value > 9.5
}
print(catalog, type(catalog))
print(catalog.keys(), type(catalog.keys()))
print(catalog.values(), type(catalog.values()))
print(catalog.items(), type(catalog.items()))

#
# lambda, map, filter, reduce
#

print()
# map(func, iterable)
secventa = (1, 2, 3, 4)
result = map(lambda x: x**3, secventa)
print(result, type(result), list(result))


# cele doua moduri sunt echivalente
def ridica_la_cub(x):
    return x**3


result = map(ridica_la_cub, secventa)
print(result, type(result), list(result))

print()
a = [1, 2, 3]
b = [10, 20, 30]
c = [5, 15, 25]
result = map(lambda x, y, z: x * y * z, a, b, c)
print(list(result))

# filter(func, iterable)
result = filter(lambda c: c >= 0, celsius)
print(result, type(result), list(result))

emails = ["user@gmail.com", "user@yahoo.com", "user@stud.ase.ro"]
valid = list(filter(lambda e: e.endswith("ase.ro"), emails))
print(valid)

print()
# reduce
suma = reduce(lambda e1, e2: e1 + e2, note)
print("Media notelor: ", suma / len(note))

# numpy
# numpay ofera un obiect de tip ndarray (N-dimensional arr)

# 1D: [1, 2, 3], dar in memorie e reprezentat transpus
# |    1    |
# |    2    |
# |    3    |

# 2D: matrice clasica, ca la matematica
# |    2    5    |
# |    3    6    |
# |    4    7    |

# in memorie, listele built-in in py nu sunt reprezentate in forma continua
# |__1_|__3_|___|___|__ana|___|___|___|___|__True_|___|___|___|
# ndarray forteaz aacelasi tip de date pentru toate elementele din colectie, deci pot avea aritmetica de pointeri si nu mai trebuie verificat tipul fiecarui element
# implementarea este scris in C si este mult mai rapida (up to 30x)
# permite operatii de tip SIMD (Single Instruction Multiple Data)
# |__1_|__3_|__4_|__6_|__2_|__9_|__11_|

l1 = [1, 3, "ana", True, None, 3.14, [4, 5]]
print(l1, l1[3])

a = np.array([1, 2, 3])
b = np.array([[3.2, 6.7], [1.8, 9.4], [3.3, 7.8]])
print("a: \n", a)
print("b: \n", b)

print()
# proprietati
print("Shape: ", a.shape, b.shape)  # (3,) <=> (3, 1)
print("Number of dimensions: ", a.ndim, b.ndim)
print("Data type: ", a.dtype, b.dtype)
print("Item size (bytes): ", a.itemsize, b.itemsize)
print("Size: ", a.size, b.size)
print("Number of bytes: ", a.nbytes, b.nbytes)

print()
#
# indexing si slicing
#
# indexing
c = [1, 2, 3, 4, 5]
print(c[0], c[1], c[len(c) - 1])  # indexare la nivel de lista

# slicing: [ start idx: end idx: step ]
print(
    c[0 : len(c)]
)  # 1 2 3 4 5 - desi mergem pana la len(c), nu se acceseaza valoarea, se merge corect pana la len(c) - 1
# print(c[0 : len(c)] + 100)  # 1 2 3 4 5
print(c[::2])  # 1 3 5
print(c[::-1])  # 5 4 3 2 1

print()
# indexing in np
a = np.array(
    [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
    ]
)

print(a[1, 2], a[1][2])
a[0, 0] = 20
print(a[0, 0])

print()
# slicing in np
a = np.array(
    [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
    ]
)
print(a[0, 1:-1])  # 2 3 4
print(a[0, 1:-1:2])  # 2 4
print(a[0, ::2])  # 1 3 5
print(a[:, 3])  # 4 9
print(a[:-1, 3])  # 4

print()
# colectii predefinite
print("Zeros: \n", np.zeros(3), np.zeros((2, 2)))
print("Ones: \n", np.ones((2, 2), dtype="int32"))
print("Full: \n", np.full((3, 2), 100))
print("Random: \n", np.random.randint(-100, 100, size=(3, 3)))
print("Identity: \n", np.identity(4))

print()
# repeat (duplicate each element) si tile (concat the structure *reps at the end)
a = np.array([1, 2, 3])
print("Tile: ", np.tile(a, 2))  # 123 123
print("Repeat: ", np.repeat(a, 2))  # 11 22 33

print()
# copii ale ndarrays si referinte
# shallow vs deep copy in ndarrays
b = a  # shallow copy
c = a.copy()  # deep copy

b[0] = 10
c[0] = 20
print("A: ", a)
print("B: ", b)
print("C: ", c)

# performanta in np
# test 1
print("\nComparatie in termeni de performanta:")
print("Test1 -------------------")

start = time.time()  # snapshot timestamp
a = np.arange(
    1, 1_000_001
)  # 1_000_001 <=> 1.000.001 (in romana la nivel conceptual, pentru lizibilitate)
ap = a**2
durata = time.time() - start

start_lista = time.time()
lst = [i for i in range(1, 1_000_001)]
lstp = [i**2 for i in lst]
durata_lista = time.time() - start_lista

# "stringuri single-line"
# """stringuri multi-line"""

print(f"Numpy: {durata:.5f}s")
print(f"Python: {durata_lista:.5f}s")
print(f"Raport: np a fost de {durata_lista/durata:.2f} ori mai rapid")  # ~ >30 times

# test 2
print("Test2 -------------------")
start = time.time()
a = np.arange(1, 1_000_001)
ap = a**2
durata = time.time() - start

start_lista = time.time()
lst = [i**2 for i in range(1, 1_000_001)]
durata_lista = time.time() - start_lista

print(f"Numpy: {durata:.5f}s")
print(f"Python: {durata_lista:.5f}s")
print(f"Raport: np a fost de {durata_lista/durata:.2f} ori mai rapid")  # ~ >15 times

print()
# broadcasting si operatii pe ndarrays
# broadcasting - modalitatea prin care np rezolva operatii intre ndarrays de forme diferite prin extinderea automata a nd-arrayului de forma mai mica astfel incat acesta sa se potriveasca celui mai mare

c = np.array([[1, 2, 3], [4, 5, 6]])
print("Broadcasting de elem - inmultire mat cu scalar: \n", c * 2)

x = np.array([[1, 2], [3, 4]])
y = np.array([[2, 2], [2, 2]])
print("Inmultire element cu element:\n", x * y)
print("Multiplicare de matrice ca la matematica:\n", x @ y)

print("\nBroadcasting----")
a = np.array(
    [
        [1, 2],
        [3, 4],
        [5, 6],
    ]
)
d = np.array([1, 2, 3])
b = np.array(
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
)

# d * b = (3, 1) x (3, 3)
# in cazul acest, prin broadcasting, np extinde vectorul a.i. inmultirea el cu el sa se efectueze
print(d * b)

# a * b = (3, 2) x (3, 3)
# eroare, deoarece broadcasting nu reconcilieaza elementele din ndarray pentru inmultire
# print(a * b)

#
# de revenit aici ca e ceva ciudat
#
