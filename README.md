# MDM Skin 0.1.0 — Kodi 22 development

Install from MDM Repo (Development), then Settings > Interface > Skin > MDM Skin. Kodi asks whether to keep the skin; if the home is not usable, let its confirmation expire to return to the previous skin. Settings remains on the home sidebar. Return to Estuary through Interface > Skin at any time.

Home has Films, TV, Search, Flix, Setup (Conf), Favourites, Add-ons, Settings, Flix settings, Home mode, Refresh rows, Now playing and Power. Two trending TMDB rows show at most twelve titles each. Select a movie for existing Flix details, or a show for its seasons. Missing credentials/network produces empty rows without modal dialogs; settings/navigation remains usable. No stream scraping, debrid calls or automatic trailers run on home.

Home mode offers Auto, Basic and Artwork. Auto uses total memory, userdata filesystem free space and Flix's existing Light artwork preference: 2 GiB RAM or less, 512 MiB free or less, Light or unknown facts means basic. Device/platform alone does not determine performance. These are recommendations, not benchmarks. Manual Artwork overrides the recommendation; Basic loads no widget includes or home artwork. The first automatic startup begins in basic and reloads once if artwork is recommended. Returning home recomputes the recommendation. It does not change accounts, playback preferences or the active skin.

The skin retains Estuary browsing/dialogs/keyboard/settings/playback windows, with attribution/licenses in ATTRIBUTION.md, ESTUARY-LICENSE.txt, LICENSE.txt and fonts/. Foundation inventory is in FOUNDATION.json. GUI API 5.18.0 requires Kodi 22; Firestick/Kodi 21 acceptance is still open.

Saved lists, personal ratings, continue watching/resume tracking, explicit trailers, full portable skin builds and Conf preventing activation on constrained devices are planned separately in the persistent MDM Skin roadmap. Kodi Favourites is available now but is not yet an MDM saved-list system.
