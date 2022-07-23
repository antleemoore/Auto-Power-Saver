import pystray

from system.file_search import menu_item_run_search

print("Initializing additional features...")
additional_features = pystray.Menu(
    pystray.MenuItem("Deep file search", menu_item_run_search),
)
