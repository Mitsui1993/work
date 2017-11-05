import os,sys

os.environ['USER_SETTINGS'] = "config.settings"

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
