from datetime import datetime

import requests


class ArchiveAPI:
    base_url = ""
    auth = None

    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth

        self.login()

    def login(self):
        login_url = f"{self.base_url}/api/v1/login"

        resp = requests.post(
            url=login_url,
            data={"username": self.auth[0], "password": self.auth[1]},
        )

        self.token = resp.json().get("token", None)

    def get_clips(self):
        api_url = f"{self.base_url}/api/v1/media"

        clip_data = []
        while True:
            resp = requests.get(url=api_url, auth=self.auth)

            if resp.status_code != 200:
                return clip_data

            resp_json = resp.json()

            clip_data.extend(resp_json["results"])

            if resp_json["next"]:
                api_url = resp_json["next"]
            else:
                return clip_data

    def get_clip_info(self, clip_id):
        api_url = f"{self.base_url}/api/v1/media/{clip_id}"

        resp = requests.get(url=api_url, auth=self.auth)

        return resp.json()

    def download(self, clip_id):
        info = self.get_clip_info(clip_id)
        media_url = info["original_media_url"]
        full_url = f"{self.base_url}{media_url}"
        r = requests.get(full_url)
        with open(f"{clip_id}.mp4", "wb") as outfile:
            outfile.write(r.content)

    def search(self, query):
        api_url = f"{self.base_url}/api/v1/search?format=json&q={query}"

        resp = requests.get(api_url, headers={"Authorization": f"Bearer {self.token}"})

        if resp.status_code == 200:
            return resp.json()
        else:
            raise Exception(f"Response {resp.status_code}: {resp.reason}")

    def upload(self, path, title, description):
        upload_url = f"{self.base_url}/api/v1/media"

        resp = requests.post(
            url=upload_url,
            files={"media_file": open(path, "rb")},
            data={"title": title, "description": description},
            auth=self.auth,
        )

        return resp
