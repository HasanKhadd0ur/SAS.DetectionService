import logging
import sys
import seqlog


class LoggingService:
    def __init__(self, name="ScraperApp", level=logging.DEBUG):
        # Configure seqlog once (usually at app startup)
        seqlog.log_to_seq(
            server_url="http://localhost:5341",  # Seq container URL
            api_key=None,                       
            level=level,
            batch_size=10,
            auto_flush_timeout=10,
            override_root_logger=False
        )

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Add console handler if not already present
        if not any(isinstance(h, logging.StreamHandler) for h in self.logger.handlers):
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
            )
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

    def get_logger(self):
        return self.logger
