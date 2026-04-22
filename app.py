import io
import time
import json
import base64
import requests
import streamlit as st
import pypdfium2 as pdfium
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ───────────────── CONFIG ─────────────────
BASE_URL = "https://registration.telangana.gov.in"
DATA_FILE = "district_data.json"

FORM_TYPES = ["1", "2", "3", "5", "6"]
PROHIB_TYPES = ["AGRI", "NONAGRI"]

OCR_URL = "https://api.ocr.space/parse/image"

# ───────────────── UI ─────────────────
st.set_page_config(page_title="Land Search Engine", layout="wide")
st.title("📋 Telangana Land Search Engine")

# ───────────────── LOAD DATA ─────────────────
@st.cache_data
def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()
district = data["district"]

# ───────────────── OCR KEY ─────────────────
def get_ocr_key():
    return st.secrets.get("OCR_API_KEY", "helloworld")

# ───────────────── SESSION ─────────────────
def create_session():
    s = requests.Session()

    retry = Retry(
        total=5,
        backoff_factor=1.2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]
    )

    s.mount("https://", HTTPAdapter(max_retries=retry))

    s.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Referer": f"{BASE_URL}/prohibitionPublicList.htm"
    })

    return s

# ───────────────── INPUTS ─────────────────
mandal = st.selectbox("Mandal", [m["name"] for m in data["mandals"]])
mandal_obj = next(m for m in data["mandals"] if m["name"] == mandal)

village = st.selectbox("Village", [v["name"] for v in mandal_obj["villages"]])
village_obj = next(v for v in mandal_obj["villages"] if v["name"] == village)

land_types = st.multiselect("Land Type", PROHIB_TYPES, default=PROHIB_TYPES)
survey = st.text_input("Survey Number", "46/1/1/2")

# ───────────────── PROGRESS UI (ALWAYS ON) ─────────────────
progress_bar = st.progress(0)
status_box = st.empty()
log_box = st.container()

logs = []

def log(msg):
    logs.append(msg)
    with log_box:
        st.write("🧾 " + msg)

def status(msg):
    status_box.info(msg)

# ───────────────── FETCH PDF ─────────────────
def fetch_pdf(session, dist, mand, vill, prohib, form):
    try:
        status(f"📥 Fetching {prohib} | Form {form}")

        r = session.post(
            f"{BASE_URL}/viewProhibitedDataPDF.htm",
            data={
                "dist_code": dist,
                "mand_code": mand,
                "vill_code": vill,
                "prohib_type": prohib,
                "formtype": form,
                "sro_code": "",
            },
            timeout=30,
            verify=False
        )

        if r.status_code != 200 or len(r.content) < 1000:
            log(f"❌ Invalid PDF for {prohib}-{form}")
            return None

        return r.content

    except Exception as e:
        log(f"❌ Fetch error: {e}")
        return None

# ───────────────── PDF → IMAGES ─────────────────
def pdf_to_images(pdf_bytes):
    pdf = pdfium.PdfDocument(io.BytesIO(pdf_bytes))
    images = []

    for i in range(len(pdf)):
        page = pdf[i]
        img = page.render(scale=2).to_pil()

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=70)
        images.append(buf.getvalue())

    return images

# ───────────────── OCR ─────────────────
def run_ocr(image_bytes):
    try:
        r = requests.post(
            OCR_URL,
            files={"file": ("img.jpg", image_bytes)},
            data={
                "apikey": get_ocr_key(),
                "language": "eng",
                "OCREngine": 2
            },
            timeout=60
        )

        j = r.json()

        if j.get("OCRExitCode") == 1:
            return j["ParsedResults"][0]["ParsedText"]

    except Exception as e:
        log(f"OCR error: {e}")

    return ""

# ───────────────── SEARCH ─────────────────
def search_pdf(pdf_bytes, survey):
    images = pdf_to_images(pdf_bytes)

    for i, img in enumerate(images):
        status(f"🔍 OCR Page {i+1}/{len(images)}")

        text = run_ocr(img)

        if survey in text:
            log("🎯 MATCH FOUND")
            return True

    return False

# ───────────────── MAIN ─────────────────
if st.button("🚀 SEARCH ALL", use_container_width=True):

    session = create_session()

    results = []
    total = len(land_types) * len(FORM_TYPES)
    step = 0

    status("🚀 Starting search...")

    for land in land_types:
        for form in FORM_TYPES:

            step += 1
            progress_bar.progress(step / total)

            pdf = fetch_pdf(
                session,
                district["code"],
                mandal_obj["code"],
                village_obj["code"],
                land,
                form
            )

            if not pdf:
                continue

            # FAST CHECK
            if survey in pdf.decode(errors="ignore"):
                log(f"⚡ Fast match: {land}-{form}")
                results.append((land, form, pdf))
                continue

            # OCR CHECK
            status(f"🧠 OCR scanning {land}-{form}")
            if search_pdf(pdf, survey):
                results.append((land, form, pdf))

            time.sleep(0.4)

    # ───────────────── RESULTS ─────────────────
    st.divider()

    if not results:
        st.error("❌ No matches found")
    else:
        st.success(f"🎯 Found {len(results)} matches")

        for i, (land, form, pdf) in enumerate(results):

            filename = f"{land}_{form}.pdf"

            with st.expander(f"📄 {land} | Form {form}", expanded=True):

                b64 = base64.b64encode(pdf).decode()

                st.markdown(
                    f"""
                    <iframe
                        src="data:application/pdf;base64,{b64}"
                        width="100%"
                        height="600px"
                    ></iframe>
                    """,
                    unsafe_allow_html=True
                )

                st.download_button(
                    "💾 Download PDF",
                    pdf,
                    file_name=filename,
                    mime="application/pdf",
                    key=f"dl_{i}"
                )