import os
import time
from playwright.sync_api import sync_playwright


class HeartfulnessCardGenerator:
    """
    Renders clean, proportional cards matching the Redmi Notes parchment aesthetic.
    """

    @classmethod
    def _generate_html_template(cls, data):
        # Clean extra quotation marks or spaces
        kn_quote = data.get("kannada_quote", "").strip().strip("“\"").strip("”\"").strip()
        en_quote = data.get("english_quote", "").strip().strip("“\"").strip("”\"").strip()

        # Dynamic sizing for quote length so it never looks sparse or cramped
        max_len = max(len(kn_quote), len(en_quote))
        if max_len < 100:
            font_size = "23px"
            line_height = "1.85"
            section_gap = "34px"
        elif max_len < 200:
            font_size = "21px"
            line_height = "1.75"
            section_gap = "28px"
        else:
            font_size = "19px"
            line_height = "1.65"
            section_gap = "22px"

        return f"""
        <!DOCTYPE html>
        <html lang="kn">
        <head>
        <meta charset="UTF-8">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Kannada:wght@400;600;700&family=Noto+Serif+Kannada:wght@600;700&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}

            /* Canvas sized to match the Redmi Notes reference card aspect ratio */
            body {{
                width: 580px;
                min-height: 1040px;
                background-color: #F8F5F0;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 30px 24px;
                font-family: 'Noto Sans Kannada', 'Plus Jakarta Sans', sans-serif;
                -webkit-font-smoothing: antialiased;
            }}

            /* Outer parchment box */
            .card-wrapper {{
                width: 532px;
                background-color: #FBF9F5;
                border: 1.5px solid #DDD3C4;
                position: relative;
                padding: 44px 34px 30px;
                display: flex;
                flex-direction: column;
            }}

            /* Corner ornamental brackets matching Mi Notes */
            .corner {{
                position: absolute;
                width: 14px;
                height: 14px;
                border-color: #C8BAA8;
                border-style: solid;
            }}
            .c-tl {{ top: 4px; left: 4px; border-width: 2px 0 0 2px; }}
            .c-tr {{ top: 4px; right: 4px; border-width: 2px 2px 0 0; }}
            .c-bl {{ bottom: 4px; left: 4px; border-width: 0 0 2px 2px; }}
            .c-br {{ bottom: 4px; right: 4px; border-width: 0 2px 2px 0; }}

            /* Content container */
            .content {{
                display: flex;
                flex-direction: column;
            }}

            /* Section Styling */
            .section {{
                margin-bottom: {section_gap};
            }}

            /* Kannada Headings */
            .header-kn {{
                font-family: 'Noto Serif Kannada', serif;
                font-size: 23px;
                font-weight: 700;
                color: #4A352F;
                margin-bottom: 12px;
                letter-spacing: 0.2px;
            }}
            .date-kn {{
                font-size: 18px;
                font-weight: 600;
                color: #5A443D;
                margin-bottom: 22px;
            }}
            .quote-kn {{
                font-size: {font_size};
                line-height: {line_height};
                font-weight: 400;
                color: #382823;
                text-align: left;
                margin-bottom: 18px;
            }}
            .author-kn {{
                font-size: 19px;
                font-weight: 700;
                color: #4A352F;
            }}

            /* Subtle separator */
            .separator {{
                height: 1px;
                background-color: #EADFD0;
                margin: 6px 0 {section_gap};
                width: 100%;
            }}

            /* English Headings */
            .header-en {{
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 21px;
                font-weight: 700;
                color: #4A352F;
                margin-bottom: 10px;
                letter-spacing: -0.2px;
            }}
            .date-en {{
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 17px;
                font-weight: 600;
                color: #5A443D;
                margin-bottom: 20px;
            }}
            .quote-en {{
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: {font_size};
                line-height: {line_height};
                font-weight: 400;
                color: #382823;
                text-align: left;
                margin-bottom: 18px;
            }}
            .author-en {{
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 19px;
                font-weight: 700;
                color: #4A352F;
            }}

            /* Footer */
            .footer {{
                margin-top: 36px;
                text-align: center;
                font-size: 13px;
                color: #A99B8B;
                letter-spacing: 0.5px;
            }}
        </style>
        </head>
        <body>
            <div class="card-wrapper">
                <div class="corner c-tl"></div>
                <div class="corner c-tr"></div>
                <div class="corner c-bl"></div>
                <div class="corner c-br"></div>

                <div class="content">
                    <!-- Kannada Section -->
                    <div class="section">
                        <div class="header-kn">{data.get('kannada_header', 'ಒಂದು ಸುಂದರ ವಿಚಾರ')}</div>
                        <div class="date-kn">{data.get('kannada_date', '')}</div>
                        <div class="quote-kn">“{kn_quote}”</div>
                        <div class="author-kn">{data.get('kannada_author', '~ ದಾಜಿ')}</div>
                    </div>

                    <div class="separator"></div>

                    <!-- English Section -->
                    <div class="section">
                        <div class="header-en">{data.get('english_header', 'One Beautiful Thought')}</div>
                        <div class="date-en">{data.get('english_date', '')}</div>
                        <div class="quote-en">“{en_quote}”</div>
                        <div class="author-en">{data.get('english_author', '~ Daaji')}</div>
                    </div>
                </div>

                <div class="footer">Created with Heartfulness</div>
            </div>
        </body>
        </html>
        """

    @classmethod
    def create_card(cls, data, output_filename="daily_thought.png"):
        """Renders cleanly proportioned card matching Redmi Notes format."""
        html_content = cls._generate_html_template(data)
        with sync_playwright() as p:
            browser = p.chromium.launch()
            # Viewport set to standard compact note aspect
            page = browser.new_page(viewport={"width": 580, "height": 1040})
            page.set_content(html_content)
            page.wait_for_load_state("networkidle")
            time.sleep(0.5)

            # Locate the wrapper card and snapshot it tightly
            card_element = page.locator(".card-wrapper")
            card_element.screenshot(path=output_filename)
            browser.close()

        return output_filename

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
