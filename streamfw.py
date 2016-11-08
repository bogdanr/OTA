from flask import Response, stream_with_context

import requests

def get_stream_fw(name):
  url = 'https://media.giphy.com/media/9Sxp3YOKKFEBi/giphy.gif'
  req = requests.get(url, stream = True)
  return Response(stream_with_context(req.iter_content(chunk_size=1024)), content_type = req.headers["content-type"])

