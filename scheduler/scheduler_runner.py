import time

from apscheduler.schedulers.background import BackgroundScheduler

from job_discovery.discovery_runner import run_discovery
from job_matching.matching_runner import run_matching
from notifications.notifier import send_notification


def run_bot_cycle():
    print("=" * 60)
    print("AUTOMATION CYCLE STARTED")
    print("=" * 60)

    try:
        print("\n[1] Running job discovery...")
        run_discovery()

        print("\n[2] Running job matching...")
        run_matching()

        send_notification(
            "Job Auto Applicator",
            "Automation cycle completed successfully.",
        )

    except Exception as error:

        send_notification(
            "Job Auto Applicator - ERROR",
            f"Automation cycle failed: {error}",
        )

        raise

    print("\nAutomation cycle completed.")
    print("=" * 60)


def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        run_bot_cycle,
        trigger="interval",
        minutes=30,
        id="job_auto_applicator_cycle",
        replace_existing=True,
    )

    scheduler.start()

    print("=" * 60)
    print("JOB AUTO APPLICATOR SCHEDULER")
    print("=" * 60)
    print("Scheduler started successfully.")
    print("Bot cycle interval : 30 minutes")
    print("Press Ctrl+C to stop.")
    print("=" * 60)

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping scheduler...")

        scheduler.shutdown()

        print("Scheduler stopped.")


if __name__ == "__main__":
    start_scheduler()