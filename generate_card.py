import os
import time
from playwright.sync_api import sync_playwright


class HeartfulnessCardGenerator:
    """
    Renders high-contrast, elder-friendly bilingual thought cards
    with natural left alignment, robust cross-platform symbols, and centered titles.
    """

    @classmethod
    def _generate_html_template(cls, data):
        kn_quote = data.get("kannada_quote", "").strip().strip("“\"").strip("”\"").strip()
        en_quote = data.get("english_quote", "").strip().strip("“\"").strip("”\"").strip()

        # Dynamic size scaling prioritizing legibility for elders
        max_len = max(len(kn_quote), len(en_quote))
        if max_len < 120:
            kn_fs = "25px"
            en_fs = "24px"
            lh = "1.8"
        elif max_len < 220:
            kn_fs = "23px"
            en_fs = "22px"
            lh = "1.7"
        else:
            kn_fs = "21px"
            en_fs = "20px"
            lh = "1.6"

        return f"""
        <!DOCTYPE html>
        <html lang="kn">
        <head>
        <meta charset="UTF-8">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Noto+Serif+Kannada:wght@500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700&display=swap" rel="stylesheet">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}

            body {{
                width: 630px;
                min-height: 1080px;
                background-color: #EDE8DF;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 30px 20px;
                font-family: 'Noto Serif Kannada', 'Plus Jakarta Sans', sans-serif;
                -webkit-font-smoothing: antialiased;
            }}

            /* Main Card Frame */
            .card-wrapper {{
                width: 574px;
                background: radial-gradient(circle at 50% 25%, #FCFBF9 0%, #F5F0E6 100%);
                border: 1.5px solid #D5C7B5;
                position: relative;
                padding: 40px 36px 30px;
                box-shadow: 0 10px 25px rgba(60, 45, 30, 0.08);
            }}

            /* Inset Decorative Hairline */
            .inner-border {{
                position: absolute;
                top: 8px; left: 8px; right: 8px; bottom: 8px;
                border: 1px solid rgba(184, 158, 126, 0.45);
                pointer-events: none;
            }}

            /* Corner Ornaments */
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

            /* Centered Title Areas */
            .title-area {{
                text-align: center;
                margin-bottom: 22px;
            }}

            /* Kannada Typography */
            .header-kn {{
                font-family: 'Noto Serif Kannada', serif;
                font-size: 24px;
                font-weight: 700;
                color: #6E261B;
                letter-spacing: 0.5px;
                margin-bottom: 6px;
            }}
            .date-kn {{
                font-family: 'Noto Serif Kannada', serif;
                font-size: 16px;
                font-weight: 600;
                color: #7D5C4E;
            }}
            .quote-container-kn {{
                position: relative;
                padding-left: 20px;
                border-left: 3.5px solid #C48E7C;
                margin-bottom: 12px;
            }}
            .quote-kn {{
                font-family: 'Noto Serif Kannada', serif;
                font-size: {kn_fs};
                line-height: {lh};
                font-weight: 600;
                color: #2D1A16;
                text-align: left;
            }}
            .author-kn {{
                text-align: right;
                font-family: 'Noto Serif Kannada', serif;
                font-size: 19px;
                font-weight: 700;
                color: #6E261B;
                margin-bottom: 24px;
            }}

            /* Universal Center Divider (Standard Unicode Glyphs) */
            .divider {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 16px;
                margin: 4px 0 28px;
            }}
            .divider-line {{
                height: 1px;
                background: linear-gradient(90deg, transparent, #CEBFA8, transparent);
                flex-grow: 1;
            }}
            .divider-symbol {{
                color: #9E7D63;
                font-size: 11px;
                letter-spacing: 6px;
            }}

            /* English Typography */
            .header-en {{
                font-family: 'Cinzel', serif;
                font-size: 19px;
                font-weight: 700;
                color: #1A3644;
                letter-spacing: 2px;
                text-transform: uppercase;
                margin-bottom: 6px;
            }}
            .date-en {{
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 14px;
                font-weight: 600;
                color: #5C707A;
            }}
            .quote-container-en {{
                position: relative;
                padding-left: 20px;
                border-left: 3.5px solid #6C8E9C;
                margin-bottom: 12px;
            }}
            .quote-en {{
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: {en_fs};
                line-height: {lh};
                font-weight: 600;
                color: #172429;
                text-align: left;
                letter-spacing: 0.1px;
            }}
            .author-en {{
                text-align: right;
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 18px;
                font-weight: 700;
                color: #1A3644;
                margin-bottom: 16px;
            }}

            /* Footer */
            .footer {{
                margin-top: 18px;
                text-align: center;
                font-family: 'Cinzel', serif;
                font-size: 12px;
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

                <div class="corner c-tl"></div>
                <div class="corner c-tr"></div>
                <div class="corner c-bl"></div>
                <div class="corner c-br"></div>

                <!-- Kannada Section -->
                <div class="title-area">
                    <div class="header-kn">{data.get('kannada_header', 'ಒಂದು ಸುಂದರ ವಿಚಾರ')}</div>
                    <div class="date-kn">{data.get('kannada_date', '')}</div>
                </div>
                <div class="quote-container-kn">
                    <div class="quote-kn">“{kn_quote}”</div>
                </div>
                <div class="author-kn">{data.get('kannada_author', '~ ದಾಜಿ')}</div>

                <!-- Center Divider with Standard Shapes -->
                <div class="divider">
                    <div class="divider-line"></div>
                    <div class="divider-symbol">✦ ❖ ✦</div>
                    <div class="divider-line"></div>
                </div>

                <!-- English Section -->
                <div class="title-area">
                    <div class="header-en">{data.get('english_header', 'One Beautiful Thought')}</div>
                    <div class="date-en">{data.get('english_date', '')}</div>
                </div>
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
            page = browser.new_page(viewport={"width": 630, "height": 1100})
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
