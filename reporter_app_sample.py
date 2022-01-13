#!/usr/bin/python3
import sys, argparse
from health_reporter import Error, ErrorType, ErrorSource, HealthReporter
import time

# мини приложуха для отправки кипэлайвов от подсистемы, 
# и репорта об ошибках с помощью healthReporter
def main(argv):
    msg_type = ErrorType.error
    msg_source = ErrorSource.GPSservice

    error_code = "GPS00010"

    redis_host = "127.0.0.1"
    redis_port = 6379

    error_state = True



    parser = argparse.ArgumentParser()
    parser.add_argument("--type", help="status reported: error, warning, ok")
    parser.add_argument("--source", help="source name (DBW, Planner, GPS... (device_errors:source)")
    parser.add_argument("--code", help="if status not ok: Error code to be reported - string")
    parser.add_argument("--host", help="Redis host (192.168.4.203 default)")
    parser.add_argument("--port", help="Redis port (6379 default)")


    args = parser.parse_args()
    if args.type:
        if args.type == "ok":
            error_state = False
        elif args.type == "error":
            error_state = True
            msg_type = ErrorType.error
        elif args.type == "warning":
            error_state = True
            msg_type == ErrorType.warning
    if args.source:
        for s in ErrorSource:
            if s.name == args.source:
                msg_source = s
    if args.code:
        error_code = args.code


    errorSender = HealthReporter(msg_source, redis_host, redis_port)
    cycle_time = errorSender.getKeepaliveCycleTimeSec()
    e = Error(msg_source, msg_type, error_code)

    while True:
        # т.к. служба может стартануть раньше редиса,
        # ожидаем его готовности
        if errorSender.isConnected():
            break
        time.sleep(1)
    
    if not errorSender.initConfig():
        print("Failed to init healthReporter config from Redis")
        return False

    while True:
        # если условие не выполняется - 
        # система в целом еще не сконфигурирована
        # например, не все устройства подключены,
        # или не указаны необходимые устройства
        # поэтому не нужно рапортовать об ошибках
        if errorSender.isRedisConfigReady():
            print("ready")
            break
        time.sleep(1)

    while True:
        # cycle to check health
        # active errors should be reported
        # not less frequently than cycleTime

        # также отправку ошибок и keepaliveов
        # можно вести из разных потоков, т.к.
        # redis-py потокобезопасный
        time.sleep(3)
        if error_state:
            errorSender.pushError(e)
        if errorSender.getSecondsToNextKeepalive() < 0:
            errorSender.keepalive()      
        print("spin")


if __name__ == "__main__":
   main(sys.argv[1:])
