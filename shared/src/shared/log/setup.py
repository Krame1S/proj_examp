import logging
import logging.handlers
import queue

from colorama import Fore, Style
from opentelemetry import trace

LEVEL_COLORS = {
    logging.DEBUG: Fore.CYAN,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.RED + Style.BRIGHT,
}


class TraceContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        ctx = trace.get_current_span().get_span_context()
        record.trace_id = format(ctx.trace_id, "032x") if ctx.is_valid else ""
        return True


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        msg = record.getMessage()

        # Если это /metrics - делаем серым
        if "GET /metrics" in msg or "GET /metrics/" in msg:
            color = Fore.LIGHTBLACK_EX  # или Fore.WHITE с Style.DIM
        else:
            color = LEVEL_COLORS.get(record.levelno, "")

        reset = Style.RESET_ALL
        level = f"{color}{record.levelname:<8}{reset}"
        trace_val = getattr(record, "trace_id", "")
        trace_id = f" trace={trace_val}" if trace_val else ""
        return f"{level} [{record.name} - {self.formatTime(record)}]{trace_id} {record.getMessage()}"


def setup_logging(level: str = "INFO") -> None:
    log_queue: queue.Queue = queue.Queue()
    queue_handler = logging.handlers.QueueHandler(log_queue)
    queue_handler.addFilter(TraceContextFilter())

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter())

    listener = logging.handlers.QueueListener(log_queue, console_handler)
    listener.start()

    root = logging.getLogger()
    root.setLevel(getattr(logging, level, logging.INFO))
    root.addHandler(queue_handler)

    for name in ("asyncpg", "uvicorn.access"):
        logging.getLogger(name).setLevel(logging.WARNING)
