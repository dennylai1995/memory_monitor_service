import configparser
import logging
import logging.handlers
import os
import subprocess
import sys
import time


def log_setup(log_path, log_size, log_count):
    # check if log folder exists
    if not os.path.isdir(os.path.dirname(log_path)):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    file_handler = logging.handlers.RotatingFileHandler(
        log_path, maxBytes=log_size, backupCount=(log_count - 1))
    file_formatter = logging.Formatter(
        '%(asctime)s[PID=%(process)d][%(levelname)s]: %(message)s')
    file_handler.setFormatter(file_formatter)

    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter(
        '[%(levelname)s]: %(message)s')
    stream_handler.setFormatter(stream_formatter)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def memory_monitor(log_path, logger, alert_mem_threshold, prob_interval):
    logger.info(
        f'== Start memory monitoring [Threshold: {alert_mem_threshold} | Interval: {prob_interval} | Log path: {log_path}] ==')
    while True:
        # when log folder disappear, exit program with error
        if not os.path.exists(os.path.dirname(log_path)):
            logger.error(f'!! Log folder not found, exit program !!')
            sys.exit(1)

        total, used, free, shared, buff, avail = map(
            int, os.popen('free | grep Mem').readlines()[-1].split()[1:])
        current_memory = round(((total - avail)/total)*100, 1)  # unit: percent

        if current_memory > alert_mem_threshold:
            logger.info(f'## current memory usage: {current_memory}% ##')
            logger.info("\n" + subprocess.check_output(
                "echo '%CPU %MEM ARGS' && ps -e -o pcpu,pmem,args --sort=-pmem | head -11 | tail -10", shell=True).decode())
            logger.info(
                "----------------------------------------------------------")
            logger.info(
                "\n" + subprocess.check_output("free", shell=True).decode())

        time.sleep(prob_interval)


def main():
    # read config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    log_folder = config['LOGGING'].get('LogFolder')
    log_name = config['LOGGING'].get('LogName')
    log_size = config['LOGGING'].getint('LogSize')
    log_count = config['LOGGING'].getint('LogCount')

    log_path = os.path.join(log_folder, log_name)

    mb = 1000000  # bytes = 1M
    logger = log_setup(log_path, log_size * mb, log_count)

    alert_mem_threshold = config['MONITOR'].getfloat('AlertMemoryThreshold')
    prob_interval = config['MONITOR'].getfloat('ProbInterval')

    memory_monitor(log_path, logger, alert_mem_threshold, prob_interval)


if __name__ == '__main__':
    main()
