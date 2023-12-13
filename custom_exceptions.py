class ResponseError(Exception):
	'''
	Custom error that is raised when the response code is not 200
	'''
	def __init__(self, message, value):
		self.messaage = message
		self.value = value