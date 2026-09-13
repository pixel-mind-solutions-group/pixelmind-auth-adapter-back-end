import os
import subprocess
import zipfile
import shutil
import time

BASE_DIR = r"c:\My Working Directory\P-DEV\GitHub\Server\User Management\v2\pixelmind-auth-adapter-backend"
BRAND_DIR = os.path.join(BASE_DIR, "brand_assets")
SVG_DIR = os.path.join(BRAND_DIR, "svg")
MOCKUP_DIR = os.path.join(BRAND_DIR, "mockups")
SCRATCH_DIR = os.path.join(BASE_DIR, "scratch")
PACKAGE_DIR = os.path.join(SCRATCH_DIR, "meskOra_Brand_Package_HQ")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

if os.path.exists(PACKAGE_DIR):
    shutil.rmtree(PACKAGE_DIR)
os.makedirs(PACKAGE_DIR, exist_ok=True)

png_dir = os.path.join(PACKAGE_DIR, "01_High_Resolution_PNGs")
svg_dir = os.path.join(PACKAGE_DIR, "02_Vector_SVGs")
mockups_dir = os.path.join(PACKAGE_DIR, "03_Photorealistic_Mockups")
guidelines_dir = os.path.join(PACKAGE_DIR, "04_Guidelines_&_Interactive_Viewer")

os.makedirs(png_dir, exist_ok=True)
os.makedirs(svg_dir, exist_ok=True)
os.makedirs(mockups_dir, exist_ok=True)
os.makedirs(guidelines_dir, exist_ok=True)

# 1. Copy Vector SVGs
print("Copying Vector SVGs...")
for f in os.listdir(SVG_DIR):
    if f.endswith(".svg"):
        shutil.copy2(os.path.join(SVG_DIR, f), os.path.join(svg_dir, f))

# 2. Copy Mockups
print("Copying Mockup Images...")
mockup_renames = {
    "meskora_office_signage_1789055062241.jpg": "meskOra_3D_Architectural_Office_Signage_HQ.jpg",
    "meskora_stationery_1789055147687.jpg": "meskOra_Corporate_Stationery_&_App_HQ.jpg"
}
for f in os.listdir(MOCKUP_DIR):
    if f in mockup_renames:
        shutil.copy2(os.path.join(MOCKUP_DIR, f), os.path.join(mockups_dir, mockup_renames[f]))
    elif f.endswith((".jpg", ".png")):
        shutil.copy2(os.path.join(MOCKUP_DIR, f), os.path.join(mockups_dir, f))

# 3. Copy Interactive Viewer & SVGs for local viewing inside the zip
print("Copying Viewer...")
shutil.copy2(os.path.join(BRAND_DIR, "index.html"), os.path.join(guidelines_dir, "Brand_Showcase_Interactive.html"))
viewer_svg_dir = os.path.join(guidelines_dir, "svg")
os.makedirs(viewer_svg_dir, exist_ok=True)
for f in os.listdir(SVG_DIR):
    if f.endswith(".svg"):
        shutil.copy2(os.path.join(SVG_DIR, f), os.path.join(viewer_svg_dir, f))
viewer_mockups_dir = os.path.join(guidelines_dir, "mockups")
os.makedirs(viewer_mockups_dir, exist_ok=True)
for f in os.listdir(MOCKUP_DIR):
    if f.endswith((".jpg", ".png")):
        shutil.copy2(os.path.join(MOCKUP_DIR, f), os.path.join(viewer_mockups_dir, f))

# 4. Generate High-Resolution PNGs via Chrome Headless
html_temp_dir = os.path.join(SCRATCH_DIR, "html_temp")
os.makedirs(html_temp_dir, exist_ok=True)

