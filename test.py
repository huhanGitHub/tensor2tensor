import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os
import collections
import base64
import cStringIO
import pydub
import shutil
from scipy.io import wavfile

import IPython
import google.colab

from tensor2tensor import models
from tensor2tensor import problems
from tensor2tensor.layers import common_layers
from tensor2tensor.utils import trainer_lib
from tensor2tensor.utils import t2t_model
from tensor2tensor.utils import registry
from tensor2tensor.utils import metrics

# Enable TF Eager execution
from tensorflow.contrib.eager.python import tfe
tfe.enable_eager_execution()

# Other setup
Modes = tf.estimator.ModeKeys

# Setup some directories
data_dir = os.path.expanduser("/home/huhan/20g_disk_d/python/projects/t2t/data")
tmp_dir = os.path.expanduser("/home/huhan/20g_disk_d/python/projects/t2t/tmp")
train_dir = os.path.expanduser("/home/huhan/20g_disk_d/python/projects/t2t/train")
checkpoint_dir = os.path.expanduser("/home/huhan/20g_disk_d/python/projects/t2t/checkpoints")
tf.gfile.MakeDirs(data_dir)
tf.gfile.MakeDirs(tmp_dir)
tf.gfile.MakeDirs(train_dir)
tf.gfile.MakeDirs(checkpoint_dir)

gs_ckpt_dir = "gs://tensor2tensor-checkpoints/"

problem_name = "librispeech_clean"
asr_problem = problems.problem(problem_name)
encoders = asr_problem.feature_encoders(None)

model_name = "transformer"
hparams_set = "transformer_librispeech_tpu"

hparams = trainer_lib.create_hparams(hparams_set, data_dir=data_dir, problem_name=problem_name)
asr_model = registry.model(model_name)(hparams, Modes.PREDICT)


def encode(x):
    waveforms = encoders["waveforms"].encode(x)
    encoded_dict = asr_problem.preprocess_example({"waveforms": waveforms, "targets": []}, Modes.PREDICT, hparams)

    return {"inputs": tf.expand_dims(encoded_dict["inputs"], 0), "targets": tf.expand_dims(encoded_dict["targets"], 0)}


def decode(integers):
    integers = list(np.squeeze(integers))
    if 1 in integers:
        integers = integers[:integers.index(1)]
    return encoders["targets"].decode(np.squeeze(integers))