import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('deepfakedetection-2b199-firebase-adminsdk-oj5r5-1d5e59f012.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

class Requests(object):
	def __init__(self, request_id = "NA", type = "NA", link = "NA", status = "NA", result = "NA"):
		self.request_id = request_id
		self.type = type
		self.youtube_link = link
		self.status = status
		self.result = result

class UpdateRequests(object):
	def __init__(self, status = "NA", result = "NA"):
		self.status = status
		self.result = result

class UpdateRequestsModel(object):
	def __init__(self, model_data, status = "NA", result = "NA"):
		self.model_data = model_data
		self.status = status
		self.result = result

def store_new_request(request_id, type, link):
	doc_ref = db.collection(u'requests').document(request_id)

	req = Requests(request_id=request_id, type = type, link = link, status=u'CREATED')
	doc_ref.set(req.__dict__)

def update_request_status(request_id, status, result = "NA"):
	doc_ref = db.collection(u'requests').document(request_id)
	req = UpdateRequests(status=status, result = result)
	doc_ref.set(req.__dict__, merge=True)

def update_model_result(model_data, request_id, status, result = "NA"):
	doc_ref = db.collection(u'requests').document(request_id)
	req = UpdateRequestsModel(model_data = model_data, status=status, result = result)
	doc_ref.set(req.__dict__, merge=True)

def query_request_data(request_id):
	doc_ref = db.collection(u'requests').document(request_id)
	doc = doc_ref.get()
	if doc.exists:
		print(f'Document data: {doc.to_dict()}')
		return doc.to_dict()
	else:
		print(u'No such document!')