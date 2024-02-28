import os
import shutil
import subprocess


def remove_user_and_group(username, group):
    try:
        subprocess.run(['sudo', 'userdel', '-r', username])
    except subprocess.CalledProcessError:
        pass  # User doesn't exist

    try:
        subprocess.run(['sudo', 'groupdel', group])
    except subprocess.CalledProcessError:
        pass  # Group doesn't exist

def remove_virtual_environment(venv_path):
    shutil.rmtree(venv_path, ignore_errors=True)

def remove_systemd_service_file(service_file_path):
    if os.path.exists(service_file_path):
        os.remove(service_file_path)

def disable_and_stop_service():
    subprocess.run(['sudo', 'systemctl', 'disable', 'ocr_server'])
    subprocess.run(['sudo', 'systemctl', 'stop', 'ocr_server'])

def main():
    # Read configuration values
    config = configparser.ConfigParser()
    config.read('config.ini')
    project_path = config.get('project_path', os.path.expanduser('~/OCRServer'))
    venv_path = config.get('venv_path', os.path.join(project_path, 'venv'))
    username = config.get('username', 'ocr_server_user')
    group = config.get('group', 'ocr_server_group')

    # Disable and stop the service
    disable_and_stop_service()

    # Remove virtual environment, systemd service file, user, and group
    remove_virtual_environment(venv_path)
    remove_systemd_service_file('/etc/systemd/system/ocr_server.service')
    remove_user_and_group(username, group)

    print("Cleanup/Uninstall completed.")

if __name__ == "__main__":
    main()
