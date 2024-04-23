import os
import sys


BASEDIR = os.getcwd()

data_dir = os.path.join(BASEDIR, "data")
logger_dir = os.path.join(BASEDIR, "logger")
src_dir = os.path.join(BASEDIR, "src")

sys.path.extend([data_dir, logger_dir, src_dir])


from src.main import syncronize, send_team_email, RETOOL_WF_WEBHOOK


if __name__ == "__main__":
    # syncronize()
    send_team_email(url=RETOOL_WF_WEBHOOK)
