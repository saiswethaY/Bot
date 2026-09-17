from scheduler.scheduler_runner import run_bot_cycle


def main():
    print("=" * 60)
    print("SCHEDULER CYCLE TEST")
    print("=" * 60)

    run_bot_cycle()

    print("\nScheduler cycle test completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()