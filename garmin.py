import requests
import json
from pathlib import Path

#Enter your cookie and token below
COOKIE = ""
TOKEN = ""

def make_header():
    header = {
        "authority":"connect.garmin.com",
        "scheme": "https",
        "accept":"application/json",
        "accept-encoding":"gzip, deflate, br",
        "accept-language":"sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6",
        "x-requested-with":"XMLHttpRequest",
        "nk":"NT",
        "x-app-ver":"4.61.5.0",
        "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "di-backend":"connectapi.garmin.com",
        "dnt":"1",
        "x-requested-with":"XMLHttpRequest",
        "cookie":COOKIE,
        "authorization":TOKEN,
        }
    return header


def get_activity_list(limit, start=0, end=1670394939677):
    headers = make_header()
    url = f"https://connect.garmin.com/activitylist-service/activities/search/activities?&limit={limit}&excludeChildren=false&start={start}&_={end}"
    r = requests.get(url, headers=headers)
    print(f"status_code={r.status_code}")
    return r

def download_activity(id, start_time):
    headers = make_header()
    headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    headers["path"] =f"/modern/proxy/download-service/export/tcx/activity/{id}"
    headers["referer"] = f"https://connect.garmin.com/modern/activity/{id}"
    headers["sec-fetch-dest"] = "document"
    headers["sec-fetch-mode"] = "navigate"

    headers.pop("nk")
    headers.pop("di-backend")
    headers.pop("x-requested-with")

    url =f"https://connect.garmin.com/modern/proxy/download-service/export/tcx/activity/{id}" 
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        start_time = start_time.replace(" ", "T").replace(":", "")
        with open(f"activites/{start_time}_{id}.tcx", "wb") as f:
            f.write(r.content)
        return r.status_code


if __name__ == '__main__':
    limit = 1000
    r = get_activity_list(limit)
    activites = json.loads(r.content)
    print(f"found n={len(activites)} activites")

    p = Path("./activites")
    if not p.exists():
        p.mkdir()

    for i, a in enumerate(activites):
        id = a["activityId"]
        start_time = a["startTimeLocal"]
        status_code = download_activity(id, start_time)
        if status_code == 200:
            print(f"downloading ... {i} of {len(activites)}")
        else:
            print(f"ERR status_code = {status_code}")