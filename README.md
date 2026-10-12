# Kanca - Word Game

Türkçe ipuçlarının İngilizce karşılıklarını ok yönünde yazdığın çengel bulmaca. Tek dosya, kurulum gerektirmez: `index.html`'i tarayıcıda aç.

- 4 seviye (A1, A2, B1, B2), her birinde 12 bulmaca; B1 ve B2 bir önceki seviyede 6 bulmaca çözünce açılır
- Her gün değişen günün bulmacası
- Kontrol et, Harf aç (−15), Kelime aç (−40), puan ve süre bonusu
- Öğrenilen kelimeler listesi ve istatistikler; ilerleme tarayıcıda saklanır
- Telefonda ekran klavyesi, masaüstünde fiziksel klavye ve yan panel

Her bulmaca klasik bir çengel bulmacadır: 9×9 ızgarada ipucu kareleri araya serpiştirilmiştir, kelimelerin çoğu iki yönde kesişir. Seviyeler A1–C2 (12'şer bulmaca) ve IELTS (6 konu × 3 band, 36 bulmaca).

## Geliştirme

```sh
python3 tools/pack_arrow.py   # bütün bulmacaları üretir -> data/arrow.json (paralel, ~15 dk)
python3 tools/fix_weak.py     # seviye kelimesi az kalan bulmacaları yeniden üretir
python3 tools/build.py        # src/app.html + veri -> index.html
```

Kelime listeleri ve Türkçe ipuçları `data/` klasöründe (`vocab-*.tsv`, `fill-*.tsv`, `words.tsv`); `tools/dictionary.py` bunları seviyelere göre birleştirir.

## iOS ve Android uygulaması

Uygulama [Capacitor](https://capacitorjs.com) ile paketlenir (`ios/`, `android/`). Telefon sürümü internetsiz çalışır: yazı tipleri `fonts/` içinde gelir.

```sh
npm install
npm run sync      # www/ üretir ve iki projeye kopyalar
npm run ios       # Xcode'da açar: iPhone'u seç, Çalıştır
npm run apk       # Android APK: android/app/build/outputs/apk/debug/app-debug.apk (JDK 21 gerekir)
npm run assets    # assets/ içindeki simge ve açılış görselinden tüm boyutları üretir
```

Telefonda ek olarak: durum çubuğu temaya uyar, Android geri tuşu uygulama içinde geri gider, kelimeler telefonun kendi sesli okumasıyla okunur, kelime bulununca ve bulmaca bitince titreşim olur, ekran dikey kalır.
