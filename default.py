"""Local home choice. Never changes the active skin, Flix preferences or accounts."""
import os
import re
import shutil
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "resources"))
from adaptive import memory_mb, recommend


ACCENTS = (
    ("MDM Red", "E50914"),
    ("Purple", "8754CF"),
    ("Blue", "317DD4"),
    ("Teal", "28A99E"),
    ("Gold", "EAB64D"),
)
ACCENT_SETTING = "mdm_home_accent"
REPO_SETTING = "device_mdm_home_repository"
REPOSITORIES = {
    "repository.mdm.repo": "Public",
    "repository.mdm.repo.dev": "Dev",
}


def luminance(rgb):
    channels = (int(rgb[i:i+2],16)/255 for i in (0,2,4))
    linear = (value/12.92 if value <= .04045 else ((value+.055)/1.055)**2.4 for value in channels)
    return sum(weight*value for weight,value in zip((.2126,.7152,.0722),linear))


def valid_accent(value):
    return re.fullmatch(r"[0-9A-F]{6}",value) and (luminance(value)+.05)/(luminance("202024")+.05) >= 3


def apply_accent(accent):
    window = xbmcgui.Window(10000)
    window.setProperty("mdm_home_accent", "FF"+accent)
    window.setProperty("mdm_home_accent_text", "FFFFFFFF" if luminance(accent)<=.179 else "FF000000")


def set_trailer_key():
    window = xbmcgui.Window(10000)
    if xbmc.getCondVisibility("System.Platform.Android"):
        if window.getProperty("mdm_trailer_key"):
            return
        import subprocess

        try:
            model = subprocess.check_output(
                ["/system/bin/getprop", "ro.product.model"], text=True, timeout=1
            ).strip()
        except (OSError, subprocess.SubprocessError, UnicodeError):
            model = ""
        key = "firetv" if re.fullmatch(r"AFT[A-Z0-9]+", model) else "generic"
    else:
        desktop = any(xbmc.getCondVisibility("System.Platform." + platform)
                      for platform in ("Windows", "OSX", "Linux"))
        key = "keyboard" if desktop else "generic"
    window.setProperty("mdm_trailer_key", key)


def choose_accent(current):
    dialog = xbmcgui.Dialog()
    choice = dialog.select("Home accent colour",[name for name, _ in ACCENTS]+["Custom hex colour…"])
    if not 0 <= choice <= len(ACCENTS):
        return
    if choice < len(ACCENTS):
        accent = ACCENTS[choice][1]
    else:
        keyboard = xbmc.Keyboard(current,"Home accent colour (six hex digits)")
        keyboard.doModal()
        if not keyboard.isConfirmed():
            return
        accent = keyboard.getText().strip().lstrip("#").upper()
        if not valid_accent(accent):
            dialog.ok("Home accent colour","Enter six hex digits and choose a colour that stands out against the dark home screen.")
            return
    xbmc.executebuiltin("Skin.SetString("+ACCENT_SETTING+","+accent+")")
    apply_accent(accent)


def repository_shortcut(action):
    enabled = [repo for repo in REPOSITORIES
               if xbmc.getCondVisibility(f"System.AddonIsEnabled({repo})")]
    saved = xbmc.getInfoLabel(f"Skin.String({REPO_SETTING})")
    repo = saved if saved in REPOSITORIES else next(iter(enabled), None)

    if action == "choose_repository":
        options = list(REPOSITORIES)
        labels = [
            f"MDM Repo ({REPOSITORIES[option]})" + ("" if option in enabled else " — unavailable")
            for option in options
        ]
        choice = xbmcgui.Dialog().select(
            "Home repository shortcut", ["Automatic"] + labels,
            preselect=options.index(saved) + 1 if saved in options else 0,
        )
        if 0 <= choice <= len(options):
            saved = options[choice - 1] if choice else "auto"
            xbmc.executebuiltin(f"Skin.SetString({REPO_SETTING},{saved})", True)
            repo = saved if saved in REPOSITORIES else next(iter(enabled), None)

    label = f"MDM Repo ({REPOSITORIES[repo]})" if repo else "MDM Repo"
    xbmcgui.Window(10000).setProperty("mdm_home_repository_label", label)
    if action == "open_repository":
        if repo in enabled:
            xbmc.executebuiltin(f"ActivateWindow(addonbrowser,addons://{repo}/,return)")
        else:
            target = label if repo else "an MDM repository"
            xbmcgui.Dialog().ok("MDM Repo", f"Install or enable {target} in Kodi Add-ons, or change the shortcut in MDM Settings.")
            xbmc.executebuiltin("ActivateWindow(addonbrowser)")


