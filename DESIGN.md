# EV Compare — Design direction

**Subject:** spec comparison of battery-electric cars and trucks sold in Indonesia.
**Audience:** fleet owners, buyers and workshop technicians, mostly on phones.
**Primary job:** put 2–3 vehicles side by side and make the differences obvious.

## Direction: "workshop datasheet"
Specs should read like a manufacturer's service datasheet: precise, tabular, calm.
The one bold element is **high-voltage orange**, which on real EVs marks HV cabling.
In this app it is reserved for the Technician mode, so the colour means "deeper,
technician-level data" and nothing else.

Compared before deciding:
- Zecar EV database: search, filters and spec cards with a WLTP-only range field. Lesson: always show the test cycle, since Indonesian sources mix WLTP, NEDC, CLTC and unstated claims.
- Apple product compare: fixed columns, each chosen independently. Lesson: one column per vehicle, with values aligned by row.
- Indonesian/Indian car portals (Oto, CarWale): a Brand → Model → Variant picker. Lesson: we add Year, because Indonesian specs change with facelifts.

## Color (roles)
| Token | Hex | Role |
|---|---|---|
| ink | #15212B | Primary text |
| muted | #52606B | Secondary text (5.9:1 on white) |
| ground | #F1F3F4 | App background |
| surface | #FFFFFF | Lists, cells, cards |
| line | #D5DBDF | Hairlines, outlines |
| cobalt | #1E4FC2 | Interactive tint: buttons, selection, links |
| best / best-bg | #17643F / #DFF1E7 | Best value in a row |
| hv / hv-bg / hv-text | #C2410C / #FDE9DA / #9A3412 | Technician mode only |
| warn / warn-bg | #7C4A03 / #FCF0D9 | Range test-cycle warning; dashed outline for single-source values (#A15C00) |

All text pairs pass 4.5:1 (checked with hig_checker.py).

## Type
- **Barlow** (DIN-style grotesque, a nod to German engineering datasheets) for all UI text.
- **Barlow Semi Condensed** for large titles, model names and every spec value. It is narrow enough for three columns on a 390 pt phone. Use tabular figures.
- Scale (pt): large title 30/34 bold · title 20/24 semibold · headline 17/22 semibold · body 16/22 · subhead 14/19 · footnote 13/18 · caption 12/16. Nothing smaller than 12.
- Sentence case everywhere. No all-caps labels. No monospace.

## Spacing and shape
- 4 pt grid: 4, 8, 12, 16, 24, 32. Screen margin 16.
- Radius: 8 for spec cells, 10 for inset-grouped lists, 12 for controls, 20 for the top of a sheet.
- No drop shadows, except under the segmented-control thumb.

