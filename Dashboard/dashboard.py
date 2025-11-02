import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.set_page_config(page_title="🚲 Bike Sharing Dashboard", layout="wide")

st.markdown("""
<style>
#MainMenu, footer {visibility: hidden;}
body {background-color: #0f1116;}

.title-box {
    background:#0b0d12; padding:24px; border-radius:12px; color:white;
    margin-bottom:18px; border:1px solid #1f2937;
}
.kpi-box {
    background:#111318; padding:26px; border-radius:14px; border:1px solid #1f2937;
    text-align:center; box-shadow:0 2px 10px rgba(0,0,0,0.4);
}
.kpi-title { font-size:14px; color:#8b96a7; margin-bottom:6px; }
.kpi-value { font-size:30px; font-weight:700; color:#00eaff; text-shadow:0 0 8px rgba(0,234,255,.55); }

.section-title { font-size:18px; font-weight:600; color:white; margin-top:15px; margin-bottom:5px; }

.card {
    background:#111318; padding:18px; border-radius:12px; border:1px solid #1f2937;
    box-shadow:0 2px 12px rgba(0,0,0,.45);
}
.insight {
    background:#0e1726; padding:18px 20px; border-radius:12px;
    font-size:17px; line-height:1.6; color:#d1e9ff; border:1px solid #1e293b; margin-top:8px;
}
.insight b{color:#fff}
.badge{display:inline-block;background:#13223a;border:1px solid #1e3a5f;color:#a5d8ff;
       border-radius:999px;padding:2px 10px;margin-right:6px;font-size:12px}
</style>
""", unsafe_allow_html=True)

plt.rcParams.update({
    "text.color": "white",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "axes.edgecolor": "#334155"
})

st.markdown(
    '<div class="title-box"><h2>🚲 Bike Sharing Analytics Dashboard</h2>'
    '<div>Daily & Hourly Demand • Seasonality • Patterns • Manual Segmentation</div></div>',
    unsafe_allow_html=True
)

DAY_URL  = "https://raw.githubusercontent.com/atha25/DicodingAnalisisData/refs/heads/main/Dashboard/day.csv"
HOUR_URL = "https://raw.githubusercontent.com/atha25/DicodingAnalisisData/refs/heads/main/Dashboard/hour.csv"

@st.cache_data
def load_data():
    df_day  = pd.read_csv(DAY_URL)
    df_hour = pd.read_csv(HOUR_URL)
    df_day["dteday"]  = pd.to_datetime(df_day["dteday"], errors="coerce")
    df_hour["dteday"] = pd.to_datetime(df_hour["dteday"], errors="coerce")
    season = {1:"Spring",2:"Summer",3:"Fall",4:"Winter"}
    weekday = {0:"Sun",1:"Mon",2:"Tue",3:"Wed",4:"Thu",5:"Fri",6:"Sat"}
    df_day["season_lbl"]  = df_day["season"].map(season)
    df_day["weekday_lbl"] = df_day["weekday"].map(weekday)
    df_hour["season_lbl"]  = df_hour["season"].map(season)
    df_hour["weekday_lbl"] = df_hour["weekday"].map(weekday)
    return df_day, df_hour

df_day, df_hour = load_data()

total_rent = int(df_day["cnt"].sum())
avg_daily  = float(df_day["cnt"].mean())
peak_date  = df_day.loc[df_day["cnt"].idxmax(), "dteday"].date()

col1, col2, col3 = st.columns(3)
col1.markdown(f'<div class="kpi-box"><div class="kpi-title">Total Rentals</div><div class="kpi-value">{total_rent:,}</div></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="kpi-box"><div class="kpi-title">Avg Daily Rentals</div><div class="kpi-value">{avg_daily:,.0f}</div></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="kpi-box"><div class="kpi-title">Peak Day</div><div class="kpi-value">{peak_date}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">📅 Daily Trend</div>', unsafe_allow_html=True)

