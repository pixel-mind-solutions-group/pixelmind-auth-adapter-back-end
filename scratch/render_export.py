import subprocess
import os

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
svg_file = r"c:\My Working Directory\P-DEV\GitHub\Server\User Management\v2\pixelmind-auth-adapter-backend\brand_assets\svg\01-primary-horizontal.svg"
out_png = r"c:\My Working Directory\P-DEV\GitHub\Server\User Management\v2\pixelmind-auth-adapter-backend\brand_assets\test_render.png"

uri = "file:///" + svg_file.replace("\\", "/")
cmd = [
    chrome,
    "--headless=new",
    "--disable-gpu",
    "--force-device-scale-factor=2",
    "--window-size=1600,600",
    f"--screenshot={out_png}",
    uri
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Exit code:", res.returncode)
print("Exists:", os.path.exists(out_png))
if os.path.exists(out_png):
    print("Size:", os.path.getsize(out_png))
