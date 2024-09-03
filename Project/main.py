import connect
import QA_Data
from Playwright_Checks import simple_checks as checks
from dotenv import load_dotenv


def main(startID: int, endID: int):
    print("Starting QA Checks")
    load_dotenv()

    for id in range(startID, endID):
        course = QA_Data.Course(id, "Some course")
        connect.start_session(id)


if __name__ == "__main__":
    startID = int(input("What is the course index to start from? "))
    endID = int(input("What is the last ID to check? "))
    main(startID, endID)
