import os
import time
from playwright.sync_api import sync_playwright


class HeartfulnessCardGenerator:
    """
    Renders dynamic, high-aesthetic 9:16 WhatsApp Status thought cards
    with balanced bilingual color separation and content-aware scaling.
    """

    @staticmethod
    def _compute_font_sizes(text_len):
        """Dynamically scales font sizes based on quote length."""
        if text_len < 120:
            return {"quote_fs": "31px", "lh": "1.75", "head_fs": "32px", "author_fs": "25px"}
        elif text_len < 220:
            return {"quote_fs": "27px", "lh": "1.65", "head_fs": "30px", "author_fs": "23px"}
        else:
            return {"quote_fs": "23px", "lh": "1.55", "head_fs": "28px", "author_fs": "21px"}

    @classmethod
    def _generate_html_template(cls, data):
        kn_quote = data.get("kannada_quote", "").strip().strip("“\"").strip("”\"").strip()
        en_quote = data.get("english_quote", "").strip().strip("“\"").strip("”\"").strip()

        # Compute balanced font size according to the longer passage
        max_len = max(len(kn_quote), len(en_quote))
        sizes = cls._compute_font_sizes(max_len)

        return f"""
        <!DOCTYPE html>
        <html lang="kn">
        <head>
        <meta charset="UTF-8">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Noto+Sans+Kannada:wght@400;600;700&family=Noto+Serif+Kannada:wght@500;700&family=Plus+Jakarta+Sans:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}

            /* Standard 9:16 WhatsApp Status Canvas */
            body {{
                width: 1080px;
                height: 1920px;
                background: linear-gradient(180deg, #FBF8F3 0%, #F5EFE6 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 60px 48px;
                font-family: 'Noto Sans Kannada', 'Plus Jakarta Sans', sans-serif;
                -webkit-font-smoothing: antialiased;
            }}

            .frame {{
                width: 100%;
                height: 100%;
                border: 2px solid #D8C8B8;
                position: relative;
                padding: 80px 64px 60px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                background-color: rgba(255, 255, 255, 0.55);
                box-shadow: inset 0 0 80px rgba(216, 200, 184, 0.25);
            }}

            /* Corner Ornaments */
            .corner {{
                position: absolute;
                width: 24px;
                height: 24px;
                border-color: #A47864;
                border-style: solid;
            }}
            .c-tl {{ top: 10px; left: 10px; border-width: 3px 0 0 3px; }}
            .c-tr {{ top: 10px; right: 10px; border-width: 3px 3px 0 0; }}
            .c-bl {{ bottom: 10px; left: 10px; border-width: 0 0 3px 3px; }}
            .c-br {{ bottom: 10px; right: 10px; border-width: 0 3px 3px 0; }}

            /* Inner decorative inset ring */
            .frame::after {{
                content: '';
                position: absolute;
                top: 14px; left: 14px; right: 14px; bottom: 14px;
                border: 1px solid rgba(164, 120, 100, 0.35);
                pointer-events: none;
            }}

            .content-stack {{
                display: flex;
                flex-direction: column;
                flex-grow: 1;
                justify-content: space-evenly;
            }}

            /* Section 1: Kannada (Terracotta / Crimson Theme) */
            .section-kn {{
                color: #2F1E19;
            }}
            .header-kn {{
                color: #8C2D19;
                font-family: 'Noto Serif Kannada', serif;
                font-size: {sizes['head_fs']};
                font-weight: 700;
                letter-spacing: 0.5px;
                margin-bottom: 8px;
            }}
            .date-kn {{
                font-size: 21px;
                font-weight: 600;
                color: #7A5C50;
                margin-bottom: 24px;
            }}
            .quote-box-kn {{
                position: relative;
                padding-left: 28px;
                border-left: 4px solid #C4826F;
            }}
            .quote-kn {{
                font-size: {sizes['quote_fs']};
                line-height: {sizes['lh']};
                font-weight: 500;
                color: #261612;
                text-align: justify;
                text-justify: inter-word;
            }}
            .author-kn {{
                font-size: {sizes['author_fs']};
                font-weight: 700;
                color: #8C2D19;
                margin-top: 20px;
                text-align: right;
            }}

            /* Divider */
            .divider {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 20px;
                margin: 20px 0;
            }}
            .divider-line {{
                height: 1px;
                background: linear-gradient(90deg, transparent, #C8B8A6, transparent);
                flex-grow: 1;
            }}
            .divider-emblem {{
                color: #9C7A60;
                font-size: 16px;
                letter-spacing: 3px;
            }}

            /* Section 2: English (Deep Teal / Slate Theme) */
            .section-en {{
                color: #1A282C;
            }}
            .header-en {{
                color: #1F4E5B;
                font-family: 'Cinzel', serif;
                font-size: {sizes['head_fs']};
                font-weight: 700;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                margin-bottom: 8px;
            }}
            .date-en {{
                font-size: 20px;
                font-weight: 600;
                color: #556E75;
                font-family: 'Plus Jakarta Sans', sans-serif;
                margin-bottom: 24px;
            }}
            .quote-box-en {{
                position: relative;
                padding-left: 28px;
                border-left: 4px solid #5C8996;
            }}
            .quote-en {{
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: {sizes['quote_fs']};
                line-height: {sizes['lh']};
                font-weight: 400;
                color: #172428;
                font-style: italic;
                text-align: justify;
                text-justify: inter-word;
            }}
            .author-en {{
                font-family: 'Cinzel', serif;
                font-size: {sizes['author_fs']};
                font-weight: 700;
                color: #1F4E5B;
                margin-top: 20px;
                text-align: right;
                letter-spacing: 1px;
            }}

            /* Footer */
            .footer {{
                text-align: center;
                padding-top: 15px;
                font-size: 17px;
                letter-spacing: 2px;
                text-transform: uppercase;
                color: #8C7C70;
                font-weight: 600;
            }}
        </style>
        </head>
        <body>
            <div class="frame">
                <div class="corner c-tl"></div>
                <div class="corner c-tr"></div>
                <div class="corner c-bl"></div>
                <div class="corner c-br"></div>

                <div class="content-stack">
                    <!-- Kannada Section -->
                    <div class="section-kn">
                        <div class="header-kn">{data.get('kannada_header', 'ಒಂದು ಸುಂದರ ವಿಚಾರ')}</div>
                        <div class="date-kn">{data.get('kannada_date', '')}</div>
                        <div class="quote-box-kn">
                            <div class="quote-kn">“ {kn_quote} ”</div>
                        </div>
                        <div class="author-kn">{data.get('kannada_author', '~ ದಾಜಿ')}</div>
                    </div>

                    <!-- Divider -->
                    <div class="divider">
                        <div class="divider-line"></div>
                        <div class="divider-emblem">✦ 𑁍 ✦</div>
                        <div class="divider-line"></div>
                    </div>

                    <!-- English Section -->
                    <div class="section-en">
                        <div class="header-en">{data.get('english_header', 'One Beautiful Thought')}</div>
                        <div class="date-en">{data.get('english_date', '')}</div>
                        <div class="quote-box-en">
                            <div class="quote-en">“ {en_quote} ”</div>
                        </div>
                        <div class="author-en">{data.get('english_author', '~ Daaji')}</div>
                    </div>
                </div>

                <div class="footer">Heartfulness</div>
            </div>
        </body>
        </html>
        """

    @classmethod
    def create_card(cls, data, output_filename="daily_thought.png"):
        """Renders 1080x1920 px vertical WhatsApp status card."""
        html_content = cls._generate_html_template(data)
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1080, "height": 1920})
            page.set_content(html_content)
            page.wait_for_load_state("networkidle")
            time.sleep(0.6)  # Ensure web fonts finish rasterizing
            page.screenshot(path=output_filename, full_page=False, omit_background=False)
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
