class ResponseError(Exception):
	'''
	Custom error that is raised when the response code is not 200
	'''
	def __init__(self, value):
		self.messaage = "Response Error: "
		self.value = value