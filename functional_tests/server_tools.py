from os import path
import subprocess
THIS_FOLDER = path.abspath(path.dirname(__file__))

def create_session_on_server(host, email):
    return subprocess.check_output(
        [
            'fab',
            'create_session_on_server:email={}'.format(email), #12
            '--host=ubuntu@{}'.format(host),
            '--hide=everything,status', #3
            '-i/home/stlk/.ssh/aws-linux.pem',
        ],
        cwd=THIS_FOLDER
    ).decode().strip() #4


def reset_database(host):
    subprocess.check_call(
        [
            'fab',
            'reset_database',
            '--host=ubuntu@{}'.format(host),
            '-i/home/stlk/.ssh/aws-linux.pem',
        ],
        cwd=THIS_FOLDER
    )