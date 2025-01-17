# Auralize

This AI project consist in a app based on a
convolutional neural network that can classify
the environmental sound in 50 classes.

## Installation

To install the project you need to have python
installed in your machine. You can install it
from the official website: https://www.python.org/

to install the project you need to install the
requirements in the requirements.txt file.

```bash
pip install -r requirements.txt
```

it is recommended to use a virtual environment
to install the requirements. The setup bash file
will create a virtual environment and install the
requirements.

```bash
bash setup.sh
```

Also you need to install gtk4 to run the app,
make, makefile and gcc.

```bash
    sudo apt-get install make
    sudo apt-get install makefile
    sudo apt-get install gcc
    sudo apt-get install libgtk-4-dev
```

## AI Model

The AI model is a convolutional neural network
that was trained with the ESC-50 dataset. The
model was trained with 14 epochs and has an
accuracy of 0.50.


To train the model you need to download all data
and convert it to spectrogram images. The data
is installed with the setup.py file in the ia
folder.

```bash
    python setup.py
```

To train the model you need to run the train.py
file in the ia folder. If you would like to train
with more epochs or batches you can change the them.
That is in the train.py at the end of the file. The
default values are 14 epochs and 32 batches.

```bash
    python train.py
```

To use the last model you need to run the model.py
file in the ia folder. The model.py file will load
the last model and predict the sound of the file 
path put in the predict function.

```bash
    python model.py
```

## Usage

To run the app you need to run the Makefile in the 
main folder. The Makefile will compile the app and
run it.

```bash
    make
```
