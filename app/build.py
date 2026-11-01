"""Build EV Compare from the data folder.

Usage (from the repository root):  python3 app/build.py
Writes dist/index.html (the website, one self-contained file) and dist/ev-compare.dc.html (the Claude Design version).
Run python3 data/validate.py first; the GitHub workflow does both on every push.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, "app", "template.dc.html")
DIST = os.environ.get("EVC_DIST", os.path.join(ROOT, "dist"))
OUT = os.path.join(DIST, "ev-compare.dc.html")

KEYS = ["id", "type", "segment", "make", "model", "variant", "status_id", "assembly",
        "battery_chemistry", "battery_gross_kwh", "battery_usable_kwh", "voltage_architecture",
        "range_km", "range_standard", "motor_count", "drive", "motor_type", "power_kw", "torque_nm",
        "ac_connector", "dc_connector", "dc_protocol", "ac_max_kw", "dc_max_kw", "dc_10_80_min",
        "gvw_kg", "payload_kg", "cell_supplier", "cell_format", "battery_cooling",
        "pack_nominal_voltage_v", "motor_supplier", "inverter_tech", "onboard_charger_kw",
        "heat_pump", "v2l", "v2l_kw", "battery_warranty", "platform", "notes", "sources",
        "uncertain_fields", "notes_id", "data_as_of", "field_sources", "charger_install_idr", "service_cost_year_idr", "free_service_years", "insurance_pct", "tax_year_idr", "depreciation_pct_year", "cell_count", "cell_config", "pack_voltage_min_v", "pack_voltage_max_v", "pack_weight_kg", "gear_ratio", "regen_max_kw", "hv_disconnect_location", "aux_battery", "coolant_type", "coolant_loops", "obd_port", "diag_protocol", "ota", "seats", "seat_layout", "length_mm", "width_mm", "height_mm", "wheelbase_mm", "ground_clearance_mm", "kerb_weight_kg", "boot_l", "frunk_l", "headroom_front_mm", "headroom_rear_mm", "legroom_front_mm", "legroom_rear_mm", "turning_radius_m", "tyre_size", "accel_0_100_s", "top_speed_kmh", "cab_type", "cargo_length_mm", "cargo_width_mm", "cargo_height_mm", "price_otr_idr", "vehicle_warranty", "service_interval", "free_service", "ac_full_hours", "charge_port", "battery_preheat", "wading_mm", "battery_ip", "airbags", "airbag_positions", "adas", "crash_rating", "axle_config", "axle_front_kg", "axle_rear_kg", "gcw_kg", "towing_kg", "range_full_payload_km", "epto_kw", "aux_battery_location", "hv_wait_min", "coolant_spec"]
NUMERIC = ["battery_gross_kwh", "battery_usable_kwh", "range_km", "motor_count", "power_kw",
           "torque_nm", "ac_max_kw", "dc_max_kw", "dc_10_80_min", "gvw_kg", "payload_kg",
           "pack_nominal_voltage_v", "onboard_charger_kw", "v2l_kw", "cell_count", "pack_voltage_min_v", "pack_voltage_max_v", "pack_weight_kg", "gear_ratio", "regen_max_kw", "seats", "length_mm", "width_mm", "height_mm", "wheelbase_mm", "ground_clearance_mm", "kerb_weight_kg", "boot_l", "frunk_l", "headroom_front_mm", "headroom_rear_mm", "legroom_front_mm", "legroom_rear_mm", "turning_radius_m", "accel_0_100_s", "top_speed_kmh", "cargo_length_mm", "cargo_width_mm", "cargo_height_mm", "price_otr_idr", "ac_full_hours", "wading_mm", "airbags", "axle_front_kg", "axle_rear_kg", "gcw_kg", "towing_kg", "range_full_payload_km", "epto_kw", "hv_wait_min"]

MODE = sys.argv[1] if len(sys.argv) > 1 else "real"
SAMPLE = MODE == "sample"
REAL_CARS = MODE == "real"          # real car data from data/cars, sample trucks
FILES = []   # sample data is not part of the repository; the app is built from data/cars and data/trucks

def load_real_cars(folder=os.path.join(ROOT, "data", "cars"), type_="car"):
    """Flatten data/<cars|trucks>/<make>/<model>.json into the app's row format."""
    from urllib.parse import urlparse
    out = []
    for root, _, fs in os.walk(folder):
        for f in sorted(fs):
            if not f.endswith(".json"):
                continue
            d = json.load(open(os.path.join(root, f)))
            for t in d.get("trims", []):
                v = dict(t.get("values", {}))
                v.update(id=t["id"], type=type_, make=d["make"], model=d["model"], variant=t.get("variant"), model_year=t.get("model_year"),
                         status_id=t.get("status"), data_as_of=t.get("data_as_of"), notes=t.get("notes") or "", notes_id=t.get("notes_id"))
                fsrc, urls = {}, []
                for k, lst in (t.get("sources") or {}).items():
                    lst = [x for x in lst if str(x.get("url", "")).startswith("http")]
                    if not lst:
                        continue
                    domains = {urlparse(x["url"]).netloc.replace("www.", "") for x in lst}
                    first = lst[0]
                    # a figure is "other market" only if none of its sources is Indonesian
                    mkt = first.get("market") if all(x.get("market") for x in lst) else None
                    fsrc[k] = dict(title=first.get("title"), url=first["url"], date=first.get("date"), type=first.get("type"), sources=len(domains), market=mkt,
                                   all=[dict(title=x.get("title"), url=x["url"]) for x in lst])
                    for x in lst:
                        if x["url"] not in [u["url"] for u in urls]:
                            urls.append(dict(title=x.get("title"), url=x["url"]))
                v["field_sources"] = fsrc
                v["sources"] = urls
                v["uncertain_fields"] = []
                out.append(v)
    return out
