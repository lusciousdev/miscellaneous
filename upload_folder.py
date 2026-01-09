import sys
import os
sys.path.append(os.path.abspath(__file__))

import mediacms
import json
from pathlib import Path
import glob

cred_json = {}
with open(Path(os.path.abspath(__file__)).parent / "secrets.json", 'r') as cred_file:
    cred_json = json.load(cred_file)

api = mediacms.ArchiveAPI("http://10.0.1.7:8004/", (cred_json["USERNAME"], cred_json["PASSWORD"]))

folder_path = Path(".")
mp4_files = sorted(glob.glob((str)(folder_path / "*.mp4")), reverse=True)

for file_path in mp4_files:
    video_file = Path(file_path)
    desc_file = video_file.with_suffix(".txt")

    video_name = video_file.stem

    search_result = api.search(video_name)

    if int(search_result["count"]) > 0:
        print(f"skipping {video_name}")
        continue

    with open(desc_file, 'r', encoding="utf-8") as desc:
        print(f"uploading {video_name}")
        api.upload(file_path, video_file.stem, desc.read().rstrip())
