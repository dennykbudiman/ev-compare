# EV Compare data: field guide (cars)

One JSON file per model: `data/cars/<make-slug>/<model-slug>.json` (lower case, hyphens, e.g. `data/cars/byd/atto-3.json`).

```json
{
  "make": "BYD",
  "model": "Atto 3",
  "trims": [
    {
      "id": "byd-atto-3-2025-advanced-plus",
      "model_year": 2025,
      "variant": "Advanced Plus",
      "status": "on sale",
      "data_as_of": "2026-10",
      "values": { "segment": "SUV", "battery_gross_kwh": 49.92, "range_km": 410, "range_standard": "NEDC" },
      "sources": {
        "battery_gross_kwh": [ { "url": "https://...", "title": "Page title", "date": "2026-08", "type": "official" } ],
        "range_km": [ { "url": "https://...", "title": "...", "date": "2026-08", "type": "media" } ]
      },
      "notes": "Short English note: conflicts between sources, global vs Indonesian spec, etc.",
      "notes_id": "The same note in natural Indonesian (decimal comma, thousands dot)."
    }
  ]
}
```

## Rules
- One trim = one model year + one variant as sold in Indonesia. Include model years 2020 to 2026 that were officially on sale in Indonesia (no grey imports). If a trim is unchanged across years, include ONE record per model year only when specs or price differ; otherwise one record with the latest model year and a note "Same specs 2024–2026".
- `id`: make-model-year-variant, lower case, hyphens, unique.
- `status`: "on sale" or "discontinued" (in Indonesia).
- Every value in `values` MUST have at least one entry in `sources` under the same key. No source → leave the field out. Never guess, never estimate, never copy from another trim unless a source says it applies.
- If two sources disagree, use the official Indonesian figure (brand website / official brochure / official launch press release); otherwise the most recent reliable one. Put the conflict in `notes`.
- Prefer Indonesian-market sources: brand .co.id / .id sites, official brochures, launch releases, then oto.com, carmudi.co.id, moladin.com, detik.com, kompas.com, cnnindonesia.com, kumparan.com, gridoto.com, otodriver.com, autofun.co.id. Global specs (other markets) only if no Indonesian figure exists — then add "(global spec)" in notes for that field.
- `type` of a source: "official" (brand site, brochure, official release), "press" (news report of the launch/press release), "media" (review, spec database, dealer list).
- `market` of a source: leave it out for Indonesian sources. When a figure comes from another market because no Indonesian figure exists, add `"market"` with one of: Malaysia, Thailand, Philippines, Singapore, Vietnam, Australia, Japan, Korea, China, India, Europe, UK, United States, Global. The app labels these figures (e.g. "Malaysia spec") and never marks them as best.
- `date`: YYYY-MM of publication (or of access if undated).
- Use `null`? No: leave unknown fields out entirely. Use the string "n/a" only when the vehicle genuinely does NOT have the feature (e.g. no DC fast charging → dc_max_kw "n/a", dc_connector "n/a", dc_10_80_min "n/a", dc_protocol "n/a"). It still needs a source showing it isn't offered (spec sheet listing AC only is fine).
- Strings in English. Numbers as plain numbers in the unit given below (no units in the value).

