"""
Script to render an animated terminal GIF for privacylens showing the complete end-to-end workflow:
1. Installation: pip install privacyaudit
2. Execution: privacylens audit credit_risk_model.pkl train_data.csv test_data.csv --report compliance.html
3. Audit output table & compliance report generation.
"""

from PIL import Image, ImageDraw, ImageFont

def render_installation_audit_gif(output_gif_path="demo.gif"):
    # Dark theme colors (Catppuccin Mocha)
    BG_COLOR = (30, 30, 46)        # #1E1E2E
    HEADER_BG = (24, 24, 37)       # #181825
    TEXT_COLOR = (205, 214, 244)   # #CDD6F4
    GREEN = (166, 227, 161)        # #A6E3A1
    CYAN = (137, 220, 235)         # #89DCEB
    YELLOW = (249, 226, 175)       # #F9E2AF
    RED = (243, 139, 168)          # #F38BA8
    MUTED = (108, 112, 134)        # #6C7086

    WIDTH = 940
    HEIGHT = 580
    FONT_SIZE = 14

    try:
        font = ImageFont.truetype("consola.ttf", FONT_SIZE)
        font_bold = ImageFont.truetype("consolab.ttf", FONT_SIZE)
    except IOError:
        font = ImageFont.load_default()
        font_bold = font

    # Full End-to-End Installation + Audit script
    lines_script = [
        ("> pip install privacyaudit", CYAN, True),
        ("Downloading privacyaudit-1.1.0-py3-none-any.whl (48 kB)", MUTED, False),
        ("Successfully installed privacyaudit-1.1.0 rich-13.7.0 scikit-learn-1.4.0", GREEN, False),
        ("", TEXT_COLOR, False),
        ("> privacylens audit credit_risk_model.pkl train_data.csv test_data.csv --report compliance.html", CYAN, True),
        ("Loading model: credit_risk_model.pkl (RandomForestClassifier)...", YELLOW, False),
        ("Loading datasets: train_data.csv (10,000 samples) | test_data.csv (3,000 samples)...", MUTED, False),
        ("Auditing model across all 5 privacy vulnerability vectors...", MUTED, False),
        ("", TEXT_COLOR, False),
        ("            privacylens 5-Point Privacy Audit Report            ", CYAN, True),
        ("+----------------------------------------------------------------+", MUTED, False),
        ("| Check                              |    Score     |    Risk    |", TEXT_COLOR, True),
        ("|------------------------------------+--------------+------------|", MUTED, False),
        ("| Membership Inference Attack        |    0.250     |   MEDIUM   |", YELLOW, False),
        ("|------------------------------------+--------------+------------|", MUTED, False),
        ("| PII Leakage Detection              |    1.000     |    HIGH    |", RED, True),
        ("|------------------------------------+--------------+------------|", MUTED, False),
        ("| Model Inversion Risk               |    0.799     |    HIGH    |", RED, True),
        ("|------------------------------------+--------------+------------|", MUTED, False),
        ("| Attribute Inference Risk           |    0.000     |    LOW     |", GREEN, False),
        ("|------------------------------------+--------------+------------|", MUTED, False),
        ("| Differential Privacy (Epsilon)     |    1.000     |    HIGH    |", RED, True),
        ("+----------------------------------------------------------------+", MUTED, False),
        ("+------------------------------- Audit Summary -------------------------------+", MUTED, False),
        ("| Model: credit_risk_model.pkl (RandomForestClassifier)                        |", TEXT_COLOR, False),
        ("| Overall Risk: HIGH RISK — Model memorisation detected                       |", RED, True),
        ("+-----------------------------------------------------------------------------+", MUTED, False),
        ("", TEXT_COLOR, False),
        ("Interactive Compliance Report exported to: compliance.html", GREEN, True),
        ("Audit complete: 3 critical privacy vulnerabilities flagged.", RED, True)
    ]

    frames = []

    # Progressive reveal frame generation
    for step in range(1, len(lines_script) + 1):
        img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
        draw = ImageDraw.Draw(img)

        # Draw Window Bar (Mac/Linux window controls style)
        draw.rectangle([0, 0, WIDTH, 36], fill=HEADER_BG)
        draw.ellipse([15, 12, 27, 24], fill=(255, 95, 86))   # Red dot
        draw.ellipse([35, 12, 47, 24], fill=(255, 189, 46))  # Yellow dot
        draw.ellipse([55, 12, 67, 24], fill=(39, 201, 63))   # Green dot

        # Draw Window Title
        draw.text((WIDTH // 2 - 120, 10), "zsh — pip install & privacylens audit", font=font, fill=MUTED)

        # Draw terminal lines
        y = 50
        for i in range(step):
            text, color, is_bold = lines_script[i]
            f = font_bold if is_bold else font
            draw.text((20, y), text, font=f, fill=color)
            y += 16

        frames.append(img)

    # Add hold frames at the end
    last_frame = frames[-1]
    for _ in range(18):
        frames.append(last_frame)

    # Save animated GIF
    frames[0].save(
        output_gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=220,
        loop=0
    )
    print(f"Installation + Audit GIF successfully generated: {output_gif_path}")

if __name__ == "__main__":
    render_installation_audit_gif()