def run():
    if xbmc.getSkinDir() != "skin.mdm.skin":
        return
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    if action == "settings_menu":
        options = (
            ("MDM Setup", "RunAddon(script.mdm.conf)"),
            ("Flix settings", "flix_settings"),
            ("Home mode", "choose"),
            ("Manage lists and ratings", "ActivateWindow(Videos,plugin://plugin.video.mdm.flix/?action=library_home,return)"),
            ("Add-ons", "ActivateWindow(addonbrowser)"),
            ("Kodi settings", "ActivateWindow(settings)"),
            ("Home list shortcut", "RunPlugin(plugin://plugin.video.mdm.flix/?action=library_home_list_choose)"),
            ("Home accent colour", "accent"),
            ("Home repository shortcut", "choose_repository"),
        )
        choice = xbmcgui.Dialog().select("Settings", [label for label, _ in options])
        if not 0 <= choice < len(options):
            return
        action = options[choice][1]
        if action not in ("choose", "flix_settings", "accent", "choose_repository"):
            xbmc.executebuiltin(action)
            return
    repository_shortcut(action)
    if action in ("choose_repository", "open_repository"):
        return
    accent = xbmc.getInfoLabel("Skin.String("+ACCENT_SETTING+")").upper()
    if not valid_accent(accent):
        accent = ACCENTS[0][1]
    if action == "accent":
        choose_accent(accent)
        return
    apply_accent(accent)
    set_trailer_key()
    try:
        flix = xbmcaddon.Addon("plugin.video.mdm.flix")
        if action == "flix_settings":
            flix.openSettings()
        # Whitelisted, non-secret mode in the widget URL invalidates cached
        # directory items when the playback preference changes. Metadata still
        # uses the existing Core cache. No source requests occur on home.
        mode_key = "autoplay" if flix.getSetting("playback_mode") == "Autoplay" else "select"
        xbmcgui.Window(10000).setProperty("mdm_widget_mode", mode_key)
    except RuntimeError:
        xbmcgui.Window(10000).setProperty("mdm_widget_mode", "select")
    memory = memory_mb(xbmc.getInfoLabel("System.Memory(total)"))
    try:
        free = shutil.disk_usage(xbmcvfs.translatePath("special://profile/")).free
    except (OSError, ValueError):
        free = None
    try:
        light = xbmcaddon.Addon("plugin.video.mdm.flix").getSetting("device_artwork") == "Light"
    except RuntimeError:
        light = True
    artwork_recommended, _ = recommend(memory, free, light)
    preview_recommended = not light and memory is not None and memory >= 6144
    automatic = ("Full" if preview_recommended else "Balanced") if artwork_recommended else "Basic"
    options = {
        "Auto": "Auto — recommended: " + automatic,
        "Full": "Full — artwork, rows and muted trailer previews",
        "Balanced": "Balanced — artwork and rows",
        "Light": "Light — simpler artwork and rows",
        "Basic": "Basic — menu only",
    }
    mode = xbmc.getInfoLabel("Skin.String(device_mdm_home_mode)")
    if mode == "Artwork":
        mode = "Full" if preview_recommended else "Balanced"
    if mode not in options:
        mode = "Auto"
    if action == "choose":
        modes = list(options)
        choice = xbmcgui.Dialog().select(
            "MDM Home mode", list(options.values()), preselect=modes.index(mode),
        )
        if not 0 <= choice < len(modes):
            return
        mode = modes[choice]
        xbmc.executebuiltin(f"Skin.SetString(device_mdm_home_mode,{mode})", True)
    # Do not reload underneath Kodi's "keep this skin?" confirmation or another
    # modal dialog. If it remains open, this home visit stays in its current mode.
    monitor = xbmc.Monitor()
    for _ in range(200):
        if not xbmc.getCondVisibility("System.HasActiveModalDialog"):
            break
        if monitor.waitForAbort(0.1):
            return
    else:
        return
    effective = automatic if mode == "Auto" else mode
    desired = effective != "Basic"
    window = xbmcgui.Window(10000)
    window.setProperty("mdm_home_mode", effective)
    window.setProperty("mdm_preview_enabled", "true" if effective == "Full" else "false")
    current = xbmc.getCondVisibility("Skin.HasSetting(device_mdm_artwork)")
    if bool(current) != desired:
        xbmc.executebuiltin("Skin.SetBool(device_mdm_artwork)" if desired else "Skin.Reset(device_mdm_artwork)")
        # Includes are selected on skin load. Read back before requesting a
        # single reload; a failed setter must not create an endless reload loop.
        monitor = xbmc.Monitor()
        for _ in range(10):
            if bool(xbmc.getCondVisibility("Skin.HasSetting(device_mdm_artwork)")) == desired:
                xbmc.executebuiltin("ReloadSkin()")
                break
            if monitor.waitForAbort(0.05):
                break


if __name__ == "__main__":
    run()
