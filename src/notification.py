from system import resource_path
from notifypy import Notify


def send_notification(msg, config):
    if config.disable_notifications == True:
        return
    notification = Notify()
    notification.title = f"Auto Power Saver"
    notification.message = msg
    notification.icon = resource_path("resources/green_power.jpeg")
    notification.send()


def handle_notification_settings(config):
    config.disable_notifications = (
        True if config.disable_notifications == False else False
    )
    config.config.set(
        "main",
        "disable_notifications",
        f'{"True" if config.disable_notifications == True else "False"}',
    )
    if config.disable_notifications == False:
        send_notification("Notifications have been enabled.", config=config)
