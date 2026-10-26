# Generates assets/eu_addr_map.py from the SMWDisX (https://github.com/IsoFrieze/SMWDisX) symbol files.
# Usage: python3 other/gen_eu_addr_map.py SMW_U.sym SMW_E1.sym > assets/eu_addr_map.py
import sys
def load(p):
    d = {}
    for line in open(p):
        if line.startswith(';') or not line.strip(): continue
        a, n = line.split(None, 1); n = n.strip()
        if n.startswith(':'): continue
        d[n] = int(a, 16)
    return d
u, e = load(sys.argv[1]), load(sys.argv[2])
pairs = sorted({(u[n], e[n]) for n in u if n in e and (u[n] >> 16) == (e[n] >> 16) and (u[n] >> 16) < 0x10 and u[n] & 0x8000})
# drop anchors that don't change the shift relative to the previous anchor in the same bank
out, last = [], {}
for ua, ea in pairs:
    b = ua >> 16
    if last.get(b) != ea - ua:
        out.append((ua, ea)); last[b] = ea - ua
print('# US -> Europe (Rev 1) ROM address anchors, generated from SMWDisX SMW_U.sym / SMW_E1.sym.')
print('# Each entry (us, eu): US addresses from us up to the next entry in the same bank are shifted by eu - us.')
print('kAnchors = [')
for ua, ea in out: print(f'  (0x{ua:06X}, 0x{ea:06X}),')
print(']')
