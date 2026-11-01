"""Check EV Compare data files. Usage: python3 data/validate.py [folder-or-file ...] (default: data/cars and data/trucks)."""
import json, os, re, sys
NUM = {"price_otr_idr","battery_gross_kwh","battery_usable_kwh","pack_nominal_voltage_v","pack_voltage_min_v","pack_voltage_max_v","cell_count","pack_weight_kg",
       "range_km","motor_count","power_kw","torque_nm","gear_ratio","regen_max_kw","ac_max_kw","onboard_charger_kw","dc_max_kw","dc_10_80_min","ac_full_hours","v2l_kw",
       "wading_mm","airbags","seats","length_mm","width_mm","height_mm","wheelbase_mm","ground_clearance_mm","kerb_weight_kg","boot_l","frunk_l","headroom_front_mm",
       "headroom_rear_mm","legroom_front_mm","legroom_rear_mm","turning_radius_m","accel_0_100_s","top_speed_kmh","hv_wait_min",
       "gvw_kg","payload_kg","gcw_kg","towing_kg","axle_front_kg","axle_rear_kg","cargo_length_mm","cargo_width_mm","cargo_height_mm","range_full_payload_km","epto_kw","cargo_volume_m3","price_quote_idr","gradeability_pct"}
BOOL = {"battery_preheat","heat_pump","v2l","ota","battery_swap"}
TEXT = {"segment","assembly","vehicle_warranty","battery_warranty","service_interval","free_service","battery_chemistry","voltage_architecture","cell_supplier","cell_format",
        "cell_config","battery_cooling","range_standard","drive","motor_type","motor_supplier","inverter_tech","ac_connector","dc_connector","dc_protocol","dc_time_window",
        "charge_port","platform","battery_ip","airbag_positions","adas","crash_rating","seat_layout","tyre_size","hv_disconnect_location","aux_battery","aux_battery_location",
        "coolant_type","coolant_spec","coolant_loops","obd_port","diag_protocol","axle_config","cab_type","body_type","price_quote_basis","transmission"}
ENUM = {"segment": {"City car","Hatchback","Sedan","Crossover","SUV","MPV"}, "assembly": {"CKD Indonesia","CBU import"},
        "range_standard": {"WLTP","WLTC","NEDC","CLTC","EPA"}, "drive": {"FWD","RWD","AWD"}}
RANGE = {"price_otr_idr": (5e7, 1e10), "battery_gross_kwh": (5, 250), "battery_usable_kwh": (5, 250), "range_km": (50, 1200), "power_kw": (10, 1200),
         "torque_nm": (50, 2500), "ac_max_kw": (1, 22), "dc_max_kw": (10, 600), "dc_10_80_min": (5, 180), "ac_full_hours": (1, 40), "seats": (2, 9),
         "length_mm": (2400, 6000), "width_mm": (1300, 2300), "height_mm": (1200, 2200), "wheelbase_mm": (1600, 3600), "kerb_weight_kg": (500, 4000),
         "accel_0_100_s": (2, 25), "top_speed_kmh": (60, 350), "boot_l": (0, 3000), "turning_radius_m": (3, 8)}
STYPES = {"official", "press", "media"}
MARKETS = {"Malaysia","Thailand","Philippines","Singapore","Vietnam","Australia","New Zealand","Japan","Korea","China","India","Middle East","Europe","UK","United States","Latin America","Africa","Global"}
TRUCK_BODY = {"Pickup","Van","Minibus","Rigid truck","Tractor head","Mining truck"}
QUOTE_BASIS = {"off the road","chassis only","basis not stated"}
TRUCK_SEGS = {"Pickup","Small cargo","Light","Medium","Heavy"}
TRUCK_STD = {"C-WTVC","JE05"}
TRUCK_DRIVE = {"4x2","4x4","6x2","6x4","8x4"}
TRUCK_RANGE = {"battery_gross_kwh": (5, 1000), "battery_usable_kwh": (5, 1000), "range_km": (30, 1200), "power_kw": (10, 1500), "torque_nm": (50, 40000), "ac_max_kw": (1, 50),
               "dc_max_kw": (10, 1200), "length_mm": (3000, 16000), "width_mm": (1300, 3500), "height_mm": (1500, 4500), "wheelbase_mm": (1800, 7000), "kerb_weight_kg": (800, 60000),
               "gvw_kg": (1500, 120000), "payload_kg": (200, 100000), "gcw_kg": (3000, 150000), "seats": (1, 20), "top_speed_kmh": (30, 200), "boot_l": (0, 30000), "turning_radius_m": (3, 30)}
