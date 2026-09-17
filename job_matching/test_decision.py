from job_matching.decision import make_application_decision


def main():
    test_scores = [95, 80, 70, 69, 50]

    for score in test_scores:
        decision = make_application_decision(score)

        print(
            f"Score: {score}% "
            f"-> Decision: {decision}"
        )


if __name__ == "__main__":
    main()