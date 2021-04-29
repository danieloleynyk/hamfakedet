import logging
from telegram.ext import CallbackContext

logger = logging.getLogger()


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        logger.info("removed previous job")
        job.schedule_removal()
    return True
