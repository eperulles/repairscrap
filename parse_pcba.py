"""
parse_pcba.py  —  Re-genera assets/pcba_components.json
Incluye: designator, x, y, rotation, footprint, comment, layer, sx, sy
sx/sy = ancho/alto real del componente en mm según el footprint.
"""

import csv, json, re, os

CSV_PATH  = r"C:\Users\Administrator\Desktop\PCBA 048\Pick Place for W78201169C-Logic20230424.csv"
OUT_PATH  = r"C:\Users\Administrator\Desktop\reparaciones\assets\pcba_components.json"

# Tamaños reales por footprint (largo × ancho en mm, orientación normal)
# Fuentes: IPC-7351, datasheet land patterns
FOOTPRINT_SIZE = {
    # Pasivos SMD
    "0201": (0.6,  0.3),
    "0402": (1.0,  0.5),
    "0603": (1.6,  0.8),
    "0805": (2.0,  1.25),
    "1206": (3.2,  1.6),
    "1210": (3.2,  2.5),
    "2512": (6.4,  3.2),
    "2010": (5.0,  2.5),
    "1812": (4.5,  3.2),
    # Transistores / diodos
    "SOT23":   (2.9,  1.6),
    "SOT23-5": (2.9,  1.6),
    "SOT23-6": (2.9,  1.6),
    "SOT323":  (2.0,  1.25),
    "SOT363":  (2.0,  1.25),
    "SOD123":  (3.8,  1.5),
    "SOD323":  (2.0,  1.2),
    "DO214AA": (5.3,  2.7),
    "DO214AC": (5.3,  2.7),
    # ICs pequeños
    "SOIC8":   (5.0,  4.0),
    "SOIC14":  (9.0,  4.0),
    "SOIC16":  (10.3, 4.0),
    "TSSOP8":  (3.0,  3.0),
    "TSSOP14": (5.0,  4.4),
    "TSSOP16": (5.0,  4.4),
    "TSSOP20": (6.5,  4.4),
    "SOP8":    (5.0,  4.0),
    "SOP16":   (10.3, 3.9),
    "MSOP8":   (3.0,  3.0),
    # QFP / QFN
    "QFP44":   (10.0, 10.0),
    "QFP64":   (14.0, 14.0),
    "QFP100":  (16.0, 16.0),
    "QFP120":  (20.0, 14.0),
    "QUAD120": (20.0, 14.0),
    "QFN16":   (4.0,  4.0),
    "QFN24":   (4.0,  4.0),
    "QFN32":   (5.0,  5.0),
    "QFN48":   (7.0,  7.0),
    "QFN64":   (9.0,  9.0),
    # Conectores y pads
    "PAD2":    (2.5,  1.5),
    "PAD":     (2.0,  2.0),
    # Capacitores electrolíticos
    "CAP_TH":  (5.0,  5.0),
    # Inductores
    "IND_SMD": (2.5,  2.0),
}

def footprint_size(fp):
    """Devuelve (sx, sy) en mm para un footprint dado."""
    fp_up = fp.upper().strip()
    # Búsqueda exacta
    if fp_up in FOOTPRINT_SIZE:
        return FOOTPRINT_SIZE[fp_up]
    # Búsqueda parcial: si el nombre del footprint contiene un patrón conocido
    for key, size in FOOTPRINT_SIZE.items():
        if key in fp_up:
            return size
    # Fallback: componente genérico pequeño
    return (1.6, 0.8)

def strip_mm(val):
    """Convierte '81.5914mm' → 81.5914"""
    return float(val.replace("mm", "").replace('"', "").strip())

components = []
with open(CSV_PATH, encoding="latin-1", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        d   = (row.get("Designator") or "").strip().strip('"')
        fp  = (row.get("Footprint") or "").strip().strip('"')
        cmt = (row.get("Comment") or "").strip().strip('"')
        lay = (row.get("Layer") or "T").strip().strip('"')
        rot_raw = (row.get("Rotation") or "0").strip().strip('"')
        rot = float(rot_raw) if rot_raw else 0.0
        mx  = (row.get("Mid X") or "").strip().strip('"')
        my  = (row.get("Mid Y") or "").strip().strip('"')
        if not d or not mx or not my:
            continue
        x = strip_mm(mx)
        y = strip_mm(my)
        # Filter: keep only components within the board outline (132.5 x 110.9 mm)
        # Allow a small margin of 5 mm beyond the board edge
        if not (-5 <= x <= 138) or not (-5 <= y <= 116):
            continue
        sx, sy = footprint_size(fp)
        components.append({
            "d":   d,
            "x":   round(x, 4),
            "y":   round(y, 4),
            "r":   rot,          # rotation degrees (Altium convention)
            "fp":  fp,
            "cmt": cmt,
            "lay": lay[0].upper(),  # 'T' or 'B'
            "sx":  sx,
            "sy":  sy,
        })

print(f"Parsed {len(components)} components")
xs = [c["x"] for c in components]
ys = [c["y"] for c in components]
print(f"X: {min(xs):.2f} – {max(xs):.2f} mm")
print(f"Y: {min(ys):.2f} – {max(ys):.2f} mm")

with open(OUT_PATH, "w") as f:
    json.dump(components, f, separators=(",", ":"))

print(f"Written → {OUT_PATH}")
