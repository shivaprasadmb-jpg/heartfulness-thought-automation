import os
import yagmail
import datetime

# We reuse your existing flawless generator class
from generate_card import HeartfulnessCardGenerator

# ==============================================================================
# 1. CONFIGURATION (Stored in GitHub Secrets)
# ==============================================================================
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
DESTINATION_EMAIL = os.environ.get("DESTINATION_EMAIL") # e.g., your_phone@gmail.com

IMAGE_FILENAME = "daily_thought.png"

# ==============================================================================
# 2. GENERATE AND DISPATCH VIA EMAIL
# ==============================================================================
def main():
    try:
        # Today's dynamic date formatting
        now = datetime.datetime.now()
        english_date_str = now.strftime("%A, %B %d, %Y")
        
        # Simplified placeholder thought (Restore IMAP fetch here when needed)
        todays_thought = {
            "kannada_header": "ಒಂದು ಸುಂದರ ವಿಚಾರ",
            "kannada_date": f"ಭಾನುವಾರ, {now.strftime('%d %B %Y')}", # Basic Kannada date format
            "kannada_quote": (
                "“ ಧ್ಯಾನದ ಸಮಯದಲ್ಲಿ ಅಂತರಾತ್ಮನನ್ನು ಭೇಟಿಯಾಗಲು ನೀವು ಉತ್ಸುಕರಾಗಿದ್ದೀರಾ?"
                " ಚಡಪಡಿಕೆ, ಉತ್ಸಾಹ ಮತ್ತು ಅನುರಕ್ತಿಯ ಭಾವಗಳು ಧ್ಯಾನಕ್ಕೆ ಜೀವ ತುಂಬುತ್ತವೆ. ”"
            ),
            "kannada_author": "~ ದಾಜಿ",
            "english_header": "One Beautiful Thought",
            "english_date": english_date_str,
            "english_quote": (
                "“ Do you feel inspired to meet your inner Self during meditation?"
                " That attitude of impatience, enthusiasm and passion brings life"
                " to meditation. ”"
            ),
            "english_author": "~ Daaji",
        }
        
        # Generate the impeccable card
        image_path = HeartfulnessCardGenerator.create_card(todays_thought, IMAGE_FILENAME)
        
        # Initialize yagmail
        yag = yagmail.SMTP(GMAIL_USER, GMAIL_APP_PASSWORD)
        
        subject = f"Heartfulness Daily Thought: {english_date_str}"
        
        # Attach the image directly as the body of the email
        contents = [
            "Your flawless Heartfulness daily thought card has been generated on the cloud.",
            "Please share this image with your 3 groups.",
            yagmail.inline(image_path),
        ]
        
        yag.send(to=DESTINATION_EMAIL, subject=subject, contents=contents)
        print(f"Successfully emailed perfect card to {DESTINATION_EMAIL}")
        
    except Exception as e:
        print(f"Cloud generation/email failed: {e}")
        raise

if __name__ == "__main__":
    main()