import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 

df_bikeday = pd.read_csv("https://raw.githubusercontent.com/atha25/DicodingAnalisisData/refs/heads/main/Dashboard/day.csv")
df_bikehour = pd.read_csv("https://raw.githubusercontent.com/atha25/DicodingAnalisisData/refs/heads/main/Dashboard/hour.csv")

df_bikeday['dteday'] = pd.to_datetime(df_bikeday['dteday'])

def time_bin(hr):
    if hr <= 5:
        return "Dawn"
    elif hr <= 10:
        return "Morning"
    elif hr <= 15:
        return "Afternoon"
    elif hr <= 20:
        return "Evening"
    else:
        return "Midnight"

df_bikehour['Time_Period'] = df_bikehour['hr'].apply(time_bin)

# Set page title and layout
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title('Bike Sharing Analysis Dashboard')

# Add a brief introduction
st.markdown("""
Dashboard ini menyajikan analisis komprehensif terhadap data penyewaan sepeda, dengan mengeksplorasi perilaku pengguna dari berbagai perspektif seperti jenis pengguna (casual vs registered), pola penggunaan harian dan jam-an, perbedaan berdasarkan musim, kondisi cuaca, serta pembagian waktu dalam satu hari. Tujuan dari analisis ini adalah untuk mengidentifikasi tren utama dan faktor-faktor yang memengaruhi tingkat permintaan, sehingga dapat digunakan sebagai dasar dalam pengambilan keputusan berbasis data terkait perencanaan operasional, distribusi unit sepeda, strategi layanan, dan peningkatan pengalaman pengguna secara keseluruhan.
""")

# Menentukan Pertanyaan Bisnis
st.header('Business Questions')
st.markdown("""
- Apa perbedaan pola penyewaan sepeda antara Casual User dan Registered User?
- Bagaimana perbandingan atau pola dari penyewaan sepeda antar hari?
- Bagaimana jumlah penyewaan sepeda bervariasi berdasarkan musim, dan musim mana yang permintaannya paling tinggi?
""")

# Exploratory Data Analysis (EDA) 
st.header('Exploratory Data Analysis (EDA)')

# Pertanyaan 1: Casual vs Registered Users
st.subheader('Daily Bike Rentals: Casual vs Registered')
fig1, ax1 = plt.subplots(figsize=(12, 6)) 
ax1.plot(df_bikeday['dteday'], df_bikeday['casual'], label='Casual', color='blue')
ax1.plot(df_bikeday['dteday'], df_bikeday['registered'], label='Registered', color='orange')
ax1.set_xlabel('Date')
ax1.set_ylabel('Number of Rentals')
ax1.set_title('Daily Bike Rentals: Casual vs Registered')
ax1.legend()
ax1.grid(alpha=0.3)
plt.xticks(rotation=45)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d')) 
ax1.xaxis.set_major_locator(mdates.AutoDateLocator()) 
plt.tight_layout() 
st.pyplot(fig1)
st.markdown("""
**Insight:**
Pengguna registered secara konsisten jauh lebih tinggi daripada casual, menunjukkan bahwa layanan bike sharing lebih dominan digunakan untuk kebutuhan mobilitas rutin (commuting) daripada aktivitas rekreasi.
""")

# Pertanyaan 2: Average Bike Rentals by Weekday
st.subheader('Average Bike Rentals by Weekday')
fig2, ax2 = plt.subplots(figsize=(8, 5))
weekday_rentals = df_bikeday.groupby('weekday')['cnt'].mean()
ax2.bar(weekday_rentals.index, weekday_rentals.values)
ax2.set_xlabel("Weekday (0=Sunday, 1=Monday, ..., 6=Saturday)")
ax2.set_ylabel("Average Rentals")
ax2.set_title("Average Bike Rentals by Weekday")
plt.xticks(rotation=0)
plt.tight_layout()
st.pyplot(fig2)
st.markdown("""
**Insight:**
Rata-rata penyewaan relatif tinggi dan stabil sepanjang hari kerja, dengan sedikit peningkatan pada pertengahan hingga akhir minggu, menandakan penggunaan konsisten untuk rutinitas harian.
""")

# Pertanyaan 3: Average Bike Rentals by Season
st.subheader('Average Bike Rentals by Season')
fig3, ax3 = plt.subplots(figsize=(8, 5))
season_rentals = df_bikeday.groupby('season')['cnt'].mean()
ax3.bar(season_rentals.index, season_rentals.values, tick_label=["Spring", "Summer", "Fall", "Winter"])
ax3.set_xlabel("Season")
ax3.set_ylabel("Average Rentals")
ax3.set_title("Average Bike Rentals by Season")
plt.xticks(rotation=0)
plt.tight_layout()
st.pyplot(fig3)
st.markdown("""
**Insight:**
Musim Fall (musim gugur) memiliki jumlah penyewaan tertinggi, diikuti Summer dan Winter, sedangkan Spring menunjukkan penggunaan paling rendah, mencerminkan pengaruh kuat kondisi cuaca terhadap permintaan.
""")

