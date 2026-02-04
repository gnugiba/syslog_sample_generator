import logging
import sys
import socket
import time
from logging.handlers import SysLogHandler

def get_params(name, value=None):
    try:
        idx = sys.argv.index(name)
        return sys.argv[idx + 1]
    except (ValueError, IndexError):
        return value

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def main():
    try:
        logger = logging.getLogger()
        logger.setLevel(logging.NOTSET)
        host = get_params('--host', '127.0.0.1')

        syslog_handler = SysLogHandler(address=(host,514), socktype=socket.SOCK_DGRAM)

        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        syslog_handler.setFormatter(log_format)
        
        # add handler to logger
        logger.addHandler(syslog_handler)
        local_ip = get_local_ip()
        
        while True:
            logger.info('This is info message')
            logger.warning('This is warning message')
            logger.error('This is error message')
            print(f'sent syslog msg to {host}:514, from {local_ip}')
            time.sleep(2)
    except KeyboardInterrupt :
        print('Keyboard interrupt') 
    finally:
        logger.removeHandler(syslog_handler)
        syslog_handler.close()

if __name__ == "__main__":
    main()
