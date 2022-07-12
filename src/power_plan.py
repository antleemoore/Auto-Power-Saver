import re
import subprocess
from notification import send_notification
from system import get_powershell_path


def get_plans():
    cmd_output = str(subprocess.check_output(
        f"{get_powershell_path()} powercfg /list", shell=True))
    powerplans = re.findall(r'\((.*?) *\)', cmd_output)
    powerplans.pop(0)
    guid = re.findall(r'(?<=GUID: ).*?(?=\s)', cmd_output)
    guid = [x for x in guid if x != '']
    options = {}
    for i in range(powerplans.__len__()):
        options[powerplans[i]] = guid[i]
    return options

def set_plan(name, config):
    plans = get_plans()
    try:
        subprocess.call(
            f"{get_powershell_path()} powercfg /setactive {plans[name]}", shell=True)
        send_notification(f"The power plan was switched to {name}", config=config)
    except:
        send_notification(
            f"You are missing the {name} power plan.  Create it in settings.", config=config)
        return False
    return True