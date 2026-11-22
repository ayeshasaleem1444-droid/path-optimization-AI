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
  time from distance, OSRM duration, hour, peak flag.

## Progress

- Day 1 (2026-11-13): Geocoding with Nominatim + first OSRM route built
  by hand — Packages Mall → Barkat Market: 8.16 km, ~10.3 min, code Ok.
- Day 2 (2026-11-17): Live-location tests. Laptop and phone first repeated
  one wrong network position (Shahdara Bagh) even on mobile data; after a
  GPS lock the phone located accurately near home. Lesson: the app must
  always show the found location and let the user confirm or correct it.
- Day 3 (2026-11-18): Screen layout built and simplified — form and
  Leaflet map side by side, dashboard menu with panels, result cards
  relabelled Fuel Needed / Route Status. Pushed in two commits.
- Day 4 (2026-11-21): Location dropdowns replaced with free-text inputs —
  the user now types any start and destination in Lahore instead of
  picking from the fixed node list.
- Day 5 (2026-11-21): Nominatim geocoding wired into the app — typed
  place names become coordinates and markers on the map. Live test
  passed: Packages Mall → MAO College.
- Day 6 (2026-11-21): OSRM route call added after geocoding — real
  distance and duration now show in the result cards (Packages Mall →
  MAO College: 14.27 km, 16 min; own test, Shahdara → Kalma Chowk:
  15.64 km, 17 min). OSRM time is a car in free-flow conditions — the
  baseline the AI model will learn to correct. Lessons: getElementById
  is case-sensitive, and a block of code only works inside the function
  that owns its variables.
