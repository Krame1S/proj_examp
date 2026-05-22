import logging
import logging.handlers
import queue

from colorama import Fore, Style


LEVEL_COLORS = {
    logging.DEBUG: Fore.CYAN,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.RED + Style.BRIGHT,
}


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        color = LEVEL_COLORS.get(record.levelno, "")
        reset = Style.RESET_ALL
        level = f"{color}{record.levelname:<8}{reset}"
        return f"{level} [{record.name} - {self.formatTime(record)}] {record.getMessage()}"


def setup_logging(level: str = "INFO") -> None:

    """Configure async queue-based logging with colored console output."""
    log_queue: queue.Queue = queue.Queue()
    queue_handler = logging.handlers.QueueHandler(log_queue)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter())

    listener = logging.handlers.QueueListener(log_queue, console_handler)
    listener.start()

    root = logging.getLogger()
    root.setLevel(getattr(logging, level, logging.INFO))
    root.addHandler(queue_handler)

    # Suppress noisy third-party loggers
    for name in ("asyncpg",):
        logging.getLogger(name).setLevel(logging.WARNING)