## Components (iOS HIG)
- **Segmented control** for Cars / Trucks, 44 pt tall.
- **Vehicle slots** (max 3): tap to change the trim, × to remove (44 × 44 hit area).
- **Picker**: full-screen modal navigation stack with four real steps (Brand → Model → Year → Trim), so a 4-part progress bar is justified. Cancel sits top-left. The back button carries the previous screen's title. Inset-grouped lists use 52 pt rows with chevrons. Brands are grouped A–Z. Search appears on the Brand step and jumps straight to a model. Class filter pills: segment for cars, truck class for trucks.
- **Year step** always shows, even when a model has only one year.
- **Trim cards** show battery, range, power, drive layout and DC max. Every card is a checkbox. The picker opens with the current comparison already ticked, and ticks carry across brands and models within one session. Up to 3 in total; the other cards dim at the limit. Columns follow tick order, left to right. "Done (n of 3)" applies the selection; Cancel discards it. "Untick all" sits at the top right of every picker step as plain red text (#B42318, 6.6:1 on white), grey when nothing is ticked. It asks for confirmation first, then clears all ticks and returns to the Brand step. Ticks are plain checkmarks, not numbers.
- **Sections fold**: each section title is a 44 pt button with a chevron. A folded section shows its row count ("12 rows"). All open by default.
- **Spec rows (compact)**: 12 pt label above, 15 pt values in cells with 5 × 8 px padding and 6 px radius, 5 px between columns, 8 px between rows. All-empty rows still show. Best value is green. Missing data shows "—". Single-source data gets a dashed amber outline.
- **Row titles** use the long form of any abbreviation (e.g. "Gross Vehicle Weight", "Vehicle-to-Load"). Values keep their abbreviations. There is no glossary block.
- **Abbreviation notes**: technical abbreviations on the compare screen have a dotted underline. Common ones get no note: units, AC/DC, FWD/RWD/AWD, SUV/MPV, "Approx.", "maks.". Tapping it opens a dark note beside it with the full form, plus the Indonesian meaning in ID mode. Tapping anywhere else or scrolling closes it.
- **Motion**: only in response to actions. Screens push in from the right and the sheet rises (220–280 ms). Turned off under reduced motion.

## Technician details
- The toggle adds technician rows inside their matching sections. Each has an orange label (#9A3412) with the high-voltage triangle icon.
- Vehicle: platform. Battery: usable capacity, pack nominal voltage, pack voltage range, cell supplier, cell format, cell count and configuration, pack weight, pack cooling, battery warranty. Motor: motor supplier, inverter semiconductor, reduction gear ratio (up to 3 decimals), maximum regenerative braking. Charging: on-board charger, Vehicle-to-Load.
- Technician-only section "Service and diagnostics" (orange title + icon): high-voltage service disconnect, auxiliary battery, coolant, cooling loops, heat pump, diagnostic port, diagnostic protocol, over-the-air updates.

## Section order
Vehicle → Price and ownership → Battery → Range → Motor → Charging → Safety → Service and diagnostics (Technician only) → Basic information.
- Price and ownership: on-the-road price (Jakarta), shown as "IDR 545 million" / "Rp 545 juta"; vehicle warranty; battery warranty (moved here from Technician details); service interval; free service package.
- Charging adds: AC full-charge time (0–100%), charge port location, battery preheating, Vehicle-to-Load with output in kW (visible to everyone, moved from Technician details). (Vehicle-to-Grid and Vehicle-to-Home removed as not relevant.)
- Safety: wading depth, battery Ingress Protection rating, airbags, advanced driver assistance features, crash test rating.
- Trucks add: axle configuration, rated axle load (front / rear), Gross Combination Weight, towing capacity (Vehicle); range at full payload (Range); electric power take-off (Motor).

## Basic information (last section)
Seating, dimensions (L × W × H), wheelbase, ground clearance, kerb weight, boot and front-boot capacity, headroom and legroom (front / rear), turning radius, tyre size, 0–100 km/h, top speed. Boot, front boot, headroom and legroom are hidden for trucks. Trucks instead get "Seats in cab" (relabelled Seating), "Cab type" and "Cargo body size (L × W × H)". Basic information is always the last section, after Service and diagnostics when Technician details is on.

## Language
- English is the default, with an EN / ID switch in the header.
- Indonesian terms: trim is "Tipe"; GVW stays "GVW"; technical abbreviations stay unchanged.
- Indonesian mode uses a decimal comma and a thousands dot (60,5 kWh; 1.500 kg).
- Text values are translated from English into natural, contextual Indonesian (no Indonesian sources needed), kept in tr_id.json. Proper names, standards, codes and tyre sizes stay as they are. The build lists any value without a translation.

## Decisions left to the owner
- App name and icon.
- Vehicle photos (skipped for now).

## Changes after the 10-persona review (31 Oct 2026)
- **Picker tray**: every picker step has a bottom bar with the selected vehicles as chips (tap to remove) and "Done (n of 3)". Tapping a dimmed trim at the limit shows "Remove one below to add another".
- **Best-value rules**: no green box on Technician rows; none on range and energy rows when test cycles differ; none at all when the compared trucks are from different classes (a banner says so); none when the gap is under 3%.
- **Numbers**: thousands separators on all values; prices of IDR 1 billion and up shown as "IDR 1.35 billion" / "Rp 1,35 miliar".
- **Real-world range and running cost** (Range section): estimated real-world range (claimed × test-cycle factor: WLTP/WLTC 0.85, EPA 0.95, NEDC 0.72, CLTC 0.70, C-WTVC 0.80, unstated 0.75; trucks use range at full payload); estimated consumption (usable kWh ÷ real-world range); energy cost per 100 km at home (PLN 3,500 VA+ tariff Rp 1.699,53/kWh + 10% charging loss) and at a public charger (~Rp 2.466/kWh, excl. per-session fee). Each method is explained once under its row.
- **DC fast-charge time** labelled "(10–80%)".
- **Technician icon**: wrench instead of the warning triangle.
- **Indonesian**: "Detail teknis", "Hanya yang berbeda", "Terbaik", "km/jam", "Jarak bebas ke tanah", "Aki tambahan", "rekaan", "filter segmen", "Rating Ingress Protection baterai (tahan air dan debu)", "Jumlah Berat yang Diperbolehkan (JBB)", "Jumlah Berat Kombinasi yang Diperbolehkan (JBKB)"; Indonesian meanings added for CCS2, CCS, MCS, WLTP, NEDC, CLTC, IGBT.
- **Price region**: Jakarta OTR only (most regions are a markup on Jakarta pricing).

## Future: share and save (planned, not built)
1. Share link: the comparison is encoded in the page address (vehicle IDs, language, toggles), so a WhatsApp link opens the same comparison. No account needed.
2. Share as image: a "Share" button renders a tidy summary card (vehicles and key rows) to a picture for WhatsApp or Instagram.
3. Export PDF: the full comparison, with sources and data date, for finance or partners.
4. Saved comparisons: kept on the phone first; synced to an account later (with hosting).
5. Preset comparisons: e.g. "model vs usual rivals" for dealers.

## Changes, round 2 (31 Oct 2026)
- **Picker header**: the brand/model/year path sits on the same line as "Step x of 4" (right-aligned), above the large title.
- **Done** is grey and disabled when nothing is ticked.
- **Truck vehicle boxes** show a class pill ("Light class" / "Kelas Ringan").
- **Section renamed**: "Price, warranty and service package" / "Harga, garansi, dan paket servis".
- **Toolbar**: Technician details | Key specs | View. Technician and Key specs are mutually exclusive.
- **Key specs** shows only key rows: price, battery warranty, real-world range (cars) or range at full payload (trucks), energy cost at home, peak power, DC 10–80% time, crash rating, seats, boot (cars), GVW and payload (trucks), total cost of ownership, cost per km.
- **View options sheet**: Differences only; Same test cycle only (range and cost values tested differently from the first column read "Different test method"); Hide calculated values. The button shows how many are on, e.g. "View (2)".
- **Journalist items**: a source button on each row opens a sheet per vehicle (value, published source link, date, type, single-source or 2+ sources; calculated rows explain their method); calculated values in italics with a legend entry; "Power (peak)" and "DC max (peak)"; "Data as of" date per vehicle in Sources and notes.
- **Cost of ownership** (last section, before Sources and notes): adjustable distance per day (cars 30/50/100/250 km, trucks 100/200/300 km), ownership period (3/5/8 years), share charged at home or depot (100/80/50/0%). Rows: purchase price, charger installation, energy, service and tyres (free-package years not charged), insurance (% of price per year), annual tax, resale value (fixed yearly depreciation, subtracted), total cost of ownership, cost per km. Trucks assume 300 working days a year.
- **Accessibility**: table semantics (section = table, hidden column headers with vehicle names, row headers, cells named "vehicle: value, best, single source"); check icon for best and dashed-circle icon for single source (also in the legend); all text sizes in rem so they follow the phone's text size, and columns stack with vehicle names when root text is 20 px or more; focus moves into the picker, sheets, notes and confirmation, Tab is trapped inside them, Escape closes the top layer, and focus returns to the button that opened them; a polite live region announces removals, comparisons and toggle changes; filter pills 44 pt; back button named "Back to …"; trim cards read their name and stats; notes no longer close on scroll. Not yet: dark mode and high-contrast theme.

## Changes, round 3 (31 Oct 2026)
- **Removed**: the View options sheet (Same test cycle only, Hide calculated values) and the whole Cost of ownership section, which relied on too many assumptions. The toolbar is now Technician details | Key specs | Differences only. Key specs no longer includes total cost or cost per km.
- **Fixed**: a label clash that showed "Done ({n} of 3)" on sheet Done buttons. Sheets now use their own "Done" label.
- **IDR**: no tap note.
- **Display themes**: a Display button (half-filled circle) beside EN/ID opens Automatic / Light / Dark / High contrast. Automatic follows the phone's dark mode and "increase contrast" settings. Every colour is a token on the app root (`--ground`, `--surface`, `--ink`, `--muted`, `--accent`, `--on-accent`, `--best`, `--best-bg`, `--hv`, `--warn`, `--unc`, `--danger`, `--tip-bg` and others), redefined per theme. All text pairs in Dark and High contrast pass 4.5:1.
  - Dark: ground #0E1317, surface #182026, ink #E9EEF2, muted #A9B5BF, accent #7AA2FF with dark text on accent, best #8EE0B1 on #133524, technician orange #FF8B57.
  - High contrast: white ground, black text, near-black lines (#1F1F1F), accent #0030A0, best #003D1B on #BDEBCD, technician orange #8A2400.

## Changes, round 4: "less AI" pass

Copy (final-review skill, independent reviewer): plainer EN and more natural ID wording; "test method not stated"; "Untick all trims?"; neutral "clear the filter"; HV row renamed "High-voltage service disconnect location"; GB/T full name; NEDC/CLTC optimism notes; softer IP68 note. Kept "(tahan air dan debu)" and did not use "filter segmen".

Visual (chosen by the owner from the design audit):
- Neutral greys replace the blue-tinted slate in light and dark (ink #141414, muted #575757, line #D6D6D6, ground #F0F0F0; dark ground #111111, surface #1C1C1C). All text pairs re-checked, 4.7:1 or better.
- Three corner sizes only: 4 (cells, badges, checkboxes), 10 (cards, buttons, segmented controls, lists), 20 (sheets, dialogs). Fully round shapes only on switches. Segmented tracks have no inner padding so the selected segment can share the 10 radius.
- Fewer pills: truck class is plain text on the vehicle card; Sample badge, filter buttons and tray chips are no longer round.
- Calmer header: "Compare" is a 17px title; Display button has no fill; EN/ID is a text switch with an underline on the active language.
- View control: one segmented control "All specs | Key specs | Technician" (Technician always in HV orange text), plus a "Differences only" switch row.
- Add vehicle: the dashed button is gone. An "+ Add" slot sits in the pinned vehicle row: full width when nothing is chosen, a 52px column otherwise. Spec rows keep a matching empty 52px column so columns stay aligned.
- Sources: tap a row's name (not an icon) to open its sources; a line under the legend says so. Sources and source-sheet entries are each one inset list with dividers.
- Technician rows: a continuous 3px HV-orange line down the left edge replaces the per-row wrench; the legend explains it while Technician is on. The section header keeps its wrench.

Not applied: flat one-surface table (owner kept the separate cells).
- High contrast: spec cells get a 1px #4D4D4D outline (token --cell-line, transparent in light and dark), because cells and background are both white in that theme.
- Tappable abbreviations keep their brackets and trailing punctuation on the same line (wrapped in a no-break span), e.g. "(WLTP," never splits.
- High contrast: picker lists, trim cards, sources list and source sheet list also get the --cell-line outline.

## Adaptive layout (all screen sizes)

One design that measures the width it actually has (ResizeObserver on the root and the scroll area), so it adapts to any phone, tablet, split view, laptop window or desktop. No device detection.

| Size class | Width | Page padding | Layout |
|---|---|---|---|
| Compact | under 600 px | 16 | Phone layout: spec name above the values. Up to 3 vehicles fill the width; 4 or more become 128 px columns and the table scrolls sideways. |
| Regular | 600 to 1023 px | 24 | Real table: spec names in a pinned left column (160 px under 768 wide, 200 px above), vehicle columns at least 140 px. |
| Wide | 1024 px and up | 32 | Same table, 240 px label column, vehicle columns at least 170 px; one-row top bar (title, Cars/Trucks, view switch, Display, language). |

- Limit is 10 vehicles on every screen (owner's call). Columns share the width while they fit; past that they keep their minimum width and the table scrolls sideways. A legend line says so.
- While scrolling sideways these stay put: top bar, section titles, warnings, row notes, the spec-name column (tablet and wide), the corner cell and the legend. The vehicle row stays pinned to the top.
- Tablet and wide: "Differences only" moves into the table's top-left corner with a count ("2 of 10 vehicles"); the view switch moves into the top bar.
- Tablet and wide: the vehicle picker opens as a 560 px centred panel over the comparison; Display and Sources open as 480 px centred panels. Phones keep the full-screen picker and bottom sheets.
- Text follows the system text size (rem). Phone with very large system text still stacks values with vehicle names.
- Technician line: on tablet and wide it lives in the pinned label column, so it stays visible while scrolling sideways. On phones it sits at the row edge and scrolls with the table.
- Canvas shows the same design on three boards: phone 390 x 844, tablet portrait 820 x 1180, wide 1280 x 800.
- Not built: the side list of sections floated in the plan; with up to 10 vehicles the width goes to columns instead.
- Edge bounce on all four sides, drawn by the app. The browser's own "rubber-band" bounce (iOS, iPadOS, Mac trackpads) is off (overscroll-behavior: none) because it drags pinned parts with the content. Instead the app springs only the moving parts:
  - Sideways: vehicle cards and value cells slide; spec names, corner switch, section titles, warnings, notes and legend stay put.
  - Pull down at the top: everything moves down together (nothing is pinned yet).
  - Push up at the bottom: the page moves up under the pinned vehicle row, which stays put.
  - Works for finger drags, trackpad and mouse wheel, and for a fling that hits the edge. Resistance follows the iOS curve; spring-back 0.5 s.

## Fixes from the independent review (round 1: serious)
- Weights in tonnes (Gross Vehicle Weight / JBB, Gross Combination Weight / JBKB) show up to 2 decimals (4.25 t, 2.95 t). One decimal had rounded legal weights and contradicted trim names.
- Phone with very large system text: the stacked vehicle cards scroll away with the page instead of staying pinned (each value already carries its vehicle name in this mode). Before, 3+ vehicles covered most of the screen and 10 made the table unreachable.

## Fixes from the independent review (round 2: important)
- Removing a vehicle shows "<vehicle> removed · Undo" at the bottom for 6 seconds; Undo puts it back in the same column. Cleared when switching Cars/Trucks or opening the picker. Screen readers hear that undo is available.
- Change and Remove buttons name the full vehicle with trim and year, so trims of the same model are distinguishable to screen readers.
- Picker trim cards show the test method with range ("Range, NEDC" / "Jarak, NEDC").
- Source sheet: calculated rows built on a single-source claimed range say so; entries with no source no longer show a date.

## Fixes from the independent review (round 3: small fixes and owner decisions)
Owner decisions applied:
- Row names are underlined (solid, light grey; abbreviations stay dotted) so they read as tappable; bigger tap area (full label cell on tablet and wide, taller strip on phone).
- "—" now means "Not in our data" / "Belum ada di data kami" (was "Not published").
- No best-value mark on gross battery capacity or on price (value judgements).
- "Differences only" is greyed out with "Add a second vehicle to use this" until 2+ vehicles are chosen.
- Kept: default trucks (owner chose not to change them).
Small fixes:
- Off switch track and empty checkbox border darkened to 3:1 (light #8A8A8A / #858585, dark #6B6B6B).
- Legend sample number follows the language (12.3 / 12,3).
- Units never split inside (no-break spaces, word joiner after "/"); numbers stay whole; prices may break only after "IDR"/"Rp".
- Keyboard: arrow keys, Home and End move between Cars/Trucks and between the three views (roving focus); Tab stays inside the abbreviation note.
- Table semantics: the test-method warning sits outside the table; row notes are read with the spec name and hidden as a separate block.
- Reduced motion: all transitions off, including the chevron and the bounce spring-back.
- Top bar is one row only from 1280 px wide; below that it uses two rows.
- Indonesian: "SPKLU" (with tap note) replaces "stasiun pengisian umum"; row title uses the long form per the abbreviation rule; "energi yang hilang" replaces "daya yang hilang"; "tetapi masih berupa perkiraan".
- Removed leftovers of the cost-of-ownership section and the old toolbar.
Not changed: trim names (e.g. "S battery") stay as the maker names them, in both languages.

## Fixes from the 8-identity panel review (fleet manager, technician, first-time buyer, journalist, low-vision user, older owner, engineer, dealer)
Calculations and best marks
- Trucks: no real-world estimate. Consumption and energy cost use the published full-payload range only; otherwise "—" with a note. Truck cost row is "on a PLN tariff" and notes that depot business tariffs differ.
- Public-charger cost now includes 5% charging loss (home keeps 10%). Tariff notes carry an "as of" date. Consumption is labelled "from the battery".
- WLTC factor lowered to 0.8 (Japanese WLTC skips the extra-high phase); WLTC note rewritten.
- Best mark: only on published figures (never on calculated rows), and only when first place beats second place by at least 3%.
- Test-method banner names which vehicle uses which method, in one short sentence.
- Single-source flag also comes from a source count of 1. Source sheet shows the real-world calculation per vehicle ("Claimed 420 km (WLTP) × 0.85").
Presentation
- "Not available" (the vehicle doesn't have it, e.g. no DC fast charging) is separate from "—" (not in our data). Data uses "n/a"; legend explains both.
- Key specs: claimed range with its test method for cars and trucks; trucks also get connector and AC full-charge time.
- AC full-charge time shows the power it assumes ("at 7 kW"); AC max shows a three-phase note when any value is above 7.4 kW.
- A context line under the pinned vehicles: "EV Compare · SAMPLE DATA · Oct 2026 · ✓ best · italic = estimate · dashed = single source", so screenshots keep their meaning.
- Picker trim cards show the OTR Jakarta price first. Cancel is always top right.
- Display button has a text label. "Harga OTR (on the road) Jakarta".
Technician
- New rows: auxiliary battery location; wait after high-voltage disconnect (with a zero-volt check note); coolant specification and capacity.
- Notes for DIN 70121, ISO 15118 and GB/T 27930 explain the protocol; cell configuration row explains "s" and "p".
Accessibility and layout
- iPhone and iPad Safari: rem follows the system text size (-apple-system-body, touch devices only), so the large-text layout can switch on.
- Narrow widths (page zoom): no 320 px floor; values stack below 340 px; the view switch stacks its three options.
- Undo: focus moves to it; it stays 10 s and pauses while hovered or focused; button reads "Kembalikan" in Indonesian with a full "Put back <vehicle>" label; focus returns to the vehicle row when it closes.
- High contrast: disabled Done has a visible label and border; picker step bars differ in thickness as well as colour.
- Selected segments get a 2 px accent border; EN/ID targets 44 px; top-bar tab order matches what is on screen; focus ring uses light ink on dark surfaces; scroll padding keeps focused items clear of pinned parts.
- Cells hyphenate before splitting a word; vehicle-card text keeps clear of the ×; wide-screen columns at least 150 px.
Data (sample)
- Mitsubishi L100 is in the Pickup class. Pack voltages come from cell count × cell voltage, and the build warns if nominal voltage falls outside the min–max range or does not match the cells.
Owner decisions on the panel's open items:
- Different truck classes: still no best marks (no per-class ranking).
- Technician view keeps the normal section order.
- The app opens on Key specs; in Key specs the price section comes first.
- A plain summary sits above the table when 2+ vehicles are chosen: costs less, goes further, carries more (trucks) or boot space (cars), and safety. It follows the best-mark rules (published figures only, same class, same test method, 3% lead); otherwise it says why it doesn't rank. Safety lists crash ratings without ranking.
- Monthly running cost under both energy-cost rows ("≈ IDR 361,300 a month"), 30 days a month. The daily distance is editable in a number box under the Range section ("Monthly cost uses [40] km a day"); it starts at 40 km for cars and 100 km for trucks, and each mode keeps its own value. The row note states the current value. The box can be cleared and retyped; costs only change on a whole number from 1 to 1,500, and leaving the box empty or invalid puts back the last valid number.
- The summary is collapsible (open by default), with a chevron like the sections.
- No saved comparisons or rival presets.

## Real car data (Nov 2026)
- data/ folder in GitHub-ready layout: cars/<brand>/<model>.json (one record per trim and model year), FIELDS.md, validate.py, assumptions.json, id.json, README.md, RESEARCH_BRIEF.md.
- Coverage: battery-electric passenger cars sold in Indonesia, model years 2024–2026: 226 trims, 89 models, 29 brands; 156 on sale, 70 discontinued; 4,866 sourced figures (about 30% with two or more sources).
- Researched in five brand groups; validator 0 errors; independent spot-check of 40 random figures: 39 confirmed against their source, 1 removed (VinFast VF 5 power, unit not stated).
- Notes translated to Indonesian (notes_id); new text values translated in tr_id.json / id.json.
- Build: `python3 build.py real` loads real cars and keeps sample trucks ("Sample data" shows only on Trucks). Defaults: BYD Atto 3 2026 Advanced Plus vs Geely EX5 2026 Pro.
- App: discontinued trims say "No longer sold" in the picker and on the vehicle card; DC charge times measured over another window (e.g. 30–80%) say so and are not ranked; each figure's source sheet lists every source link.
- Gaps: Smart, Lotus, Audi not researched (search limit; no evidence of Indonesian sales found); Changan line-up check incomplete; Porsche has no OTR prices; many technician fields unpublished.
- Nov 2026 extension to model years 2020–2023 (owner's choice: start at the first official EV sales, Hyundai Ioniq Electric and Kona Electric, Nov 2020; no grey imports). Added 46 trims in three groups; now 272 trims, 92 models, 30 brands. Independent spot-check of 25 older figures: 24 confirmed, 1 removed (Air ev 2023 Lite seat layout). Validator year range 2020–2026.
- Nov 2026 other-market fill (owner: "for cars without an Indonesian spec, find it in another market and note it"). Rules in FIELDS.md "Figures from other markets": same version only (battery, chemistry, power, drive must match); right-hand-drive Southeast Asia first, then Philippines/Australia, home market/global, Europe/UK; never price, assembly, warranties, service or segment; range only with that market's test standard.
  - Each borrowed source has a `market` tag; build.py sets the field's market only when all its sources share one.
  - App: the cell shows "Malaysia spec" / "spesifikasi Malaysia" under the value; the source sheet shows the market; such figures get no best mark and are not used in the summary; the legend explains the label.
  - Result: 1,631 figures across 196 of 272 trims (Malaysia 724, Europe 487, Australia 197, Thailand 86, others 137). Coverage now: gross battery 94%, range 95%, power 95%, torque 93%, drive 92%, length 93%, AC/DC max 64%, DC time 67%, boot 62%, seats 80%, airbags 66%, 0–100 67%, top speed 69%, kerb weight 43%.
  - Independent spot-check of 34 borrowed figures: 32 confirmed for the same version, 2 sources unreachable. Removed Denza Z9 GT flash-charging figures (1,500 kW / 5 min apply to the China-only flash-charging version).
  - Known doubts: some "gross" capacities are really usable (Mercedes EQA/EQB/EQE/EQS, MINI); Volvo EX90 400 V vs 800 V; Sealion 7 Extended voltage; Malaysian "weight" may not be kerb weight; Taycan Turbo S 2021 power; Nissan Leaf is the previous generation.
  - No matching foreign version found: Kona Electric gen 2, Geely EX2, Polytron, VinFast VF 5, Wuling BinguoEV, Chery Eksion and Q, Seres 3 and E1 B-Type, Jaecoo J5 and others; those fields stay empty.
- Nov 2026 doubt check:
  - Battery labels: Mercedes-Benz EQA/EQB/EQE/EQE SUV/EQS and MINI Cooper SE/JCW Indonesian figures are usable capacity; moved to battery_usable_kwh, gross added from European/Australian specs. Countryman SE ALL4 usable 64.6 kWh added.
  - Volvo EX90: Indonesian car (111 kWh, 510 hp, 250 kW) is the 400 V version; voltage corrected from 800 V (Moladin showed the later 800 V update).
  - BYD Sealion 7 Extended: voltage left out (Moladin ~400 V conflicts with 800 V for the same 91.3 kWh AWD version abroad).
  - Malaysian "Weight" figures checked against other sources: they are kerb weights; kept.
  - Nissan Leaf: second-generation 40 kWh car confirmed still listed (oto.com, Oct 2026); no third-generation Indonesian launch found. AC socket corrected to Type 2 (Antara, Aug 2021).
  - Owner: "do what gives accurate information" → new exception rule in FIELDS.md (a clearly wrong or different-basis Indonesian figure is replaced by the labelled same-version figure from another market). Applied: Taycan Turbo S 2021 power 560 kW (Porsche US MY21 sheet, overboost/Launch Control, like the other Taycans); Sealion 7 Performance DC 150 kW (Malaysia); Sealion 7 Extended 800 V (Thailand, AWD Ultimate 91.39 kWh).

## Real truck data (Nov 2026)
- Owner scope: all four kinds (pickups, small cargo/vans incl. light-commercial minibuses, light/medium trucks, heavy trucks and tractors), model years 2020–2026.
- Format: data/trucks/<brand>/<model>.json, same as cars plus truck fields; TRUCK_FIELDS.md sets classes by gross vehicle weight (Small cargo ≤3.5 t, Light ≤8.5 t, Medium ≤16 t, Heavy >16 t; Pickup by body). Validator checks truck fields, class vs GVW and payload < GVW.
- Inventory: 24 candidate models; only those offered for sale through an official channel kept. Left out: exhibition-only (Isuzu Elf EV, Hino Dutro Z EV, Daihatsu Gran Max EV concept, Mercedes eActros, others), Foton eView Connect, Sany SKT105E, XCMG XDR80TE, VKTR (no model/GVW).
- Result: 41 trims, 21 models, 12 brands (Pickup 3, Small cargo 27, Light 3, Medium 3, Heavy 5); 4 trims with other-market figures. Independent spot-check of 30 figures: 30 confirmed. Sany SE588 80 t / 120 t left out of GVW (sources disagree whether it is GVW or payload).
- App: build.py loads real trucks when data/trucks has files; "Sample data" label gone. Default truck pair: JAC N35 EV C5 vs Farizon V8E Cargo Van (both 3.5 t small cargo with price, range and payload). Truck summary "Goes further" falls back to claimed range when no full-payload range is published (same rules as the best marks).
- Gaps: payload published for only 13 of 41 trims; AC/DC charging power mostly unpublished; few OTR prices for trucks (most quoted off the road or chassis only, kept in notes).

## Truck review round (6 independent reviewers, Nov 2026)
Reviewers: fleet manager, workshop technician, data auditor, first-time van buyer (Indonesian), heavy/mining operator, accessibility and layout. Source check: 25 more truck figures, all confirmed (55/55 with the first spot-check).
Owner decisions: body type with no best across types; truck running cost from claimed range as an italic estimate (never best, not for mining trucks); depot tariff business B-2 by default with a household / B-2 / B-3 choice; research the possibly missing models.
- New truck fields: body_type (required: Pickup, Van, Minibus, Rigid truck, Tractor head, Mining truck), cargo_volume_m3, price_quote_idr + price_quote_basis (only when no OTR price; own row "Quoted price (not on the road)"), gradeability_pct, battery_swap, transmission. Validator updated.
- Best marks for trucks: same class AND same body type; never on torque or DC charge time; never on claimed range when any range has no stated test method. Payload larger than JBB minus kerb weight is flagged ("may include the body") and not ranked. Summary follows the same rules and names both vehicles in a tie (shared with cars).
- Running cost for trucks: full-payload range when published, else claimed range × test-method factor (italic, "estimate from claimed range"); mining trucks not estimated. Tariff choice under the Range section; B-2 Rp 1,444.70, B-3 Rp 1,114.74, household Rp 1,699.53 per kWh (PLN, 26–31 Oct 2026).
- Truck mode hides rows where none of the chosen trucks has a value (removes empty Technician rows, empty GCW/towing rows, crash rating for heavy trucks). Technician view always shows a high-voltage safety reminder for trucks; pack nominal voltage row explains that full-charge voltage is 10–15% higher.
- Key specs for trucks add body type, cargo volume, quoted price, vehicle warranty and GCW (shown only when a value exists). Class row explains the weight bands.
- Layout and language: "Trucks & vans" tab; cards show class and short body type, variant line clamped to 2 lines, aria label includes class, body and "No longer sold"; scroll padding follows the measured pinned header; text size re-read on resize; model year added to names when two years of the same truck are chosen; Indonesian variant names use decimal commas and JBB; range-method warning shortened for more than 4 vehicles; glossary adds GCW, SWB, LWB, MWB, OTR; picker shows truck stats (price, body, payload, JBB, battery, range).
- Data fixes: Foton eTunland torque removed (copied from JAC T9 comparison); eAumark 7T torque (axle basis unclear) and 14T power (copied from 7T) removed; Farizon F3E Australian GVW and copied DC time removed, class Light; Sany notes fixed; N90 price source and L100 launch price notes.
- Default truck pair: Wuling Mitra EV Blind Van Long Range vs DFSK Gelora E Blind Van (same class and body type, both with OTR price).
- Added after the missing-model check: LINXYS G050 and G100-R (Wuling commercial brand, orders at GIICOMVEC 2026, quoted Rp 275 juta, basis not stated), XCMG XWE105 wide-body mining truck (GM Mobil, launched Sept 2024), Foton eAumark 8.5T. Not added (display only or no price): XCMG XT370DT, XT150CD, XGE105, XGE150, SAG Max EV, LINXYS G230V. Tariff choice uses buttons, not a dropdown.

## Truck gap fill from other markets (Nov 2026)
Owner: "scrape the internet for more stats; you can use specs outside Indonesia". Four research passes (Foton; JAC, Farizon, LINXYS; vans and light trucks; heavy trucks), brief in data/RESEARCH_BRIEF_TRUCKS_FILL.md. Allowed source markets extended with New Zealand, Middle East, Latin America and Africa.
- 127 values added or changed; independent spot-check of 30: all confirmed. Matching rule made precise in TRUCK_FIELDS.md: powertrain and charging figures need the same battery, motor and drive; weights, payload and body figures also need the same GVW, wheelbase and body.
- Foton eAumark 8.5T and 9T are the same truck (Foton Brazil sells it as the 9T at 8,500 kg GVW with identical specs): merged into foton-eaumark-2026-9t, GVW 8,500 kg (Light class); change to 9,000 kg / Medium if Foton Indonesia registers it so.
- Sany SE588: 80 t / 120 t are gross combination weight (Brazilian launch, PBTC); power 480 kW (the 650 figure was hp).
- Coverage (45 truck trims): payload 16→18, AC power 6→9, DC power 10→12, AC connector 4→6, DC connector 18→23, transmission 24→31, warranties 13–14→16, gradeability 5→8, and smaller gains elsewhere. Main remaining gaps: payload, kerb weight, AC/DC charging power; Indonesian sources rarely publish them and most foreign versions differ.
