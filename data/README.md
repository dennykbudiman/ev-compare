# EV Compare data

Battery-electric passenger cars sold in Indonesia, model years 2020–2026. Data as of October 2026.

- `cars/<brand>/<model>.json`: one file per model, one record per trim and model year (272 trims, 92 models, 30 brands).
- `FIELDS.md`: the format, every field, its unit and the sourcing rules.
- `validate.py`: run `python3 data/validate.py` before every change (checks cars and trucks); it must report 0 errors.
- `assumptions.json`: electricity tariffs, charging losses, real-world range factors and default km per day used by the app's calculated rows.
- `id.json`: Indonesian translations of text values.
- `RESEARCH_BRIEF.md`, `RESEARCH_BRIEF_2020.md`, `RESEARCH_BRIEF_MARKETS.md`: the instructions each research round followed.
- `sources/`: copies of source documents that are not online (e.g. dealer price lists), cited by their GitHub address.
- `GAPS.txt`: every trim with the fields still missing.

Trims per model year: 2020: 4, 2021: 5, 2022: 17, 2023: 20, 2024: 36, 2025: 57, 2026: 133.

Every figure has at least one source (URL, title, date, type). Figures with only one source show a dashed outline in the app.
Figures from other markets: when no Indonesian figure exists, a figure from the same version sold elsewhere is used and its source carries `"market"` (e.g. Malaysia). The app labels it ("Malaysia spec"), never marks it as best and leaves it out of the summary. Each trim's `notes` / `notes_id` say which fields came from which market. Price, assembly, warranties, service and segment are never borrowed. 1,631 figures across 196 trims come from other markets: Malaysia 724, Europe 487, Australia 197, Thailand 86, China 40, UK 23, Philippines 19, Vietnam 18, Global 13, United States 11, Japan 6, India 4, Singapore 3.

Unknown figures are left out. "n/a" means the car does not have the feature (e.g. no DC fast charging).
Trucks, pickups and vans: `trucks/<brand>/<model>.json`, same format plus truck fields (see `TRUCK_FIELDS.md`; research brief `RESEARCH_BRIEF_TRUCKS.md`). 46 trims, 24 models, 13 brands, model years 2021–2026: Pickup 3, Small cargo 28, Light 5, Medium 4, Heavy 6. Only vehicles offered for sale through an official channel are included; vehicles only shown at exhibitions (e.g. Isuzu Elf EV, Hino Dutro Z EV) are not.

Brands: Aion (16), BMW (13), BYD (31), Changan (4), Chery (18), Citroën (1), Denza (4), GWM (1), Geely (4), Hyundai (28), Jaecoo (4), Jaguar (1), Kia (6), Lexus (6), MG (8), MINI (7), Mazda (2), Mercedes-Benz (14), Neta (5), Nissan (5), Polytron (4), Porsche (18), Seres (3), Suzuki (2), Toyota (5), VinFast (9), Volvo (8), Wuling (32), XPeng (9), Zeekr (4)
