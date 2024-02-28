from src.OCRServer.OCRServer import OCRServer
from configparser import ConfigParser
from configparser import ConfigParser

from src.OCRServer.OCRServer import OCRServer


def create_ocr_server():
    # Read configurations
    app_config = read_config()


    # Create an instance of OCRServer with configurable parameters
    ocr_server_instance = OCRServer(
        debug=app_config.getboolean('flask', 'DEBUG'),
        host=app_config.get('flask', 'HOST'),
        ssl_context=(app_config.get('flask', 'SSL_CERTIFICATE'), app_config.get('flask', 'SSL_PRIVATE_KEY'))
    )

    # Run the server
    ocr_server_instance.run()

def read_config():
    config = ConfigParser()
    config.read('config.cfg')
    return config



if __name__ == '__main__':
    create_ocr_server()
