from system import resource_path
from notifypy import Notify

def send_notification(msg, config):
    if config.disable_notifications == True:
        return
    notification = Notify()
    notification.title = f"Auto Power Saver"
    notification.message = msg
    notification.icon = resource_path("green_power.jpeg")
    notification.send()