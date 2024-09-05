from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Создание объекта учетных данных
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Создание сервиса для доступа к Google Sheets
service = build('sheets', 'v4', credentials=credentials)

# Пример использования API
spreadsheet_id = '1oqCur7CjDEfb0TM1UnL26kkkhhCaDlLSmPj9jwQTOv4'
range_name = 'Sheet1!A2'

values = [
    ['Example data']
]
body = {
    'values': values
}

# Обновление данных в Google Sheet
result = service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range=range_name,
    valueInputOption='RAW',
    body=body
).execute()

print(f"{result.get('updatedCells')} cells updated.")
