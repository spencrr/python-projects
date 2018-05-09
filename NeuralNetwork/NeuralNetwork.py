import tensorflow as tf

from tensorflow.contrib.learn.python.learn.datasets.mnist import read_data_sets


mnist = read_data_sets("MNIST_data/", one_hot=True)
batch_size = 100

input_size = 28*28
hidden_nodes = (100, 100, 100)
output_size = 10


input_shape = [None, input_size]
x = tf.placeholder('float', input_shape)
y = tf.placeholder('float')

def network_model(data):
	layers = []
	for i in range(len(hidden_nodes) + 1):
		nuerons = hidden_nodes[i] if i < len(hidden_nodes) else output_size
		layers.append(
		{'weights' : tf.Varaible(tf.random_normal(
			[input_size if i == 0 else hidden_nodes[i - 1], nuerons])),
		'biases' : tf.Varaible(tf.random_normal([nuerons]))}
			)		
	for layer in layers:
		data = tf.add(tf.matmul(data, layer['weights'])) + layer['biases']
		if layers.indexOf(layer) != len(layers) - 1: 
			data = tf.nn.sigmoid(data)

	return 

def train_model(data):
	prediction = network_model(data)
	cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(prediction, y))

	optimizer = tf.train.AdamOptimizer().minimize(cost, learning_rate=1e-3)

	epochs = 10

	with tf.Session() as sess:
		sess.run(tf.initialize_all_variables())

		for epoch in epochs:
			epoch_loss = 0
			for data_set in range(int(mnist.train.num_examples / batch_size)):
				x, y = mnist.train.next_batch(batch_size)
				data_set, c = sess.run([optimizer, cost], feed_dict=
					{
					x: x, y: y
					})
				epoch_loss += c
			print('Epoch {epoch}, Loss {epoch_loss}')
		
		
		correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
		
		accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

		print('Accuracy {}'.format(accuracy.eval({x:mnist.test.images, y:mnist.test.labels})))