# Average Rentals by Weather Condition
st.subheader('Average Bike Rentals by Weather Condition')
average_rentals_by_weather = df_bikeday.groupby('weathersit')['cnt'].mean()
fig5, ax5 = plt.subplots(figsize=(8, 6))
average_rentals_by_weather.plot(kind='bar', ax=ax5)
ax5.set_title('Average Bike Rentals by Weather Condition')
ax5.set_xlabel('Weather Condition (1: Clear/Partly Cloudy, 2: Mist/Cloudy, 3: Light Snow/Light Rain)')
ax5.set_ylabel('Average Rentals')
plt.xticks(rotation=0)
plt.tight_layout()
st.pyplot(fig5)
st.markdown("""
**Insight:**
Penggunaan sepeda tertinggi terjadi pada cuaca cerah dan turun drastis saat hujan, menandakan preferensi kuat pengguna untuk bersepeda saat kondisi cuaca baik.
""")


# Average Bike Rentals by Time Period
st.subheader('Average Bike Rentals by Time Period')
average_rentals_by_time_period = df_bikehour.groupby('Time_Period')['cnt'].mean().reindex(["Dawn", "Morning", "Afternoon", "Evening", "Midnight"]) 
fig6, ax6 = plt.subplots(figsize=(8, 6))
average_rentals_by_time_period.plot(kind='bar', ax=ax6)
ax6.set_title('Average Bike Rentals by Time Period')
ax6.set_xlabel('Time Period')
ax6.set_ylabel('Average Rentals')
plt.xticks(rotation=0)
plt.tight_layout()
st.pyplot(fig6)
st.markdown("""
**Insight:**
Rata-rata penyewaan sepeda tertinggi terjadi pada waktu Sore/Malam, diikuti Siang dan Pagi, menunjukkan bahwa permintaan meningkat pada jam pulang kerja dan aktivitas sore hari.
""")


# Optional: Hourly Bike Rental Pattern
st.subheader('Hourly Bike Rental Pattern')
hourly = df_bikehour.groupby('hr')['cnt'].mean()
fig4, ax4 = plt.subplots(figsize=(10, 5))
ax4.plot(hourly.index, hourly.values, marker='o', linewidth=2)
ax4.set_xlabel("Hour of Day (0–23)")
ax4.set_ylabel("Average Rentals")
ax4.set_xticks(range(0, 24))
ax4.set_title('Hourly Bike Rental Pattern')
ax4.grid(alpha=0.3)
plt.tight_layout()
st.pyplot(fig4)
st.markdown("""
**Insight:**
Rata-rata penyewaan sepeda tertinggi terjadi pada waktu Sore/Malam, diikuti Siang dan Pagi, menunjukkan bahwa permintaan meningkat pada jam pulang kerja dan aktivitas sore hari.
""")

# Conclusion
st.header('Conclusion')
st.markdown("""
- Berdasarkan grafik Daily Bike Rentals: Casual vs Registered, terlihat bahwa jumlah penyewaan oleh registered users secara konsisten jauh lebih tinggi daripada casual users pada hampir seluruh periode waktu. Registered users menunjukkan pola yang stabil dengan peningkatan signifikan pada hari kerja, menandakan penggunaan yang berkaitan dengan aktivitas rutin sehari-hari seperti commuting. Sementara itu, casual users cenderung meningkat pada akhir pekan, yang mengindikasikan penggunaan lebih banyak untuk keperluan rekreasi atau aktivitas santai.
- Grafik Average Bike Rentals by Weekday menunjukkan bahwa jumlah penyewaan relatif tinggi dan stabil sepanjang minggu, dengan sedikit peningkatan pada hari Kamis–Sabtu. Hal ini mengindikasikan bahwa penggunaan bike sharing tetap kuat sepanjang minggu, namun sedikit lebih tinggi mendekati akhir pekan, kemungkinan karena meningkatnya aktivitas rekreasi sekaligus masih kuatnya penggunaan rutin.
- Grafik Average Bike Rentals by Season menunjukkan bahwa Fall (musim gugur) memiliki jumlah rata-rata penyewaan tertinggi, diikuti Summer, kemudian Winter, sementara Spring menjadi musim dengan penyewaan terendah. Pola ini menegaskan bahwa kondisi cuaca dan kenyamanan bersepeda memainkan peran penting dalam permintaan layanan, di mana cuaca di Fall dan Summer memberikan kondisi terbaik untuk bersepeda.
""")

# Footer
st.markdown("---")

st.markdown("Created by Muhammad Athaurahman")
