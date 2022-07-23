from system.system import resource_path
from notifypy import Notify


def send_notification(msg, config):
    if config.disable_notifications == True:
        print("Notifications are disabled")
        return
    notification = Notify()
    notification.title = f"Auto Power Saver"
    notification.message = msg
    notification.icon = resource_path("resources/images/green_power.jpeg")
    print("Sending system notification to user")
    notification.send()


def handle_notification_settings(config):
    config.disable_notifications = True if config.disable_notifications == False else False
    print("Changing disable notifications setting to", config.disable_notifications)
    config.write_to_config()
    if config.disable_notifications == False:
        send_notification("Notifications have been enabled.", config=config)
