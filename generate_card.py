# ==============================================================================
# Save this entire block as: C:\Users\admin\documents\trading_engine\generate_card.py
# ==============================================================================
import os
import time

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: 'playwright' library not found.")
    print("Run: pip install playwright && python -m playwright install chromium")
    raise


class HeartfulnessCardGenerator:
    """
    Generates pixel-perfect Kannada/English thought cards using an HTML engine.
    This method ensures perfect Unicode rendering and text-wrapping.
    """

    @staticmethod
    def _generate_html_template(data):
        # Using Google Fonts for Noto Sans Kannada ensures correct glyph shaping
        return f"""
        <!DOCTYPE html>
        <html lang="kn">
        <head>
        <meta charset="UTF-8">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Kannada:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                width: 540px; height: 1080px;
                background-color: #faf7f2;
                display: flex; justify-content: center; align-items: center;
                font-family: 'Noto Sans Kannada', sans-serif;
                color: #553c35;
            }}
            .card-container {{
                width: 480px; height: 1000px;
                border: 1.5px solid #dcd4c8;
                padding: 45px 35px;
                position: relative;
                background-color: #faf7f2;
            }}
            /* Corner notches matching traditional notes theme */
            .corner-tl, .corner-tr, .corner-bl, .corner-br {{
                position: absolute; width: 10px; height: 10px; border-color: #dcd4c8; border-style: solid; border-width: 0;
            }}
            .corner-tl {{ top: -1px; left: -1px; border-right-width: 1.5px; border-bottom-width: 1.5px; }}
            .corner-tr {{ top: -1px; right: -1px; border-left-width: 1.5px; border-bottom-width: 1.5px; }}
            .corner-bl {{ bottom: -1px; left: -1px; border-right-width: 1.5px; border-top-width: 1.5px; }}
            .corner-br {{ bottom: -1px; right: -1px; border-left-width: 1.5px; border-top-width: 1.5px; }}

            .section {{ margin-bottom: 35px; }}
            h2 {{ font-size: 21px; font-weight: 700; margin-bottom: 12px; }}
            .date {{ font-size: 17px; font-weight: 600; margin-bottom: 25px; }}
            .quote {{ font-size: 19px; line-height: 1.6; margin-bottom: 25px; text-align: justify; font-weight: 400; }}
            .author {{ font-size: 18px; font-weight: 700; }}
            .footer {{
                position: absolute; bottom: 20px; width: 100%; left: 0;
                text-align: center; font-size: 13px; color: #9c9288; font-weight: 600;
            }}
        </style>
        </head>
        <body>
            <div class="card-container">
                <div class="corner-tl"></div><div class="corner-tr"></div>
                <div class="corner-bl"></div><div class="corner-br"></div>

                <!-- Kannada Section -->
                <div class="section">
                    <h2>{data.get('kannada_header', 'ಒಂದು ಸುಂದರ ವಿಚಾರ')}</h2>
                    <div class="date">{data.get('kannada_date', 'Sunday, September 27, 2026')}</div>
                    <div class="quote">“ {data.get('kannada_quote', '')} ”</div>
                    <div class="author">{data.get('kannada_author', '~ ದಾಜಿ')}</div>
                </div>

                <!-- English Section -->
                <div class="section" style="margin-top: 60px;">
                    <h2>{data.get('english_header', 'One Beautiful Thought')}</h2>
                    <div class="date">{data.get('english_date', 'Sunday, September 27, 2026')}</div>
                    <div class="quote">“ {data.get('english_quote', '')} ”</div>
                    <div class="author">{data.get('english_author', '~ Daaji')}</div>
                </div>

                <div class="footer">Created with Heartfulness</div>
            </div>
        </body>
        </html>
        """

    @classmethod
    def create_card(cls, data, output_filename="daily_thought.png"):
        """
        Renders the provided thought data into a high-quality PNG image.
        """
        print(f"Preparing to generate image card: {output_filename}...")
        html_content = cls._generate_html_template(data)

        with sync_playwright() as p:
            # Launch headless browser (Chromium)
            try:
                browser = p.chromium.launch()
            except Exception as e:
                print(f"Error launching browser: {e}")
                print("Make sure you ran: python -m playwright install chromium")
                raise

            # Create a page matching the card's intended aspect ratio
            page = browser.new_page(viewport={"width": 540, "height": 1080})
            page.set_content(html_content)

            # Wait for Google Fonts to load fully before screenshotting
            page.wait_for_load_state("networkidle")
            # Small buffer for font rendering stability
            time.sleep(0.5)

            # Take full-page screenshot
            page.screenshot(path=output_filename, full_page=False, omit_background=False)
            browser.close()

        if os.path.exists(output_filename):
            print(f"Successfully generated pixel-perfect card: {output_filename}")
            return output_filename
        else:
            raise FileNotFoundError(f"Failed to create image: {output_filename}")


# ==============================================================================
# DATA AND TEST EXECUTION
# ==============================================================================

# Today's thought data
todays_thought = {
    "kannada_header": "ಒಂದು ಸುಂದರ ವಿಚಾರ",
    "kannada_date": "ಭಾನುವಾರ, 27 ಸೆಪ್ಟೆಂಬರ್ 2026",
    "kannada_quote": (
        "ಪ್ರಜ್ಞೆ ಮತ್ತು ಅರಿವಿನ ನಡುವಿನ ವ್ಯತ್ಯಾಸವೇನು? ಪ್ರಜ್ಞೆ ಬದಲಾಗುತ್ತಾ"
        " ಹೋಗುತ್ತದೆ. ಪ್ರಜ್ಞೆಯು ಹೇಗೆ ಕಾರ್ಯ ನಿರ್ವಹಿಸುತ್ತಿದೆ ಎಂಬುದನ್ನು ನೋಡುವುದೇ"
        " ಅರಿವು."
    ),
    "kannada_author": "~ ದಾಜಿ",
    "english_header": "One Beautiful Thought",
    "english_date": "Sunday, September 27, 2026",
    "english_quote": (
        "What is the difference between consciousness and awareness?"
        " Consciousness keeps changing. Awareness is to see how"
        " consciousness is functioning."
    ),
    "english_author": "~ Daaji",
}

# GENERATE THE IMAGE
# We assign the output filename here
image_path = HeartfulnessCardGenerator.create_card(todays_thought, "todays_update.png")