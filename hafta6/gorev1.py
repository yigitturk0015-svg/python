yakit = 15

print("Başlangıç Yakıtı:",yakit)


if:  evet
    print("Uçuşa başlayalım!")
else:
    print("uçuş sona erdi.")

print("uçuş için gereken yakıt:",yakit)

yakit -= 5 #yakit = yakit - 5 


if yakit >= 10:
    print("Uçuş Başarılı!")
else:
    print("Yetersiz Yakıt! Gerekli Olan Yakıt Miktarı:",10)


