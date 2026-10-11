# Çengel İngilizce

Türkçe ipuçlarının İngilizce karşılıklarını ok yönünde yazdığın çengel bulmaca. Tek dosya, kurulum gerektirmez: `index.html`'i tarayıcıda aç.

- 4 seviye (A1, A2, B1, B2), her birinde 12 bulmaca; B1 ve B2 bir önceki seviyede 6 bulmaca çözünce açılır
- Her gün değişen günün bulmacası
- Kontrol et, Harf aç (−15), Kelime aç (−40), puan ve süre bonusu
- Öğrenilen kelimeler listesi ve istatistikler; ilerleme tarayıcıda saklanır
- Telefonda ekran klavyesi, masaüstünde fiziksel klavye ve yan panel

Her bulmaca dört adet 3×3 bloktan oluşur; her blok hem yatay hem dikey anlamlı kelimeler verir.

## Geliştirme

```sh
python3 tools/squares.py   # kelime listesinden tüm 3×3 kelime karelerini bulur -> data/squares.json
python3 tools/pack.py      # seviyelere ve günlük bulmacalara dağıtır -> data/data.json
python3 tools/build.py     # src/app.html + veri -> index.html
```

Kelime listesi ve Türkçe ipuçları `tools/squares.py` içinde.
