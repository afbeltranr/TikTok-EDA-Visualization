import os
import gspread
from google.oauth2.service_account import Credentials

def test_google_api_connection():
    """Test connection to Google Sheets API and verify data retrieval."""
    try:
        # Load credentials from the environment variable
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise ValueError("Google credentials path not set in environment variable.")
        
        # Authenticate with the Google API
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(credentials_path, scopes=scope)
        client = gspread.authorize(credentials)

        # Access the Google Sheet
        sheet_url = os.getenv("GOOGLE_SHEET_URL")
        if not sheet_url:
            raise ValueError("Google Sheet URL not set in environment variable.")
        
        sheet = client.open_by_url(sheet_url).sheet1
        data = sheet.get_all_records()

        # Verify data retrieval
        assert len(data) > 0, "The dataset is empty or could not be retrieved."
        print("✅ Google Sheets API test passed.")
    
    except Exception as e:
        print(f"❌ Google Sheets API test failed: {e}")
        raise

if __name__ == "__main__":
    test_google_api_connection()
