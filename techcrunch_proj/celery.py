import logging
import os
from celery import Celery
from celery.signals import after_setup_logger
from django.conf import settings


def configure_celery_log(sender=None, **kwargs):
    """
    Configures logging for Celery.

    Removes existing handlers from the Celery logger,
    sets the log level to INFO, defines a log format,
    creates a console handler with the same log level and format,
    creates a file handler to save logs to a file,
    and adds both handlers to the Celery logger.

    Args:
        sender: The sender of the signal.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    # Get the Celery logger
    celery_logger = logging.getLogger('celery')

    # Remove existing handlers to prevent duplicates
    celery_logger.handlers = []

    # Set the desired log level (e.g., INFO, DEBUG, etc.)
    celery_logger.setLevel(logging.INFO)

    # Define the log format
    log_format = logging.Formatter('[%(asctime)s] : %(message)s')

    # Create a console handler and set its log level and format
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)

    # Create a file handler to save logs to a file
    log_file_path = os.path.join(settings.BASE_DIR, 'logs', 'celery.log')
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_format)

    # Add both handlers to the Celery logger
    celery_logger.addHandler(console_handler)
    celery_logger.addHandler(file_handler)


# Connect the configure_celery_log function to the after_setup_logger signal
after_setup_logger.connect(configure_celery_log)

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techcrunch_proj.settings')

# Create a Celery application named 'techcrunch_proj' with the broker URL from Django settings
app = Celery('techcrunch_proj', broker=settings.CELERY_BROKER_URL)

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Define the beat schedule for a daily task
app.conf.beat_schedule = {
    'every-day-start-daily-scrape': {
        'task': 'techcrunch_app.tasks.daily_search_task',
        'schedule': 6480,  # One day (in seconds)
    },
}

# Connect the configure_celery_log function again to ensure it's applied after setup
after_setup_logger.connect(configure_celery_log)

# Autodiscover tasks from all registered Django apps
app.autodiscover_tasks()

# Disable propagation of logs from the Celery logger to prevent duplicate logging
logging.getLogger('celery').propagate = True

app.conf.worker_logfile = 'path/to/logfile.log'
app.conf.broker_connection_retry_on_startup = True

# Instructions for running Celery worker and beat processes
# celery -A techcrunch_proj worker -l INFO -P eventlet
# celery -A techcrunch_proj beat --loglevel=INFO
