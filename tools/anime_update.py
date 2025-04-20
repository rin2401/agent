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

db = client.open_by_key(SHEET_KEY)
sheet = db.get_worksheet_by_id(WORKSHEET_ID)

def update_anime_sheet(ids=[]):
    """
    Update the sheet with id and current_episodes for each anime id in ids.
    If id exists, update the row. Otherwise, append a new row.
    """
    # Get all existing records and build id->row mapping
    records = sheet.get_all_records()
    print(records)
    id_to_row = {row['id']: idx+2 for idx, row in enumerate(records) if 'id' in row}  # +2 because Google Sheets is 1-indexed and header is row 1
    ids = set(ids + list(id_to_row.keys()))
    print(ids)
    for anime_id in ids:
        info = crawl_anilist(int(anime_id))
        current_episodes = info['current_episodes'] if info else None
        row_data = [anime_id, current_episodes]
        if anime_id in id_to_row:
            # Update existing row
            row_num = id_to_row[anime_id]
            sheet.update(range_name=f"A{row_num}:B{row_num}", values=[row_data])
        else:
            # Append new row
            sheet.append_row(row_data)

if __name__ == "__main__":
    ID = 1193967919
    s = db.get_worksheet_by_id(ID)
    records = s.get_all_records()
    ids = [r['anilist_id'] for r in records if r.get('anilist_id')]
    update_anime_sheet(ids)
