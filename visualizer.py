from datetime import datetime
import matplotlib.pyplot as plt

# DOSYA AYARI
dosya_adi = "global_influenza_temiz.csv"

tarihler = []
vakalar = []

print("📊 Küresel temizlenmiş CSV dosyası okunuyor...")

# 1. TEMİZ CSV DOSYASINI SAF PYTHON İLE OKU
with open(dosya_adi, mode="r", encoding="utf-8") as f:
    # Başlık satırını atla (Tarih,Vaka_Sayisi)
    f.readline()
    
    for satir in f:
        satir = satir.strip()
        if not satir:
            continue
            
        parcalar = satir.split(",")
        tarih_metin = parcalar[0]
        vaka_metin = parcalar[1]
        
        try:
            # Tarihleri matplotlib'in doğru sıralaması için datetime nesnesine çeviriyoruz
            tarih_obj = datetime.strptime(tarih_metin, "%Y-%m-%d")
            vaka = int(vaka_metin)
            
            tarihler.append(tarih_obj)
            vakalar.append(vaka)
        except Exception:
            continue

print(f"✅ Toplam {len(tarihler)} haftalık küresel veri başarıyla grafiğe hazırlandı.")

# -------------------------------------------------------------
# 2. MANUEL TREND HESAPLAMA (52 Haftalık Hareketli Ortalama)
# Sinyal işlemedeki alçak geçiren filtre (low-pass filter) mantığıyla 
# yüksek frekanslı salgın gürültülerini temizliyoruz.
trend_sinyali = []
pencere_boyutu = 52

for i in range(len(vakalar)):
    if i < pencere_boyutu // 2 or i >= len(vakalar) - (pencere_boyutu // 2):
        trend_sinyali.append(None)
    else:
        pencere = vakalar[i - (pencere_boyutu // 2) : i + (pencere_boyutu // 2)]
        trend_sinyali.append(sum(pencere) / len(pencere))
# -------------------------------------------------------------

# 3. GÖRSELLEŞTİRME
plt.figure(figsize=(14, 6))

# Ham Küresel Sinyal (Arka planda daha yumuşak görünsün diye tealsı/turkuaz renkte)
plt.plot(tarihler, vakalar, label="Küresel Influenza Sinyali (Ham Veri)", color="#008080", alpha=0.4, linewidth=1.5)

# Elle Hesaplanan Küresel Trend (Ön planda net görünsün diye mor renkte)
temiz_trend_x = [tarihler[i] for i in range(len(trend_sinyali)) if trend_sinyali[i] is not None]
temiz_trend_y = [trend_sinyali[i] for i in range(len(trend_sinyali)) if trend_sinyali[i] is not None]
plt.plot(temiz_trend_x, temiz_trend_y, label="Küresel Trend (52 Haftalık Hareketli Ortalama)", color="#4B0082", linewidth=2.5)

# Grafik Süslemeleri ve Biçimlendirme
plt.title("WHO FluNet - Dünya Geneli Agrege Edilmiş Influenza Sinyal ve Trend Analizi", fontsize=13, fontweight='bold')
plt.xlabel("Yıllar", fontsize=11)
plt.ylabel("Haftalık Pozitif Vaka Sayısı (Küresel)", fontsize=11)
plt.legend(fontsize=10)
plt.grid(True, linestyle=":", alpha=0.5)

# Zaman ekseninin altındaki tarih yazılarının birbirine girmemesi ve otomatik ayarlanması için
plt.gcf().autofmt_xdate() 
plt.tight_layout()

# Grafiği ekrana bas
plt.show()