import sys

while True:
    try:
        N = int(input("kac sorgu gerceklesecek?"))
        break
    except ValueError:
        print("dogal sayi gir.")

katalog = {}

for n in range(N):
    print(n+1,". kisinin numara, isim, soyisim ve yasini giriniz: ")
    m = list(input().split())
    if len(m) >= 4:
        while True:
            try:
                nbr = int(m[0])
                if nbr in katalog:
                    print("numara cakismasi. cikis.")
                    sys.exit()
                break
            except ValueError:
                print("numara dogal sayi degil. cikis.")
                sys.exit()

        while True:
            try:
                yas = int(m[len(m) - 1])
                break
            except ValueError:
                print("yas dogal sayi degil. cikis.")
                sys.exit()
        while True:
            try:
                soyad = str(m[len(m) - 2])
                break
            except ValueError:
                print("sayad harf degil. cikis.")
                sys.exit()

        del m[len(m)-2:]
        del m[:1]
        while True:
            try:
                isim = str(m)
                break
            except ValueError:
                print("Isim harf degil. cikis.")
                sys.exit()
        Bilgiler = (isim, soyad, yas)
        katalog[nbr]= Bilgiler
    else:
        print ("Eksik girdi. Program durdu.")
        sys.exit()
sirali_katalog = sorted(katalog.items())
print(sirali_katalog)
