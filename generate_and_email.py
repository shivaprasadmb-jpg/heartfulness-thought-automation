import email
from email.header import decode_header
import imaplib
import os
import re
import datetime
import html
import yagmail
from generate_card import HeartfulnessCardGenerator

GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
DESTINATION_EMAIL = os.environ.get("DESTINATION_EMAIL")
IMAGE_FILENAME = "daily_thought.png"


def get_current_heartfulness_dates():
    """Generates localized IST date strings."""
    ist_offset = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    now = datetime.datetime.now(ist_offset)

    kannada_months = [
        "ಜನವರಿ", "ಫೆಬ್ರವರಿ", "ಮಾರ್ಚ್", "ಏಪ್ರಿಲ್", "ಮೇ", "ಜೂನ್", 
        "ಜುಲೈ", "ಆಗಸ್ಟ್", "ಸೆಪ್ಟೆಂಬರ್", "ಅಕ್ಟೋಬರ್", "ನವೆಂಬರ್", "ಡಿಸೆಂಬರ್"
    ]
    kannada_weekdays = [
        "ಭಾನುವಾರ", "ಸೋಮವಾರ", "ಮಂಗಳವಾರ", "ಬುಧವಾರ", "ಗುರುವಾರ", "ಶುಕ್ರವಾರ", "ಶನಿವಾರ"
    ]

    english_date = now.strftime("%A, %B %d, %Y")
    k_weekday = kannada_weekdays[int(now.strftime("%w"))]
    k_month = kannada_months[now.month - 1]
    k_day = now.strftime("%d").lstrip("0")
    k_year = now.strftime("%Y")

    kannada_date = f"{k_weekday}, {k_day} {k_month} {k_year}"
    return kannada_date, english_date


def clean_text(raw_html_or_text):
    """Strips <style>, <script>, and all HTML markup cleanly."""
    # 1. Strip CSS style blocks completely so CSS font names like 'Helvetica' vanish
    text = re.sub(r'<style[^>]*>[\s\S]*?</style>', ' ', raw_html_or_text, flags=re.IGNORECASE)
    # 2. Strip Script blocks
    text = re.sub(r'<script[^>]*>[\s\S]*?</script>', ' ', text, flags=re.IGNORECASE)
    # 3. Strip HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # 4. Unescape HTML entities (&nbsp;, &quot;, etc.)
    text = html.unescape(text)
    # 5. Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def clean_quote_punctuation(text):
    """Cleans up quotation marks and spacing before punctuation."""
    t = text.strip().strip("“\"").strip("”\"").strip()
    t = re.sub(r'\s+([,.:;?!])', r'\1', t)
    return t


