import os
try:
    import settings
except ImportError:
    print "You must create settings file "
    exit(1)

REPO_PATH = settings.REPO_PATH
assert os.path.exists(REPO_PATH), '%s does not exists' % REPO_PATH

BASE_PATH = getattr(settings, "BASE_PATH", os.path.join(REPO_PATH, 'data', 'base'))
MP_PATH = getattr(settings, "MP_PATH", os.path.join(REPO_PATH, 'data', 'mp'))
MODS_PATH = getattr(settings, "MODS_PATH", [])

ALL_PATHS = [BASE_PATH, MP_PATH] + MODS_PATH