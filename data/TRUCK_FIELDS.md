# EV Compare data: field guide (trucks, pickups and vans)

One JSON file per model: `data/trucks/<make-slug>/<model-slug>.json` (lower case, hyphens, e.g. `data/trucks/mitsubishi-fuso/ecanter.json`).
The file format, sourcing rules, source types, `market` tags, "n/a" use and the other-market rules are the SAME as for cars: read `FIELDS.md` first. This file lists only what is different for trucks.

## Classes (`segment`, required)
| segment | what goes in it |
|---|---|
| Pickup | pickup body (single, extended or double cab), any weight |
| Small cargo | vans, blind vans, minibuses used for cargo, micro trucks; gross vehicle weight up to 3.5 t |
| Light | truck chassis (cab + box, flatbed, tipper, etc.), gross vehicle weight above 3.5 t and up to 8.5 t |
| Medium | gross vehicle weight above 8.5 t and up to 16 t |
| Heavy | gross vehicle weight above 16 t, and every tractor head, dump truck and mining truck of that size |
Use the gross vehicle weight (JBB, Jumlah Berat yang Diperbolehkan) as registered or published for Indonesia. If only a foreign figure exists, use it and say so in notes.

## Trims
- A trim = one model year + one variant as sold in Indonesia. Trucks are often sold by gross vehicle weight, wheelbase, battery size or body; each of those is its own trim when the specs differ.
- `id`: make-model-year-variant, e.g. `mitsubishi-fuso-ecanter-2024-fe-8-5t`.
- Body built by a local karoseri (box, tipper) is usually not part of the brand's spec; record only what the brand or a cited source states for the chassis or the complete vehicle, and say which in notes.

## Truck fields (in addition to the car fields)
| key | meaning | unit / allowed values |
|---|---|---|
| gvw_kg | gross vehicle weight (JBB) | kg |
| payload_kg | payload (rated load) as published; say in notes if it is chassis payload (body and load) or load only | kg |
| gcw_kg | gross combination weight (JBKB), tractors and trucks with trailers | kg |
| towing_kg | braked towing capacity (pickups) | kg |
| axle_config | e.g. "4x2", "6x4", "4x4" | text |
| axle_front_kg / axle_rear_kg | rated axle loads | kg |
| cab_type | e.g. "Single cab", "Double cab", "Day cab", "Sleeper cab", "Standard cab", "Wide cab", "Van" | text |
| cargo_length_mm / cargo_width_mm / cargo_height_mm | inside dimensions of the load bed or box (only if published) | mm |
| range_full_payload_km | range at full payload, only if the source says so explicitly | km |
| epto_kw | electric power take-off (for bodies such as tippers, refrigerated boxes) | kW |
| body_type | REQUIRED for trucks. One of: "Pickup", "Van" (blind/panel/cargo van), "Minibus" (passenger van, shuttle), "Rigid truck" (cab-chassis truck with box, drop-side, tipper or other body, including mini trucks), "Tractor head" (on-road prime mover), "Mining truck" (off-road haul/dump truck or mining tractor, not for public roads) | text |
| cargo_volume_m3 | load space volume as published (van load area or factory box) | m³ |
| price_quote_idr | ONLY when there is no OTR price: the price as quoted (off the road, chassis only, "from"); never shown as OTR | rupiah |
| price_quote_basis | required with price_quote_idr: "off the road", "chassis only" or "basis not stated" | text |
| gradeability_pct | maximum gradeability as published | % |
| battery_swap | battery swapping offered for this truck in Indonesia | true / false |
| transmission | e.g. "Single-speed reduction gear", "2-speed", "6-speed automated manual" | text |
- `drive` for trucks: use the axle layout words the source uses: "RWD", "4x2", "4x4", "6x2", "6x4", "8x4", "AWD". Pickups: "4x2" or "4x4" (or RWD/AWD if that's what the source says).
- `range_standard` for trucks may also be "C-WTVC" (China heavy-vehicle cycle) or "JE05" (Japan). Leave it out if the test method is not stated (most truck ranges are "manufacturer test" or "up to"; say so in notes).
- Best marks in the app are only given between trucks of the same class AND the same body_type, so set body_type on every trim.
- `seats` = seats in the cab. Car-only fields (boot_l, frunk_l, headroom, legroom, airbags for cars, accel_0_100_s) only if published.
- Prices: OTR (on the road) Jakarta when published. Many trucks are sold off the road or as a chassis only; then leave price_otr_idr out, put the quoted price in price_quote_idr with its price_quote_basis, and explain in notes.

## Validation
Run `python3 data/validate.py data/trucks` from the project folder; it must report 0 errors.