LOCAL_ONLY = {"price_quote_idr","price_quote_basis","price_otr_idr","assembly","vehicle_warranty","battery_warranty","service_interval","free_service","segment"}
def check(path):
    errs, warns = [], []
    truck = "/trucks/" in path.replace("\\", "/")
    try: d = json.load(open(path))
    except Exception as e: return [f"{path}: not valid JSON: {e}"], []
    for k in ("make", "model", "trims"):
        if k not in d: errs.append(f"{path}: missing '{k}'")
    ids = set()
    for t in d.get("trims", []):
        tid = t.get("id", "?")
        p = f"{path} [{tid}]"
        for k in ("id", "model_year", "variant", "status", "data_as_of", "values", "sources"):
            if k not in t: errs.append(f"{p}: missing '{k}'")
        if tid in ids: errs.append(f"{p}: duplicate id")
        ids.add(tid)
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", str(tid)): errs.append(f"{p}: id must be lower-case words joined by hyphens")
        if t.get("status") not in ("on sale", "discontinued"): errs.append(f"{p}: status must be 'on sale' or 'discontinued'")
        if t.get("model_year") not in range(2020, 2027): errs.append(f"{p}: model_year must be 2020–2026")
        v, s = t.get("values", {}), t.get("sources", {})
        if "segment" not in v: errs.append(f"{p}: values.segment is required")
        for k, x in v.items():
            if k not in NUM | BOOL | TEXT: errs.append(f"{p}: unknown field '{k}'"); continue
            if x is None: errs.append(f"{p}: {k} is null; leave unknown fields out")
            elif x == "n/a": pass
            elif k in NUM and not isinstance(x, (int, float)): errs.append(f"{p}: {k} must be a number, got {x!r}")
            elif k in BOOL and not isinstance(x, bool): errs.append(f"{p}: {k} must be true/false, got {x!r}")
            elif k in TEXT and not isinstance(x, str): errs.append(f"{p}: {k} must be text, got {x!r}")
            allowed = ENUM.get(k)
            if truck and k == "segment": allowed = TRUCK_SEGS
            if truck and k == "range_standard": allowed = ENUM[k] | TRUCK_STD
            if truck and k == "drive": allowed = ENUM[k] | TRUCK_DRIVE
            if k == "body_type": allowed = TRUCK_BODY
            if k == "price_quote_basis": allowed = QUOTE_BASIS
            if allowed and x not in allowed and x != "n/a": errs.append(f"{p}: {k} must be one of {sorted(allowed)}, got {x!r}")
            rng = (TRUCK_RANGE.get(k) or RANGE.get(k)) if truck else RANGE.get(k)
            if rng and isinstance(x, (int, float)) and not (rng[0] <= x <= rng[1]): warns.append(f"{p}: {k}={x} looks out of range {rng}")
            if not truck and k in {"gvw_kg","payload_kg","gcw_kg","towing_kg","axle_front_kg","axle_rear_kg","cargo_length_mm","cargo_width_mm","cargo_height_mm","range_full_payload_km","epto_kw","axle_config","cab_type","body_type","cargo_volume_m3","price_quote_idr","price_quote_basis","gradeability_pct","battery_swap","transmission"}: errs.append(f"{p}: {k} is a truck-only field")
            src = s.get(k)
            if not src: errs.append(f"{p}: {k} has no source")
            else:
                for e in src:
                    if not str(e.get("url", "")).startswith("http"): errs.append(f"{p}: {k} source without url")
                    if e.get("type") not in STYPES: errs.append(f"{p}: {k} source type must be official/press/media")
                    if not re.fullmatch(r"20\d\d-\d\d", str(e.get("date", ""))): errs.append(f"{p}: {k} source date must be YYYY-MM")
                    if "market" in e and e["market"] not in MARKETS: errs.append(f"{p}: {k} source market must be one of {sorted(MARKETS)}")
                if all("market" in e for e in src) and k in LOCAL_ONLY: errs.append(f"{p}: {k} must come from an Indonesian source")
        for k in s:
            if k not in v: warns.append(f"{p}: source for '{k}' but no value")
        if truck and "body_type" not in v: warns.append(f"{p}: body_type missing")
        if ("price_quote_idr" in v) != ("price_quote_basis" in v): errs.append(f"{p}: price_quote_idr and price_quote_basis go together")
        if "price_quote_idr" in v and "price_otr_idr" in v: errs.append(f"{p}: price_quote_idr only when there is no OTR price")
        if truck and isinstance(v.get("payload_kg"), (int, float)) and isinstance(v.get("gvw_kg"), (int, float)) and v["payload_kg"] >= v["gvw_kg"]: errs.append(f"{p}: payload not below gross vehicle weight")
        if truck and isinstance(v.get("gvw_kg"), (int, float)):
            g = v["gvw_kg"]; seg = v.get("segment")
            want = None if seg == "Pickup" else ("Small cargo" if g <= 3500 else "Light" if g <= 8500 else "Medium" if g <= 16000 else "Heavy")
            if want and seg != want and not (seg == "Heavy" and g > 16000): warns.append(f"{p}: gvw {g} kg suggests class {want}, not {seg}")
        if isinstance(v.get("battery_usable_kwh"), (int, float)) and isinstance(v.get("battery_gross_kwh"), (int, float)) and v["battery_usable_kwh"] > v["battery_gross_kwh"]:
            errs.append(f"{p}: usable capacity larger than gross")
        vn, lo, hi = v.get("pack_nominal_voltage_v"), v.get("pack_voltage_min_v"), v.get("pack_voltage_max_v")
        if all(isinstance(z, (int, float)) for z in (vn, lo, hi)) and not lo <= vn <= hi: errs.append(f"{p}: nominal voltage outside min–max")
        if v.get("dc_connector") == "n/a" and isinstance(v.get("dc_max_kw"), (int, float)): errs.append(f"{p}: dc_connector n/a but dc_max_kw given")
        mk = {k for k, lst in s.items() if lst and all("market" in e for e in lst)}
        if mk and not re.search(r"market|spec|spesifikasi", (t.get("notes", "") + t.get("notes_id", "")), re.I): warns.append(f"{p}: other-market figures ({', '.join(sorted(mk))}) not mentioned in notes")
    return errs, warns
def main():
    targets = sys.argv[1:] or [x for x in ("data/cars", "data/trucks") if os.path.isdir(x)]
    files = []
    for t in targets:
        if os.path.isdir(t):
            for r, _, fs in os.walk(t): files += [os.path.join(r, f) for f in fs if f.endswith(".json")]
        else: files.append(t)
    E = W = 0; trims = 0
    for f in sorted(files):
        e, w = check(f)
        try: trims += len(json.load(open(f)).get("trims", []))
        except Exception: pass
        for x in e: print("ERROR", x)
        for x in w: print("WARN ", x)
        E += len(e); W += len(w)
    print(f"{len(files)} files, {trims} trims, {E} errors, {W} warnings")
    sys.exit(1 if E else 0)
main()
