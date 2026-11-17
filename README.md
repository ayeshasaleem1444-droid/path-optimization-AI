# Path Optimization — Live APIs & AI

A Flask web app that finds the shortest path between two places in Lahore.
It began with my own A\* search (f(n) = g(n) + h(n), haversine heuristic)
over a small static graph of 6 Lahore hubs — and is now being upgraded
to live data: the user will enter any start and destination in Lahore.

## Planned live stack (free, no API keys)

- Nominatim (OpenStreetMap) — place name → coordinates
- OSRM — real road-network routing: distance + duration
- Leaflet + OpenStreetMap tiles — route line on a map
- Fuel estimate — distance ÷ vehicle mileage × fuel price
- AI model (planned) — a regression model that predicts actual travel
  time from distance, OSRM duration, hour, peak flag and weather

## Progress

- Day 1 (2026-11-13): Geocoding with Nominatim + first OSRM route built
  by hand — Packages Mall → Barkat Market: 8.16 km, ~10.3 min, code Ok.
- Day 2 (2026-11-17): Live-location tests. Laptop and phone first repeated
  one wrong network position (Shahdara Bagh) even on mobile data; after a
  GPS lock the phone located accurately near home. Lesson: the app must
  always show the found location and let the user confirm or correct it.
