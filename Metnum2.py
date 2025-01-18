import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Judul dan deskripsi aplikasi
st.title("Aplikasi Metode Numerik - Newton-Raphson 3D")
st.write("""
Aplikasi ini menggunakan metode Newton-Raphson untuk menyelesaikan sistem persamaan non-linear dalam ruang 3D.
Anda dapat memasukkan fungsi-fungsi non-linear di bawah ini.
""")

# Input fungsi
st.header("Input Fungsi dan Parameter")
func1_input = st.text_input("Masukkan fungsi pertama f1(x, y, z):", "x**2 + y**2 + z**2 - 1")
func2_input = st.text_input("Masukkan fungsi kedua f2(x, y, z):", "x**2 - y**2 + z - 0.5")
func3_input = st.text_input("Masukkan fungsi ketiga f3(x, y, z):", "x - y + z - 0.5")

x0 = st.number_input("Tebakan awal x0:", value=0.5)
y0 = st.number_input("Tebakan awal y0:", value=0.5)
z0 = st.number_input("Tebakan awal z0:", value=0.5)
max_iter = st.number_input("Jumlah iterasi maksimum:", value=10, step=1)
tolerance = st.number_input("Toleransi error:", value=1e-6, format="%.1e")

# Kalkulasi Newton-Raphson
st.header("Hasil")
if st.button("Hitung"):
    # Definisikan simbol
    x, y, z = sp.symbols('x y z')

    # Pars fungsi
    f1 = sp.sympify(func1_input)
    f2 = sp.sympify(func2_input)
    f3 = sp.sympify(func3_input)

    # Jacobian matrix
    jacobian = sp.Matrix([[f1.diff(var) for var in (x, y, z)],
                          [f2.diff(var) for var in (x, y, z)],
                          [f3.diff(var) for var in (x, y, z)]])

    # Konversi fungsi dan jacobian ke bentuk numerik
    f_numeric = sp.lambdify((x, y, z), [f1, f2, f3], "numpy")
    jacobian_numeric = sp.lambdify((x, y, z), jacobian, "numpy")

    # Newton-Raphson Iterasi
    iterasi = 0
    error = float("inf")
    solusi = np.array([x0, y0, z0], dtype=float)

    hasil = []

    while error > tolerance and iterasi < max_iter:
        try:
            # Evaluasi fungsi dan Jacobian
            f_val = np.array(f_numeric(*solusi), dtype=float)
            jacobian_val = np.array(jacobian_numeric(*solusi), dtype=float)

            # Update solusi
            delta = np.linalg.solve(jacobian_val, -f_val)
            solusi += delta

            # Hitung error
            error = np.linalg.norm(delta, ord=2)
            hasil.append((iterasi + 1, *solusi, error))
            iterasi += 1
        except Exception as e:
            st.error(f"Kesalahan dalam perhitungan: {e}")
            break

    # Tampilkan hasil
    if hasil:
        st.write("Iterasi selesai.")
        st.table(
            {
                "Iterasi": [row[0] for row in hasil],
                "x": [row[1] for row in hasil],
                "y": [row[2] for row in hasil],
                "z": [row[3] for row in hasil],
                "Error": [row[4] for row in hasil],
            }
        )
    else:
        st.write("Tidak ada hasil. Pastikan input sudah benar.")

    # Plot hasil
    st.header("Visualisasi")
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Plot fungsi 3D
    u = np.linspace(-1.5, 1.5, 30)
    v = np.linspace(-1.5, 1.5, 30)
    U, V = np.meshgrid(u, v)
    W1 = eval(func1_input.replace("x", "U").replace("y", "V").replace("z", "0"))
    W2 = eval(func2_input.replace("x", "U").replace("y", "V").replace("z", "0"))

    ax.contour3D(U, V, W1, 50, cmap='Reds', alpha=0.5)
    ax.contour3D(U, V, W2, 50, cmap='Blues', alpha=0.5)

    # Plot solusi
    ax.scatter(solusi[0], solusi[1], solusi[2], color='black', label="Solusi", s=100)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    st.pyplot(fig)
