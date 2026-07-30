import urllib.request
import re

# The icons you requested
icons = "python,cpp,c,java,mysql,mongodb,js,html,css"
url = f"https://skillicons.dev/icons?i={icons}"

print(f"Fetching icons from {url}...")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
svg_data = urllib.request.urlopen(req).read().decode('utf-8')

# We need to increase the viewBox and height of the SVG so the icons don't clip when they jump up
vb_match = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg_data)
w, h = int(vb_match.group(1)), int(vb_match.group(2))
height_match = re.search(r'height="([\d\.]+)"', svg_data)
svg_height = float(height_match.group(1))

jump_amount = 40 # The amount the icons will jump up

# Adjust viewBox to allow space at the top
new_vb = f'viewBox="0 -{jump_amount} {w} {h + jump_amount}"'
svg_data = re.sub(r'viewBox="0 0 \d+ \d+"', new_vb, svg_data)

# Adjust height attribute proportionately
new_height = svg_height * ((h + jump_amount) / h)
svg_data = re.sub(r'height="[\d\.]+"', f'height="{new_height:.2f}"', svg_data)

# Create the CSS animation and stagger the delays
num_icons = len(icons.split(','))
delays = "\n  ".join([f"g:nth-child({i+1}) {{ animation-delay: {i * 0.1:.1f}s; }}" for i in range(num_icons)])

style_block = f"""
<style>
  @keyframes wave {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-{jump_amount}px); }}
  }}
  g {{
    animation: wave 1.5s ease-in-out infinite;
  }}
  {delays}
</style>
"""

# Inject the CSS block right after the opening <svg> tag
insert_pos = svg_data.find('>') + 1
animated_svg = svg_data[:insert_pos] + style_block + svg_data[insert_pos:]

# Save the final animated SVG
output_file = "wave-icons.svg"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(animated_svg)

print(f"Success! Saved animated icons to {output_file}")
