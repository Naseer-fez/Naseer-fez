import urllib.request
import re

# The icons you requested
icons = "python,cpp,c,java,mysql,mongodb,js,html,css"
url = f"https://skillicons.dev/icons?i={icons}"

print(f"Fetching icons from {url}...")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
svg_data = urllib.request.urlopen(req).read().decode('utf-8')

# Extract all <g> tags containing the icons
matches = list(re.finditer(r'<g transform="translate\((\d+), 0\)">.*?</g>', svg_data, flags=re.DOTALL))
g_blocks = [m.group(0) for m in matches]
num_icons = len(g_blocks)

# We want 4 icons visible at a time. To make the marquee seamless, 
# we duplicate the first 4 icons and place them at the end.
duplicates = []
for i in range(4):
    original_g = g_blocks[i]
    new_x = (num_icons + i) * 300
    new_g = re.sub(r'transform="translate\(\d+, 0\)"', f'transform="translate({new_x}, 0)"', original_g)
    duplicates.append(new_g)

all_g_blocks = g_blocks + duplicates

# Extract the <defs> block (which contains gradients/styles needed by the icons)
defs_match = re.search(r'<defs>.*?</defs>', svg_data, flags=re.DOTALL)
defs_block = defs_match.group(0) if defs_match else ""

# Calculate animation parameters
total_scroll_distance = num_icons * 300
animation_duration = num_icons * 1.5  # Adjust speed here

style_block = f"""
  <style>
    @keyframes scroll {{
      0% {{ transform: translateX(0); }}
      100% {{ transform: translateX(-{total_scroll_distance}px); }}
    }}
    .carousel {{
      animation: scroll {animation_duration}s linear infinite;
    }}
  </style>
"""

# Construct the final SVG. 
# viewBox width 1200 = exactly 4 icons (4 * 300).
# height 48, width 225 to maintain the 1200:256 aspect ratio.
final_svg = f"""<svg width="450" height="96" viewBox="0 0 1200 256" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
{style_block}
{defs_block}
<g class="carousel">
  {''.join(all_g_blocks)}
</g>
</svg>"""

output_file = "carousel-icons.svg"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(final_svg)

print(f"Success! Saved carousel animated icons to {output_file}")
