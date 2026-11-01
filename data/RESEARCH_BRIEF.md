# Research brief: EV Compare car data (Indonesia)

You are researching battery-electric PASSENGER CARS sold in Indonesia, model years 2024, 2025 and 2026, for the brands assigned to you. No hybrids, no plug-in hybrids, no range extenders, no commercial vans/pickups/trucks.

1. Read /home/claude/evc/data/FIELDS.md fully. It defines the file format, every field, units and the sourcing rules. Follow it exactly.
2. For each assigned brand, first confirm which BEV models and variants were actually on sale in Indonesia in 2024–2026 (including ones since discontinued). The list you were given is a starting point from an October 2026 price list; add anything missing for your brands, drop anything not a passenger BEV.
3. For each model, write one file /home/claude/evc/data/cars/<make-slug>/<model-slug>.json with one record per trim (see the year rule in FIELDS.md).
4. Priority of fields (fill these first, for every trim): segment, assembly, price_otr_idr, battery_chemistry, battery_gross_kwh, range_km, range_standard, motor_count, drive, motor_type, power_kw, torque_nm, ac_connector, dc_connector, ac_max_kw, dc_max_kw, dc_10_80_min (+dc_time_window), battery_warranty, vehicle_warranty, seats, length/width/height/wheelbase, ground_clearance, kerb_weight, boot_l, airbags, adas, crash_rating, v2l/v2l_kw, accel_0_100_s, top_speed_kmh. Then anything else you find on the way. Technician fields only from official/service documents.
5. Sources: Indonesian-market first (brand .co.id/.id site, brochure PDF, launch press release, then oto.com, carmudi.co.id, moladin.com, detik.com, cnnindonesia.com, kumparan.com, gridoto.com, otodriver.com, autofun.co.id, paultan/zigwheels only for Indonesian launches). kompas.com blocks automated fetching; skip it. A figure needs at least one source with URL, title, YYYY-MM date and type. Record a second source when you happen to have one (it lifts the "single source" flag). Never invent or estimate; leave a field out instead.
6. Prices: Jakarta on-the-road, latest known for that model year. If a later price change applies, use the latest and mention the change in notes.
7. Write notes in plain English: conflicts between sources, global-vs-Indonesian specs, renamed variants.
8. When done, run `cd /home/claude/evc && python3 data/validate.py data/cars/<make-slug>` for each of your brands and fix every ERROR. Look at WARN lines and fix real mistakes.
9. Work efficiently: use WebSearch to find the best 1–3 pages per model (an official spec page or a full spec table covers many fields at once), then WebFetch them. Don't fetch the same page twice. Save scratch notes only under /tmp/claude-0/-home-claude/74001e6e-b9a3-5e38-885f-4573421658b2/scratchpad/research/<your-group>/.
10. Do not edit any file outside /home/claude/evc/data/cars/<your brands>/ and your scratch folder.

Earlier research leads (unverified, use as hints only): /tmp/claude-0/-home-claude/74001e6e-b9a3-5e38-885f-4573421658b2/scratchpad/notes.txt

## Report back (under 300 words)
- Files written and number of trims per model.
- Models you could not find enough data for, and why.
- The 5 most important conflicts or doubts (field, values, sources).
- Validator result line.
