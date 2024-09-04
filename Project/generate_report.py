# handles turning the QA Data into a report
import xlsxwriter
from datetime import date

import xlsxwriter.worksheet
import QA_Data


def generate_excel_report(course: QA_Data.Course, timeTaken: str = ""):
    print("Starting report generation")
    workbook = xlsxwriter.Workbook(
        "./Reports/{}_CanvasValidationReport.xlsx".format(course.title)
    )
    worksheet = workbook.add_worksheet()
    worksheet.name = "Stats"

    # Set column width
    worksheet.set_column("A:A", 10)
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

    print("Report created: {}.xlsx".format(course.title))
    workbook.close()


def create_stat(
    worksheet: xlsxwriter.worksheet, col, row, stat_title: str, stat_value: str
):
    incrementedCol = chr(ord(col) + 1)

    worksheet.write(f"{col}{row}", stat_title)
    worksheet.write(f"{incrementedCol}{row}", stat_value)
