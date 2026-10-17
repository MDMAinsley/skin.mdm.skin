# MDM Skin 0.2.0 — Kodi 22 development

Install from MDM Repo (Development), then Settings > Interface > Skin > MDM Skin. Kodi asks whether to keep the skin; if the home is not usable, let its confirmation expire to return to the previous skin. Settings remains on the home sidebar. Return to Estuary through Interface > Skin at any time.

Home has Films, TV, Search, Flix, Setup (Conf), Favourites, Add-ons, Settings, Flix settings, Home mode, Refresh rows, Now playing and Power. Two trending TMDB rows show at most twelve titles each. Select a movie to use your Source Select/Autoplay preference, or a show for its seasons. Missing credentials/network produces empty rows without modal dialogs; settings/navigation remains usable. No stream scraping, debrid calls or automatic trailers run on home.

Home mode offers Auto, Basic and Artwork. Auto uses total memory, userdata filesystem free space and Flix's existing Light artwork preference: 2 GiB RAM or less, 512 MiB free or less, Light or unknown facts means basic. Device/platform alone does not determine performance. These are recommendations, not benchmarks. Manual Artwork overrides the recommendation; Basic loads no widget includes or home artwork. The first automatic startup begins in basic and reloads once if artwork is recommended. Returning home recomputes the recommendation. It does not change accounts, playback preferences or the active skin.

The skin retains Estuary browsing/dialogs/keyboard/settings/playback windows, with attribution/licenses in ATTRIBUTION.md, ESTUARY-LICENSE.txt, LICENSE.txt and fonts/. Foundation inventory is in FOUNDATION.json. GUI API 5.18.0 requires Kodi 22; Firestick/Kodi 21 acceptance is still open.

Saved lists, personal ratings, continue watching/resume tracking, explicit trailers, full portable skin builds and Conf preventing activation on constrained devices are planned separately in the persistent MDM Skin roadmap. Kodi Favourites is available now but is not yet an MDM saved-list system.

Home mode and its derived artwork flag use device_ keys, excluded by Conf portable-build validation. Each device makes its own recommendation.


## Search and title clicks (0.2.0 / Flix 0.7.0)

Search opens one keyboard and returns mixed Film/TV results in TMDB relevance order (people excluded); pagination retains the query. Movie and episode clicks go directly to Source Select or Autoplay according to the Flix preference when the list is loaded. Shows open seasons/episodes, including specials. Hold/menu, keyboard C or mouse right-click > Title information opens metadata without searching for sources. Existing saved legacy details links still work.

Home rows remain visible while loading, so Kodi can apply asynchronous results without leaving the screen. Native item actions distinguish playable items from folders and retain the context menu. Empty rows fall back to the sidebar. Home Flix settings refreshes the mode-sensitive widget URL after closing; ordinary Flix settings requests a container refresh. Reopen a catalogue page after changing playback preferences externally.

Artwork currently uses Kodi's texture cache; no global cache deletion is performed. Active-set, bounded MDM-owned artwork caching/eviction is recorded for the cache milestone, with stale removal only after successful replacement and preservation of other addons' images.


0.2.1 — 17 October 2026
Remove the home-only 175-pixel context-menu translation, which moved the menu after Kodi computed its screen bounds and clipped TV-row menu actions. Keep Kodi positioning, scrolling and the existing film/TV row layout. DialogContextMenu.xml now intentionally differs from the pinned Estuary foundation by removal of that translation.
