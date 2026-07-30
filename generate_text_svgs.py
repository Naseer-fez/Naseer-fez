import urllib.request
import urllib.parse
import base64
import re
import os

# Font name and URL
FONT_NAME = "JetBrains Mono"
FONT_WEIGHT = "400;700"
GOOGLE_FONTS_URL = f"https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap"

print("Fetching font CSS...")
req = urllib.request.Request(
    GOOGLE_FONTS_URL, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
)
with urllib.request.urlopen(req) as response:
    css_content = response.read().decode('utf-8')

# Extract woff2 urls
urls = re.findall(r'url\((https://[^)]+\.woff2)\)', css_content)
if not urls:
    print("Could not find WOFF2 URLs")
    exit(1)

print(f"Found {len(urls)} font files. Downloading the first one for 400 and another for 700 if available...")
font_faces = []

# To keep it simple, we will just embed all the @font-face rules we find in the CSS, replacing the URL with base64 data
css_with_base64 = css_content
for url in set(urls):
    print(f"Downloading {url}...")
    with urllib.request.urlopen(url) as response:
        font_data = response.read()
    b64_font = base64.b64encode(font_data).decode('utf-8')
    data_url = f"data:font/woff2;base64,{b64_font}"
    css_with_base64 = css_with_base64.replace(url, data_url)

# Helper to create SVG
def create_svg(filename, title, lines, height=250):
    svg_template = f"""<svg width="800" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      {css_with_base64}
      .card {{
        fill: rgba(255, 255, 255, 0.7);
        stroke: rgba(255, 255, 255, 0.5);
        stroke-width: 2px;
      }}
      .title {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 28px;
        font-weight: 700;
        fill: #2d3748;
      }}
      .text {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 18px;
        font-weight: 400;
        fill: #4a5568;
      }}
      .emoji {{
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', sans-serif;
      }}
      .highlight {{
        fill: #ec4899;
        font-weight: 700;
      }}
    </style>
    <!-- Glassmorphism shadow / blur filter -->
    <filter id="glass">
      <feDropShadow dx="0" dy="10" stdDeviation="15" flood-color="#000000" flood-opacity="0.05" />
    </filter>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#f3f4f6" stop-opacity="0.6"/>
    </linearGradient>
  </defs>

  <!-- Background Card -->
  <rect x="20" y="20" width="760" height="{height-40}" rx="20" fill="url(#bg-grad)" stroke="#ffffff" stroke-width="2" filter="url(#glass)" />
  
  <!-- Content -->
  <text x="60" y="70" class="title">{title}</text>
"""
    y = 120
    for line in lines:
        # Simple hack to colorize first characters if it's a bullet
        if line.startswith("- "):
            line = line[2:]
            svg_template += f'  <circle cx="65" cy="{y-6}" r="4" fill="#ec4899" />\n'
            svg_template += f'  <text x="85" y="{y}" class="text">{line}</text>\n'
        else:
            svg_template += f'  <text x="60" y="{y}" class="text">{line}</text>\n'
        y += 35

    svg_template += "</svg>"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg_template)
    print(f"Generated {filename}")

# Generate specific SVGs
create_svg("svg_intro.svg", "Hi, I'm Naseer", [
    "Welcome to my GitHub profile!",
    "I'm a young tech enthusiast and student, passionate about",
    "understanding the technology I use every day.",
    "My journey is driven by curiosity and a desire",
    "to build solutions for real-world problems."
], height=260)

create_svg("svg_about.svg", "About Me", [
    "- Student, self-learner, and experimenter",
    "- 🛠️ Love building and tinkering with projects",
    "- 💡 Always keen to discover how things work",
    "- 😢 Always Thinking what to Name The Variables"
], height=260)

create_svg("svg_working_on.svg", "What I'm working on", [
    "- Exploring programming fundamentals in Python & C",
    "- Building small projects and automations",
    "- Documenting what I learn along the way"
], height=220)

create_svg("svg_goals.svg", "Goals", [
    "- Deepen my understanding of computers and software",
    "- Solve practical problems with code",
    "- Connect and collaborate with fellow learners"
], height=220)

create_svg("svg_connect.svg", "Connect with me", [
    "- GitHub: Naseer-fez (You are here!)",
    "- Let's build something awesome together 🚀"
], height=180)

print("Done!")
