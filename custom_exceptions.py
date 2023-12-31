class ResponseError(Exception):
	'''
	Custom error that is raised when the response code is not 200
	'''
	def __init__(self, status_code):
		self.status_code = status_code
		self.messaage = f"\nResponse Error: {status_code}"

class ReAttemptFail(Exception):
	'''
	Custom error that is raised when the reattempt function in the reusable_func fails.
	'''
	def __init__(self, value):
		self.value = value
		self.messaage = "-----Reattempt Failed------"