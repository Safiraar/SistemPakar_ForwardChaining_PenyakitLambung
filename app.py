# =============================
# FILE: app.py
# =============================
import streamlit as st
from rules import (
    penyakit, 
    gejala,
    forward_chaining, 
    certainty_factor,
    cf_user_map
)

st.set_page_config(page_title="Sistem Pakar Penyakit Lambung", layout="wide")

# ===== Session State =====
if "page" not in st.session_state:
    st.session_state.page = "Beranda"

if "diagnosa_selesai" not in st.session_state:
    st.session_state.diagnosa_selesai = False

if "nama" not in st.session_state:
    st.session_state.nama = ""

if "usia" not in st.session_state:
    st.session_state.usia = 0

if "selected_gejala" not in st.session_state:
    st.session_state.selected_gejala = []

if "hasil" not in st.session_state:
    st.session_state.hasil = {}
    
if "cf_user" not in st.session_state:
    st.session_state.cf_user = {}


# ===== Sidebar Navigation =====
st.sidebar.title("📌 Page")
st.session_state.page = st.sidebar.radio(
    "Pilih Halaman",
    ["Beranda", "Diagnosa", "Hasil"]
)

# =============================
# PAGE 1: BERANDA
# =============================
if st.session_state.page == "Beranda":
    st.title("🩺 Sistem Pakar Deteksi Penyakit Lambung")
    st.write(
        "Sistem ini dirancang untuk membantu mendeteksi kemungkinan penyakit lambung "
        "berdasarkan gejala yang Anda rasakan. \n\n"
        "Anda akan diminta untuk memasukkan identitas singkat serta memilih gejala, "
        "kemudian sistem akan melakukan analisis menggunakan metode **Forward Chaining** dan **Certainty Factor**."
    )
    st.info("Gunakan menu di samping kiri untuk melanjutkan ke halaman Diagnosa.")

# =============================
# PAGE 2: DIAGNOSA
# =============================
elif st.session_state.page == "Diagnosa":
    st.title("📝 Input Data & Gejala")

    # =========================
    # INPUT DATA USER
    # =========================
    st.subheader("Data Pengguna")

    st.session_state.nama = st.text_input(
        "Nama",
        st.session_state.nama
    )

    st.session_state.usia = st.number_input(
        "Usia",
        min_value=0,
        max_value=120,
        value=st.session_state.usia
    )

    st.divider()

    # =========================
    # PILIH GEJALA (2 KOLOM)
    # =========================
    st.subheader("Pilih Gejala")

    col1, col2 = st.columns(2)

    # -------- KIRI: LIST GEJALA --------
    with col1:
    st.markdown("### Daftar Gejala")
    for kode, nama_gejala in gejala.items():
        checked = kode in st.session_state.selected_gejala
        if st.checkbox(nama_gejala, value=checked, key=kode):
            if kode not in st.session_state.selected_gejala:
                st.session_state.selected_gejala.append(kode)

            st.session_state.cf_user[kode] = st.selectbox(
                "Tingkat Keyakinan",
                list(cf_user_map.keys()),
                key=f"cf_{kode}"
            )
        else:
            if kode in st.session_state.selected_gejala:
                st.session_state.selected_gejala.remove(kode)
                st.session_state.cf_user.pop(kode, None)



    # -------- KANAN: RECEIPT REAL-TIME --------
    with col2:
        st.markdown("### Ringkasan")
        st.write(f"**Nama** : {st.session_state.nama}")
        st.write(f"**Usia** : {st.session_state.usia} tahun")
        st.write("**Gejala yang dipilih:**")

        if st.session_state.selected_gejala:
            for g in st.session_state.selected_gejala:
                st.write(f"- {gejala[g]}")
        else:
            st.caption("Belum ada gejala yang dipilih")

    st.divider()

    # =========================
    # TOMBOL PROSES DIAGNOSA
    # =========================
    if st.button("🔍 Proses Diagnosa"):
        if not st.session_state.nama or not st.session_state.selected_gejala:
            st.warning("Nama dan minimal satu gejala wajib diisi.")
        else:
            # 1. Forward Chaining → cari kandidat penyakit
            kandidat = forward_chaining(st.session_state.selected_gejala)
            # 2. Certainty Factor → hitung tingkat keyakinan
            st.session_state.hasil = certainty_factor(
                kandidat,
                st.session_state.selected_gejala,
                st.session_state.cf_user
            )

            st.session_state.diagnosa_selesai = True

    # =========================
    # PESAN SUKSES (DI BAWAH TOMBOL)
    # =========================
    if st.session_state.diagnosa_selesai:
        st.success(
            "✅ Berhasil melakukan diagnosa. "
            "Silakan menuju halaman **Hasil** melalui menu di sidebar."
        )

# =============================
# PAGE 3: HASIL
# =============================
elif st.session_state.page == "Hasil":
    st.title("📄 Hasil Diagnosa")

    if not st.session_state.hasil:
        st.error("Belum ada proses diagnosa.")
    else:
        hasil_urut = dict(sorted(
            st.session_state.hasil.items(),
            key=lambda x: x[1],
            reverse=True
        ))

        kode_tertinggi = next(iter(hasil_urut))

        st.subheader("Receipt")
        st.write(f"Nama : {st.session_state.nama}")
        st.write(f"Usia : {st.session_state.usia} tahun")
        st.write("Gejala:")
        for g in st.session_state.selected_gejala:
            st.write(f"- {gejala[g]}")

        st.divider()
        st.subheader("Hasil Diagnosa")
        st.success(f"Penyakit Anda : **{penyakit[kode_tertinggi]}**")
        # st.write(f"Dengan tingkat kecocokan: **{hasil_urut[kode_tertinggi]*100:.2f}%**")

        st.subheader("Detail Certainty Factor")
        for k, v in hasil_urut.items():
            st.write(f"{penyakit[k]} : {v*100:.2f}%")
            
    st.caption("⚠️ Sistem ini hanya sebagai alat bantu.")
    
st.sidebar.caption("Sistem by: Safira Aulia Rahma-4611422125")
