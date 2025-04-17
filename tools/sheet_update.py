import gspread
import requests
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name("../creds.json", scope)
client = gspread.authorize(creds)

sheet = client.open_by_key(
    "1vgeMqs4N4qxL6qN2sAgRcpJcLzB4Au7Fy-tzrpzJmhE"
).get_worksheet_by_id(969007831)


def crawl(pid):
    url = "https://viettelstore.vn/Site/_Sys/ajax.asmx/ProductRule_GetPriceByRule"
    pid = pid
    payload = {"id": "e09f5a3d-f208-438b-84b7-14ef773b7966", "pid": pid}
    r = requests.request("POST", url, json=payload).json()
    r = r["d"]["data"]
    r["id"] = pid
    r["url"] = f"https://viettelstore.vn/dien-thoai/--pid{pid}.html"

    data = sheet.get_all_records()

    M = {d.get("id"): d for d in data}
    if pid not in M:
        M[pid] = r
    else:
        M[pid].update(r)

    df = pd.DataFrame(M.values())
    df = df.fillna("")

    sheet.update([df.columns.values.tolist()] + df.values.tolist())


ids = [317054, 317053, 293822, 293821]
for id in ids:
    crawl(id)
