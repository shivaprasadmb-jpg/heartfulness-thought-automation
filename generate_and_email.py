import os
import datetime
import yagmail
from generate_card import HeartfulnessCardGenerator

GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
DESTINATION_EMAIL = os.environ.get("DESTINATION_EMAIL")

IMAGE_FILENAME = "daily_thought.png"

def get_current_heartfulness_dates():
    now = datetime.datetime.now()
    kannada_months = ["ಜನೆವರಿ", "ಫೆಬ್ರವರಿ", "ಮಾರ್ಚ್", "ಏಪ್ರಿಲ್", "ಮೇ", "ಜೂನ್", 
                      "ಜುಲೈ", "ಆಗಸ್ಟ್", "ಸೆಪ್ಟೆಂಬರ್", "ಅಕ್ಟೋಬರ್", "ನವೆಂಬರ್", "ಡಿಸೆಂಬರ್"]
    kannada_weekdays = ["ಭಾನುವಾರ", "ಸೋಮವಾರ", "ಮಂಗಳವಾರ", "ಬುಧವಾರ", "ಗುರುವಾರ", "ಶುಕ್ರವಾರ", "ಶನಿವಾರ"]
    
    english_date = now.strftime("%A, %B %d, %Y")
    k_weekday = kannada_weekdays[int(now.strftime("%w"))]
    k_month = kannada_months[now.month - 1]
    k_day = now.strftime("%d")
    k_year = now.strftime("%Y")
    kannada_date = f"{k_weekday}, {k_day} {k_month} {k_year}"
    return kannada_date, english_date

def main():
    kannada_date_str, english_date_str = get_current_heartfulness_dates()

    todays_thought = {
        "kannada_header": "ಒಂದು ಸುಂದರ ವಿಚಾರ",
        "kannada_date": kannada_date_str,
        "kannada_quote": "ಧ್ಯಾನದ ಸಮಯದಲ್ಲಿ ಅಂತರಾತ್ಮನನ್ನು ಭೇಟಿಯಾಗಲು ನೀವು ಉತ್ಸುಕರಾಗಿದ್ದೀರಾ? ಚಡಪಡಿಕೆ, ಉತ್ಸಾಹ ಮತ್ತು ಅನುರಕ್ತಿಯ ಭಾವಗಳು ಧ್ಯಾನಕ್ಕೆ ಜೀವ ತುಂಬುತ್ತವೆ.",
        "kannada_author": "~ ದಾಜಿ",
        "english_header": "One Beautiful Thought",
        "english_date": english_date_str,
        "english_quote": "Do you feel inspired to meet your inner Self during meditation? That attitude of impatience, enthusiasm and passion brings life to meditation.",
        "english_author": "~ Daaji",
    }

    # Generate 1080x1920 Status card
    image_path = HeartfulnessCardGenerator.create_card(todays_thought, IMAGE_FILENAME)

    schedule_text = f"""🌿 {kannada_date_str.split(',')[0]} | {english_date_str.split(',')[0]} 🌿
ಹಾರ್ಟ್‌ಫುಲ್‌ನೆಸ್ | Heartfulness 
━━━━━━━━━━━━━━━
🌅 ಬೆಳಿಗ್ಗೆ 6:00 AM | Morning Meditation
🌙 ರಾತ್ರಿ 8:50 PM | Night Meditation

🕊️ Being Heartful Every Day | ಪ್ರತಿ ದಿನ ಹೃತ್ಪೂರ್ವಕವಾಗಿರುವುದು
🔴 YouTube Live: https://www.youtube.com/@BeingHeartfulEveryDay/live
━━━━━━━━━━━━━━━"""

    # Yagmail dispatch with direct attachment
    yag = yagmail.SMTP(GMAIL_USER, GMAIL_APP_PASSWORD)
    
    subject = f"Heartfulness Thought & Schedule: {english_date_str}"
    body = [
        f"Daily update generated successfully on {datetime.datetime.now().strftime('%H:%M:%S')}.\n",
        "1. Save/share the attached 9:16 vertical card directly to WhatsApp Status.\n",
        "2. Copy the schedule text below for group broadcasts:\n",
        "----------------------------------------",
        schedule_text,
        "----------------------------------------",
    ]

    # attachments parameter guarantees a direct download file icon in Gmail
    yag.send(
        to=DESTINATION_EMAIL,
        subject=subject,
        contents=body,
        attachments=image_path
    )
    print("Dispatched image and broadcast text to email successfully.")

if __name__ == "__main__":
    main()
