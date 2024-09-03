import Main


def main():
    print("Starting QA Checks")

    course = Main.Course(1, "Some course")
    print("Inspecting", course.title)


if __name__ == "__main__":
    main()
