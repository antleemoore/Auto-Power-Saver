import pystray

from system.file_search import menu_item_run_search

additional_features = pystray.Menu(
    pystray.MenuItem("Run deep file search", menu_item_run_search),
)