KEYS.insert(6, "model_year")
NUMERIC.append("model_year")
NUMERIC.extend(["charger_install_idr", "service_cost_year_idr", "free_service_years", "insurance_pct", "tax_year_idr", "depreciation_pct_year"])
TR = json.load(open(os.path.join(ROOT, "data", "id.json")))
TR_PREFIX = {"Long-life coolant, ": "Cairan pendingin tahan lama, ", "Low-conductivity coolant for the battery loop, ": "Cairan pendingin berkonduktivitas rendah untuk sirkuit baterai, "}
NO_TR = {"id", "type", "segment", "make", "model", "variant", "status_id", "notes", "notes_id", "sources", "uncertain_fields", "range_standard"}
missing = set()
VARIANT_ID = [("t GVW", "t JBB"), (" wheelbase", " sumbu roda"), ("M battery", "baterai M"), ("5 batteries", "5 baterai"), ("Two-Seater Blind Van", "Blind Van Dua Kursi"),
              ("Box body", "Bodi boks"), ("Mini truck (drop-side deck)", "Truk mini (bak terbuka)"), ("Cab-chassis", "Sasis-kabin"), ("Wide-body dump truck", "Dump truck bodi lebar"), ("(16-seat passenger)", "(penumpang, 16 kursi)"),
              ("(16-seat)", "(16 kursi)"), ("dump truck", "dump truck"), ("tractor head", "tractor head")]
rows, seen = [], set()
TRUCK_DIR = os.path.join(ROOT, "data", "trucks")
REAL_TRUCKS = REAL_CARS and os.path.isdir(TRUCK_DIR) and any(f.endswith(".json") for _, _, fs in os.walk(TRUCK_DIR) for f in fs)
def all_records():
    for p in FILES:
        if not os.path.exists(p):
            print("missing", os.path.basename(p)); continue
        for v in json.load(open(p)):
            if REAL_CARS and v.get("type") == "car":
                continue
            if REAL_TRUCKS and v.get("type") == "truck":
                continue
            yield v
    if REAL_CARS:
        for v in load_real_cars():
            yield v
    if REAL_TRUCKS:
        for v in load_real_cars(TRUCK_DIR, "truck"):
            yield v

KEYS.extend(["dc_time_window", "status", "body_type", "cargo_volume_m3", "price_quote_idr", "price_quote_basis", "gradeability_pct", "battery_swap", "transmission"])
NUMERIC.extend(["cargo_volume_m3", "price_quote_idr", "gradeability_pct"])
for v in all_records():
    if True:
        v = {k: v.get(k) for k in KEYS}
        for k in NUMERIC:
            x = v[k]
            if isinstance(x, str) and x != "n/a":
                m = re.search(r"[\d.]+", x.replace(",", ""))
                v[k] = float(m.group()) if m else None
        if isinstance(v["model_year"], float):
            v["model_year"] = int(v["model_year"])
        v["sources"] = v["sources"] or []
        if not v["sources"] and not (SAMPLE or REAL_CARS):
            print("no source, dropped:", v["id"]); continue
        if v["id"] in seen:
            v["id"] += "-2"
        seen.add(v["id"])
        v["uncertain_fields"] = v["uncertain_fields"] or []
        if (SAMPLE or (REAL_CARS and not REAL_TRUCKS and v.get("type") == "truck")) and not v["notes_id"]:
            v["notes_id"] = "Data contoh untuk pratinjau desain; akan diganti dengan dataset hasil riset."
        tr = {}
        for k, x in v.items():
            if k in NO_TR or not isinstance(x, str) or x == "n/a":
                continue
            if x in TR:
                tr[k] = TR[x]
            elif any(x.startswith(a) for a in TR_PREFIX):
                a = next(a for a in TR_PREFIX if x.startswith(a))
                tr[k] = TR_PREFIX[a] + re.sub(r"(\d)\.(\d)", r"\1,\2", x[len(a):])
            elif any(c.isalpha() for c in x) and x.lower() not in {s.lower() for s in TR.values()}:
                missing.add(x)
        # Indonesian variant names: decimal comma and a few truck words (car trim names stay as sold)
        if v.get("variant"):
            vid = re.sub(r"(\d)\.(\d)", r"\1,\2", v["variant"])
            if v.get("type") == "truck":
                for en_w, id_w in VARIANT_ID:
                    vid = vid.replace(en_w, id_w)
            if vid != v["variant"]:
                tr["variant"] = vid
        v["tr"] = tr
        rows.append(v)

