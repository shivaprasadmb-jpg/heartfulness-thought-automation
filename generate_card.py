import os
import time
from playwright.sync_api import sync_playwright


class HeartfulnessCardGenerator:
    """
    Renders an elegant, aesthetically refined daily thought card
    with textured parchment, balanced editorial typography, and subtle motif accents.
    """

    @classmethod
    def _generate_html_template(cls, data):
        kn_quote = data.get("kannada_quote", "").strip().strip("“\"").strip("”\"").strip()
        en_quote = data.get("english_quote", "").strip().strip("“\"").strip("”\"").strip()

        # Dynamic size scaling based on quote volume
        max_len = max(len(kn_quote), len(en_quote))
        if max_len < 110:
            kn_quote_fs = "23px"
            en_quote_fs = "22px"
            line_height = "1.85"
            content_padding = "24px 38px"
        elif max_len < 220:
            kn_quote_fs = "21px"
            en_quote_fs = "20px"
            line_height = "1.75"
            content_padding = "18px 36px"
        else:
            kn_quote_fs = "19px"
            en_quote_fs = "18px"
            line_height = "1.6"
            content_padding = "12px 32px"

        return f"""
        <!DOCTYPE html>
        <html lang="kn">
        <head>
        <meta charset="UTF-8">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Noto+Serif+Kannada:wght@500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700&display=swap" rel="stylesheet">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}

            body {{
                width: 620px;
                min-height: 1060px;
                background-color: #EDE8DF;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 30px 24px;
                font-family: 'Noto Serif Kannada', 'Cormorant Garamond', serif;
                -webkit-font-smoothing: antialiased;
            }}

            /* Main Card Frame with layered borders & subtle paper glow */
            .card-wrapper {{
                width: 564px;
                background: radial-gradient(circle at 50% 30%, #FCFBF8 0%, #F6F1E7 100%);
                border: 1.5px solid #D5C7B5;
                position: relative;
                padding: {content_padding};
                box-shadow: 0 10px 30px rgba(70, 50, 35, 0.08);
            }}

            /* Inset gold-parchment hairline frame */
            .inner-border {{
                position: absolute;
                top: 8px; left: 8px; right: 8px; bottom: 8px;
                border: 1px solid rgba(184, 158, 126, 0.45);
                pointer-events: none;
            }}

            /* Four decorative vintage corner brackets */
            .corner {{
                position: absolute;
                width: 14px;
                height: 14px;
                border-color: #A38265;
                border-style: solid;
            }}
            .c-tl {{ top: 3px; left: 3px; border-width: 2.5px 0 0 2.5px; }}
            .c-tr {{ top: 3px; right: 3px; border-width: 2.5px 2.5px 0 0; }}
            .c-bl {{ bottom: 3px; left: 3px; border-width: 0 0 2.5px 2.5px; }}
            .c-br {{ bottom: 3px; right: 3px; border-width: 0 2.5px 2.5px 0; }}

            /* Subtle watermark lotus motif */
            .watermark-emblem {{
                position: absolute;
                top: 48%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 140px;
                color: rgba(180, 155, 130, 0.06);
                user-select: none;
                pointer-events: none;
                font-family: 'Cinzel', serif;
            }}

            /* Header Badges */
            .header-kn {{
                font-size: 21px;
                font-weight: 700;
                color: #6E261B;
                letter-spacing: 0.3px;
                margin-bottom: 6px;
            }}
            .date-kn {{
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 15px;
                font-weight: 600;
                color: #8C6A5A;
                margin-bottom: 20px;
                text-transform: capitalize;
            }}

            /* Quote block with left accent spine */
            .quote-container-kn {{
                position: relative;
                padding-left: 18px;
                border-left: 2.5px solid #C48E7C;
                margin-bottom: 16px;
            }}
            .quote-kn {{
                font-size: {kn_quote_fs};
                line-height: {line_height};
                font-weight: 600;
                color: #301E1A;
                text-align: justify;
                text-justify: inter-word;
            }}
            .author-kn {{
                text-align: right;
                font-size: 18px;
                font-weight: 700;
                color: #6E261B;
                margin-bottom: 26px;
            }}

            /* Spiritual emblem separator */
            .divider {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 16px;
                margin: 10px 0 24px;
            }}
            .divider-line {{
                height: 1px;
                background: linear-gradient(90deg, transparent, #CEBFA8, transparent);
                flex-grow: 1;
            }}
            .divider-symbol {{
                color: #9E7D63;
                font-size: 13px;
                letter-spacing: 4px;
            }}

            /* English Section */
            .header-en {{
                font-family: 'Cinzel', serif;
                font-size: 18px;
                font-weight: 700;
                color: #1A3644;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                margin-bottom: 6px;
            }}
            .date-en {{
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 14px;
                font-weight: 600;
                color: #637882;
                margin-bottom: 20px;
            }}
            .quote-container-en {{
                position: relative;
                padding-left: 18px;
                border-left: 2.5px solid #7899A6;
                margin-bottom: 16px;
            }}
            .quote-en {{
                font-family: 'Cormorant Garamond', serif;
                font-size: {en_quote_fs};
                line-height: {line_height};
                font-weight: 600;
                font-style: italic;
                color: #1E282D;
                text-align: justify;
                text-justify: inter-word;
            }}
            .author-en {{
                text-align: right;
                font-family: 'Cinzel', serif;
                font-size: 16px;
                font-weight: 700;
                color: #1A3644;
                letter-spacing: 1px;
                margin-bottom: 16px;
            }}

            /* Bottom subtle brand footer */
            .footer {{
                margin-top: 18px;
                text-align: center;
                font-family: 'Cinzel', serif;
                font-size: 11px;
                letter-spacing: 3px;
                text-transform: uppercase;
                color: #A39382;
                font-weight: 600;
            }}
        </style>
        </head>
        <body>
            <div class="card-wrapper">
                <div class="inner-border"></div>
                <div class="watermark-emblem">𑁍</div>

                <div class="corner c-tl"></div>
                <div class="corner c-tr"></div>
                <div class="corner c-bl"></div>
                <div class="corner c-br"></div>

                <!-- Kannada Section -->
                <div class="header-kn">{data.get('kannada_header', 'ಒಂದು ಸುಂದರ ವಿಚಾರ')}</div>
                <div class="date-kn">{data.get('kannada_date', '')}</div>
                <div class="quote-container-kn">
                    <div class="quote-kn">“{kn_quote}”</div>
                </div>
                <div class="author-kn">{data.get('kannada_author', '~ ದಾಜಿ')}</div>

                <!-- Center Divider -->
                <div class="divider">
                    <div class="divider-line"></div>
                    <div class="divider-symbol">✦ 𑁍 ✦</div>
                    <div class="divider-line"></div>
                </div>

                <!-- English Section -->
                <div class="header-en">{data.get('english_header', 'One Beautiful Thought')}</div>
                <div class="date-en">{data.get('english_date', '')}</div>
                <div class="quote-container-en">
                    <div class="quote-en">“{en_quote}”</div>
                </div>
                <div class="author-en">{data.get('english_author', '~ Daaji')}</div>

                <div class="footer">Heartfulness</div>
            </div>
        </body>
        </html>
        """

    @classmethod
    def create_card(cls, data, output_filename="daily_thought.png"):
        """Renders an aesthetically balanced card cropped exactly to bounds."""
        html_content = cls._generate_html_template(data)
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 620, "height": 1100})
            page.set_content(html_content)
            page.wait_for_load_state("networkidle")
            time.sleep(0.5)

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
