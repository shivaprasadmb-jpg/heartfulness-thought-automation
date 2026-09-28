import email
from email.header import decode_header
import imaplib
import os
import re
import datetime
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


def clean_quote_text(text):
    """Cleans up quotation marks and accidental space-comma typos."""
    t = text.strip().strip("“\"").strip("”\"").strip()
    t = re.sub(r'\s+([,.:;?!])', r'\1', t)
    return t


def fetch_latest_thought_from_email(fallback_kn_date, fallback_en_date):
    """
    Connects to Google's raw All Mail folder to read the daily 3:30 AM email,
    bypassing category tabs (Updates/Promotions) and client caching.
    """
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)

        # Open '[Gmail]/All Mail' to catch the email wherever Gmail filed it
        status, _ = mail.select('"[Gmail]/All Mail"', readonly=True)
        if status != "OK":
            mail.select("inbox", readonly=True)

        # Search for recent messages containing 'Thought' or 'ವಿಚಾರ'
        status, message_ids = mail.search(None, '(OR (SUBJECT "Thought") (BODY "Beautiful Thought"))')
        id_list = message_ids[0].split() if message_ids and message_ids[0] else []

        if not id_list:
            status, all_ids = mail.search(None, 'ALL')
            id_list = all_ids[0].split()[-15:] if all_ids and all_ids[0] else []

        if not id_list:
            mail.logout()
            raise ValueError("No matching emails found on server.")

        # Walk backwards from the newest email to find the matching thought
        target_body = None
        for msg_id in reversed(id_list[-10:]):
            _, data = mail.fetch(msg_id, "(RFC822)")
            raw = email.message_from_bytes(data[0][1])

            body_content = ""
            if raw.is_multipart():
                for part in raw.walk():
                    if part.get_content_type() in ["text/plain", "text/html"]:
                        payload = part.get_payload(decode=True)
                        if payload:
                            body_content += payload.decode("utf-8", errors="ignore")
            else:
                payload = raw.get_payload(decode=True)
                if payload:
                    body_content += payload.decode("utf-8", errors="ignore")

            if "ಒಂದು ಸುಂದರ ವಿಚಾರ" in body_content or "One Beautiful Thought" in body_content:
                target_body = body_content
                break

        mail.logout()

        if not target_body:
            raise ValueError("Could not find thought keywords in recent emails.")

        kn_match = re.search(r"ಒಂದು ಸುಂದರ ವಿಚಾರ[\s\S]*?[“\"]([\s\S]*?)[”\"]", target_body)
        en_match = re.search(r"(?:One Beautiful Thought|Beautiful Thought)[\s\S]*?[“\"]([\s\S]*?)[”\"]", target_body)

        kn_text = clean_quote_text(kn_match.group(1)) if kn_match else ""
        en_text = clean_quote_text(en_match.group(1)) if en_match else ""

        if not kn_text or not en_text:
            raise ValueError("Failed to extract quote boundaries from email body.")

        print("Successfully extracted dynamic daily thought from Gmail server.")
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
        print(f"IMAP note: {e}. Using active safety fallback.")
        return {
            "kannada_header": "ಒಂದು ಸುಂದರ ವಿಚಾರ",
            "kannada_date": fallback_kn_date,
            "kannada_quote": "ಸಮಚಿತ್ತ, ಕೇಂದ್ರೀಕರಣ ಮತ್ತು ಉತ್ಸುಕತೆಗಳು ನಮ್ಮ ಭವಿಷ್ಯವನ್ನು ನಿರ್ಮಿಸಲು ಸೂಕ್ತವಾದ ಕಂಪನ ಕ್ಷೇತ್ರವನ್ನು ರಚಿಸುವಲ್ಲಿ ಮಹತ್ವದ ಪಾತ್ರ ವಹಿಸುತ್ತವೆ.",
            "kannada_author": "~ ದಾಜಿ",
            "english_header": "One Beautiful Thought",
            "english_date": fallback_en_date,
            "english_quote": "Poise, focus and enthusiasm go a long way in creating the right vibratory field for us to design our destiny.",
            "english_author": "~ Daaji",
        }


def main():
    kannada_date_str, english_date_str = get_current_heartfulness_dates()

    # 1. Fetch dynamic quotes from Gmail
    thought_data = fetch_latest_thought_from_email(kannada_date_str, english_date_str)

    # 2. Render status card
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

    # 3. Dispatch to inbox with both the attachment AND the ready-to-copy schedule
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
    print("Dispatched image card and schedule broadcast successfully.")


if __name__ == "__main__":
    main()
