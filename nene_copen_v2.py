import numpy as np
import random

class NN(object):
    def __init__(self, sizesArray):
        # [inputLayerSize, hiddenLayerSize, outputLayerSize]
        self.sizesArray = sizesArray
        self.numLayers = len(self.sizesArray)
        # Initialize weights and biases with normal distribution
        self.weights = [np.random.randn(y, x) for x, y in zip(sizesArray[:-1], sizesArray[1:])]
        self.biases = [np.random.randn(y, 1) for y in sizesArray[1:]]
        self.lastsamplingrate = None


    def forward(self, X):
        # Computes layer-layer activation: activation = (input vector * layer weights) + biases
        wat = np.reshape(np.array(X), (self.sizesArray[0], 1))
        for b, w in zip(self.biases, self.weights):
            wat = self.sigmoid(np.dot(w, wat) + b)
        return wat

    def sigmoid(self, z):
        return 1/(1+np.exp(-z))

    def sigmoidPrime(self, z):
        return self.sigmoid(z)*(1-self.sigmoid(z))

    '''
    Les funcions posteriors tenen a veure amb descens per gradient o _gradient descent_
    Si el plot del cost fos no-convex, podriem quedar-mos estancats en un minim local
    en lloc del minim global. Per aixo fem els errors al quadrat, ja que les equacions
    quadratiques *solen ser* convexes.
    '''

    # J is [1 x outputLayerSize]
    # mean squared error, MSE
    def cost(self, X, y):
        self.yHat = self.forward(X)
        J = 0.5*sum((y-self.yHat)**2)
        return J

    def gradientDescent(self, trainingData, stages, batchSize, samplingRate):
        self.lastsamplingrate = samplingRate
        n = len(trainingData)
        for j in xrange(stages):
            random.shuffle(trainingData)
            # Use chunks of data
            batchesArray = [trainingData[k:k+batchSize] for k in xrange(0, n, batchSize)]
            for bat in batchesArray:
                # Update the weights
                self.updateBatch(bat, samplingRate)
            #print "Stage", j, "of", stages, "..."


    # Update network weight with backprop, deal with matrices
    def updateBatch(self, bat, samp):
        nablaB = [np.zeros(b.shape) for b in self.biases]           # nabla = "inverted Delta", "gradient"
        nablaW = [np.zeros(w.shape) for w in self.weights]

        '''
        BAT STRUCTURE:
        Array of length n, containing n pairs of (inputVec, answerVec)
            where       len(inputVec) = inputLayerSize
                        answerVec = [0, 1] or [1, 0]

        To update based on final user feedback, we submit the right answer making a 1-pair batch.
        It will be called using the last sampling rate used.
        '''


        for x, y in bat:
            deltaNablaB, deltaNablaW = self.backprop(x, y)          # partial derivatives
            nablaB = [nb + dnb for nb, dnb in zip(nablaB, deltaNablaB)]     # we add the little deviation
            nablaW = [nw + dnw for nw, dnw in zip(nablaW, deltaNablaW)]
        self.weights = [w - (samp/len(bat))*nw for w, nw in zip(self.weights, nablaW)]
        self.biases  = [b - (samp/len(bat))*nb for b, nb in zip(self.biases, nablaB)]


    def batchFeedback(self, bat):
        samp = self.lastsamplingrate
        nablaB = [np.zeros(b.shape) for b in self.biases]
        nablaW = [np.zeros(w.shape) for w in self.weights]

        deltaNablaB, deltaNablaW = self.backprop(bat[0], bat[1])          # more corrections
        nablaB = [nb + dnb for nb, dnb in zip(nablaB, deltaNablaB)]
        nablaW = [nw + dnw for nw, dnw in zip(nablaW, deltaNablaW)]
        self.weights = [w - (samp/len(bat))*nw for w, nw in zip(self.weights, nablaW)]
        self.biases  = [b - (samp/len(bat))*nb for b, nb in zip(self.biases, nablaB)]


    def backprop(self, x, y):
        # returns the gradient vector for the cost function
        # older weights get adjusted based on the activity of the next layers
        nablaW = [np.zeros(w.shape) for w in self.weights]
        nablaB = [np.zeros(b.shape) for b in self.biases]
        act = x
        actArray = [x]
        zArray = []
        for b, w in zip(self.biases, self.weights):      # for all layers
            z = np.dot(w, act) + b
            zArray.append(z)
            act = self.sigmoid(z)
            actArray.append(act)

        debug1 = self.costDer(actArray[-1], y)
        debug2 = self.sigmoidPrime(zArray[-1])
        delta = debug1 * debug2
        nablaB[-1] = delta
        nablaW[-1] = np.dot(delta, actArray[-2].transpose())

        for l in xrange(2, self.numLayers): # since we have 3 layers it will only run 1 iteration
            z = zArray[-l]
            sPrime = self.sigmoidPrime(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sPrime
            nablaB[-l] = delta
            nablaW[-l] = np.dot(delta, actArray[-l-1].transpose())
        return (nablaB, nablaW)

    def test(self, dataToTest):
        resultArray = [(np.argmax(self.forward(x)), y) for (x, y) in dataToTest]
        return sum(int(x == y) for (x, y) in resultArray)

    def getAnswer(self, arrayToTest):
        # Remember that, when testing, we specify the index of the 2-pos output vector:
        # a '0' means neurone 0 -> would hire, and '1' means neurone 1 -> would not

        if np.argmax(self.forward(arrayToTest)) == 0:
            return True
        else:
            return False

    def correct(self, profileInfo, flag):
        if (flag):
            batSubmit = [np.reshape(np.array(profileInfo), (self.sizesArray[0], 1)), np.reshape(np.array([1, 0]), (self.sizesArray[-1], 1))]
        else:
            batSubmit = [np.reshape(np.array(profileInfo), (self.sizesArray[0], 1)), np.reshape(np.array([0, 1]), (self.sizesArray[-1], 1))]

        self.batchFeedback(batSubmit)


    def debugPrintStateToFile(self, filename):
        f = open(str(filename), "a")
        for b, w in zip(self.biases, self.weights):
            s = str(b) + ',' + str(w) + '\n'
            f.write(s)
        f.close()

    def costDer(self, actArray, y):
        return (actArray - y) # xd
