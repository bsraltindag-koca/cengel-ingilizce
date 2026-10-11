import json, random
from collections import Counter
d=json.load(open('data/squares.json',encoding='utf-8'))
W=d['W']; sq=[tuple(s) for s in d['sq']]; common=set(d['common'])
def ws(s): return list(s)+[s[0][i]+s[1][i]+s[2][i] for i in range(3)]
def lvl(s): return sum(w not in common for w in ws(s))
pools={'A1':[s for s in sq if lvl(s)<=1],'A2':[s for s in sq if lvl(s)==2],'B1':[s for s in sq if lvl(s)==3],'B2':[s for s in sq if lvl(s)>=4]}
random.seed(7)
def build(pool,n,use):
    out=[]
    for _ in range(n):
        chosen=[];inp=set()
        cand=pool[:]; random.shuffle(cand)
        for _ in range(4):
            best=min((s for s in cand if not (set(ws(s))&inp)), key=lambda s: sum(use[w] for w in ws(s))+3*lvl(s)+random.random())
            chosen.append(best); inp|=set(ws(best))
            for w in ws(best): use[w]+=1
        out.append([''.join(s) for s in chosen])
    return out
use=Counter()
P={k:build(v,12,use) for k,v in pools.items()}
P['daily']=build(pools['A1']+pools['A2'],30,Counter())
used=set()
for k in P:
    for p in P[k]:
        for s in p:
            t=(s[0:3],s[3:6],s[6:9]); used|=set(ws(t))
clues={w:W[w] for w in sorted(used)}
json.dump({'levels':P,'clues':clues},open('data/data.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
for k in P: print(k, len(pools.get(k,[])), P[k][0])
print(len(clues),'clues used')
