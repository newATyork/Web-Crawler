# "stack and queue data structure" http://cis.poly.edu/cs6913/stack.txt 

class qQueue:
	def __init__(self) :
		self.queue = []
	def enqueue(self, object) :
		self.queue.append(object)
	def dequeue(self) :
		tmp = self.queue[0]
		del self.queue[0]
		return tmp
	def size(self) :
		return len(self.queue)