render_tasks = [
    # Champion Variations
    ("01-primary-horizontal.svg", "01_meskOra_Primary_Horizontal_Dark.png", 2400, 700, "#0A192F", "90%"),
    ("01-primary-horizontal.svg", "01_meskOra_Primary_Horizontal_Light.png", 2400, 700, "#FFFFFF", "90%"),
    ("01-primary-horizontal.svg", "01_meskOra_Primary_Horizontal_Transparent.png", 2400, 700, "transparent", "90%"),
    ("02-compact-horizontal.svg", "02_meskOra_Compact_Horizontal_Dark.png", 2000, 550, "#0A192F", "90%"),
    ("02-compact-horizontal.svg", "02_meskOra_Compact_Horizontal_Light.png", 2000, 550, "#FFFFFF", "90%"),
    ("03-stacked-vertical.svg", "03_meskOra_Stacked_Vertical_Dark.png", 1600, 1600, "#0A192F", "85%"),
    ("03-stacked-vertical.svg", "03_meskOra_Stacked_Vertical_Light.png", 1600, 1600, "#FFFFFF", "85%"),
    ("04-icon-only.svg", "04_meskOra_Icon_Only_Dark.png", 1200, 1200, "#0A192F", "80%"),
    ("04-icon-only.svg", "04_meskOra_Icon_Only_Transparent.png", 1200, 1200, "transparent", "80%"),
    ("05-wordmark-isolated.svg", "05_meskOra_Wordmark_Isolated_Dark.png", 2200, 600, "#0A192F", "90%"),
    ("05-wordmark-isolated.svg", "05_meskOra_Wordmark_Isolated_Light.png", 2200, 600, "#FFFFFF", "90%"),
    ("06-monochrome-black.svg", "06_meskOra_Monochrome_Black_WhiteBG.png", 2400, 700, "#FFFFFF", "90%"),
    ("06-monochrome-black.svg", "06_meskOra_Monochrome_Black_Transparent.png", 2400, 700, "transparent", "90%"),
    ("07-dark-background.svg", "07_meskOra_Dark_OLED_Edition.png", 2400, 700, "#0A192F", "100%"),
    ("08-light-background.svg", "08_meskOra_Light_Corporate_Paper.png", 2400, 700, "#FFFFFF", "100%"),
    ("09-favicon-app-icon.svg", "09_meskOra_App_Icon_1024x1024.png", 1024, 1024, "#0A192F", "100%"),
    ("10-social-media-avatar.svg", "10_meskOra_Social_Media_Avatar_1200x1200.png", 1200, 1200, "#0A192F", "100%"),

    # All 7 Distinct Concepts Previews
    ("concept-1-mobius-nexus.svg", "Concept_01_Mobius_Nexus_Flagship.png", 1200, 1200, "#070B14", "75%"),
    ("concept-2-quantum-node.svg", "Concept_02_Quantum_Node.png", 1200, 1200, "#070B14", "75%"),
    ("concept-3-dynamic-apex.svg", "Concept_03_Dynamic_Apex.png", 1200, 1200, "#070B14", "75%"),
    ("concept-4-neural-nexus.svg", "Concept_04_Neural_Nexus.png", 1200, 1200, "#070B14", "75%"),
    ("concept-5-prism-core.svg", "Concept_05_Prism_Core.png", 1200, 1200, "#070B14", "75%"),
    ("concept-6-modernist-monogram.svg", "Concept_06_Modernist_Monogram.png", 1200, 1200, "#070B14", "75%"),
    ("concept-7-catalyst-pulse.svg", "Concept_07_Catalyst_Pulse.png", 1200, 1200, "#070B14", "75%"),
]

print(f"Rendering {len(render_tasks)} high-resolution PNG assets...")

