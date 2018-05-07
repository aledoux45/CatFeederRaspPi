from pybrain.datasets                 import ClassificationDataSet
from pybrain.tools.shortcuts          import buildNetwork
from pybrain.supervised.trainers      import BackpropTrainer
from pybrain.structure.modules        import SoftmaxLayer
from pybrain.utilities                import percentError
from PIL import Image
# import picamera
import os
import numpy as np
from scipy.misc import toimage

# Inputs
height = 48
width = 64
hiddenlayers = [400, 50, 50]
# murkafolder = '/home/pi/camera/murka'
# masyafolder = '/home/pi/camera/masya'
murkafolder = '/Users/Yoshcakes/Documents/Murka'
masyafolder = '/Users/Yoshcakes/Documents/Masya'


# Build dataset
ds = ClassificationDataSet(height*width, 1, nb_classes=2, class_labels=['Murka','Masya'])

for trainingpicture in [f for f in os.listdir(murkafolder) if f.endswith('.png')]:
    im = Image.open(os.path.join(murkafolder, trainingpicture))
    imlow = im.resize((width, height), Image.ANTIALIAS)
    # Convert black and white (L = luminosity; 0 = black; 255 = white)
    bw_im = imlow.convert('L')
    pixels = [bw_im.getpixel((i, j)) for j in range(height) for i in range(width)] # list of black and white pixels
    # Normalize the pixels to average brightness
    avgluminosity = sum(pixels)/len(pixels)
    processedpixels = map(lambda p: min(p + 255/2 - avgluminosity, 255) if (avgluminosity < 255/2) else max(p + 255/2 - avgluminosity, 0), pixels)

    # Save lowres images
    a = np.array(processedpixels)
    a = a.reshape(-1, width)
    im = toimage(a)
    im.save(os.path.join(murkafolder + '/bw', trainingpicture))

    # Populate database
    ds.appendLinked(processedpixels, [0]) # 0 = Murka; 1 = Masya

for trainingpicture in [f for f in os.listdir(masyafolder) if f.endswith('.png')]:
    im = Image.open(os.path.join(masyafolder, trainingpicture))
    imlow = im.resize((width, height), Image.ANTIALIAS)
    # Convert black and white (L = luminosity; 0 = black; 255 = white)
    bw_im = imlow.convert('L')
    pixels = [bw_im.getpixel((i, j)) for j in range(height) for i in range(width)] # list of black and white pixels
    # Normalize the pixels to average brightness
    avgluminosity = sum(pixels)/len(pixels)
    processedpixels = map(lambda p: min(p + 255/2 - avgluminosity, 255) if (avgluminosity < 255/2) else max(p + 255/2 - avgluminosity, 0), pixels)

    # Save lowres images
    a = np.array(processedpixels)
    a = a.reshape(-1, width)
    im = toimage(a)
    im.save(os.path.join(masyafolder + '/bw', trainingpicture))

    ds.appendLinked(processedpixels, [1]) # 0 = Murka; 1 = Masya

print "There are", ds.nClasses, "classes"
print "Class 0 is", ds.getClass(0)

tstdata_temp, trndata_temp = ds.splitWithProportion(0.25)

tstdata = ClassificationDataSet(height*width, 1, nb_classes=2, class_labels=['Murka','Masya'])
for n in xrange(0, tstdata_temp.getLength()):
    tstdata.addSample( tstdata_temp.getSample(n)[0], tstdata_temp.getSample(n)[1] )

trndata = ClassificationDataSet(height*width, 1, nb_classes=2, class_labels=['Murka','Masya'])
for n in xrange(0, trndata_temp.getLength()):
    trndata.addSample( trndata_temp.getSample(n)[0], trndata_temp.getSample(n)[1] )

trndata._convertToOneOfMany()
tstdata._convertToOneOfMany()

print "Total number of patterns: ", len(ds)
print "Number of training patterns: ", len(trndata)
print "Number of testing patterns: ", len(tstdata)
print "Input and output training dimensions: ", trndata.indim, trndata.outdim
print "Input and output testing dimensions: ", tstdata.indim, tstdata.outdim
print "First sample (input, target, class):"
print trndata['input'][0], trndata['target'][0], trndata['class'][0]

# Build neural network
fnn = buildNetwork(trndata.indim, hiddenlayers[0], hiddenlayers[1], hiddenlayers[2], trndata.outdim, outclass=SoftmaxLayer)
trainer = BackpropTrainer(fnn, dataset=trndata, learningrate=0.005, momentum=0.0, verbose=True, weightdecay=0.0)

# Train neural network
trainer.trainEpochs(10)
# trainer.trainUntilConvergence(continueEpochs=5, validationProportion=0.25) # Can take a long time
# trainer.train() # Train on one epoch only

# Training error and testing error
trnresult = percentError( trainer.testOnClassData(), trndata['class'] )
tstresult = percentError( trainer.testOnClassData(dataset=tstdata ), tstdata['class'] )

print "The hidden layers are", hiddenlayers[0], hiddenlayers[1], hiddenlayers[2]
print "Percentage training error: ", trnresult
print "Percentage testing error: ", tstresult

# Test on a couple pictures:
testout = []
for i in xrange(tstdata.getLength()):
    out = fnn.activate(trndata['input'][i])
    testout.append(out.argmax() == trndata['class'][i])
print "Correctly classified", sum(t == True for t in testout)[0], "/", len(testout)

# Take new picture
# with picamera.PiCamera() as camera:
#     camera.resolution = (res, res)
#     newpicture = '/home/pi/camera/newpicture.jpg'
#     camera.capture(newpicture)
#     im = Image.open(newpicture)
#     bw_im = im.convert('1') # Convert black and white
#     pixels = [bw_im.getpixel((i, j)) for i in range(res) for j in range(res)] # list of black and white pixels
#
# # Get results
# net.activate(pixels)