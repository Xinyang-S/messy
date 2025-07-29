import os
import sys
import logging
import colorlog
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from concurrent_log_handler import ConcurrentRotatingFileHandler
import json
from datetime import datetime

# 全局日志目录
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# ANSI 彩色控制台
console_formatter = colorlog.ColoredFormatter(
    "%(log_color)s[%(asctime)s] [%(levelname)8s] [%(threadName)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red,bg_white',
    },
    reset=True,
    style='%'
)

# JSON 文件格式（适合 ELK）
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "lineno": record.lineno,
            "thread": record.threadName,
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry, ensure_ascii=False)

# 单例日志器
def get_logger(name: str = "app",
               log_level: str = "DEBUG",
               console: bool = True,
               file: bool = True,
               json_file: bool = True,
               max_bytes: int = 10 * 1024 * 1024,  # 10MB
               backup_count: int = 5) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:  # 已存在则直接返回
        return logger

    logger.setLevel(getattr(logging, log_level.upper(), logging.DEBUG))

    # 1. 控制台
    if console:
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(console_formatter)
        logger.addHandler(ch)

    # 2. 普通文本文件（多进程安全 + 按大小轮转）
    if file:
        file_path = os.path.join(LOG_DIR, f"{name}.log")
        fh = ConcurrentRotatingFileHandler(
            file_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        fh.setFormatter(logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(threadName)s] %(name)s | %(message)s"
        ))
        logger.addHandler(fh)

    # 3. JSON 文件（按天轮转）
    if json_file:
        json_path = os.path.join(LOG_DIR, f"{name}.json")
        jh = TimedRotatingFileHandler(
            json_path, when="midnight", interval=1, backupCount=backup_count, encoding="utf-8"
        )
        jh.setFormatter(JSONFormatter())
        logger.addHandler(jh)

    return logger