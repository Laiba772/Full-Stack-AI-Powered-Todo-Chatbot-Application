import logging
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    """
    A custom log formatter that outputs records as JSON.
    """
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "pathname": record.pathname,
            "lineno": record.lineno,
            "funcName": record.funcName,
        }
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        if record.stack_info:
            log_record["stack_info"] = self.formatStack(record.stack_info)
        
        # Add any extra attributes from the log record, but only if they're JSON serializable
        for key, value in record.__dict__.items():
            if key not in log_record and not key.startswith('_'):
                try:
                    json.dumps(value)  # Test if value is JSON serializable
                    log_record[key] = value
                except (TypeError, ValueError):
                    # If not JSON serializable, convert to string representation
                    log_record[key] = str(value)

        return json.dumps(log_record)

def configure_structured_logging():
    """
    Configures structured logging for the application.
    """
    # Remove all existing handlers from the root logger
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        handler.close()

    handler = logging.StreamHandler()
    formatter = JsonFormatter()
    handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.INFO, # Default level
        handlers=[handler]
    )

    # Example usage:
    # logger = logging.getLogger(__name__)
    # logger.info("This is a structured log message", extra={"user_id": "123", "request_id": "abc"})