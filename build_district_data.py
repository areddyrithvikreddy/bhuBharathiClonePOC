"""
build_district_data.py
======================
Fetches all mandal → village codes for a given district
and saves them to district_data.json.

Usage:
    pip install requests
    python build_district_data.py
"""

import json
import time
import requests

# ── CONFIG ────────────────────────────────────────────────────────────────────

# Pick any district code+name from the list below
DISTRICT = {"code": "19_1", "name": "ADILABAD"}

# All districts from the site (for reference — change DISTRICT above)
ALL_DISTRICTS = [
    {"code": "19_1",  "name": "ADILABAD"},
    {"code": "22_2",  "name": "BHADRADRI KOTHAGUDEM"},
    {"code": "21_1",  "name": "HANUMAKONDA"},
    {"code": "16_1",  "name": "HYDERABAD"},
    {"code": "20_2",  "name": "JAGTIAL"},
    {"code": "21_3",  "name": "JANGAON"},
    {"code": "21_4",  "name": "JAYASHANKAR BHOOPALPALLY"},
    {"code": "14_2",  "name": "JOGULAMBA GADWAL"},
    {"code": "18_2",  "name": "KAMAREDDY"},
    {"code": "20_1",  "name": "KARIMNAGAR"},
    {"code": "22_1",  "name": "KHAMMAM"},
    {"code": "19_4",  "name": "KOMARAM BHEEM ASIFABAD"},
    {"code": "21_5",  "name": "MAHABUBABAD"},
    {"code": "14_1",  "name": "MAHABUBNAGAR"},
    {"code": "19_3",  "name": "MANCHERIAL"},
    {"code": "17_1",  "name": "MEDAK"},
    {"code": "15_2",  "name": "MEDCHAL-MALKAJGIRI"},
    {"code": "21_6",  "name": "MULUGU"},
    {"code": "14_3",  "name": "NAGARKURNOOL"},
    {"code": "23_1",  "name": "NALGONDA"},
    {"code": "14_5",  "name": "NARAYANPET"},
    {"code": "19_2",  "name": "NIRMAL"},
    {"code": "18_1",  "name": "NIZAMABAD"},
    {"code": "20_4",  "name": "PEDDAPALLI"},
    {"code": "20_3",  "name": "RAJANNA SIRCILLA"},
    {"code": "15_1",  "name": "RANGAREDDY"},
    {"code": "17_2",  "name": "SANGAREDDY"},
    {"code": "17_3",  "name": "SIDDIPET"},
    {"code": "23_2",  "name": "SURYAPET"},
    {"code": "15_3",  "name": "VIKARABAD"},
    {"code": "14_4",  "name": "WANAPARTHY"},
    {"code": "21_2",  "name": "WARANGAL"},
    {"code": "23_3",  "name": "YADADRI BHUVANAGIRI"},
]

OUTPUT_FILE = "district_data.json"
BASE_URL    = "https://registration.telangana.gov.in"
DELAY       = 1.0   # seconds between village fetch requests

# ── SESSION ───────────────────────────────────────────────────────────────────

def make_session():
    s = requests.Session()
    s.headers["User-Agent"] = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) "
        "Gecko/20100101 Firefox/149.0"
    )
    s.headers["Referer"] = f"{BASE_URL}/prohibitionPublicList.htm"
    return s


# ── FETCH MANDALS ─────────────────────────────────────────────────────────────

def fetch_mandals(session, dist_code):
    resp = session.post(
        f"{BASE_URL}/MandalDetails.htm",
        data=f"dist_code={dist_code}",
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01",
        },
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    return [
        {"code": m["code"], "name": m["name"]}
        for m in data.get("mandalDetails", [])
    ]


# ── FETCH VILLAGES ────────────────────────────────────────────────────────────

def fetch_villages(session, dist_code, mand_code):
    resp = session.post(
        f"{BASE_URL}/VillageDetails.htm?dist_code={dist_code}&mand_code={mand_code}",
        headers={"Accept": "application/json, text/plain, */*"},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    # Try both known keys
    villages = data.get("villageDetails") or data.get("villDetails") or []
    return [
        {"code": str(v["code"]), "name": v["name"]}
        for v in villages
    ]


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    session = make_session()
    dist = DISTRICT

    print(f"\nFetching mandals for {dist['name']} ({dist['code']}) ...")
    mandals = fetch_mandals(session, dist["code"])
    print(f"  → {len(mandals)} mandals found")

    result = {
        "district": dist,
        "mandals": []
    }

    for i, mandal in enumerate(mandals, 1):
        print(f"  [{i:02}/{len(mandals)}] {mandal['name']} ({mandal['code']}) — fetching villages ...", end=" ", flush=True)
        try:
            villages = fetch_villages(session, dist["code"], mandal["code"])
            print(f"{len(villages)} villages")
        except Exception as e:
            print(f"ERROR: {e}")
            villages = []

        result["mandals"].append({
            "code": mandal["code"],
            "name": mandal["name"],
            "villages": villages,
        })

        time.sleep(DELAY)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    total_villages = sum(len(m["villages"]) for m in result["mandals"])
    print(f"\n✓ Saved to {OUTPUT_FILE}")
    print(f"  {len(mandals)} mandals, {total_villages} villages total\n")


if __name__ == "__main__":
    main()