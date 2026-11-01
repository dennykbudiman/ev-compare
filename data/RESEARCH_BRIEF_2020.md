# Research brief: earlier model years (2020–2023)

Same job as /home/claude/evc/data/RESEARCH_BRIEF.md (read it and /home/claude/evc/data/FIELDS.md first; every rule still applies), but now for model years 2020, 2021, 2022 and 2023 of battery-electric PASSENGER CARS officially sold in Indonesia. No grey imports, no hybrids, no commercial vans.

- Many models already have files with 2024–2026 trims. ADD your earlier-year trims to the existing file (load the JSON, append to "trims", write back with indent=2, ensure_ascii=False). Never change or delete existing trims.
- New models (e.g. Hyundai Ioniq Electric) get new files.
- Earlier-year trims are almost always "discontinued".
- Year rule: one record per model year only when specs or price changed; otherwise one record for the first model year it was sold with a note like "Same specs 2021–2023". Don't duplicate a 2024 record backwards if nothing changed; just note in the earliest record that it continued.
- Prices: the launch or last known Jakarta OTR price for that model year. Older prices are often only in launch news; that's fine as a source.
- Every trim needs BOTH "notes" (English) and "notes_id" (natural Indonesian, decimal comma and thousands dot, keep names/units/abbreviations).
- Web searches are limited; spend them on finding one rich spec page per model (launch article with a full spec table, or the brand's archived spec page).
- When done: `cd /home/claude/evc && python3 data/validate.py` must show 0 errors for the whole folder.

Report (under 250 words): models and trims added per brand, models you looked for but found no official Indonesian sale of, top 3 doubts, validator line.
