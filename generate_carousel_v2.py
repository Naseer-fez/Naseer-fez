import urllib.request
import xml.etree.ElementTree as ET
import copy

print("Fetching icons...")
icons = "python,cpp,c,java,mysql,mongodb,js,html,css"
url = f"https://skillicons.dev/icons?i={icons}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
svg_data = urllib.request.urlopen(req).read()

# Register namespaces so the output doesn't get cluttered with ns0: prefixes
ET.register_namespace('', 'http://www.w3.org/2000/svg')
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

root = ET.fromstring(svg_data)
ns = {'svg': 'http://www.w3.org/2000/svg'}

# Find all <g> elements that represent individual icons
# We identify them by checking if they have a transform attribute starting with 'translate'
icon_groups = []
for g in root.findall('./svg:g', ns):
    transform = g.get('transform', '')
    if transform.startswith('translate'):
        icon_groups.append(g)

num_icons = len(icon_groups)

# Duplicate the first 4 icons and update their translate coordinates
duplicates = []
for i in range(4):
    dup = copy.deepcopy(icon_groups[i])
    new_x = (num_icons + i) * 300
    dup.set('transform', f'translate({new_x}, 0)')
    duplicates.append(dup)

# Create a container group for the marquee animation
carousel_g = ET.Element('{http://www.w3.org/2000/svg}g', {'class': 'carousel'})

# Move original icon groups into the carousel container
for g in icon_groups:
    root.remove(g)
    carousel_g.append(g)

# Append duplicated groups to the carousel container
for dup in duplicates:
    carousel_g.append(dup)

# Add the carousel container to the root SVG
root.append(carousel_g)

# Define the CSS animation
total_scroll_distance = num_icons * 300
animation_duration = num_icons * 1.5  # Adjust scroll speed here

style_element = ET.Element('{http://www.w3.org/2000/svg}style')
style_element.text = f"""
    @keyframes scroll {{
      0% {{ transform: translateX(0); }}
      100% {{ transform: translateX(-{total_scroll_distance}px); }}
    }}
    .carousel {{
      animation: scroll {animation_duration}s linear infinite;
    }}
"""
root.insert(0, style_element)

# Set the viewport to exactly 4 items wide (4 * 300 = 1200)
root.set('width', '450')
root.set('height', '96')
root.set('viewBox', '0 0 1200 256')

# Write the fixed SVG
tree = ET.ElementTree(root)
tree.write('carousel-icons.svg', encoding='utf-8', xml_declaration=False)

print("Generated carousel-icons.svg successfully!")
