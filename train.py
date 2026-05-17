from datetime import datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error

# 1. TEMİZLENMİŞ KÜRESEL VERİYİ OKUMA
dosya_adi = "global_influenza_temiz.csv"
tarihler = []
vakalar = []

with open(dosya_adi, mode="r", encoding="utf-8") as f:
    f.readline() # Başlığı geç
    for satir in f:
        satir = satir.strip()
        if not satir: continue
        parcalar = satir.split(",")
        try:
            t_obj = datetime.strptime(parcalar[0], "%Y-%m-%d")
            v_val = int(parcalar[1])
            tarihler.append(t_obj)
            vakalar.append(v_val)
        except:
            continue

# 2. PANDEMİ ÖNCESİ VE SONRASI OLARAK VERİYİ BÖLME (Train-Test Split)
sinir_tarihi = datetime(2020, 1, 1)

# CRITICAL FIX: İçinde 0 vaka olan haftalar modeli patlatmasın diye tüm verilere +1 ekliyoruz!
train_tarih = [t for t in tarihler if t < sinir_tarihi]
train_vaka = [vakalar[i] + 1 for i in range(len(tarihler)) if tarihler[i] < sinir_tarihi]

test_tarih = [t for t in tarihler if t >= sinir_tarihi]
test_vaka = [vakalar[i] + 1 for i in range(len(tarihler)) if tarihler[i] >= sinir_tarihi]

print(f"📈 Eğitim verisi (1999-2019): {len(train_vaka)} hafta")
print(f"📉 Test/Tahmin dönemi (2020+): {len(test_vaka)} hafta")

# 3. GELENEKSEL MODELİN (HOLT-WINTERS) EĞİTİLMESİ
print("🤖 Model eğitiliyor ve gelecek tahmini üretiliyor...")
model = ExponentialSmoothing(train_vaka, 
                             trend="add", 
                             seasonal="mul", 
                             seasonal_periods=52).fit()

# Gelecek adımı tahmin et
tahminler_ham = model.forecast(len(test_vaka))

# 4. GERÇEK DEĞERLERE DÖNÜŞ (Eklediğimiz +1'leri geri çıkartıyoruz)
train_vaka_orj = [v - 1 for v in train_vaka]
test_vaka_orj = [v - 1 for v in test_vaka]
tahminler = [max(0, t - 1) for t in tahminler_ham] # Tahmin eksiye düşerse 0 yap koruması

# 5. HATA ANALİZİ
mae = mean_absolute_error(test_vaka_orj, tahminler)
print(f"📊 Pandemi Dönemi İçin Ortalama Sapma (MAE): {mae:.2f} Vaka")

# 6. MUHTEŞEM NİHAİ GRAFİK
plt.figure(figsize=(14, 6))

# Eğitim Verisi (Geçmiş)
plt.plot(train_tarih, train_vaka_orj, label="Eğitim Verisi (Pandemi Öncesi Normal Dünya)", color="#008080", alpha=0.5)

# Gerçekleşen (Pandemideki çöküş)
plt.plot(test_tarih, test_vaka_orj, label="Gerçekleşen Küresel Durum (COVID-19 Çöküşü)", color="red", linewidth=2)

# Modelin Tahmini
plt.plot(test_tarih, tahminler, label="Modelin Gelecek Tahmini (Normal Salgın Döngüsü)", color="darkorange", linestyle="--", linewidth=2.5)

plt.title("Zaman Serisi Tahmin Modeli Sonuçları: Gerçek Dünya Şoku vs. İstatistiki Beklenti", fontsize=13, fontweight='bold')
plt.xlabel("Yıllar")
plt.ylabel("Haftalık Pozitif Vaka Sayısı")
plt.legend(fontsize=10)
plt.grid(True, linestyle=":", alpha=0.5)
plt.gcf().autofmt_xdate()
plt.tight_layout()

# Grafiği kaydet
plt.savefig("nihai_tahmin_grafigi.png", dpi=300)
print("💾 Grafik başarıyla 'nihai_tahmin_grafigi.png' olarak kaydedildi!")
plt.show()