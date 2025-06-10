import openpyxl
from datetime import datetime

def log_metrics_to_excel(session_id, eou_delay, ttft, ttfb, total_latency):

    print("Logging metrics to Excel file...")
    print(f"Session ID: {session_id}")
    print(f"EOU Delay: {eou_delay}")
    print(f"TTFT (Time to First Token): {ttft}")
    print(f"TTFB (Time to First Byte): {ttfb}")
    print(f"Total Latency: {total_latency}")

    file_name = "session_metrics.xlsx"

    try:
        # opening the Excel file
        workbook = openpyxl.load_workbook(file_name)
        sheet = workbook.active
        print("Existing Excel file found and loaded.")
    except FileNotFoundError:
        # If file doesn't exist, create a new workbook
        print("Excel file not found. Creating a new one.")
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Add headers
        headers = ["Session ID", "Timestamp", "EOU Delay", "TTFT", "TTFB", "Total Latency"]
        sheet.append(headers)

    # Get current timestamp for logging
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append the metrics as a new row
    sheet.append([session_id, timestamp, eou_delay, ttft, ttfb, total_latency])

    # Save the workbook
    workbook.save(file_name)
    print("Metrics saved successfully in the Excel file.")
