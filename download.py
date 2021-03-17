import requests

url = "https://firmware-dot-specknet-pyramid-test.ew.r.appspot.com/get_update_firmware"
file_name = "app_update.zip"

import urllib.request
import shutil
...
# Download the file from `url` and save it locally under `file_name`:
with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
    shutil.copyfileobj(response, out_file)