colA, colB = st.columns([3,1])  
with colA:
    
    df_day["smooth"] = df_day["cnt"].rolling(window=7, center=True, min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(9.5, 3.8), dpi=140)
    ax.plot(df_day["dteday"], df_day["cnt"], color="#3b82f6", linewidth=1.2, alpha=0.55, label="Daily")
    ax.plot(df_day["dteday"], df_day["smooth"], color="#00eaff", linewidth=2.2, label="7D Avg")

    
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

    
    ax.grid(alpha=0.25)
    ax.set_ylabel("Rentals", fontsize=10, color="white")
    ax.set_xlabel("")
    ax.tick_params(axis='x', rotation=45, labelsize=9, colors="white")
    ax.tick_params(axis='y', colors="white")
    ax.set_facecolor("#0b0d12")
    fig.patch.set_facecolor("#0b0d12")
    for spine in ax.spines.values():
        spine.set_color("#334155")
    ax.legend(frameon=False, loc="upper left", labelcolor="white")

    st.pyplot(fig)

with colB:
    st.markdown(f"""
    <div class="insight">
    🔍 <b>Insight:</b><br>
    • Pola musiman jelas: naik ke <b>musim panas</b>, turun di <b>musim dingin</b>.<br>
    • Garis <b>7-day average</b> memperhalus noise harian sehingga tren mudah dibaca.<br>
    • Hari puncak: <b>{df_day.loc[df_day["cnt"].idxmax(), "dteday"].date()}</b>.
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-title">👥 Casual vs Registered</div>', unsafe_allow_html=True)
colA, colB = st.columns([2,1])

with colA:
    avg_users = df_day[["casual","registered"]].mean()
    fig, ax = plt.subplots(figsize=(5,3))
    bars = ax.bar(["Casual","Registered"], avg_users, color=["#14b8a6","#6366f1"])
    for i,v in enumerate(avg_users):
        ax.text(i, v+50, f"{v:.0f}", ha="center", fontsize=11)
    ax.set_ylabel("Avg Users", fontsize=10)
    st.pyplot(fig)

with colB:
    reg_ratio = (avg_users["registered"] / max(avg_users["casual"],1))
    st.markdown(f"""
    <div class="insight">
    👤 <b>Insight:</b><br>
    • Pengguna registered secara konsisten jauh lebih tinggi daripada casual, menunjukkan bahwa layanan bike sharing lebih dominan digunakan untuk kebutuhan mobilitas rutin (commuting) daripada aktivitas rekreasi.
    """, unsafe_allow_html=True)

st.markdown('<div class="section-title">⏱️ Hourly Pattern</div>', unsafe_allow_html=True)
colA, colB = st.columns([2,1])

with colA:
    df_hour_group = df_hour.groupby("hr")["cnt"].mean()
    fig, ax = plt.subplots(figsize=(5.5,3))
    ax.plot(df_hour_group.index, df_hour_group.values, marker="o", color="#e11d48")
    ax.grid(alpha=0.25); ax.set_xlabel("Hour", fontsize=10); ax.set_ylabel("Avg Rentals", fontsize=10)
    st.pyplot(fig)

with colB:
    peak_hr = int(df_hour_group.idxmax())
    st.markdown(f"""
    <div class="insight">
    🕒 <b>Insight:</b><br>
    • Puncak jelas di jam <b>07–09</b> & <b>17–19</b> (komuter).<br>
    • Lakukan <b>redistribusi sepeda</b> sebelum puncak & tambah petugas lapangan saat periode ini.<br>
    • <b>Outlier</b> di data <i>hour.csv</i> mengindikasikan lonjakan/penurunan ekstrem (rush hour/cuaca ekstrem).
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-title">📊 Average Rentals by Weekday</div>', unsafe_allow_html=True)

weekday_map = {
    0: "Sun", 1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat"
}
df_day["weekday_name"] = df_day["weekday"].map(weekday_map)

weekday_avg = df_day.groupby("weekday_name")["cnt"].mean().reindex(["Sun","Mon","Tue","Wed","Thu","Fri","Sat"])

colA, colB = st.columns([2,1])

with colA:
    fig, ax = plt.subplots(figsize=(6,3))

    bars = ax.bar(weekday_avg.index, weekday_avg.values, color="#0ea5e9")

    
    for i, v in enumerate(weekday_avg):
        ax.text(i, v + 50, f"{v:.0f}", ha="center", fontsize=12, color="white", fontweight="bold")

    ax.set_facecolor("#0b0d12")
    fig.patch.set_facecolor("#0b0d12")
    ax.grid(alpha=0.2, linestyle="--")
    ax.set_ylabel("Avg Rentals", fontsize=10, color="white")
    ax.set_xlabel("Day of Week", fontsize=10, color="white")

    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_color("#334155")

    st.pyplot(fig)

with colB:
    st.markdown("""
    <div class="insight" style="font-size:16px;">
    📌 <b>Insight:</b><br>
    Jumlah sewa meningkat pada hari kerja, terutama Jumat — menunjukkan pola mobilitas pekerja. 
    Akhir pekan tetap tinggi, tetapi sedikit lebih rendah dari hari kerja.
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-title">⌛ Time Segments (Manual Binning)</div>', unsafe_allow_html=True)
colA, colB = st.columns([2,1])

with colA:
    df_bin = df_hour.copy()
    def time_bin(h):
        return ("Subuh" if h<=5 else "Pagi" if h<=10 else
                "Siang" if h<=15 else "Sore" if h<=20 else "Malam")
    df_bin["period"] = df_bin["hr"].apply(time_bin)
    
    order = pd.CategoricalDtype(categories=["Subuh","Pagi","Siang","Sore","Malam"], ordered=True)
    df_bin["period"] = df_bin["period"].astype(order)
    period_avg = df_bin.groupby("period")["cnt"].mean()

    fig, ax = plt.subplots(figsize=(5.5,3))
    bars = ax.bar(period_avg.index.astype(str), period_avg.values, color="#9333ea")
    for i,v in enumerate(period_avg):
        ax.text(i, v+20, f"{v:.0f}", ha="center", fontsize=11)
    st.pyplot(fig)

with colB:
    top_seg = period_avg.idxmax()
    st.markdown(f"""
    <div class="insight">
    🌇 <b>Insight:</b><br>
    • Permintaan tertinggi pada periode <b>{top_seg}</b> — cocok untuk <b>promo time-based</b> & penambahan unit sementara.<br>
    • Periode <b>Subuh</b> dan <b>Tengah Malam</b> relatif rendah → jadwalkan <b>maintenance</b> di waktu ini.
    </div>
    """, unsafe_allow_html=True)

st.markdown("### 🧠 Additional Insights (EDA)")

st.markdown("""
<div style="background:#0b1220; padding:18px; border-radius:10px; border:1px solid #1e293b;">

<span style="background:#1e40af; padding:4px 10px; border-radius:20px; color:white; font-size:12px;">Outlier</span> 
<b>hour.csv</b> memiliki outlier → indikasi jam sibuk / kondisi cuaca ekstrem menimbulkan lonjakan/penurunan tajam.<br><br>

<span style="background:#1e40af; padding:4px 10px; border-radius:20px; color:white; font-size:12px;">Stable</span> 
<b>day.csv</b> relatif stabil → tren harian halus tanpa fluktuasi ekstrem signifikan.<br><br>

<span style="background:#0369a1; padding:4px 10px; border-radius:20px; color:white; font-size:12px;">Season</span> 
Rata-rata sewa tertinggi pada <b>musim Fall</b> (kemarau menuju gugur).<br><br>

<span style="background:#0d9488; padding:4px 10px; border-radius:20px; color:white; font-size:12px;">Weekday</span> 
<b>Hari Jumat</b> menjadi hari dengan sewa tertinggi — mencerminkan pola komuter.<br><br>
<span style="background:#64748b; padding:4px 10px; border-radius:20px; color:white; font-size:12px;">Quality</span> 
Dataset bersih: <b>tidak ada nilai Null</b> & <b>tanpa duplikat signifikan</b> (berdasarkan pemeriksaan EDA).<br>

</div>
""", unsafe_allow_html=True)

