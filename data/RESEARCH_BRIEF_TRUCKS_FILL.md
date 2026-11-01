# Research brief: filling truck spec gaps (Nov 2026)

Goal: fill missing fields in existing truck records, using Indonesian sources first and the same version sold in another market where no Indonesian figure exists.

Read first and follow exactly: `data/FIELDS.md` (format, sourcing, "Figures from other markets", the exception and battery-label rules) and `data/TRUCK_FIELDS.md` (truck fields and classes). Look at the existing records before you add anything.

## What to fill (in this order)
1. Fleet essentials: payload_kg, gvw_kg, kerb_weight_kg, cargo_volume_m3 and cargo box size, ac_max_kw and dc_max_kw, ac_connector / dc_connector, dc_10_80_min (+ dc_time_window), battery_chemistry, battery_usable_kwh (only if published as usable).
2. Technical: voltage_architecture, pack_nominal_voltage_v, motor_type, motor_supplier, cell_supplier, transmission, gradeability_pct, top_speed_kmh, turning_radius_m, tyre_size, dimensions, wheelbase, axle loads, towing_kg (pickups).
3. Technician fields only from official documents (owner's manual, body builder guide, service information).
Indonesian-only fields (never from another market): price_otr_idr, price_quote_idr, assembly, warranties, service, segment.

## Other markets
- Only the exact same version: same battery capacity and chemistry, same motor power, same drive/axle layout, and for trucks the same GVW and wheelbase where they differ by market. If you can't tell which foreign version matches, leave the field out.
- Preferred order: Malaysia, Thailand, Singapore, Philippines, Vietnam; then Australia, New Zealand; then the maker's home market or global page (China, Japan, Korea, Global); then Middle East, Latin America, Africa, Europe, UK, United States.
- Tag every such source with `"market"` and add a sentence to `notes` and `notes_id` saying which fields came from which market.
- If an Indonesian figure is clearly wrong or on a different basis, the exception rule in FIELDS.md applies: replace it with the labelled same-version figure and explain why.

## Rules that matter most
- Never guess, never estimate, never copy a figure between trims unless a source says it applies to that trim.
- Do not change existing values unless a better source shows they are wrong; then explain the change in notes.
- Keep `notes_id` natural Indonesian (decimal comma, thousands dot), no raw field names.
- Run `python3 data/validate.py data/trucks/<make-slug>` from the repository root; 0 errors.
- Do not edit anything outside your assigned make folders, do not edit app files, and do not commit or push.

Finish with a short report: per trim, which fields you added (and from which market), what you changed and why, and what you looked for but could not find.
