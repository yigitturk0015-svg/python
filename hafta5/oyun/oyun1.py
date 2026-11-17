import random

# Oyun başlangıç değerleri
yakit = 30
mesafe = 100
gun = 1

print("=== UZAY YOLCULUĞU OYUNUNA HOŞ GELDİN ===")
print("Hedef: Yakıtın bitmeden 100 ışık yılı uzaklıktaki gezegene ulaşmak!\n")

# Oyun döngüsü: Mesafe 0'dan büyük ve yakıt 0'dan fazla olduğu sürece devam eder
while mesafe > 0 and yakit > 0:
    print(f"--- {gun}. GÜN ---")
    print(f"Kalan Mesafe: {mesafe} ışık yılı | Mevcut Yakıt: {yakit}")
    
    secim = input("Ne yapmak istersin? (1: Hızlı Git [10 Yakıt], 2: Normal Git [5 Yakıt], 3: Yakıt Ara): ")
    
    if secim == "1":
        if yakit >= 10:
            yakit -= 10
            gidilen_yol = random.randint(25, 35)
            mesafe -= gidilen_yol
            print(f"\n🚀 Tam gaz ilerledin! {gidilen_yol} ışık yılı yol aldın.")
        else:
            print("\n⚠️ Hızlı gitmek için yeterli yakıtın yok! (En az 10 yakıt gerekli)")
            continue # Günü saymadan tekrar seçim yaptırır
            
    elif secim == "2":
        yakit -= 5
        gidilen_yol = random.randint(10, 20)
        mesafe -= gidilen_yol
        print(f"\n🛸 Güvenli hızda ilerledin. {gidilen_yol} ışık yılı yol aldın.")
        
    elif secim == "3":
        bulunan_yakit = random.randint(3, 12)
        yakit += bulunan_yakit
        print(f"\n⛽ Yakınlardaki bir asteroitte {bulunan_yakit} birim yakıt buldun!")
        
    else:
        print("\n❌ Geçersiz seçim! Lütfen 1, 2 veya 3'e bas.")
        continue

    gun += 1
    print("-" * 40)

# Oyun sonu kontrolü (Senin yazdığın if-else mantığı)
if mesafe <= 0:
    print(f"\n🎉 TEBRİKLER! {gun - 1} günde hedef gezegene başarıyla ulaştın!")
    print(f"Kalan Yakıtın: {yakit}")
else:
    print("\n💥 OYUN BİTTİ! Uzayın derinliklerinde yakıtın tükendi...")
    print(f"Gezegene sadece {mesafe} ışık yılı kalmıştı.")