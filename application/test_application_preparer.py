from application.application_preparer import prepare_application


def main():
    application_id = 1

    prepare_application(application_id)

    print("=" * 50)
    print("APPLICATION PREPARATION TEST")
    print("=" * 50)
    print(f"Application ID : {application_id}")
    print("Resume version : resume_v1")
    print("=" * 50)


if __name__ == "__main__":
    main()