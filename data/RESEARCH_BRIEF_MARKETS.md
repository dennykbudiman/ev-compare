# Research brief: fill gaps from other markets

Goal: for each car trim in your brands, fill technical fields that are still missing because no Indonesian figure was found, using the SAME version sold in another market. Every borrowed figure is tagged with its market so the app can label it.

Read first: /home/claude/evc/data/FIELDS.md (whole file, especially "Figures from other markets") and /home/claude/evc/data/RESEARCH_BRIEF.md (sourcing and working rules still apply).
Gap list: /home/claude/evc/data/GAPS.txt (one line per trim: file | id | missing fields).

Rules
1. Never change or remove an existing value or source. Only ADD missing fields (to "values") with their sources (to "sources"), each source entry carrying "market": "<Market>".
2. Same version only: match battery capacity and chemistry, motor power and drive layout with the Indonesian trim. Indonesian variant names often differ from foreign ones; match on specs, not names. If unsure, skip.
3. Never fill: price_otr_idr, assembly, vehicle_warranty, battery_warranty, service_interval, free_service, segment.
4. Market order: Malaysia, Thailand, Singapore, then Philippines, Australia, then the brand's home market or global spec page (China, Korea, Japan, Global), then Europe/UK. Good spec sources: brand Malaysia/Thailand/Singapore/Australia sites and brochures, paultan.org, carlist.my, autofun.co.th, motortrend/caranddriver only for US models, ev-database.org (Europe, label market "Europe"), the brand's global press kit.
5. If a field has range_km borrowed, also take range_standard from the same page and market. If the Indonesian trim already has range_km, do not add a foreign range.
6. Priority fields (do these first for every trim): battery_chemistry, battery_gross_kwh, battery_usable_kwh, drive, motor_type, torque_nm, power_kw, ac_max_kw, dc_max_kw, dc_10_80_min (+dc_time_window), ac_connector, dc_connector, v2l, v2l_kw, length/width/height/wheelbase, ground_clearance_mm, kerb_weight_kg, boot_l, frunk_l, seats, airbags, adas, accel_0_100_s, top_speed_kmh, heat_pump, battery_cooling, voltage_architecture. Then the rest if the same page has them. Technician fields only from official documents.
7. A trim of the same model and year often shares a page: fill all its trims from one or two pages.
8. Append to each changed trim's "notes" and "notes_id" one sentence listing which fields came from which market and site, e.g. "Kerb weight, boot capacity and torque from the Malaysian spec (paultan.org)." / "Berat kosong, kapasitas bagasi, dan torsi dari spesifikasi Malaysia (paultan.org)." Use the brand/model names and units unchanged; Indonesian number style (decimal comma).
9. Edit files with a Python script: load JSON, add, dump with indent=2 and ensure_ascii=False. Keep a backup of each original file in your scratch folder.
10. Web searches are limited and shared. Spend them on finding one rich foreign spec page per model; WebFetch the page; extract everything you can. If searches run out, stop cleanly and report what is left.
11. Finish with `cd /home/claude/evc && python3 data/validate.py data/cars/<brand>` for each brand: 0 errors.

Report (under 250 words): fields added per brand (count), which markets you used most, models you couldn't match to a foreign version and why, top 3 doubts, validator line.
