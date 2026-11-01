# Research brief: electric trucks, pickups and vans (Nov 2026)

Task: for each model assigned to you, research every trim officially sold in Indonesia (model years 2020–2026) and write one JSON file per model to `data/trucks/<make-slug>/<model-slug>.json`.

Read first, and follow exactly:
1. `data/FIELDS.md`: file format, sourcing rules, source types, "n/a", other-market rules (including the exception rule and the battery-label rule).
2. `data/TRUCK_FIELDS.md`: truck classes, truck fields, trim rules.

Priorities, in order:
1. Fields that matter most to a fleet buyer: segment (class), gvw_kg, payload_kg, battery_gross_kwh (and usable if published), range_km (+ range_standard only if stated), range_full_payload_km (only if stated), power_kw, torque_nm, drive / axle_config, ac_max_kw, dc_max_kw, dc_10_80_min (+ dc_time_window), ac/dc connectors, price_otr_idr (only if published as OTR; otherwise note the price and basis), assembly, warranties.
2. Then: battery chemistry and supplier, voltage, motor type and supplier, dimensions, wheelbase, kerb weight, cab type, seats, cargo body size, top speed, tyre size, gcw_kg, towing_kg, axle loads, epto_kw.
3. Technician fields only from official documents (body builder guides, owner's manuals, service information).

Sources, in order of preference: the brand's Indonesian website and brochures; Indonesian launch press releases (GIIAS, IIMS, GJAW, ICVE); Indonesian trade and auto media (e.g. otomotif.kompas.com, oto.detik.com, gridoto.com, otodriver.com, truckmagz.com, majalahtruk, trukmania, katadata OTO, kontan, bisnis.com, cnbcindonesia.com); then the same version in another market (Malaysia, Thailand, Philippines, Australia, then Japan/China/Korea/Global, then Europe), tagged with `market` and written up in notes.

Rules that trip people up:
- Never guess and never copy a figure between trims unless a source says it applies.
- Truck ranges are often "up to" or "manufacturer test": leave range_standard out unless the cycle is named.
- Many truck prices are off the road, or chassis only, or "from": leave price_otr_idr out and write the quote and its basis in notes.
- If GVW puts the truck in a different class than its marketing, follow GVW (see TRUCK_FIELDS.md) and say so in notes.
- notes_id: natural Indonesian, decimal comma, thousands dot.
- Run `python3 data/validate.py data/trucks/<make-slug>` and fix every ERROR before you finish. Warnings about class vs GVW must be checked and either fixed or explained in notes.

Finish with a short report: files written, trims, which key fields are missing and why, and anything you were unsure of.
