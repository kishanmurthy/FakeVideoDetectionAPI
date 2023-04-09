import random
import uuid
from urllib.parse import urlencode, urlparse

#pip3 install flask==2.1.3
#pip3 install aioflask

from aioflask import Flask, abort, jsonify, render_template, request
from flask_cors import CORS

from database_access import query_request_data, store_new_request
from file_download import downloadYoutubeVideos, downloadYoutubeShorts
import asyncio

app = Flask(__name__)
CORS(app)

@app.route('/')
def application_start():
    return "Hello"

@app.route('/detect_authenticity', methods=["POST"])
async def detect_authenticity():
	request_id = str(uuid.uuid4())
	av_link = request.json['url']
	ytype = ""
	video_id = ""
	if "watch" in av_link:
		ytype = "videos"
		query_dict = {}
		parse = urlparse(av_link)
		for ele in parse.query.split('&'):
			key, value = ele.split('=')
			query_dict[key] = value 
		video_id = query_dict['v']
		asyncio.create_task(downloadYoutubeVideos(request_id, video_id))

	else:
		ytype = "shorts"
		video_id = av_link.rsplit('/', 1)[1]
		asyncio.create_task(downloadYoutubeShorts(request_id, video_id))
		
	store_new_request(request_id, ytype, video_id)
	return jsonify({'resquest_id':request_id})

@app.route('/get_status')
def get_status():
	request_id = request.args['request_id']
	data = query_request_data(request_id)
	return jsonify({'status':data["status"]})


@app.route('/get_link')
def get_link():
	request_id = request.args['request_id']
	data = query_request_data(request_id)
	return jsonify({'url':data["youtube_link"]}) 

@app.route('/get_result')
def get_result():
	request_id = request.args['request_id']
	data = query_request_data(request_id)
	if data["status"] == "COMPLETED":
		return data["result"]
	else:
		return "NA"

if __name__ == '__main__':
   app.run()