def fetch_latest_thought_from_email(fallback_kn_date, fallback_en_date):
    """
    Connects to Gmail's All Mail folder, scans recent thought emails,
    and extracts authentic Kannada and English sentences.
    """
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)

        status, _ = mail.select('"[Gmail]/All Mail"', readonly=True)
        if status != "OK":
            mail.select("inbox", readonly=True)

        status, message_ids = mail.search(None, '(OR (SUBJECT "One Beautiful Thought") (SUBJECT "Thought"))')
        id_list = message_ids[0].split() if message_ids and message_ids[0] else []

        if not id_list:
            status, all_ids = mail.search(None, 'ALL')
            id_list = all_ids[0].split()[-20:] if all_ids and all_ids[0] else []

        if not id_list:
            mail.logout()
            raise ValueError("No messages found in mail storage.")

        kn_text = ""
        en_text = ""

        # Scan backwards across messages to capture both parts
        for msg_id in reversed(id_list[-15:]):
            _, data = mail.fetch(msg_id, "(RFC822)")
            raw = email.message_from_bytes(data[0][1])

            body_content = ""
            if raw.is_multipart():
                for part in raw.walk():
                    ctype = part.get_content_type()
                    if ctype in ["text/plain", "text/html"]:
                        payload = part.get_payload(decode=True)
                        if payload:
                            body_content += payload.decode("utf-8", errors="ignore") + "\n"
            else:
                payload = raw.get_payload(decode=True)
                if payload:
                    body_content = payload.decode("utf-8", errors="ignore")

            plain = clean_text(body_content)

            # Extract Kannada quote (must contain Indic characters and spaces)
            if not kn_text and "ಒಂದು ಸುಂದರ ವಿಚಾರ" in plain:
                for match in re.finditer(r"[“\"]([^”\"]{20,})[”\"]", plain):
                    candidate = match.group(1).strip()
                    if any('\u0c80' <= c <= '\u0cff' for c in candidate):
                        kn_text = clean_quote_punctuation(candidate)
                        break

            # Extract English quote (must be an actual sentence with multiple words)
            if not en_text and "One Beautiful Thought" in plain:
                for match in re.finditer(r"[“\"]([^”\"]{20,})[”\"]", plain):
                    candidate = match.group(1).strip()
                    # Must contain spaces and be a natural English sentence, not CSS metadata
                    if " " in candidate and not candidate.lower().startswith("font") and "helvetica" not in candidate.lower():
                        en_text = clean_quote_punctuation(candidate)
                        break

            if kn_text and en_text:
                break

        mail.logout()

        if not kn_text or not en_text:
            raise ValueError(f"Incomplete quote capture. kn='{kn_text[:25]}', en='{en_text[:25]}'")

        print(f"Successfully extracted: '{en_text[:40]}...'")
        return {
            "kannada_header": "ಒಂದು ಸುಂದರ ವಿಚಾರ",
            "kannada_date": fallback_kn_date,
            "kannada_quote": kn_text,
            "kannada_author": "~ ದಾಜಿ",
            "english_header": "One Beautiful Thought",
            "english_date": fallback_en_date,
            "english_quote": en_text,
            "english_author": "~ Daaji",
        }

    except Exception as e:
        print(f"Extraction notice: {e}. Using active safety fallback.")
        return {
            "kannada_header": "ಒಂದು ಸುಂದರ ವಿಚಾರ",
            "kannada_date": fallback_kn_date,
            "kannada_quote": "ಹೃದಯಾಧಾರಿತ ಧ್ಯಾನದ ಅಭ್ಯಾಸದಲ್ಲಿ, ನಾವು ನಮ್ಮ ಅಸ್ತಿತ್ವದ ಅತಿ ಸರಳ ಮತ್ತು ಪರಿಶುದ್ಧವಾದ ಅಂಶವನ್ನು ಅನ್ವೇಷಿಸುತ್ತೇವೆ ಹಾಗು ಅನುಭವಿಸುತ್ತೇವೆ.",
            "kannada_author": "~ ದಾಜಿ",
            "english_header": "One Beautiful Thought",
            "english_date": fallback_en_date,
            "english_quote": "In a heart-based meditation practice, we explore and experience the simplest and purest aspect of our existence.",
            "english_author": "~ Daaji",
        }


def main():
    kannada_date_str, english_date_str = get_current_heartfulness_dates()

    thought_data = fetch_latest_thought_from_email(kannada_date_str, english_date_str)
    image_path = HeartfulnessCardGenerator.create_card(thought_data, IMAGE_FILENAME)

    weekday_kn = kannada_date_str.split(",")[0]
    weekday_en = english_date_str.split(",")[0]

    schedule_text = f"""🌿 {weekday_kn} | {weekday_en} 🌿
ಹಾರ್ಟ್‌ಫುಲ್‌ನೆಸ್ | Heartfulness 
━━━━━━━━━━━━━━━
🌅 ಬೆಳಿಗ್ಗೆ 6:00 AM | Morning Meditation
🌙 ರಾತ್ರಿ 8:50 PM | Night Meditation

🕊️ Being Heartful Every Day | ಪ್ರತಿ ದಿನ ಹೃತ್ಪೂರ್ವಕವಾಗಿರುವುದು
🔴 YouTube Live: https://www.youtube.com/@BeingHeartfulEveryDay/live
━━━━━━━━━━━━━━━"""

    yag = yagmail.SMTP(GMAIL_USER, GMAIL_APP_PASSWORD)
    subject = f"Heartfulness Thought & Schedule: {english_date_str}"
    
    body = f"""Daily update generated successfully on {datetime.datetime.now().strftime('%H:%M:%S')}.

1. The 9:16 vertical card is attached below for WhatsApp Status.
2. Copy the schedule text below for group broadcasts:

----------------------------------------
{schedule_text}
----------------------------------------
"""

    yag.send(
        to=DESTINATION_EMAIL,
        subject=subject,
        contents=body,
        attachments=image_path,
    )
    print("Dispatched today's card and broadcast schedule successfully.")


if __name__ == "__main__":
    main()
    
