import streamlit as st
import time

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Animasi IEEE 754 — Konversi Pecahan ke Biner",
    page_icon="🔢",
    layout="centered"
)

# ── STYLE ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }

    .header-box {
        background: #1a1a2e;
        color: white;
        padding: 20px 28px;
        border-radius: 10px;
        margin-bottom: 24px;
    }
    .header-box h2 { color: white; margin: 0 0 4px 0; font-size: 22px; }
    .header-box p  { color: #aab4d4; margin: 0; font-size: 13px; }

    .langkah-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        animation: fadeIn 0.4s ease;
    }
    .langkah-card.active {
        border: 2px solid #0055cc;
        background: #f0f4ff;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .langkah-no {
        display: inline-block;
        background: #1a1a2e;
        color: white;
        border-radius: 50%;
        width: 28px; height: 28px;
        text-align: center;
        line-height: 28px;
        font-weight: bold;
        font-size: 13px;
        margin-right: 10px;
    }
    .langkah-no.active { background: #0055cc; }

    .operasi {
        font-family: 'Courier New', monospace;
        font-size: 16px;
        color: #333;
    }
    .hasil-pecahan { color: #555; }
    .bit-0 {
        display: inline-block;
        background: #e3f2fd;
        color: #0055cc;
        font-weight: bold;
        font-size: 18px;
        border-radius: 4px;
        padding: 2px 10px;
        font-family: monospace;
    }
    .bit-1 {
        display: inline-block;
        background: #e8f5e9;
        color: #2e7d32;
        font-weight: bold;
        font-size: 18px;
        border-radius: 4px;
        padding: 2px 10px;
        font-family: monospace;
    }

    .biner-result {
        background: #1a1a2e;
        color: white;
        border-radius: 10px;
        padding: 20px 24px;
        margin: 20px 0;
        text-align: center;
    }
    .biner-result .label { color: #aab4d4; font-size: 13px; margin-bottom: 8px; }
    .biner-result .nilai {
        font-family: 'Courier New', monospace;
        font-size: 28px;
        font-weight: bold;
        letter-spacing: 4px;
        color: #7ecfff;
    }

    .normalisasi-box {
        background: #fff8e1;
        border-left: 4px solid #f9a825;
        border-radius: 6px;
        padding: 14px 18px;
        margin: 12px 0;
    }
    .normalisasi-box h4 { color: #e65100; margin: 0 0 8px 0; font-size: 14px; }
    .normalisasi-box p  { margin: 4px 0; font-family: monospace; font-size: 15px; }

    .ieee-box {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 18px 22px;
        margin: 12px 0;
    }
    .ieee-row {
        display: flex;
        align-items: center;
        margin: 8px 0;
        font-family: monospace;
        font-size: 14px;
    }
    .ieee-label {
        width: 90px;
        font-weight: bold;
        color: #1a1a2e;
    }
    .ieee-sign     { background: #fce4ec; color: #c62828; padding: 4px 10px; border-radius: 4px; font-weight: bold; }
    .ieee-exp      { background: #e8eaf6; color: #283593; padding: 4px 10px; border-radius: 4px; font-weight: bold; letter-spacing: 2px; }
    .ieee-mantissa { background: #e8f5e9; color: #1b5e20; padding: 4px 10px; border-radius: 4px; font-weight: bold; letter-spacing: 1px; font-size: 12px; }
    .ieee-final    {
        background: #1a1a2e;
        color: #7ecfff;
        padding: 10px 16px;
        border-radius: 8px;
        font-size: 13px;
        letter-spacing: 2px;
        margin-top: 10px;
        text-align: center;
        font-family: monospace;
    }

    .footer {
        text-align: center;
        color: #aaa;
        font-size: 12px;
        margin-top: 40px;
        padding-top: 16px;
        border-top: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# ── FUNGSI KONVERSI ────────────────────────────────────────────────────────────
def konversi_pecahan(nilai):
    """Hitung langkah-langkah konversi pecahan desimal ke biner via ×2"""
    langkah = []
    sisa = nilai
    maks = 23  # max bit mantissa IEEE 754
    while sisa > 0 and len(langkah) < maks:
        hasil  = sisa * 2
        bit    = int(hasil)
        sisa   = hasil - bit
        langkah.append({
            "input"  : round(sisa + bit - bit + (hasil - bit + bit - bit), 10),
            "operasi": f"{round(sisa + bit - (hasil - bit), 10)} × 2 = {round(hasil, 10)}",
            "input_val": round(hasil - bit + (bit * 0), 10),
            "hasil"  : round(hasil, 10),
            "bit"    : bit,
            "sisa"   : round(sisa, 10),
        })
        # Simpan nilai input sebelum perkalian
        langkah[-1]["input_val"] = round(nilai if len(langkah) == 1 else
                                          langkah[-2]["sisa"], 10)
        langkah[-1]["operasi"]   = f"{langkah[-1]['input_val']} × 2 = {round(hasil, 10)}"
        if sisa == 0:
            break
    return langkah

def normalisasi(biner_str, nilai_asli):
    """Normalisasi biner pecahan ke bentuk 1.xxx × 2^n"""
    if "." not in biner_str:
        return biner_str, 0
    # Cari posisi '1' pertama
    bagian = biner_str.replace("0.", "")
    geser  = 0
    for i, c in enumerate(bagian):
        if c == "1":
            geser = -(i + 1) if nilai_asli < 1 else i
            mantissa = bagian[i+1:]
            break
    else:
        return biner_str, 0
    return mantissa, geser

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <h2>🔢 Animasi Konversi Pecahan ke IEEE 754</h2>
    <p>Arsitektur dan Organisasi Komputer</p>
</div>
""", unsafe_allow_html=True)

# ── INPUT ─────────────────────────────────────────────────────────────────────
st.markdown("**Masukkan bilangan pecahan desimal yang ingin dikonversi:**")

col1, col2 = st.columns([3, 1])
with col1:
    nilai = st.number_input(
        "Nilai (contoh: 0.15625, 0.375, 0.1)",
        min_value=0.0, max_value=1.0,
        value=0.15625, step=0.001,
        format="%.5f"
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    mulai = st.button("▶  Mulai", use_container_width=True, type="primary")

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "langkah_tampil" not in st.session_state:
    st.session_state.langkah_tampil = 0
if "nilai_terakhir" not in st.session_state:
    st.session_state.nilai_terakhir = nilai
if "langkah_data" not in st.session_state:
    st.session_state.langkah_data = []
if "selesai" not in st.session_state:
    st.session_state.selesai = False

# Reset kalau nilai berubah atau tombol mulai ditekan
if mulai or nilai != st.session_state.nilai_terakhir:
    st.session_state.langkah_tampil = 0
    st.session_state.nilai_terakhir = nilai
    st.session_state.langkah_data   = konversi_pecahan(nilai)
    st.session_state.selesai        = False
    st.rerun()

langkah_data  = st.session_state.langkah_data
langkah_tampil = st.session_state.langkah_tampil

if not langkah_data:
    st.info("Klik **▶ Mulai** untuk memulai animasi.")
    st.stop()

st.divider()
st.markdown("### Langkah-langkah Konversi (×2)")
st.caption("💡 Klik **Langkah Berikutnya** untuk maju satu langkah sekaligus.")

# ── TAMPILKAN LANGKAH ─────────────────────────────────────────────────────────
for i in range(langkah_tampil):
    lk  = langkah_data[i]
    bit = lk["bit"]
    bit_html = f'<span class="bit-{"1" if bit==1 else "0"}">{bit}</span>'
    aktif = "active" if i == langkah_tampil - 1 else ""
    no_html = f'<span class="langkah-no {aktif}">{i+1}</span>'

    st.markdown(f"""
    <div class="langkah-card {aktif}">
        {no_html}
        <span class="operasi">{lk['operasi']}</span>
        &nbsp;&nbsp;→&nbsp;&nbsp;
        Bagian bulat: {bit_html}
        &nbsp;&nbsp;
        <span style="color:#888;font-size:13px;">sisa: {lk['sisa']}</span>
    </div>
    """, unsafe_allow_html=True)

# ── KONTROL ───────────────────────────────────────────────────────────────────
if langkah_tampil < len(langkah_data) and not st.session_state.selesai:
    col_a, col_b = st.columns([2, 1])
    with col_a:
        if st.button("⏩  Langkah Berikutnya", use_container_width=True):
            st.session_state.langkah_tampil += 1
            if st.session_state.langkah_tampil == len(langkah_data):
                st.session_state.selesai = True
            st.rerun()
    with col_b:
        if st.button("⏭  Tampilkan Semua", use_container_width=True):
            st.session_state.langkah_tampil = len(langkah_data)
            st.session_state.selesai = True
            st.rerun()

# ── HASIL AKHIR ───────────────────────────────────────────────────────────────
if langkah_tampil == len(langkah_data):
    bits = "".join(str(lk["bit"]) for lk in langkah_data)
    biner_str = f"0.{bits}"

    st.divider()

    # Hasil biner
    st.markdown(f"""
    <div class="biner-result">
        <div class="label">Hasil Konversi Biner</div>
        <div class="nilai">{biner_str}</div>
        <div style="color:#aab4d4;font-size:13px;margin-top:6px;">
            Baca bagian bulat dari atas ke bawah: {' → '.join(str(lk['bit']) for lk in langkah_data)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Normalisasi
    mantissa_raw, eksponen = normalisasi(biner_str, nilai)
    mantissa_pad = (mantissa_raw + "0" * 23)[:23]

    st.markdown(f"""
    <div class="normalisasi-box">
        <h4>📐 Normalisasi</h4>
        <p>{biner_str} = <strong>1.{mantissa_raw} × 2<sup>{eksponen}</sup></strong></p>
        <p style="color:#888;font-size:12px;">
            Geser titik desimal ke kanan sampai tersisa satu angka di depan titik
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Komponen IEEE 754
    bias     = 127
    exp_val  = eksponen + bias
    exp_bin  = bin(exp_val)[2:].zfill(8)
    sign_bit = "0" if nilai >= 0 else "1"

    st.markdown("### 🗂 Komponen IEEE 754 Single Precision")
    st.markdown(f"""
    <div class="ieee-box">
        <div class="ieee-row">
            <span class="ieee-label">Sign</span>
            <span class="ieee-sign">&nbsp;{sign_bit}&nbsp;</span>
            <span style="color:#888;font-size:12px;margin-left:12px;">
                {'positif → 0' if sign_bit=='0' else 'negatif → 1'}
            </span>
        </div>
        <div class="ieee-row">
            <span class="ieee-label">Exponent</span>
            <span class="ieee-exp">{exp_bin}</span>
            <span style="color:#888;font-size:12px;margin-left:12px;">
                {eksponen} + 127 (bias) = {exp_val} = {exp_bin}₂
            </span>
        </div>
        <div class="ieee-row">
            <span class="ieee-label">Mantissa</span>
            <span class="ieee-mantissa">{mantissa_pad}</span>
            <span style="color:#888;font-size:12px;margin-left:12px;">
                bagian setelah '1.' → pad nol sampai 23 bit
            </span>
        </div>
        <div class="ieee-final">
            {sign_bit} &nbsp; {exp_bin} &nbsp; {mantissa_pad}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tombol ulangi
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄  Coba Nilai Lain", use_container_width=True):
        st.session_state.langkah_tampil = 0
        st.session_state.langkah_data   = []
        st.session_state.selesai        = False
        st.rerun()

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Arismunandar, M.T.I. &nbsp;·&nbsp; Arsitektur dan Organisasi Komputer &nbsp;·&nbsp; STTI NIIT Jakarta
</div>
""", unsafe_allow_html=True)
