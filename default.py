"""Local home choice. Never changes the active skin, Flix preferences or accounts."""
import os
import shutil
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "resources"))
from adaptive import memory_mb, recommend


def run():
    if xbmc.getSkinDir() != "skin.mdm.skin":
        return
    memory = memory_mb(xbmc.getInfoLabel("System.Memory(total)"))
    try:
        free = shutil.disk_usage(xbmcvfs.translatePath("special://profile/")).free
    except (OSError, ValueError):
        free = None
    try:
        light = xbmcaddon.Addon("plugin.video.mdm.flix").getSetting("device_artwork") == "Light"
    except RuntimeError:
        light = True
    automatic, reason = recommend(memory, free, light)
    mode = xbmc.getInfoLabel("Skin.String(mdm_home_mode)")
    if mode not in ("Auto", "Basic", "Artwork"):
        mode = "Auto"
    if len(sys.argv) > 1 and sys.argv[1] == "choose":
        options = ["Auto — " + ("artwork" if automatic else "basic") + " (" + reason + ")", "Basic — no home widgets", "Artwork — two poster rows"]
        choice = xbmcgui.Dialog().select("MDM Home mode", options)
        if choice < 0:
            return
        mode = ("Auto", "Basic", "Artwork")[choice]
        xbmc.executebuiltin("Skin.SetString(mdm_home_mode," + mode + ")")
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
    desired = automatic if mode == "Auto" else mode == "Artwork"
    current = xbmc.getCondVisibility("Skin.HasSetting(mdm_artwork)")
    if bool(current) != desired:
        xbmc.executebuiltin("Skin.SetBool(mdm_artwork)" if desired else "Skin.Reset(mdm_artwork)")
        # Includes are selected on skin load. Read back before requesting a
        # single reload; a failed setter must not create an endless reload loop.
        monitor = xbmc.Monitor()
        for _ in range(10):
            if bool(xbmc.getCondVisibility("Skin.HasSetting(mdm_artwork)")) == desired:
                xbmc.executebuiltin("ReloadSkin()")
                break
            if monitor.waitForAbort(0.05):
                break


if __name__ == "__main__":
    run()
