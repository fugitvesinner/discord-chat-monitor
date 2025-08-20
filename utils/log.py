import datetime
import os
import logging

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'
    WHITE = '\033[37m'
    PURPLE = '\033[95m'
    
    def format(self, record):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        level_color = self.COLORS.get(record.levelname, self.WHITE)
        
        form_msg = f"{self.PURPLE}[{timestamp}]{self.RESET} - {self.WHITE}[{level_color}{record.levelname}{self.WHITE}]{self.RESET} - {record.getMessage()}"
        return form_msg

class Logger:
    def __init__(self, log_file="bot.log"):
        self.log_file = log_file
        dir = os.path.dirname(log_file)
        if dir:
            os.makedirs(dir, exist_ok=True)
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - %(message)s', datefmt='%Y-%m-%d %H:%M')
        colored_formatter = ColoredFormatter()
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(colored_formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        self.logger.info(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def warn(self, message):
        self.logger.warning(message)

logger = Logger()