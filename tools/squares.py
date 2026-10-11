# -*- coding: utf-8 -*-
import json, random, sys, itertools
A1 = """CAT:Kedi|DOG:Köpek|SUN:Güneş|SEA:Deniz|RED:Kırmızı|EGG:Yumurta|CAR:Araba|BUS:Otobüs|TEA:Çay|ICE:Buz|EYE:Göz|EAR:Kulak|ARM:Kol|LEG:Bacak|BED:Yatak|BOX:Kutu|CUP:Fincan|HAT:Şapka|PEN:Kalem|KEY:Anahtar|MAP:Harita|ART:Sanat|AGE:Yaş|ANT:Karınca|BEE:Arı|COW:İnek|PIG:Domuz|OWL:Baykuş|FOX:Tilki|RAT:Sıçan|BAT:Yarasa|ZOO:Hayvanat bahçesi|SKY:Gökyüzü|TEN:On|ONE:Bir|TWO:İki|SIX:Altı|NEW:Yeni|OLD:Yaşlı|BIG:Büyük|HOT:Sıcak|WET:Islak|DRY:Kuru|SAD:Üzgün|BAD:Kötü|FUN:Eğlence|RUN:Koşmak|EAT:Yemek yemek|SIT:Oturmak|CRY:Ağlamak|FLY:Uçmak|SEE:Görmek|ASK:Sormak|PAY:Ödemek|BUY:Satın almak|WIN:Kazanmak|YES:Evet|DAY:Gün|END:Son|TOY:Oyuncak|BOY:Erkek çocuk|MAN:Adam|SON:Oğul|LIP:Dudak|TOE:Ayak parmağı|NOT:Değil|POT:Tencere|TOP:Tepe|PIE:Turta|PEA:Bezelye|NUT:Ceviz|AIR:Hava|OIL:Yağ|GET:Almak|HAS:Sahip (o)|YET:Henüz|DIG:Kazmak|ACE:As (kart)|ANY:Herhangi|ITS:Onun (nesne)|ARE:Olmak (siz)|HIS:Onun (erkek)|HER:Onun (kadın)|YOU:Sen|SHE:O (kadın)|WHO:Kim|WHY:Neden|HOW:Nasıl|OUR:Bizim|OFF:Kapalı|OUT:Dışarı|ALL:Hepsi|AND:Ve|BUT:Ama|FOR:İçin|SAY:Söylemek|PUT:Koymak|CUT:Kesmek|HIT:Vurmak|USE:Kullanmak|TRY:Denemek|WAY:Yol|FAR:Uzak|FEW:Az|TOO:Fazla|MOM:Anne|DAD:Baba|CAB:Taksi|HEN:Tavuk|JAM:Reçel|BAG:Çanta|CAP:Kep|JOB:İş|KID:Çocuk|PET:Evcil hayvan|VET:Veteriner|GYM:Spor salonu|OWN:Kendi|ALSO:-|NOW:Şimdi|LOW:Alçak|AGO:Önce|SET:Takım|TIE:Kravat|GAS:Gaz|FOG:Sis|MUD:Çamur|INK:Mürekkep|ILL:Hasta|EGO:-|ONE:Bir|SIR:Bayım|LET:İzin vermek|CAN:Konserve kutusu|DOT:Nokta|NET:File|WEB:Ağ|FAN:Vantilatör|PAN:Tava|MUG:Kupa|RUG:Halı|LID:Kapak|TAP:Musluk|BUN:Çörek|HAM:Jambon|FIG:İncir|COD:Morina|ERA:Çağ|PAINT:-|SEW:Dikmek|HUG:Sarılmak|NAP:Şekerleme|TAX:Vergi|TIP:Bahşiş|SUM:Toplam|TAG:Etiket|MIX:Karıştırmak|ROW:Sıra|OAK:Meşe|ASH:Kül|HAY:Saman|PIN:Toplu iğne|TIN:Teneke|TUB:Küvet|VAN:Minibüs|GEM:Mücevher|LOG:Kütük|BIN:Çöp kutusu|HUT:Kulübe|JET:Jet uçağı|MAD:Deli|RAY:Işın|DYE:Boya|ODD:Tek (sayı)|AID:Yardım|AIM:Hedef|RAW:Çiğ|LIE:Yalan|DIE:Ölmek|NOD:Baş sallamak|ICY:Buzlu|HOP:Zıplamak|ZIP:Fermuar|SPY:Casus|GAP:Boşluk|PAW:Pati|FUR:Kürk|WAX:Balmumu|AXE:Balta|DEW:Çiy|EEL:Yılan balığı|APE:İri maymun|OAR:Kürek|ORE:Maden cevheri|TAN:Bronz ten|SAW:Testere|FIT:Formda|DIM:Loş|RIB:Kaburga|ROD:Çubuk|DEN:İn|TOW:Çekmek|OWE:Borçlu olmak|EVE:Arife|EWE:Dişi koyun|RYE:Çavdar|ELK:Kızıl geyik|ARC:Yay (geometri)|EBB:Cezir|OPT:Seçmek|IVY:Sarmaşık|ELM:Karaağaç|FIR:Köknar|PEG:Mandal|VOW:Yemin|BUD:Tomurcuk|IRE:Öfke|SOB:Hıçkırmak|YAM:Tatlı patates|LAP:Kucak|MAT:Paspas|JAR:Kavanoz|WAR:Savaş|LAW:Kanun|EMU:-|TEE:-|OAT:Yulaf tanesi|TOT:-|PAD:Yastıkçık|RIM:Kenar|SAP:Özsu|HID:Sakladı|HAD:Sahipti|DID:Yaptı|GOT:Aldı|RAN:Koştu|SAT:Oturdu|ATE:Yedi (fiil)|WON:Kazandı|LED:Yönetti|FED:Besledi|MET:Tanıştı|BIT:Isırdı|DUG:Kazdı|LAY:Uzanmak|LOT:Çok|BOW:Eğilmek|COT:Portatif yatak|SPA:Kaplıca|TON:Ton|POP:Patlamak|MOP:Paspas (saplı)|COP:Polis|HOG:Domuz (iri)|JOG:Hafif koşmak|BEG:Yalvarmak|PEW:-|YAK:Tibet öküzü|ZAP:-|RUB:Ovmak|SIP:Yudumlamak|RIP:Yırtmak|FOE:Düşman|DOE:Dişi geyik|HUE:Renk tonu|CUE:İşaret|SUE:Dava etmek|DUE:Vadesi gelmiş|RUE:Pişman olmak|TOO:Fazla"""
W={}
order=[]
for p in A1.split("|"):
    w,t=p.split(":",1)
    if t!='-' and w not in W and len(w)==3: W[w]=t; order.append(w)
# tier: first ~150 entries are common (A1), the rest A2
common=set(order[:150])
words=list(W)
pre={}
for w in words:
    for i in range(4): pre.setdefault(w[:i],set()).add(w)
S=set(words)
sq=[]
for r1 in words:
    for r2 in words:
        if r2==r1: continue
        if not all((r1[i]+r2[i]) in pre for i in range(3)): continue
        for r3 in words:
            if r3 in (r1,r2): continue
            cols=[r1[i]+r2[i]+r3[i] for i in range(3)]
            if all(c in S for c in cols) and len(set([r1,r2,r3]+cols))==6:
                sq.append((r1,r2,r3))
def lvl(s):
    ws=list(s)+[s[0][i]+s[1][i]+s[2][i] for i in range(3)]
    n=sum(w not in common for w in ws)
    return n
print(len(words),'words',len(sq),'squares',file=sys.stderr)
from collections import Counter
print(Counter(lvl(s) for s in sq),file=sys.stderr)
json.dump({'W':W,'sq':sq,'common':sorted(common)},open('data/squares.json','w',encoding='utf-8'),ensure_ascii=False)
