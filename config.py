settings = {}


def getSettings():
    return settings


def setSettings(key, value):
    settings[key] = value
    return settings


def update(settingsToUpdateWith):
    settings.update(settingsToUpdateWith)
    return settings
