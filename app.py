# =============================
# FILE: app.py
# =============================
import streamlit as st
from rules import penyakit, gejala, forward_chaining

st.set_page_config(page_title="Sistem Pakar Penyakit Lambung", layout="centered")

st.title("🩺 Sistem Pakar Deteksi Penyakit Lambung")
st.write("Pilih gejala yang Anda alami, lalu sistem akan menganalisis kemungkinan penyakit menggunakan metode **Forward Chaining**.")

st.subheader("Daftar Gejala")

selected_gejala = []
for kode, nama in gejala.items():
    if st.checkbox(nama):
        selected_gejala.append(kode)

if st.button("Proses Diagnosa"):
    if not selected_gejala:
        st.warning("Silakan pilih minimal satu gejala.")
    else:
        hasil = forward_chaining(selected_gejala)
        if not hasil:
            st.error("Tidak ditemukan kecocokan penyakit berdasarkan gejala yang dipilih.")
        else:
            st.subheader("Hasil Diagnosa")
            hasil_urut = dict(sorted(hasil.items(), key=lambda x: x[1], reverse=True))
            for kode, nilai in hasil_urut.items():
                st.write(f"**{penyakit[kode]}** : {nilai*100:.2f}% kecocokan")
            st.success(f"Kemungkinan terbesar: **{penyakit[next(iter(hasil_urut))]}**")

st.caption("⚠️ Hasil ini bersifat pendukung, bukan pengganti diagnosis dokter.")
