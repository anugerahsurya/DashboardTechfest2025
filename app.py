import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

st.markdown("""
    <style>
    /* 🌿 Warna sidebar */
    [data-testid="stSidebar"] {
        background-color: #4682B4;
    }

    /* ✅ Bungkus teks panjang */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    .stRadio > div,
    .stSelectbox > div {
        white-space: normal !important;
        word-break: break-word !important;
    }

    /* 🧩 Ubah selectbox agar bisa menampilkan teks panjang */
    .stSelectbox div[data-baseweb="select"] {
        max-width: none !important;
    }
    .stSelectbox .css-1xc3v61-singleValue {
        white-space: normal !important;
        text-overflow: initial !important;
        overflow-wrap: break-word !important;
        line-height: 1.3 !important;
    }

    /* 🎯 Styling tombol sidebar (opsional) */
    .sidebar .stButton button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px;
        margin-top: 5px;
        border: none;
        font-size: 16px;
    }

    .sidebar .stButton button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)



# ======================================
# Judul halaman utama
st.title("Efektivitas Penyaluran Dana Transfer ke Daerah (TKDD): Studi Perbandingan Pagu dan Realisasi TKDD di Provinsi-Provinsi Indonesia Tahun 2023")

# Sidebar menu
st.sidebar.title("DATA ANALYTICS - TECHNOLOGY FESTIVAL (TECHFEST) 2025")
# Ganti radio menjadi selectbox
menu = st.sidebar.selectbox(
    "Pokok Bahasan Analisis",
    [
        "Perbandingan Pagu dan Realisasi TKDD",
        "Persentase Realisasi TKDD per Provinsi (2023)",
        "Faktor Realisasi TKDD",
        "Hubungan Realisasi TKDD dan IPM",
        "Analisis Faktor-faktor yang Mempengaruhi IPM"
    ]
)

st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

# Identitas tim
st.sidebar.markdown("""---""")
st.sidebar.markdown("""
**Disusun oleh:**  

**Tim PopCorn**  
Anugerah Surya Atmaja  
Naufal Fadli Muzakki
""")
# ======================================
# Footer Identitas
st.markdown("""---""")


# ======================================
# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Data/DataTKDD.csv")
    return df

data_clean_tkdd = load_data()

# ======================================
# Halaman Ringkasan Data
if menu == "Perbandingan Pagu dan Realisasi TKDD":
    st.subheader("Perbandingan Pagu dan Realisasi TKDD Antar Provinsi")

    # Hitung persentase jika belum ada
    if 'Persentase Realisasi TKDD' not in data_clean_tkdd.columns:
        data_clean_tkdd['Persentase Realisasi TKDD'] = (
            data_clean_tkdd['Realisasi TKDD'] / data_clean_tkdd['Pagu TKDD']
        ) * 100

    # Urutkan data
    df_sorted = data_clean_tkdd.sort_values(by='Persentase Realisasi TKDD', ascending=False).copy()

    # ========== 1. Clustered Bar Chart ==========
    fig1, ax1 = plt.subplots(figsize=(14, 6))
    bar_width = 0.4
    index = np.arange(len(df_sorted))

    ax1.bar(index, df_sorted['Pagu TKDD'], bar_width, label='Pagu TKDD')
    ax1.bar(index + bar_width, df_sorted['Realisasi TKDD'], bar_width, label='Realisasi TKDD')

    ax1.set_xlabel('Provinsi')
    ax1.set_ylabel('Nilai (Rp)')
    ax1.set_title('Perbandingan Pagu dan Realisasi TKDD per Provinsi')
    ax1.set_xticks(index + bar_width / 2)
    ax1.set_xticklabels(df_sorted['Provinsi'], rotation=90)
    ax1.legend()
    plt.tight_layout()
    st.pyplot(fig1)

    st.markdown("""
    ### Penjelasan Visualisasi Pagu dan Realisasi TKDD

    Berdasarkan **grouped bar chart** perbandingan antara **Pagu TKDD** dan **Realisasi TKDD** di setiap provinsi di Indonesia tahun **2023**, terlihat bahwa sebagian besar provinsi mampu merealisasikan dana TKDD dengan cukup baik, di mana nilai realisasi mendekati atau bahkan sedikit melampaui pagu yang telah ditetapkan.

    Hal ini mencerminkan **efektivitas penyerapan anggaran** di banyak daerah, terutama di provinsi-provinsi besar seperti:
    - **Jawa Barat**
    - **Jawa Timur**
    - **Jawa Tengah**
    - **Sumatera Utara**

    yang juga mendapatkan alokasi dana tertinggi.

    Namun demikian, terdapat beberapa provinsi yang menunjukkan **selisih cukup besar** antara pagu dan realisasi, seperti:
    - **DKI Jakarta**
    - **Kalimantan Selatan**
    - Beberapa provinsi baru di **Papua**

    Kondisi ini dapat mengindikasikan adanya kendala dalam serapan anggaran, yang mungkin disebabkan oleh:
    - Kapasitas kelembagaan yang masih terbatas
    - Kondisi geografis yang sulit dijangkau
    - Proses administrasi yang belum optimal

    Di sisi lain, terdapat provinsi yang realisasinya **melebihi pagu**, seperti:
    - **Aceh**
    - **Sumatera Selatan**

    yang menunjukkan adanya kemungkinan **penyesuaian atau tambahan anggaran di tengah tahun**.

    **Kesimpulan:**  
    Besarnya pagu tidak selalu berbanding lurus dengan realisasi. Oleh karena itu, efektivitas penggunaan anggaran tetap menjadi isu penting dalam **pemerataan pembangunan di tingkat daerah**.
    """)

    # ========== 2. Stacked Bar Chart 100% ==========
    st.subheader("Perbandingan Pagu dan Realisasi TKDD untuk Setiap Wilayah")

    total = df_sorted['Pagu TKDD'] + df_sorted['Realisasi TKDD']
    df_sorted['Pagu (%)'] = df_sorted['Pagu TKDD'] / total * 100
    df_sorted['Realisasi (%)'] = df_sorted['Realisasi TKDD'] / total * 100

    fig2, ax2 = plt.subplots(figsize=(14, 6))
    index = np.arange(len(df_sorted))
    bar_width = 0.6

    ax2.bar(index, df_sorted['Pagu (%)'], bar_width, label='Pagu TKDD')
    ax2.bar(index, df_sorted['Realisasi (%)'], bar_width, bottom=df_sorted['Pagu (%)'], label='Realisasi TKDD')

    ax2.set_xticks(index)
    ax2.set_xticklabels(df_sorted['Provinsi'], rotation=90)
    ax2.set_ylabel('Persentase (%)')
    ax2.set_title('Stacked Bar Chart 100%: Pagu vs Realisasi TKDD per Provinsi')
    ax2.legend()
    plt.tight_layout()
    st.pyplot(fig2)

    st.markdown("""
    ### Penjelasan Visualisasi Proporsi Pagu dan Realisasi TKDD

    Berdasarkan *stacked bar chart* yang menunjukkan perbandingan persentase Pagu TKDD dan Realisasi TKDD per provinsi tahun 2023, didapatkan gambaran mengenai proporsi serapan anggaran di seluruh provinsi Indonesia.

    Terlihat bahwa sebagian besar provinsi memiliki rasio realisasi terhadap pagu yang cukup seimbang, di mana proporsi realisasi mendekati atau hanya sedikit di bawah alokasi pagu.

    Tidak terdapat perbedaan ekstrem antarprovinsi dalam hal proporsi serapan, yang mengindikasikan bahwa secara umum, pemerintah daerah mampu menyerap dana TKDD secara relatif konsisten di berbagai wilayah.

    Namun demikian, masih terdapat beberapa provinsi yang menunjukkan porsi realisasi sedikit lebih rendah dibandingkan pagu, terutama di beberapa provinsi Papua dan Kalimantan. Hal ini bisa disebabkan oleh keterbatasan kapasitas fiskal, hambatan geografis, atau tantangan dalam implementasi program.

    Sebaliknya, terdapat juga provinsi yang menunjukkan keseimbangan hampir sempurna atau bahkan realisasi yang sedikit lebih tinggi dari pagu. Ini mencerminkan efisiensi pelaksanaan anggaran atau adanya penyesuaian alokasi di tengah tahun.

    **Kesimpulan:**  
    Meskipun alokasi anggaran bervariasi antarprovinsi, tingkat serapan dana cenderung relatif seragam. Namun, tetap terdapat ruang untuk perbaikan, terutama di wilayah dengan tantangan geografis dan fiskal, guna meningkatkan efektivitas pelaksanaan anggaran secara nasional.
    """)
   

elif menu == "Persentase Realisasi TKDD per Provinsi (2023)":
    st.subheader("Persentase Realisasi TKDD per Provinsi (2023)")

    # Load data jika belum
    @st.cache_data
    def load_data_tkdd():
        return pd.read_csv("Data/DataTKDD.csv")

    data_clean_tkdd = load_data_tkdd()

    # Hitung persentase jika belum ada
    if 'Persentase Realisasi TKDD' not in data_clean_tkdd.columns:
        data_clean_tkdd['Persentase Realisasi TKDD'] = (
            data_clean_tkdd['Realisasi TKDD'] / data_clean_tkdd['Pagu TKDD']
        ) * 100

    import matplotlib.pyplot as plt
    import seaborn as sns

    df_sorted = data_clean_tkdd.sort_values(by='Persentase Realisasi TKDD', ascending=False).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(12, 10))
    sns.barplot(
        y='Provinsi',
        x='Persentase Realisasi TKDD',
        data=df_sorted,
        color='skyblue',
        ax=ax
    )

    # Tambahkan anotasi nilai persentase
    for index, row in df_sorted.iterrows():
        ax.text(
            row['Persentase Realisasi TKDD'] + 0.5,
            index,
            f"{row['Persentase Realisasi TKDD']:.1f}%",
            va='center'
        )

    ax.set_xlabel('Persentase Realisasi TKDD')
    ax.set_ylabel('Provinsi')
    ax.set_title('Persentase Realisasi TKDD per Provinsi (2023)\nDiurutkan dari Tertinggi ke Terendah')
    ax.set_xlim(0, max(df_sorted['Persentase Realisasi TKDD'].max() * 1.1, 105))
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("""
### Penjelasan Visualisasi Persentase Realisasi TKDD per Provinsi

Berdasarkan visualisasi persentase realisasi TKDD per provinsi tahun 2023, provinsi dengan tingkat realisasi tertinggi adalah **Kalimantan Timur** yang mencapai **111,0%** dari pagu anggaran. Disusul oleh **Kalimantan Selatan (110,6%)** dan **Kepulauan Riau (109,8%)**. Tingginya tingkat realisasi di provinsi-provinsi ini menunjukkan kemampuan mereka dalam menyerap anggaran secara optimal bahkan melampaui target yang ditetapkan, yang bisa mencerminkan tingginya kebutuhan fiskal atau efisiensi dalam pengelolaan anggaran.

Sementara itu, beberapa provinsi menunjukkan tingkat realisasi yang jauh lebih rendah dibandingkan provinsi lainnya. Provinsi dengan realisasi terendah adalah **Papua** dengan capaian **94,3%**, diikuti oleh **Papua Selatan (94,6%)** dan **Papua Pegunungan (94,7%)**. Tingkat realisasi yang rendah ini dapat mengindikasikan adanya kendala dalam pelaksanaan program, keterbatasan infrastruktur, atau hambatan administratif yang mempengaruhi serapan anggaran di wilayah-wilayah tersebut.

Menariknya, terdapat juga provinsi yang merealisasikan anggarannya tepat **100%** sesuai dengan pagu yang dialokasikan, yaitu **Sumatera Utara**. Pencapaian ini mencerminkan perencanaan dan pelaksanaan anggaran yang presisi dan stabil, tanpa kelebihan maupun kekurangan dana yang signifikan.

**Kesimpulan:**  
Perbandingan ini menunjukkan bahwa meskipun mayoritas provinsi mampu merealisasikan dana TKDD mendekati atau bahkan melebihi pagu, terdapat variasi antarwilayah yang perlu diperhatikan untuk meningkatkan pemerataan efektivitas serapan anggaran di seluruh Indonesia.
""")

    


elif menu == "Faktor Realisasi TKDD":
    st.subheader("Analisis Hubungan Realisasi TKDD dengan Variabel Ekonomi")

    # Load data jika belum
    @st.cache_data
    def load_data_all():
        return pd.read_csv("Data/DataKeseluruhan.csv")

    data_clean_all = load_data_all()

    # 1. Scatterplot Grid
    st.write("### Scatter Plot: Realisasi TKDD terhadap Variabel Lain")
    variabels = [
        'IPM',
        'Pagu TKDD',
        'Jumlah Penduduk',
        'Anggaran APBN per kapita',
        'Persentase Penduduk Miskin',
        'Produk Domestik Regional Bruto (PDRB) Atas Dasar Harga Berlaku',
        'Produk Domestik Regional Bruto per Kapita HB',
        'Laju Pertumbuhan PDRB atas dasar konstan 2010'
    ]

    fig1 = plt.figure(figsize=(20, 20))
    for i, var in enumerate(variabels):
        plt.subplot(3, 3, i+1)
        sns.scatterplot(data=data_clean_all, x=var, y='Realisasi TKDD')
        plt.title(f'{var} vs Realisasi TKDD')
        plt.xlabel(var)
        plt.ylabel('Realisasi TKDD')
    plt.tight_layout()
    st.pyplot(fig1)
    st.markdown("""
### Penjelasan:

**1. IPM vs Realisasi TKDD**  
Tidak terlihat pola hubungan linier yang jelas antara Indeks Pembangunan Manusia (IPM) dan Realisasi TKDD. Ini menunjukkan bahwa besarnya realisasi transfer tidak berkaitan langsung dengan tinggi rendahnya IPM suatu daerah.

**2. Pagu TKDD vs Realisasi TKDD**  
Terlihat hubungan linier positif yang sangat kuat antara pagu dan realisasi. Artinya, semakin besar pagu TKDD yang direncanakan, semakin besar pula realisasi anggaran TKDD-nya. Ini menunjukkan proses distribusi yang proporsional terhadap alokasi awal.

**3. Jumlah Penduduk vs Realisasi TKDD**  
Terdapat kecenderungan bahwa daerah dengan jumlah penduduk lebih besar cenderung menerima realisasi TKDD yang lebih tinggi. Namun, sebaran cukup variatif dan tidak terlalu terpusat.

**4. Anggaran APBN per Kapita vs Realisasi TKDD**  
Tidak tampak korelasi yang jelas. Artinya, nilai APBN per kapita tidak serta-merta menentukan tingginya realisasi TKDD. Hal ini bisa mengindikasikan bahwa perhitungan transfer daerah tidak sepenuhnya berbasis per kapita.

**5. Persentase Penduduk Miskin vs Realisasi TKDD**  
Tidak terdapat hubungan yang kuat antara persentase kemiskinan dengan realisasi TKDD. Realisasi tetap tersebar di berbagai tingkat kemiskinan, mengindikasikan bahwa penyaluran dana tidak selalu ditentukan oleh tingkat kemiskinan.

**6. Produk Domestik Regional Bruto (PDRB) Atas Dasar Harga Berlaku vs Realisasi TKDD**  
Terdapat kecenderungan bahwa daerah dengan PDRB tinggi memiliki realisasi TKDD yang lebih besar, namun hubungan ini tampak lemah dan menyebar.

**7. PDRB per Kapita HB vs Realisasi TKDD**  
Hubungan antara PDRB per kapita dengan realisasi juga tidak kuat. Daerah dengan PDRB per kapita tinggi tidak selalu mendapat realisasi TKDD yang besar, mengindikasikan bahwa kemampuan ekonomi per individu tidak menjadi penentu utama.

**8. Laju Pertumbuhan PDRB (konstan 2010) vs Realisasi TKDD**  
Tidak tampak korelasi yang jelas antara pertumbuhan ekonomi dengan realisasi TKDD. Artinya, baik daerah dengan pertumbuhan tinggi maupun rendah bisa mendapatkan realisasi dana yang besar.



---

""")

    # 2. Korelasi
    st.write("### Korelasi terhadap Realisasi TKDD")
    cols = ['Realisasi TKDD'] + variabels
    corr_matrix = data_clean_all[cols].corr()
    corr_target = corr_matrix[['Realisasi TKDD']].drop('Realisasi TKDD')

    fig2, ax = plt.subplots(figsize=(6, 6))
    sns.heatmap(corr_target, annot=True, cmap='coolwarm', center=0, fmt=".2f", ax=ax)
    plt.title('Korelasi terhadap Realisasi TKDD')
    st.pyplot(fig2)
    st.markdown("""
### Penjelasan:

Berdasarkan visualisasi korelasi terhadap **Realisasi TKDD**, variabel yang menunjukkan hubungan paling kuat adalah **Pagu TKDD** dengan korelasi sempurna mendekati 1, menegaskan bahwa besarnya alokasi awal sangat menentukan realisasi anggaran.

Selain itu, **PDRB atas dasar harga berlaku** dan **jumlah penduduk** juga memiliki korelasi positif yang cukup tinggi yaitu sebesar **0,72** dan **0,67**. Hal ini mengindikasikan bahwa daerah dengan kapasitas ekonomi dan jumlah penduduk besar cenderung mendapatkan realisasi dana yang lebih besar.

Di sisi lain, variabel seperti **IPM**, **PDRB per kapita**, dan **laju pertumbuhan ekonomi** menunjukkan korelasi yang sangat lemah terhadap realisasi TKDD, menandakan bahwa faktor kesejahteraan dan pertumbuhan tidak terlalu berpengaruh dalam distribusi dana.

Bahkan, variabel seperti **persentase penduduk miskin** dan **APBN per kapita** memiliki korelasi negatif, yang mengindikasikan bahwa wilayah dengan indikator kemiskinan tinggi justru tidak selalu mendapat realisasi anggaran yang proporsional — atau terdapat **mekanisme distribusi lain yang lebih dominan** daripada pertimbangan kesejahteraan.


---

""")

    # 3. Regresi Linear
    st.write("### Regresi Linier Berganda: Prediktor terhadap Realisasi TKDD")

    import statsmodels.api as sm

    Y = data_clean_all['Realisasi TKDD']
    X = data_clean_all[variabels]
    X = sm.add_constant(X)

    model = sm.OLS(Y, X).fit()

    params_df = pd.DataFrame({
        'Koefisien': model.params,
        't-statistik': model.tvalues,
        'p-value': model.pvalues
    })

    params_df['Keputusan'] = params_df['p-value'].apply(lambda p: 'Signifikan' if p < 0.05 else 'Tidak Signifikan')

    st.dataframe(params_df.style.format({
        'Koefisien': '{:.4f}',
        't-statistik': '{:.2f}',
        'p-value': '{:.4f}'
    }))
    st.markdown("""
### Penjelasan Hasil Regresi Linear Berganda terhadap Realisasi TKDD

Berdasarkan hasil regresi linear berganda terhadap **Realisasi TKDD**, hanya beberapa variabel yang terbukti berpengaruh secara signifikan pada taraf signifikansi 5%.

Variabel **Pagu TKDD** menunjukkan pengaruh paling dominan dengan koefisien positif dan sangat signifikan. Hal ini menegaskan bahwa **alokasi awal anggaran merupakan faktor utama yang menentukan besarnya realisasi TKDD**, karena pada dasarnya realisasi belanja mengikuti pola pagu yang telah ditetapkan sejak awal tahun anggaran.

Selain itu, variabel **PDRB Atas Dasar Harga Berlaku** memiliki pengaruh yang signifikan namun berdampak negatif terhadap realisasi TKDD. Artinya, **semakin besar total nilai produksi barang dan jasa suatu daerah (tanpa memperhitungkan inflasi), justru semakin rendah realisasi TKDD**. Hal ini dapat dijelaskan oleh asumsi bahwa daerah dengan PDRB tinggi sudah memiliki kapasitas fiskal yang memadai sehingga mendapatkan alokasi transfer yang lebih terbatas.

Sebaliknya, variabel **PDRB per Kapita Harga Berlaku** menunjukkan pengaruh yang signifikan dan berdampak positif terhadap realisasi TKDD. Artinya, **semakin tinggi produktivitas ekonomi rata-rata per individu**, maka realisasi dana transfer juga cenderung lebih besar. Hal ini bisa mencerminkan bahwa daerah dengan produktivitas per kapita tinggi memiliki kapasitas kelembagaan yang baik dalam menyerap anggaran.

Sementara itu, variabel-variabel lain seperti:
- Indeks Pembangunan Manusia (IPM)  
- Jumlah Penduduk  
- Anggaran APBN per Kapita  
- Laju Pertumbuhan PDRB  

tidak menunjukkan pengaruh signifikan terhadap realisasi TKDD. Artinya, perubahan pada variabel-variabel tersebut tidak secara konsisten berkaitan dengan besarnya realisasi anggaran.

Variabel **Persentase Penduduk Miskin** memiliki p-value yang mendekati batas signifikansi (sekitar 0,055), yang mengindikasikan **potensi pengaruh negatif**, namun belum cukup kuat untuk dianggap signifikan secara statistik pada taraf 5%.

**Interpretasi Kuantitatif Variabel Signifikan:**

1. **Setiap peningkatan 1 rupiah pada Pagu TKDD** dapat meningkatkan Realisasi TKDD sebesar **1,069 rupiah**. Hal ini mencerminkan hubungan linier yang sangat kuat antara alokasi awal dan realisasi anggaran.

2. **Setiap peningkatan 1 miliar rupiah pada PDRB Atas Dasar Harga Berlaku** berpotensi menurunkan Realisasi TKDD sebesar **1.890.709 rupiah**. Ini menggambarkan bahwa daerah dengan kapasitas ekonomi tinggi mungkin mendapatkan alokasi lebih kecil karena telah dianggap mandiri secara fiskal.

3. **Setiap peningkatan 1 rupiah pada PDRB Per Kapita HB** dapat meningkatkan Realisasi TKDD sebesar **18.680 rupiah**. Ini menunjukkan bahwa meskipun daerah tersebut tergolong mampu, peningkatan produktivitas individu tetap berkaitan dengan penyaluran dana transfer secara marginal.
""")




elif menu == "Hubungan Realisasi TKDD dan IPM":
    st.subheader("Hubungan Realisasi TKDD dan IPM")

    # Load data jika belum
    @st.cache_data
    def load_data_all():
        return pd.read_csv("Data/DataKeseluruhan.csv")

    data_clean_all = load_data_all()

    # ========================
    # Scatter Plot + Pearson
    st.write("### Scatter Plot: IPM vs Realisasi TKDD")

    from scipy.stats import pearsonr
    import matplotlib.pyplot as plt
    import seaborn as sns

    corr, pval = pearsonr(data_clean_all['IPM'], data_clean_all['Realisasi TKDD'])

    fig1, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=data_clean_all, x='IPM', y='Realisasi TKDD', color='teal', s=60, edgecolor='black', ax=ax)
    sns.regplot(data=data_clean_all, x='IPM', y='Realisasi TKDD', scatter=False, color='red', ax=ax)

    ax.set_title(f'Scatter Plot: IPM vs Realisasi TKDD\nKorelasi Pearson = {corr:.2f} (p = {pval:.4f})')
    ax.set_xlabel('IPM')
    ax.set_ylabel('Realisasi TKDD')
    ax.grid(True)
    st.pyplot(fig1)
    st.markdown("""
### Penjelasan:

Berdasarkan **scatter plot antara Indeks Pembangunan Manusia (IPM) dan Realisasi TKDD**, terlihat bahwa hubungan keduanya **bersifat lemah dan tidak signifikan secara statistik**.

- Nilai **koefisien korelasi Pearson sebesar 0,17** menunjukkan adanya hubungan positif yang sangat lemah.  
  Artinya, kenaikan IPM **cenderung diikuti** oleh kenaikan Realisasi TKDD, tetapi hubungan ini **tidak kuat dan tidak konsisten**.
- Hal ini diperkuat oleh nilai **p-value sebesar 0,3541**, yang **jauh di atas taraf signifikansi 5%**, sehingga tidak cukup bukti untuk menyimpulkan adanya korelasi signifikan.

---

### Interpretasi:

- **Sebaran titik data menyebar** tanpa pola linier yang jelas.
- Garis regresi memang menunjukkan kecenderungan naik, tetapi **area bayangan merah (confidence interval) yang lebar** menandakan ketidakpastian prediksi yang tinggi.
- Dengan demikian, **IPM bukan prediktor yang kuat** terhadap besarnya Realisasi TKDD, dan **kemungkinan besar tidak menjadi dasar utama dalam alokasi dana transfer ke daerah**.


---

""")


    # ========================
    # Uji Chi-Square
    st.write("### Uji Chi-Square: Kategori IPM vs Persentase Realisasi TKDD")

    import pandas as pd
    import scipy.stats as stats

    urutan_ipm = ["Sangat Tinggi", "Tinggi", "Sedang"]
    data_clean_all['Kategori IPM'] = pd.Categorical(data_clean_all['Kategori IPM'], categories=urutan_ipm, ordered=True)

    kontingensi = pd.crosstab(data_clean_all['Kategori IPM'], data_clean_all['Kategori Persentase Realisasi TKDD'])

    chi2, p, dof, expected = stats.chi2_contingency(kontingensi)

    st.write("#### Tabel Kontingensi")
    st.dataframe(kontingensi)

    st.write("#### Hasil Uji Chi-Square")
    st.markdown(f"""
    - **Chi-Square Statistic** : `{chi2:.4f}`  
    - **Degrees of Freedom**   : `{dof}`  
    - **P-Value**              : `{p:.4f}`
    """)

    alpha = 0.05
    if p < alpha:
        st.success("Keputusan: Tolak H0 → Terdapat hubungan antara Kategori IPM dan Kategori Persentase Realisasi TKDD.")
    else:
        st.warning("Keputusan: Gagal tolak H0 → Tidak terdapat hubungan antara Kategori IPM dan Kategori Persentase Realisasi TKDD.")
    
    st.markdown("""
### Penjelasan:

Berdasarkan hasil **analisis tabel kontingensi dan uji Chi-Square**, diperoleh bahwa **tidak terdapat hubungan yang signifikan** antara **kategori Indeks Pembangunan Manusia (IPM)** dan **kategori persentase realisasi TKDD** pada taraf signifikansi 5%.

- Nilai **p-value sebesar 0,4345**, yang **jauh di atas batas 5%**, menunjukkan **gagal menolak H₀**.
- Artinya, tingkat IPM suatu daerah **tidak berpengaruh signifikan** terhadap besar kecilnya persentase realisasi TKDD yang diterima, baik dalam kategori **90–100%** maupun **lebih dari 100%**.

---

Hal ini menunjukkan bahwa **alokasi dan realisasi dana transfer pusat ke daerah belum mempertimbangkan secara langsung aspek pembangunan manusia**. Kemungkinan besar, terdapat **faktor-faktor lain di luar IPM** yang lebih dominan dalam memengaruhi besar kecilnya **serapan anggaran TKDD** di setiap daerah.
""")


elif menu == "Analisis Faktor-faktor yang Mempengaruhi IPM":
    st.subheader("Analisis Faktor-faktor yang Mempengaruhi IPM")

    # Load data jika belum
    @st.cache_data
    def load_data_all():
        return pd.read_csv("Data/DataKeseluruhan.csv")

    data_clean_all = load_data_all()

    # ========================
    # 1. Scatter Plot Grid
    st.write("### Scatter Plot: Faktor-faktor terhadap IPM")

    import matplotlib.pyplot as plt
    import seaborn as sns

    variabels = [
        'Pagu TKDD',
        'Jumlah Penduduk',
        'Anggaran APBN per kapita',
        'Persentase Penduduk Miskin',
        'Produk Domestik Regional Bruto (PDRB) Atas Dasar Harga Berlaku',
        'Produk Domestik Regional Bruto per Kapita HB',
        'Laju Pertumbuhan PDRB atas dasar konstan 2010',
        'Realisasi TKDD'
    ]

    fig1 = plt.figure(figsize=(20, 20))
    for i, var in enumerate(variabels):
        plt.subplot(3, 3, i+1)
        sns.scatterplot(data=data_clean_all, x=var, y='IPM')
        plt.title(f'{var} vs IPM')
        plt.xlabel(var)
        plt.ylabel('IPM')
    plt.tight_layout()
    st.pyplot(fig1)
    st.markdown("""
### Penjelasan:

1. **Pagu TKDD vs IPM**  
   Tidak terlihat hubungan yang jelas antara besarnya pagu TKDD dengan IPM.  
   Sebaran data acak menunjukkan bahwa **alokasi dana belum tentu berbanding lurus dengan kualitas pembangunan manusia**.

2. **Jumlah Penduduk vs IPM**  
   Tidak terdapat pola hubungan yang konsisten.  
   Provinsi dengan jumlah penduduk besar bisa memiliki IPM tinggi maupun rendah, menunjukkan bahwa **faktor lain lebih dominan**.

3. **Anggaran APBN per Kapita vs IPM**  
   Terdapat kecenderungan **positif**: provinsi dengan **anggaran per kapita lebih tinggi** cenderung memiliki **IPM lebih baik**,  
   meskipun **hubungan tidak terlalu kuat**.

4. **Persentase Penduduk Miskin vs IPM**  
   Menunjukkan **hubungan negatif yang cukup jelas**.  
   Semakin tinggi tingkat kemiskinan, maka **IPM cenderung lebih rendah**, menegaskan bahwa **kemiskinan berdampak langsung terhadap kualitas hidup**.

5. **PDRB Atas Dasar Harga Berlaku vs IPM**  
   Ada **kecenderungan hubungan positif**, meskipun dengan **penyebaran data yang lebar**.  
   Daerah dengan ekonomi besar cenderung memiliki **IPM yang lebih tinggi**.

6. **PDRB per Kapita HB vs IPM**  
   Hubungan **positif terlihat cukup kuat**.  
   Semakin tinggi **PDRB per kapita**, maka semakin tinggi pula **IPM**, menunjukkan bahwa **kesejahteraan ekonomi individu sangat berkaitan dengan kualitas pembangunan manusia**.

7. **Laju Pertumbuhan PDRB (konstan 2010) vs IPM**  
   Tidak menunjukkan pola yang jelas.  
   Meskipun ada pertumbuhan ekonomi, **tidak selalu diikuti oleh peningkatan IPM secara langsung**.

8. **Realisasi TKDD vs IPM**  
   Sebaran data cukup acak dan **tidak menunjukkan korelasi yang kuat**.  
   Artinya, **besarnya realisasi dana transfer tidak selalu berkaitan dengan pencapaian IPM yang lebih baik**.

---

""")

    # ========================
    # 2. Korelasi terhadap IPM
    st.write("### Korelasi terhadap IPM")

    cols = ['IPM', 'Realisasi TKDD'] + variabels[:-1]  # Hindari duplikasi
    corr_matrix = data_clean_all[cols].corr()
    corr_target = corr_matrix[['IPM']].drop('IPM')

    fig2, ax = plt.subplots(figsize=(6, 6))
    sns.heatmap(corr_target, annot=True, cmap='coolwarm', center=0, fmt=".2f", ax=ax)
    plt.title('Korelasi terhadap IPM')
    st.pyplot(fig2)
    st.markdown("""
### Penjelasan:

Berdasarkan **visualisasi korelasi terhadap IPM**, variabel yang menunjukkan hubungan paling kuat adalah:

- **PDRB per Kapita Harga Berlaku** dengan nilai korelasi sebesar **0.46**
- **PDRB Atas Dasar Harga Berlaku** sebesar **0.44**

Hal ini mengindikasikan bahwa **daerah dengan tingkat output ekonomi yang tinggi**, khususnya dalam hal **pendapatan per kapita**, cenderung memiliki **kualitas pembangunan manusia yang lebih baik**.

Sebaliknya, variabel:

- **Persentase Penduduk Miskin** menunjukkan korelasi **negatif paling kuat**, yaitu sebesar **-0.69**.  
  Ini menegaskan bahwa **semakin tinggi tingkat kemiskinan di suatu wilayah**, maka **semakin rendah pula capaian IPM-nya**.  
  Korelasi negatif ini menjadi **bukti kuat bahwa kemiskinan masih menjadi faktor penghambat utama** dalam pembangunan manusia.

---

Kondisi berbeda ditunjukkan oleh pengaruh variabel berikut yang tergolong lemah.

- **Realisasi TKDD**: korelasi positif lemah (**0.17**)  
- **Pagu TKDD**: korelasi positif lemah (**0.15**)  

Hal ini menunjukkan bahwa **besarnya dana transfer ke daerah tidak secara langsung berkorelasi kuat dengan peningkatan IPM**.

Begitu pula:

- **Jumlah Penduduk** dan **Laju Pertumbuhan PDRB Konstan 2010** menunjukkan **hubungan yang sangat lemah**.
- **Anggaran APBN per Kapita** memiliki **korelasi negatif sebesar -0.13**, mengindikasikan bahwa **besarnya anggaran per orang belum tentu meningkatkan IPM**.  
  Kemungkinan terdapat **faktor distribusi dan efisiensi anggaran** yang perlu ditelaah lebih lanjut.

---

""")

    # ========================
    # 3. Regresi Linier
    st.write("### Regresi Linier Berganda: Prediktor terhadap IPM")

    import statsmodels.api as sm
    import pandas as pd

    Y = data_clean_all['IPM']
    X = data_clean_all[['Realisasi TKDD', 'Pagu TKDD', 'Jumlah Penduduk', 
                        'Anggaran APBN per kapita', 
                        'Persentase Penduduk Miskin',
                        'Produk Domestik Regional Bruto (PDRB) Atas Dasar Harga Berlaku',
                        'Produk Domestik Regional Bruto per Kapita HB',
                        'Laju Pertumbuhan PDRB atas dasar konstan 2010']]

    X = sm.add_constant(X)
    model = sm.OLS(Y, X).fit()

    params_df = pd.DataFrame({
        'Koefisien': model.params,
        't-statistik': model.tvalues,
        'p-value': model.pvalues
    })
    params_df['Keputusan'] = params_df['p-value'].apply(lambda p: 'Signifikan' if p < 0.05 else 'Tidak Signifikan')
    

    st.dataframe(params_df.style.format({
        'Koefisien': '{:.4f}',
        't-statistik': '{:.2f}',
        'p-value': '{:.4f}'
    }))
    
    st.markdown("""
### Penjelasan Hasil Regresi Linear Berganda terhadap IPM

Berdasarkan hasil regresi linear berganda terhadap **Indeks Pembangunan Manusia (IPM)**, hanya beberapa variabel yang menunjukkan pengaruh signifikan pada taraf signifikansi 5%. Variabel yang signifikan adalah **Jumlah Penduduk** dan **Persentase Penduduk Miskin**.

Variabel yang paling signifikan adalah **Persentase Penduduk Miskin**, dengan p-value sangat kecil dan koefisien negatif. Hal ini menunjukkan bahwa peningkatan tingkat kemiskinan berdampak signifikan dalam menurunkan IPM suatu daerah. Oleh karena itu, **penurunan angka kemiskinan menjadi faktor kunci dalam mendorong pembangunan manusia**.

Selain itu, variabel **Jumlah Penduduk** juga berpengaruh signifikan dengan koefisien negatif. Artinya, provinsi dengan jumlah penduduk yang lebih besar cenderung memiliki IPM yang lebih rendah. Ini dapat mengindikasikan bahwa tingginya jumlah penduduk menimbulkan tantangan dalam penyediaan layanan dasar seperti pendidikan, kesehatan, dan infrastruktur, sehingga menghambat peningkatan IPM.

Sementara itu, variabel-variabel lain seperti:
- Realisasi TKDD  
- Pagu TKDD  
- Anggaran APBN per Kapita  
- PDRB Atas Dasar Harga Berlaku  
- PDRB per Kapita Harga Berlaku  
- Laju Pertumbuhan PDRB  

tidak menunjukkan pengaruh yang signifikan terhadap IPM pada taraf signifikansi 5%. Ini mengindikasikan bahwa **besarnya anggaran atau pertumbuhan ekonomi tidak otomatis meningkatkan IPM**, apabila tidak disertai pemerataan dan efektivitas distribusi manfaat pembangunan.

**Interpretasi Kuantitatif Variabel Signifikan:**

1. **Setiap peningkatan 1% Persentase Penduduk Miskin** diperkirakan menurunkan IPM sebesar **0,454** poin. Hal ini menegaskan bahwa pengentasan kemiskinan sangat krusial dalam upaya meningkatkan kualitas pembangunan manusia.

2. **Setiap peningkatan 1 orang dalam jumlah penduduk** diperkirakan menurunkan IPM sebesar **0.000000128** poin. Ini menunjukkan pentingnya pemerataan pembangunan agar peningkatan populasi tidak memperburuk kualitas hidup masyarakat.
""")


