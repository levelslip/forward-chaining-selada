import streamlit as st
import json
from utils.inference import forward_chaining

# --- Load data ---
with open("data/gejala.json", encoding="utf-8") as f:
    gejala = json.load(f)
with open("data/penyakit.json", encoding="utf-8") as f:
    penyakit = json.load(f)
with open("data/rules.json", encoding="utf-8") as f:
    rules = json.load(f)

# --- Konfigurasi halaman ---
st.set_page_config(
    page_title="Sistem Pakar Selada",
    page_icon="🌿",
    layout="centered"
)

# --- Header ---
st.title("🌿 Sistem Pakar Deteksi Penyakit Tanaman Selada")
st.markdown("""
Gunakan sistem ini untuk mengetahui penyakit berdasarkan gejala tanaman selada.
Pilih gejala-gejala yang muncul pada tanaman, kemudian klik tombol **Diagnosa**.
""")

st.divider()

# --- Sidebar Info ---
with st.sidebar:
    st.header("ℹ️ Informasi Sistem")
    st.markdown("""
    **Metode:** Forward Chaining
    
    **Jumlah Gejala:** 18
    
    **Jumlah Penyakit:** 7
    
    **Penyakit yang dapat dideteksi:**
    - P01: Busuk lunak
    - P02: Busuk batang
    - P03: Busuk pangkal daun
    - P04: Mata kodok
    - P05: Layu Fusarium
    - P06: Busuk akar
    - P07: Layu bakteri
    """)

# --- Input gejala ---
st.subheader("📋 Pilih Gejala")
selected = st.multiselect(
    "Pilih gejala yang muncul pada tanaman selada:",
    options=list(gejala.keys()),
    format_func=lambda x: f"{x}: {gejala[x]}",
    help="Anda dapat memilih lebih dari satu gejala"
)

# Tampilkan gejala yang dipilih
if selected:
    st.info(f"**Gejala yang dipilih:** {len(selected)} gejala")
    for g in selected:
        st.write(f"- **{g}:** {gejala[g]}")

st.divider()

# --- Tombol Diagnosa ---
if st.button("🔍 Diagnosa", type="primary", use_container_width=True):
    if not selected:
        st.error("⚠️ Silakan pilih minimal satu gejala terlebih dahulu!")
    else:
        with st.spinner("Sedang menganalisis gejala..."):
            hasil = forward_chaining(selected, rules)
        
        if hasil:
            st.success(f"✅ **Hasil Diagnosa**")
            st.markdown(f"""
            ### Tanaman kemungkinan terkena penyakit:
            ## 🦠 {penyakit[hasil]} ({hasil})
            """)
            
            # Tampilkan rule yang cocok
            for rule in rules:
                if rule["then"] == hasil:
                    st.info("**Berdasarkan kombinasi gejala:**")
                    for g in rule["if"]:
                        if g in selected:
                            st.write(f"✓ {g}: {gejala[g]}")
                    break
        else:
            st.warning("⚠️ Tidak ditemukan penyakit yang cocok dengan kombinasi gejala tersebut.")
            st.markdown("""
            **Saran:**
            - Pastikan semua gejala yang relevan sudah dipilih
            - Periksa kembali kondisi tanaman
            - Konsultasikan dengan ahli pertanian jika diperlukan
            """)

# --- Footer ---
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8em;'>
    <p>Sistem Deteksi Penyakit Tanaman Selada</p>
    <p>Menggunakan Metode Forward Chaining</p>
</div>
""", unsafe_allow_html=True)