for svg_name, png_name, w, h, bg, svg_size in render_tasks:
    svg_path = os.path.join(SVG_DIR, svg_name)
    if not os.path.exists(svg_path):
        print(f"Warning: {svg_path} not found")
        continue

    with open(svg_path, "r", encoding="utf-8") as sf:
        svg_content = sf.read()

    # Wrap in clean standalone HTML
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{
    width: {w}px;
    height: {h}px;
    background-color: {bg};
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
  }}
  .svg-container {{
    width: {svg_size};
    height: {svg_size};
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  svg {{
    width: 100%;
    height: 100%;
    display: block;
  }}
</style>
</head>
<body>
<div class="svg-container">
{svg_content}
</div>
</body>
</html>
"""
    temp_html_path = os.path.join(html_temp_dir, f"temp_{png_name}.html")
    with open(temp_html_path, "w", encoding="utf-8") as hf:
        hf.write(html_content)

    output_png_path = os.path.join(png_dir, png_name)
    uri = "file:///" + temp_html_path.replace("\\", "/")

    extra_flags = []
    if bg == "transparent":
        extra_flags = ["--default-background-color=00000000"]

    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--run-all-compositor-stages-before-draw",
        f"--window-size={w},{h}",
        *extra_flags,
        f"--screenshot={output_png_path}",
        uri
    ]

    subprocess.run(cmd, capture_output=True)
    if os.path.exists(output_png_path):
        size_kb = os.path.getsize(output_png_path) // 1024
        print(f" [OK] {png_name} ({w}x{h}, {size_kb} KB)")
    else:
        print(f" [FAILED] {png_name}")

# 5. Create Brand Identity Readme & Color Codes
readme_content = """================================================================================
meskOra Technologies (Pvt) Ltd
OFFICIAL CORPORATE BRAND IDENTITY & DESIGN SYSTEM (HQ ASSETS)
================================================================================

Brand Essence:
  "Innovating. Solving. Transforming through Technology."

Typographic Capitalization Rule:
  "meskOra"
  - Strictly formatted as: lowercase 'm', 'esk', capital 'O', lowercase 'ra'.
  - Supporting line: "Technologies (Pvt) Ltd" (Medium weight, tracked letter-spacing).

--------------------------------------------------------------------------------
CORPORATE COLOR PALETTE SPECIFICATIONS
--------------------------------------------------------------------------------
1. Obsidian Navy (Primary Dark Foundation & Canvas)
   - HEX:    #0A192F
   - RGB:    10, 25, 47
   - CMYK:   88, 77, 45, 60
   - Pantone: PMS 2965 C

2. Modern Cobalt Blue (Brand Core & Accent Focal 'O')
   - HEX:    #2563EB
   - RGB:    37, 99, 235
   - CMYK:   84, 60, 0, 0
   - Pantone: PMS 2174 C

3. Electric Cyan (Catalyst Node & Active Innovation State)
   - HEX:    #00D2D3
   - RGB:    0, 210, 211
   - CMYK:   68, 0, 26, 0
   - Pantone: PMS 319 C

4. Corporate Slate (Subtitle & Metadata)
   - HEX:    #64748B
   - RGB:    100, 116, 139
   - CMYK:   58, 42, 30, 8
   - Pantone: PMS 430 C

5. Crisp White (Light Paper Canvas & High Contrast Reversed)
   - HEX:    #FFFFFF
   - RGB:    255, 255, 255
   - CMYK:   0, 0, 0, 0

--------------------------------------------------------------------------------
DIRECTORY STRUCTURE & CONTENTS
--------------------------------------------------------------------------------
├── 01_High_Resolution_PNGs/
│   ├── Primary horizontal logos (Dark, Light, Transparent backgrounds)
│   ├── Compact horizontal logos (for SaaS & Mobile headers)
│   ├── Stacked vertical logos (for Merchandise & Banners)
│   ├── Icon-only marks (Transparent & Dark)
│   ├── Isolated wordmarks
│   ├── Monochrome solid black versions
│   ├── Dark OLED & Light Corporate Paper editions
│   ├── App Store / Play Store 1024x1024 Retina App Icon
│   ├── Social media profile avatar (1200x1200px 1:1)
│   └── High-resolution previews for all 7 distinct logo concepts
│
├── 02_Vector_SVGs/
│   ├── Production vector SVG files for all 10 deliverables
│   └── Production vector SVG files for all 7 distinct concepts
│
├── 03_Photorealistic_Mockups/
│   ├── meskOra_3D_Architectural_Office_Signage_HQ.jpg
│   └── meskOra_Corporate_Stationery_&_App_HQ.jpg
│
└── 04_Guidelines_&_Interactive_Viewer/
    ├── Brand_Showcase_Interactive.html (Open in any web browser)
    ├── svg/ (vector dependencies for viewer)
    └── mockups/ (mockup dependencies for viewer)

================================================================================
(C) 2026 meskOra Technologies (Pvt) Ltd. All rights reserved.
================================================================================
"""

readme_path = os.path.join(PACKAGE_DIR, "README_Brand_Identity.txt")
with open(readme_path, "w", encoding="utf-8") as rf:
    rf.write(readme_content)

# 6. Create the final ZIP archive
zip_filename = "meskOra_Technologies_Brand_Identity_HQ.zip"
zip_path_workspace = os.path.join(BASE_DIR, zip_filename)
zip_path_artifacts = os.path.join(r"C:\Users\User\.gemini\antigravity\brain\ec5f526b-96d4-45fa-805e-332a37e7c413", zip_filename)

print(f"\nCompressing into {zip_filename}...")
with zipfile.ZipFile(zip_path_workspace, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(PACKAGE_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, PACKAGE_DIR)
            zipf.write(full_path, arcname=os.path.join("meskOra_Brand_Identity", rel_path))

shutil.copy2(zip_path_workspace, zip_path_artifacts)

zip_size_mb = os.path.getsize(zip_path_workspace) / (1024 * 1024)
print(f"\n[SUCCESS] Created ZIP archive: {zip_path_workspace}")
print(f"Size: {zip_size_mb:.2f} MB")
print(f"Copied to artifact directory: {zip_path_artifacts}")
