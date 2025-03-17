import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets Authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Google Sheet ID
SHEET_ID = "1ZBNk7zJ5bPHhfb2UgLPC27A-phWkhlvtBHiHH_JjsyU" # Replace with your actual Sheet ID
sheet = client.open_by_key(SHEET_ID).sheet1

# Load movies from Google Sheets
def load_movies():
    movies = {}
    data = sheet.get_all_records()
    for row in data:
        movies[row["Movie Name"]] = {
            "file_id": row["File ID"],
            "file_size": row["File Size"],
            "file_name": row["File Name"]
        }
    return movies

# Save movie to Google Sheets
def save_movie(movie_name, file_id, file_size, file_name):
    sheet.append_row([movie_name, file_id, file_size, file_name])

# Remove movie from Google Sheets
def remove_movie(movie_name):
    records = sheet.get_all_values()
    for i, row in enumerate(records):
        if row and row[0] == movie_name:
            sheet.delete_rows(i+1)
            return True
    return False
