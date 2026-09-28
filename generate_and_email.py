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


def fetch_latest_thought_from_email(fallback_kn_date, fallback_en_date):
    """
    Connects to Gmail via IMAP, finds the latest 'One Beautiful Thought' email,
    and extracts the Kannada and English quotes.
    """
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        mail.select("inbox")

        # Search for incoming Heartfulness thought emails
        status, messages = mail.search(None, '(SUBJECT "One Beautiful Thought")')
        if not messages[0]:
            mail.logout()
            raise ValueError("No email found with subject 'One Beautiful Thought'")

        # Fetch the most recent message
        latest_id = messages[0].split()[-1]
        _, msg_data = mail.fetch(latest_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        body = payload.decode("utf-8", errors="ignore")
                        break
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                body = payload.decode("utf-8", errors="ignore")

        mail.logout()

        # Regular expressions to parse Kannada and English quotes
        # Matches text enclosed in quotes under each language section
        kn_match = re.search(r"ಒಂದು ಸುಂದರ ವಿಚಾರ[\s\S]*?[“\"]([\s\S]*?)[”\"]", body)
        en_match = re.search(r"One Beautiful Thought[\s\S]*?[“\"]([\s\S]*?)[”\"]", body)

        kn_text = kn_match.group(1).strip() if kn_match else ""
        en_text = en_match.group(1).strip() if en_match else ""

        if not kn_text or not en_text:
            raise ValueError("Could not extract quote bodies from the email.")

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
        print(f"Dynamic email parse failed: {e}. Falling back to default.")
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

    # 1. Fetch dynamic quotes from today's incoming email
    thought_data = fetch_latest_thought_from_email(kannada_date_str, english_date_str)

    # 2. Render pixel-perfect card
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

    # 3. Dispatch to your inbox
    yag = yagmail.SMTP(GMAIL_USER, GMAIL_APP_PASSWORD)
    subject = f"Heartfulness Thought & Schedule: {english_date_str}"
    body = [
        f"Daily update generated successfully on {datetime.datetime.now().strftime('%H:%M:%S')}.\n",
        "1. Attached: 9:16 card for WhatsApp Status.\n",
        "2. Copy the schedule text below for group broadcasts:\n",
        "----------------------------------------",
        schedule_text,
        "----------------------------------------",
    ]

    yag.send(
        to=DESTINATION_EMAIL,
        subject=subject,
        contents=body,
        attachments=image_path,
    )
    print("Dispatched today's dynamic thought card successfully.")


if __name__ == "__main__":
    main()
    
