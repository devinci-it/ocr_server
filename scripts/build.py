import configparser
import grp
import logging
import os
import pwd
import secrets
import subprocess
from pathlib import Path

logging.basicConfig(level=logging.INFO)

def create_user_and_group(username, group):
    try:
        # Create group if it doesn't exist
        grp.getgrnam(group)
    except KeyError:
        subprocess.run(['sudo', 'groupadd', group])

    try:
        # Create user if it doesn't exist
        pwd.getpwnam(username)
    except KeyError:
        subprocess.run(['sudo', 'useradd', '-m', '-g', group, username])

def create_virtual_environment(venv_path):
    subprocess.run(['python3', '-m', 'venv', venv_path])

def install_requirements(venv_path):
    subprocess.run([venv_path / 'bin' / 'pip', 'install', '-r', 'requirements.txt'])

def create_systemd_service_file(project_path, venv_path, username, group, config):
    service_file_content = f"""[Unit]
Description=OCRServer Flask App
After=network.target

[Service]
User={username}
Group={group}
ExecStart=sudo -u {username} -g {group} {venv_path / 'bin' / 'python'} {project_path / 'run.py'}
WorkingDirectory={project_path}

[Install]
WantedBy=multi-user.target
"""

    service_file_path = '/etc/systemd/system/ocr_server.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_file_content)

    return service_file_path

def reload_systemd():
    subprocess.run(['sudo', 'systemctl', 'daemon-reload'])

def enable_and_start_service():
    subprocess.run(['sudo', 'systemctl', 'enable', 'ocr_server'])
    subprocess.run(['sudo', 'systemctl', 'start', 'ocr_server'])

def move_to_project_directory(project_path, username, group):
    current_directory = Path.cwd()
    subprocess.run(['sudo', 'chown', '-R', f'{username}:{group}', current_directory])
    os.chdir(project_path)

def set_ownership(directory, username, group):
    subprocess.run(['sudo', 'chown', '-R', f'{username}:{group}', directory])

def set_ssl_certificates_ownership(cert_path, key_path, username, group):
    subprocess.run(['sudo', 'chown', f'{username}:{group}', cert_path, key_path])

def generate_self_signed_certificates(cert_path, key_path):
    subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:4096', '-nodes', '-out', cert_path, '-keyout', key_path, '-days', '365', '-subj', '/CN=localhost'])

def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['flask'], config['build']

def main():
    flask_config, build_config = read_config()

    username = build_config.get('username', 'ocr_server_user')
    group = build_config.get('group', 'ocr_server_group')
    project_path = build_config.get('project_path', Path.home() / username / 'OCRServer')
    venv_path = build_config.get('venv_path', project_path / 'venv')

    try:
        logging.info(f"Creating user and group: {username}:{group}")
        create_user_and_group(username, group)

        logging.info(f"Moving to project directory: {project_path}")
        move_to_project_directory(project_path, username, group)

        logging.info(f"Creating virtual environment at: {venv_path}")
        create_virtual_environment(venv_path)

        logging.info("Installing dependencies")
        install_requirements(venv_path)

        service_file_path = create_systemd_service_file(project_path, venv_path, username, group, flask_config)
        logging.info(f"Systemd service file created at: {service_file_path}")

        logging.info("Reloading systemd")
        reload_systemd()

        logging.info("Enabling and starting OCRServer service")
        enable_and_start_service()

        logging.info("Setting ownership for the OCRServer application directory")
        set_ownership(project_path, username, group)

        ssl_certificate = flask_config.get('SSL_CERTIFICATE')
        ssl_private_key = flask_config.get('SSL_PRIVATE_KEY')

        if ssl_certificate and ssl_private_key:
            logging.info("Setting ownership for SSL certificates")
            set_ssl_certificates_ownership(ssl_certificate, ssl_private_key, username, group)
        else:
            ssl_certificate = project_path / 'ssl_cert.pem'
            ssl_private_key = project_path / 'ssl_key.pem'
            logging.info("Generating self-signed SSL certificates")
            generate_self_signed_certificates(ssl_certificate, ssl_private_key)
            set_ssl_certificates_ownership(ssl_certificate, ssl_private_key, username, group)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    # main()

    secret_key = secrets.token_hex(16)
    print(f"Your secret key is: {secret_key}")

