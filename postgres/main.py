import json
import logging
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

import schedule
import time
import os

load_dotenv()  # take environment variables from .env.
logging.basicConfig(level=logging.INFO)

logging.getLogger("schedule").setLevel(logging.DEBUG)

#def job():
#    print("I'm working...")

# schedule.every(10).seconds.do(job)
# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().day.at("12:42", "Europe/Amsterdam").do(job)
# schedule.every().minute.at(":17").do(job)

def job_with_argument(name):
    print(f"I am {name}")

def backup_db():
    rclone_config_path = os.environ.get('RCLONE_CONFIG_PATH', './rclone.conf')
    subprocess.run(['rclone', '--config', rclone_config_path, 'mkdir', 'sftp:pgbackup'], check=True)
    with tempfile.TemporaryDirectory() as tmpdirname:
        databases = json.loads(subprocess.check_output(['psql', '-c', "SELECT json_agg(datname) FROM pg_database WHERE datname NOT IN ('template0', 'template1', 'postgres')",
                                            '--tuples-only', '--no-align']))
        now = datetime.now(timezone.utc)
        ts=now.strftime('%H_%M_%S')
        remote_folder='{}/{}'.format(os.environ['PGBACKUPDIR'],now.strftime('%Y/%m/%d'))
        for database in databases:
            print("backing up",database)
            output = f'{tmpdirname}/{database}.sql'
            #print(output)
            subprocess.run(['pg_dump', database, '--column-inserts', '-f', output], check=True)
            #Path(output).touch()

            # rclone moveto /tmp/backup "sftp:/mongobackup/$BACKUP_DIR/$(date +%Y-%m-%d_%H-%M-%S).dump"
            subprocess.run(['rclone', '-v', '--config', rclone_config_path, 'moveto', output, f'sftp:{remote_folder}/{ts}/{database}.sql'], check=True)

if __name__ == '__main__':
    #backup_db()
    #exit(0)
    #schedule.every(10).seconds.do(job_with_argument, name="Peter")
    #schedule.every(10).seconds.do(backup_db)

    backup_db()
    schedule.every().day.at("11:30", "Etc/UTC").do(backup_db)

    while True:
        schedule.run_pending()
        time.sleep(1)