## Fields (all optional except segment; fill what you can source)
| key | meaning | unit / allowed values |
|---|---|---|
| segment | body type | one of: City car, Hatchback, Sedan, Crossover, SUV, MPV |
| assembly | where built for Indonesia | "CKD Indonesia" or "CBU import" |
| price_otr_idr | on-the-road price Jakarta | rupiah, full number (e.g. 415000000). For battery-subscription brands (VinFast, Polytron) use the price INCLUDING the battery and say so in notes |
| vehicle_warranty | e.g. "3 yrs / 100,000 km" | text, this exact pattern |
| battery_warranty | e.g. "8 yrs / 160,000 km" or "Lifetime (first owner)" | text |
| service_interval | e.g. "Every 20,000 km or 12 months" | text, this pattern |
| free_service | e.g. "Free periodic service for 3 years" | text |
| battery_chemistry | LFP, NMC, NCM, NCA, LMFP | text |
| battery_gross_kwh | gross capacity | kWh |
| battery_usable_kwh | usable/net capacity (only if published as such) | kWh |
| voltage_architecture | "~400 V" or "800 V" style | text |
| pack_nominal_voltage_v | nominal pack voltage | V |
| pack_voltage_min_v / pack_voltage_max_v | operating range | V |
| cell_supplier | e.g. "CATL", "FinDreams (BYD)" | text |
| cell_format | Blade, Prismatic, Pouch, Cylindrical | text |
| cell_count | number of cells | number |
| cell_config | e.g. "96s1p" | text |
| pack_weight_kg | | kg |
| battery_cooling | Liquid, Air, Direct refrigerant | text |
| range_km | claimed range | km |
| range_standard | test method of range_km | WLTP, WLTC, NEDC, CLTC, EPA — leave out if not stated |
| motor_count | number of traction motors | number |
| drive | FWD, RWD, AWD | text |
| motor_type | PMSM, Induction, EESM, or e.g. "Induction (front) + PMSM (rear)" | text |
| power_kw | combined peak power | kW (convert PS ×0.7355, hp ×0.7457; note the original) |
| torque_nm | combined peak torque | Nm |
| motor_supplier | | text |
| inverter_tech | SiC or IGBT | text |
| gear_ratio | reduction ratio, e.g. 9.5 | number |
| regen_max_kw | | kW |
| ac_connector | Type 2, GB/T, Type 1 | text |
| dc_connector | CCS2, GB/T, CHAdeMO, or "n/a" | text |
| dc_protocol | DIN 70121, ISO 15118, GB/T 27930, CHAdeMO, or "n/a" | text |
| ac_max_kw | max AC charging power | kW |
| onboard_charger_kw | on-board charger rating (often = ac_max_kw; only if stated) | kW |
| dc_max_kw | peak DC charging | kW, or "n/a" |
| dc_10_80_min | DC fast-charge time; state in notes if the source used another window (e.g. 30–80%) and put it under `dc_time_window` | minutes |
| dc_time_window | only if not 10–80%, e.g. "30–80%" | text |
| ac_full_hours | AC 0–100% time as published | hours |
| charge_port | Right rear, Left rear, Right front, Left front, Front centre | text |
| battery_preheat | battery preheating available | true / false |
| heat_pump | | true / false |
| v2l | vehicle-to-load available | true / false |
| v2l_kw | | kW |
| platform | e.g. "e-Platform 3.0", "E-GMP" | text |
| wading_mm | wading depth | mm |
| battery_ip | e.g. "IP67" | text |
| airbags | number | number |
| airbag_positions | e.g. "front, side, curtain" | text |
| adas | short list of abbreviations, e.g. "AEB, ACC, LKA, BSM, RCTA" | text |
| crash_rating | e.g. "5 stars (ASEAN NCAP 2024)" or "Not tested" | text |
| seats | number | number |
| seat_layout | e.g. "2+3", "2+2+3" | text |
| length_mm / width_mm / height_mm / wheelbase_mm / ground_clearance_mm | | mm |
| kerb_weight_kg | | kg |
| boot_l / frunk_l | boot / front boot capacity | litres |
| headroom_front_mm / headroom_rear_mm / legroom_front_mm / legroom_rear_mm | | mm |
| turning_radius_m | | m |
| tyre_size | e.g. "235/50 R18" | text |
| accel_0_100_s | | seconds |
| top_speed_kmh | | km/h |
| hv_disconnect_location / hv_wait_min / aux_battery / aux_battery_location / coolant_type / coolant_spec / coolant_loops / obd_port / diag_protocol / ota | technician details — fill ONLY from service information, owner's manuals or official documents; usually leave out | text (hv_wait_min in minutes, ota true/false) |

Before you finish, run: `python3 /home/claude/evc/data/validate.py data/cars/<make-slug>` from /home/claude/evc and fix every ERROR.

## Figures from other markets
Use another market's figure ONLY when no Indonesian figure exists for that field, and ONLY for the exact same version: same battery capacity and chemistry, same motor power and drive layout as the Indonesian trim. If you can't tell which foreign version matches, leave the field out.
- Allowed fields: all technical fields (battery, range, motor, charging, dimensions, weights, safety equipment, crash rating, performance, technician fields).
- Never from another market: price_otr_idr, assembly, vehicle_warranty, battery_warranty, service_interval, free_service, segment.
- Market preference: right-hand-drive Southeast Asia first (Malaysia, Thailand, Singapore), then Philippines/Australia, then the brand's home market or global spec page (China, Korea, Japan, Global), then Europe/UK.
- range_km from another market must come with that market's range_standard (e.g. WLTP in Malaysia), both with the same `market`.
- Crash ratings: ASEAN NCAP ratings already cover Indonesia (no market tag). Euro NCAP → market "Europe"; ANCAP → "Australia"; C-NCAP → "China". Only for the same model generation.
- Malaysian buyer's-guide sites (paultan.org, carbase.my) label kerb weight just "Weight"; checked in Nov 2026 against kerb and gross figures from other sources, it is kerb weight and may be used as kerb_weight_kg.
- Exception: when an Indonesian figure is clearly wrong or on a different basis (copied from another version, or a different rating such as normal vs overboost power), replace it with the same-version figure from another market, tagged with its `market`, and explain the replacement in `notes` / `notes_id`.
- Battery labels: Mercedes-Benz and MINI quote usable (net) capacity. Store their figure as battery_usable_kwh and take gross from a spec that states it; never store a usable figure as gross.
- Add a sentence to `notes` and `notes_id` listing which fields came from which market, e.g. "Battery chemistry, kerb weight and boot capacity from the Malaysian spec (paultan.org)." / "Kimia baterai, berat kosong, dan kapasitas bagasi dari spesifikasi Malaysia (paultan.org)."
