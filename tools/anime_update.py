import gspread
from oauth2client.service_account import ServiceAccountCredentials
from anime_crawler import crawl_anilist
import sys

# Google Sheets setup
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name("../creds.json", scope)
client = gspread.authorize(creds)

# Change these to your sheet key and worksheet id
SHEET_KEY = "12q04f4hwtVQjfVSUayDsgXLGGbqrl9urm8gp556nPQA"
WORKSHEET_ID = 33541967

sheet = client.open_by_key(SHEET_KEY).get_worksheet_by_id(WORKSHEET_ID)

def update_anime_sheet():
    """
    Update the sheet with id and current_episodes for each anime id in ids.
    If id exists, update the row. Otherwise, append a new row.
    """
    # Get all existing records and build id->row mapping
    records = sheet.get_all_records()
    id_to_row = {str(row['id']): idx+2 for idx, row in enumerate(records) if 'id' in row}  # +2 because Google Sheets is 1-indexed and header is row 1
    for anime_id in id_to_row:
        info = crawl_anilist(int(anime_id))
        current_episodes = info['current_episodes'] if info else None
        row_data = [anime_id, current_episodes]
        anime_id_str = str(anime_id)
        if anime_id_str in id_to_row:
            # Update existing row
            row_num = id_to_row[anime_id_str]
            sheet.update(f"A{row_num}:B{row_num}", [row_data])
        else:
            # Append new row
            sheet.append_row(row_data)

if __name__ == "__main__":
    update_anime_sheet()
