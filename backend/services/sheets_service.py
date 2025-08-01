    # backend/services/sheets_service.py
import gspread
from api.auth import get_gmail_credentials # We reuse the same credentials

def write_to_sheet(sheet_id: str, headers: list, data: dict):
        """
        Appends a row of data to the specified Google Sheet.
        - sheet_id: The ID of the Google Sheet.
        - headers: A list of the column headers (the questions).
        - data: A dictionary of the gathered data where keys are the questions.
        """
        creds = get_gmail_credentials()
        
        if not creds:
                print("Error: Could not get credentials for Google Sheets.")
                return {"error": "Authentication failed."}

        try:
                gc = gspread.service_account_from_dict(creds.to_json()) # This is an undocumented gspread trick to use user credentials
        except TypeError:
                # Fallback for gspread v5+ which uses a different method
                gc = gspread.auth.authorize(creds)
                
        try:
                spreadsheet = gc.open_by_key(sheet_id)
                worksheet = spreadsheet.sheet1

                # Check if headers exist, if not, write them
                existing_headers = worksheet.row_values(1)
                if not existing_headers:
                    worksheet.append_row(headers, value_input_option='RAW')

                # Prepare the row data in the correct order
                row_to_append = [data.get(header, "") for header in headers]
                
                worksheet.append_row(row_to_append, value_input_option='RAW')
                print(f"Successfully wrote data to sheet: {sheet_id}")
                return {"status": "success"}

        except gspread.exceptions.SpreadsheetNotFound:
                print(f"Error: Spreadsheet not found. Check the ID and share settings: {sheet_id}")
                return {"error": "Spreadsheet not found or permission denied."}
        except Exception as e:
                print(f"An unexpected error occurred with Google Sheets: {e}")
                return {"error": str(e)}
