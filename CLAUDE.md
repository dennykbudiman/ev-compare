# EV Compare: instructions for updating

EV Compare compares battery-electric cars, trucks and vans sold in Indonesia. The site is built from the JSON files in `data/` and published by GitHub Actions on every push to `main`.

## Before changing data
- Read `data/FIELDS.md` (all vehicles) and, for trucks, `data/TRUCK_FIELDS.md`. They are the rules; follow them exactly.
- Every value needs a source under the same key. No source → leave the field out. Never guess, estimate or copy a figure from another trim.
- Indonesian sources first. A figure from another market only for the exact same version, tagged with `market`, and explained in `notes` and `notes_id`. Price, assembly, warranties, service and segment never come from another market.
- Conflicting sources: use the official Indonesian figure; otherwise leave the field out and explain the conflict in notes.
- `notes_id` is natural Indonesian (decimal comma, thousands dot), not a word-for-word translation, and never contains raw field names.
- Trucks: `body_type` is required; class (`segment`) follows gross vehicle weight; quoted prices that are not on-the-road go in `price_quote_idr` with `price_quote_basis`.

## After changing data
1. `python3 data/validate.py` must report 0 errors.
2. `python3 app/build.py` must finish; check the `untranslated:` line it prints. New English text values need an Indonesian entry in `data/id.json` (codes, brand names and units stay as they are).
3. Open `dist/index.html` in a browser (or a headless browser) and check the vehicles you changed, in both languages.
4. Commit with a message that says which vehicles and fields changed and why.

## App changes
- `app/template.dc.html` is the single source of the app (layout, logic, strings in English and Indonesian). `app/build.py` merges the data into it and writes `dist/index.html` (website) and `dist/ev-compare.dc.html` (Claude Design version).
- `app/runtime.js` runs the template in a normal browser with Preact (`app/vendor/preact.umd.js`, pinned version, MIT licence).
- Record design decisions in `DESIGN.md`.
