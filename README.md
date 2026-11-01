# EV Compare

Compare electric cars, trucks and vans sold in Indonesia: price, range, charging, payload and technical details, in English and Bahasa Indonesia. Every figure has a source; figures from other markets are labelled and never marked as best.

**Site:** https://dennykbudiman.github.io/ev-compare/

## What's here
| Folder | What it holds |
|---|---|
| `data/cars/<brand>/<model>.json` | Passenger cars, model years 2020–2026, one record per trim and year |
| `data/trucks/<brand>/<model>.json` | Pickups, vans, minibuses and trucks |
| `data/FIELDS.md`, `data/TRUCK_FIELDS.md` | The format, every field and the sourcing rules |
| `data/validate.py` | Checks every file against the rules |
| `data/assumptions.json` | Electricity tariffs, charging losses and range factors used by calculated rows |
| `data/id.json` | Indonesian translations of text values |
| `app/` | The app (template, build script, small web runtime) |
| `DESIGN.md` | Design decisions and the history of each review round |

## How the site updates
Every push to `main` runs `.github/workflows/publish.yml`: it checks the data, builds `dist/index.html` and publishes it to GitHub Pages. If the check fails, nothing is published and the site keeps the last good version.

To build locally:
```
python3 data/validate.py
python3 app/build.py      # writes dist/index.html
```
