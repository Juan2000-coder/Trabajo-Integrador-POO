# Python program showing
# class decorator with *args
# and **kwargs

class MyDecorator:
	def __init__(self, function):
		self.function = function
	
	def __call__(self, *args, **kwargs):
		print("hola que onda")
		self.function(*args, **kwargs)
		print("hola que onda")
		# We can also add some code
		# after function call.
	
class MyClass:
	def __init__(self, name):
		self.name = name
		
	@MyDecorator
	def function(self, message):
		print(print("{}, {}".format(message, self.name)))

miobjeto = MyClass("yo")
miobjeto.function("perro")