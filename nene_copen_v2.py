import numpy as np
import random

class NN(object):
    def __init__(self, sizesArray):
        self.sizesArray = sizesArray
        self.numLayers = len(self.sizesArray)
        self.weights = [np.random.randn(y, x) for x, y in zip(sizesArray[:-1], sizesArray[1:])]
        self.biases = [np.random.randn(y, 1) for y in sizesArray[1:]]
        self.lastsamplingrate = None


    def forward(self, X):
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

    #def costPrime(self, X, y):                 _deprecated_
        #self.yHat = self.forward(X)

        #delta3 = np.multiply(-(y - self.yHat), self.sigmoidPrime(self.Z3))
        #dJdW2 = np.dot(self.a2.T, delta3)

        #delta2 = np.dot(delta3, self.W2.T)      # W2.T es la transposada
        #dJdW1 = np.dot(X.T, delta2)

        #return dJdW1, dJdw2


    def gradientDescent(self, trainingData, stages, batchSize, samplingRate):
        self.lastsamplingrate = samplingRate
        n = len(trainingData)
        for j in xrange(stages):
            random.shuffle(trainingData)
            batchesArray = [trainingData[k:k+batchSize] for k in xrange(0, n, batchSize)]
            for bat in batchesArray:
                self.updateBatch(bat, samplingRate)
            print "Stage", j, "of", stages, "..."


    # Update network weight with backprop
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
            nablaB = [nb + dnb for nb, dnb in zip(nablaB, deltaNablaB)]
            nablaW = [nw + dnw for nw, dnw in zip(nablaW, deltaNablaW)]
        self.weights = [w - (samp/len(bat))*nw for w, nw in zip(self.weights, nablaW)]
        self.biases  = [b - (samp/len(bat))*nb for b, nb in zip(self.biases, nablaB)]


    def batchFeedback(self, bat):
        samp = self.lastsamplingrate
        nablaB = [np.zeros(b.shape) for b in self.biases]
        nablaW = [np.zeros(w.shape) for w in self.weights]

        deltaNablaB, deltaNablaW = self.backprop(bat[0], bat[1])          # partial derivatives
        nablaB = [nb + dnb for nb, dnb in zip(nablaB, deltaNablaB)]
        nablaW = [nw + dnw for nw, dnw in zip(nablaW, deltaNablaW)]
        self.weights = [w - (samp/len(bat))*nw for w, nw in zip(self.weights, nablaW)]
        self.biases  = [b - (samp/len(bat))*nb for b, nb in zip(self.biases, nablaB)]


    def backprop(self, x, y):
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

        for l in xrange(2, self.numLayers):
            z = zArray[-l]
            sPrime = self.sigmoidPrime(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sPrime
            nablaB[-l] = delta
            nablaW[-l] = np.dot(delta, actArray[-l-1].transpose())
        return (nablaB, nablaW)

    def test(self, dataToTest):
        resultArray = [(np.argmax(self.forward(x)), y) for (x, y) in dataToTest]
        return sum(int(x == y) for (x, y) in resultArray)

    def testDebug(self, arrayToTest, submitChanges = False):
        forwarding = self.forward(arrayToTest)
        print forwarding
        maximumArg = np.argmax(forwarding)

        # Remember that, when testing, we specify the index of the 2-pos output vector:
        # a '0' means neurone 0 -> would hire, and '1' means neurone 1 -> would not

        if maximumArg == 0:
            print 'Y'
        else:
            print 'N'
        print "----------------\n"
        gotcha = raw_input("Did the user like the candidate (y/n)? ")

        if gotcha.lower() == 'y':
            batSubmit = [np.reshape(np.array(arrayToTest), (self.sizesArray[0], 1)), np.reshape(np.array([1, 0]), (self.sizesArray[-1], 1))]
        else:
            batSubmit = [np.reshape(np.array(arrayToTest), (self.sizesArray[0], 1)), np.reshape(np.array([0, 1]), (self.sizesArray[-1], 1))]

        if submitChanges:
            self.batchFeedback(batSubmit)

    def debugPrintStateToFile(self, filename):
        f = open(str(filename), "a")
        for b, w in zip(self.biases, self.weights):
            s = str(b) + ',' + str(w) + '\n'
            f.write(s)
        f.close()

    def costDer(self, actArray, y):
        return (actArray - y) # xd
