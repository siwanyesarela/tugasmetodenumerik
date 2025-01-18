import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Header aplikasi
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 2.8rem;
        color: #1D3557;
        font-weight: bold;
        margin-bottom: 0;
    }
    .sub-title {
        text-align: center;
        font-size: 1.6rem;
        color: #457B9D;
        margin-bottom: 30px;
    }
    .result-box {
        background-color: #A8DADC;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 20px 0;
    }
    .result-box h3 {
        color: #1D3557;
        margin: 0;
    }
    .result-box p {
        color: #1D3557;
        font-size: 1.3rem;
        margin: 5px 0 0;
    }
    .footer {
        text-align: center;
        margin-top: 30px;
        font-size: 0.9rem;
        color: #6D6875;
    }
</style>
<div class="main-title">Aplikasi Metode Numerik dengan Visualisasi 3D</div>
<div class="sub-title">Jelajahi Metode Numerik dengan Tampilan Interaktif</div>
""", unsafe_allow_html=True)

# Input fungsi matematika
st.sidebar.header("Input Parameter")
st.sidebar.write("Masukkan fungsi dan parameter integrasi")

function_input = st.sidebar.text_input(
    "Masukkan fungsi dalam variabel x:", "x**2 + 3*x + 2")

# Input batas bawah dan atas
col1, col2 = st.sidebar.columns(2)
with col1:
    a = st.number_input("Batas bawah (a):", value=0.0)
with col2:
    b = st.number_input("Batas atas (b):", value=1.0)

# Pilihan metode
method = st.sidebar.selectbox("Metode Numerik:", ["Trapezoidal"])

# Input jumlah partisi (hanya untuk Trapezoidal)
if method == "Trapezoidal":
    n = st.sidebar.number_input("Jumlah partisi (n):", min_value=1, value=10, step=1)

# Tombol hitung
if st.sidebar.button("Hitung"):
    try:
        # Konversi fungsi input ke bentuk Python
        x = sp.symbols('x')
        f = sp.sympify(function_input)
        func = sp.lambdify(x, f, 'numpy')
        
        # Membuat range nilai x untuk grafik
        x_values = np.linspace(a - abs(a)*0.2, b + abs(b)*0.2, 200)
        y_values = func(x_values)

        # Grafik 2D
        fig_2d, ax_2d = plt.subplots(figsize=(10, 6))
        ax_2d.plot(x_values, y_values, label=f"f(x) = {function_input}", color="#2A9D8F", linewidth=2)
        ax_2d.fill_between(x_values, y_values, where=[(a <= xi <= b) for xi in x_values], 
                           color="#FF69B4", alpha=0.3, label="Area Integral")
        ax_2d.axvline(a, color="#264653", linestyle="--", linewidth=1.5, label=f"Batas bawah (a={a})")
        ax_2d.axvline(b, color="#E76F51", linestyle="--", linewidth=1.5, label=f"Batas atas (b={b})")
        ax_2d.set_title("Visualisasi Fungsi (2D)", fontsize=16, fontweight="bold", pad=20)
        ax_2d.set_xlabel("x", fontsize=14, labelpad=10)
        ax_2d.set_ylabel("f(x)", fontsize=14, labelpad=10)
        ax_2d.legend(fontsize=12, loc="upper right")
        ax_2d.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

        # Grafik 3D
        fig_3d = plt.figure(figsize=(12, 8))
        ax_3d = fig_3d.add_subplot(111, projection='3d')

        X = np.linspace(a, b, 100)
        Y = func(X)
        Z = np.zeros_like(X)
        ax_3d.plot(X, Y, Z, color="#2A9D8F", label=f"f(x) = {function_input}", linewidth=2)
        ax_3d.plot_surface(
            np.array([X, X]),
            np.array([Z, Y]),
            np.array([Z, Z]),
            color="#FF69B4",
            alpha=0.3,
            rstride=100,
            cstride=100,
        )

        ax_3d.set_title("Visualisasi Fungsi (3D)", fontsize=16, fontweight="bold", pad=20)
        ax_3d.set_xlabel("x", fontsize=14, labelpad=10)
        ax_3d.set_ylabel("f(x)", fontsize=14, labelpad=10)
        ax_3d.set_zlabel("z", fontsize=14, labelpad=10)
        ax_3d.view_init(elev=30, azim=45)
        ax_3d.legend(fontsize=12, loc="upper right")

        # Perhitungan metode numerik
        if method == "Trapezoidal":
            # Implementasi metode Trapezoidal
            x_trap = np.linspace(a, b, n + 1)
            y_trap = func(x_trap)
            h = (b - a) / n
            integral = h * (0.5 * y_trap[0] + 0.5 * y_trap[-1] + np.sum(y_trap[1:-1]))
            
            st.markdown(f"""
            <div class="result-box">
                <h3>Hasil Integrasi</h3>
                <p>Menggunakan metode <b>Trapezoidal</b>: {integral:.6f}</p>
            </div>
            """, unsafe_allow_html=True)

        # Tampilkan grafik
        st.pyplot(fig_2d)
        st.pyplot(fig_3d)

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

# Footer aplikasi
st.markdown("""
<div class="footer">
    Dibuat dengan ❤️ menggunakan Streamlit | © 2025
</div>
""", unsafe_allow_html=True)