# sanity checks on the pack figures (warn only)
CELL_NOM = {"LFP": 3.2, "NMC": 3.65}
for v in rows:
    vn, lo, hi = v.get("pack_nominal_voltage_v"), v.get("pack_voltage_min_v"), v.get("pack_voltage_max_v")
    if isinstance(vn, (int, float)) and isinstance(lo, (int, float)) and isinstance(hi, (int, float)) and not (lo <= vn <= hi):
        print("CHECK voltage: nominal outside range:", v["id"], vn, lo, hi)
    n, ch = v.get("cell_count"), v.get("battery_chemistry")
    if isinstance(vn, (int, float)) and isinstance(n, (int, float)) and ch in CELL_NOM and abs(n * CELL_NOM[ch] - vn) / vn > 0.1:
        print("CHECK voltage: cells x cell voltage does not match nominal:", v["id"], n, ch, vn)

def pick(type_, hints):
    out = []
    for h in hints:
        for v in rows:
            if v["type"] == type_ and h in v["id"] and v["id"] not in out:
                out.append(v["id"]); break
    return out[:3]

defaults = {
    "car": (pick("car", ["byd-atto-3-2026-advanced-plus", "geely-ex5-2026-pro"]) if REAL_CARS else pick("car", ["atto-3-2024-superior", "ioniq-5-2024-signature", "atto-3", "ioniq-5", "binguo"]))[:2],
    "truck": (pick("truck", ["wuling-mitra-ev-2026-blind-van-long-range", "dfsk-gelora-e-2026-blind-van"]) if REAL_TRUCKS else pick("truck", ["ecanter-2024-m", "hilux", "elf"]))[:2],
}

data = json.dumps(rows, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html = open(TPL).read()
html = re.sub(r"/\*DATA\*/.*?/\*END\*/", lambda m: data, html, count=1, flags=re.S)
html = re.sub(r"/\*DEF\*/.*?/\*END\*/", lambda m: json.dumps(defaults), html, count=1, flags=re.S)
html = re.sub(r"/\*ASOF\*/.*?/\*END\*/", lambda m: '{"en":"Oct 2026","id":"Okt 2026"}', html, count=1, flags=re.S)
html = re.sub(r"/\*SAMPLE\*/.*?/\*END\*/", lambda m: "true" if SAMPLE else ("false" if REAL_TRUCKS else ('["truck"]' if REAL_CARS else "false")), html, count=1, flags=re.S)
os.makedirs(DIST, exist_ok=True)
open(OUT, "w").write(html)

# ---- website: the same template and logic, run by app/runtime.js (Preact) instead of the Claude Design runtime ----
def between(text, a, b):
    i = text.index(a) + len(a)
    return text[i:text.index(b, i)]
helmet = between(html, "<helmet>", "</helmet>")
body = between(html, "</helmet>", "</x-dc>")
logic = between(html, "data-dc-script data-props=", "</script>")
logic = logic[logic.index(">") + 1:]
APP = os.path.join(ROOT, "app")
preact = open(os.path.join(APP, "vendor", "preact.umd.js")).read()
runtime = open(os.path.join(APP, "runtime.js")).read()
for name, text in (("logic", logic), ("preact", preact), ("runtime", runtime)):
    assert "</script" not in text.lower(), name + " contains a closing script tag"
web = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>EV Compare: electric cars, trucks and vans in Indonesia</title>
<meta name="description" content="Compare electric cars, trucks and vans sold in Indonesia: price, range, charging, payload and technical details, with a source for every figure. English and Bahasa Indonesia.">
<meta name="theme-color" content="#F0F0F0">
""" + helmet + """
</head>
<body>
<div id="app"></div>
<template id="evc-tpl">""" + body + """</template>
<script>""" + preact + """</script>
<script>""" + runtime + """</script>
<script>window.EVC_LOGIC = function (DCLogic) {
""" + logic + """
;return Component; };</script>
<script>EVCRuntime.start();</script>
</body>
</html>
"""
open(os.path.join(DIST, "index.html"), "w").write(web)
open(os.path.join(DIST, ".nojekyll"), "w").write("")
by = {}
for v in rows:
    by.setdefault(v["type"], 0); by[v["type"]] += 1
print("untranslated:", sorted(missing))
print("entries", by, "defaults", defaults, "bytes", len(html))
