from googleapiclient.discovery import build
from urllib.request import urlretrieve
from configparser import ConfigParser


class Uthumer:
    _api = None
    settings = ConfigParser()
    settings.read('settings.ini')

    @property
    def api(self):
        if not self._api:
            api_params = {'developerKey': self.settings['youtube']['API_KEY'],
                          'serviceName': 'youtube',
                          'version': 'v3'}
            self._api = build(**api_params)
        return self._api

    def get_thumbs(self, video_id):
        request_params = {'id': video_id,
                          'part': 'snippet',
                          'fields': 'items(snippet(thumbnails))'}
        request = self.api.videos().list(**request_params)
        response = request.execute()
        thumbs = response['items'][0]['snippet']['thumbnails']
        return thumbs

    def get_largest_thumb_url(self, thumbs):
        for size in self.settings['youtube']['SIZES'].split(','):
            if size in thumbs:
                thumb_url = thumbs[size]['url']
                return thumb_url
        return None

    def download_thumb(self, video_id, path='wallpaper.jpg'):
        thumbs = self.get_thumbs(video_id)
        thumb_url = self.get_largest_thumb_url(thumbs)
        urlretrieve(thumb_url, path)

if __name__ == '__main__':
    uthumer = Uthumer()
    video_id = 'U-iEK0mlmuQ'
    uthumer.download_thumb(video_id)
