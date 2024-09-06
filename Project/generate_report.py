# handles turning the QA Data into a report
import xlsxwriter
from datetime import date, datetime

import xlsxwriter.worksheet
import QA_Data


def generate_excel_report(course: QA_Data.Course, timeTaken: str = ""):
    print("Starting report generation")
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")
    workbook = xlsxwriter.Workbook(
        f"./Reports/QA_{course.id}_{course.title}_{date_string}.xlsx"
    )

    generate_course_stats_page(workbook, course, timeTaken)
    generate_issues_page(workbook, course)
    generate_page_details_page(workbook, course)

    print(f"Report: Created {course.title}")
    workbook.close()


def generate_course_stats_page(workbook, course: QA_Data.Course, timeTaken: str = ""):
    print("Report: Generating course stats")
    worksheet = workbook.add_worksheet()
    worksheet.name = "Stats"

    # Set column width
    worksheet.set_column("A:A", 30)
    worksheet.set_column("B:B", 50)

    worksheet.write("B1", "Wisdom canvas error report")

    worksheet.write("A2", "Course")
    worksheet.write("B2", course.title)
    create_stat(worksheet, "A", "2", "Course", course.title)
    create_stat(worksheet, "A", "3", "ID", course.id)
    create_stat(worksheet, "A", "4", "URL", course.url)
    create_stat(worksheet, "A", "5", "Participants", course.participant_count)
    create_stat(worksheet, "A", "6", "Page count", course.page_count)
    create_stat(worksheet, "A", "7", "Module count", course.module_count)
    create_stat(worksheet, "A", "8", "Assessment count", course.assessment_count)
    create_stat(worksheet, "A", "9", "Time taken to generate", timeTaken)


def generate_issues_page(workbook, course: QA_Data.Course):
    print("Report: Generating issues")
    worksheet = workbook.add_worksheet()
    worksheet.name = "Issues"

    worksheet.set_column("A:A", 40)
    worksheet.set_column("B:B", 25)
    worksheet.set_column("C:C", 50)
    worksheet.set_column("D:D", 60)
    worksheet.set_column("E:E", 60)

    worksheet.write("A1", "Title")
    worksheet.write("B1", "Severity")
    worksheet.write("C1", "Type")
    worksheet.write("D1", "Description")
    worksheet.write("E1", "Element")
    worksheet.write("F1", "Page of containing issue")

    # issue_type, issue_description, issue_element, issue_link
    for index, issue in enumerate(course.issues):
        row_offset = index + 2
        worksheet.write(f"A{row_offset}", issue.issue_page_title)
        worksheet.write(f"B{row_offset}", issue.severity)
        worksheet.write(f"C{row_offset}", issue.issue_type)
        worksheet.write(f"D{row_offset}", issue.issue_description)
        worksheet.write(f"E{row_offset}", issue.issue_element)
        worksheet.write(f"F{row_offset}", issue.issue_link)


def generate_page_details_page(workbook, course: QA_Data.Course):
    print("Report: Generating page stats")
    worksheet = workbook.add_worksheet()
    worksheet.name = "Page Stats"

    worksheet.set_column("A:A", 40)
    worksheet.set_column("B:B", 20)
    worksheet.set_column("C:C", 20)
    worksheet.set_column("D:D", 10)
    worksheet.set_column("E:E", 10)
    worksheet.set_column("F:F", 10)
    worksheet.set_column("G:G", 10)
    worksheet.set_column("H:H", 10)

    worksheet.write("A1", "Title")
    worksheet.write("B1", "Module")
    worksheet.write("C1", "URL")
    worksheet.write("D1", "Published")
    worksheet.write("E1", "Issue Count")
    worksheet.write("F1", "Word Count")
    worksheet.write("G1", "Image Count")
    worksheet.write("H1", "Link Count")

    # issue_type, issue_description, issue_element, issue_link
    for index, page in enumerate(course.pages):
        row_offset = index + 2
        # print(row_offset)
        worksheet.write(f"A{row_offset}", page.title)
        worksheet.write(f"B{row_offset}", "page.module")
        worksheet.write(f"C{row_offset}", page.url)
        worksheet.write(f"D{row_offset}", page.published)
        worksheet.write(f"E{row_offset}", page.issue_count)
        worksheet.write(f"F{row_offset}", page.word_count)
        worksheet.write(f"G{row_offset}", page.image_count)
        worksheet.write(f"H{row_offset}", page.link_count)


def create_stat(
    worksheet: xlsxwriter.worksheet, col, row, stat_title: str, stat_value: str
):
    incrementedCol = chr(ord(col) + 1)

    worksheet.write(f"{col}{row}", stat_title)
    worksheet.write(f"{incrementedCol}{row}", stat_value)
