from datetime import datetime

# DOSYA AYARLARI
ham_dosya = "FluNet_Dataset.csv"
islenmis_dosya = "global_influenza_temiz.csv"  # Çıktı olarak alacağımız küresel temiz dosya

vaka_sozlugu = {}
toplam_satir = 0
gecerli_kayit_sayisi = 0

print("🔄 Devasa WHO FluNet veri seti KÜRESEL ölçekte işleniyor, lütfen bekleyin...")

# 1. HAM VERİYI SATIR SATIR OKU VE TÜM DÜNYAYI TOPLA
with open(ham_dosya, mode="r", encoding="utf-8") as f:
    # Başlıkları al ve indeksleri bul
    basliklar = f.readline().strip().split(",")
    tarih_idx = basliklar.index("ISO_WEEKSTARTDATE")
    vaka_idx = basliklar.index("INF_ALL")
    
    for satir in f:
        toplam_satir += 1
        parcalar = satir.strip().split(",")
        
        # Satırda eksik sütun kalma ihtimaline karşı koruma
        if len(parcalar) <= max(tarih_idx, vaka_idx):
            continue
            
        tarih_metin = parcalar[tarih_idx].strip()
        vaka_ham = parcalar[vaka_idx].strip()
        
        if not tarih_metin:
            continue
            
        try:
            # Tarihi doğrula ve standart formata getir
            tarih_obj = datetime.strptime(tarih_metin, "%Y-%m-%d")
            tarih_standart = tarih_obj.strftime("%Y-%m-%d")
            
            vaka = int(float(vaka_ham)) if vaka_ham and vaka_ham != "NaN" else 0
            
            # ÜLKE FİLTRESİ YOK: Aynı tarihteki tüm dünya vakalarını sözlükte biriktiriyoruz
            if json_tarih := vaka_sozlugu.get(tarih_standart):
                vaka_sozlugu[tarih_standart] += vaka
            else:
                vaka_sozlugu[tarih_standart] = vaka
                
            gecerli_kayit_sayisi += 1
        except Exception:
            continue

# 2. TARİHLERİ ESKİDEN YENİYE SIRALA
sirali_tarihler = sorted(vaka_sozlugu.keys())

# 3. YENİ KÜRESEL CSV DOSYASINI YAZDIR
print(f"✍️ Temizlenmiş küresel veriler '{islenmis_dosya}' dosyasına kaydediliyor...")
with open(islenmis_dosya, mode="w", encoding="utf-8") as f_out:
    # Yeni dosyanın başlıkları (Header)
    f_out.write("Tarih,Vaka_Sayisi\n")
    
    for tarih in sirali_tarihler:
        f_out.write(f"{tarih},{vaka_sozlugu[tarih]}\n")

print("\n🚀 Küresel İşlem Başarıyla Tamamlandı!")
print(f"📊 Toplam taranan ham satır: {toplam_satir}")
print(f"🌍 İşlenen toplam vaka kaydı: {gecerli_kayit_sayisi}")
print(f"📅 Oluşturulan benzersiz küresel hafta sayısı: {len(sirali_tarihler)}")
print(f"💾 Temiz küresel dosya hazır: {islenmis_dosya}")