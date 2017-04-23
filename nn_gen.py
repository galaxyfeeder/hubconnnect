import numpy as np, random


class DataGen(object):
    def gen(self, size):
        tr_d = []

        for i in range(size):
            arr = [random.uniform(0.0, 1.0) for i in range(5)]
            tr_d.append(arr)


        #### try
        training_inputs = [np.reshape(np.array(x), (5, 1)) for x in tr_d]
        #### ???

        training_results = []
        for j in range(size):
            if (random.randint(0, 1) == 1):
                vec = np.reshape(np.array([1, 0]), (2, 1))
            else:
                vec = np.reshape(np.array([0, 1]), (2, 1))
            training_results.append(vec)


        training_data = zip(training_inputs, training_results)

        #print "-----"
        #print training_data[0:5]

        return training_data
