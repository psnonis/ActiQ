"""
Python script that takes given video_id as argument and re-writes config files (for kinetics and ava) for SlowFast models.
Sample command: $ python config_sf.py N5j6382
"""

from sys import argv

video = argv[1]
stime = argv[2]
etime = argv[3]

tools = '/work/ActIQ/product/engine/tools'
cache = '/work/ActIQ/product/engine/cache'

with open(f'{tools}/sf_kinetics.yaml', 'w') as yaml:
    yaml.write(
f'TRAIN:\n\
  ENABLE: False\n\
  DATASET: kinetics\n\
  BATCH_SIZE: 64\n\
  EVAL_PERIOD: 10\n\
  CHECKPOINT_PERIOD: 1\n\
  AUTO_RESUME: True\n\
  CHECKPOINT_FILE_PATH: "{tools}/sf/demo/Kinetics/SLOWFAST_8x8_R50.pkl" # path to pretrain model to run demo\n\
  CHECKPOINT_TYPE: caffe2\n\
DATA:\n\
  NUM_FRAMES: 20\n\
  SAMPLING_RATE: 3\n\
  TRAIN_JITTER_SCALES: [256, 320]\n\
  TRAIN_CROP_SIZE: 224\n\
  TEST_CROP_SIZE: 256\n\
  INPUT_CHANNEL_NUM: [3, 3]\n\
SLOWFAST:\n\
  ALPHA: 4\n\
  BETA_INV: 8\n\
  FUSION_CONV_CHANNEL_RATIO: 2\n\
  FUSION_KERNEL_SZ: 7\n\
RESNET:\n\
  ZERO_INIT_FINAL_BN: True\n\
  WIDTH_PER_GROUP: 64\n\
  NUM_GROUPS: 1\n\
  DEPTH: 50\n\
  TRANS_FUNC: bottleneck_transform\n\
  STRIDE_1X1: False\n\
  NUM_BLOCK_TEMP_KERNEL: [[3, 3], [4, 4], [6, 6], [3, 3]]\n\
  SPATIAL_STRIDES: [[1, 1], [2, 2], [2, 2], [2, 2]]\n\
  SPATIAL_DILATIONS: [[1, 1], [1, 1], [1, 1], [1, 1]]\n\
NONLOCAL:\n\
  LOCATION: [[[], []], [[], []], [[], []], [[], []]]\n\
  GROUP: [[1, 1], [1, 1], [1, 1], [1, 1]]\n\
  INSTANTIATION: dot_product\n\
BN:\n\
  USE_PRECISE_STATS: True\n\
  NUM_BATCHES_PRECISE: 200\n\
  MOMENTUM: 0.1\n\
  WEIGHT_DECAY: 0.0\n\
SOLVER:\n\
  BASE_LR: 0.1\n\
  LR_POLICY: cosine\n\
  MAX_EPOCH: 196\n\
  MOMENTUM: 0.9\n\
  WEIGHT_DECAY: 1e-4\n\
  WARMUP_EPOCHS: 34\n\
  WARMUP_START_LR: 0.01\n\
  OPTIMIZING_METHOD: sgd\n\
MODEL:\n\
  NUM_CLASSES: 400\n\
  ARCH: slowfast\n\
  LOSS_FUNC: cross_entropy\n\
  DROPOUT_RATE: 0.5\n\
TEST:\n\
  ENABLE: False\n\
  DATASET: kinetics\n\
  BATCH_SIZE: 64\n\
DATA_LOADER:\n\
  NUM_WORKERS: 8\n\
  PIN_MEMORY: True\n\
DEMO:\n\
  ENABLE: True\n\
  LABEL_FILE_PATH: "{tools}/sf/demo/Kinetics/kinetics_400_labels.csv"\n\
  DATA_SOURCE: "{cache}/{video}.incoming.mp4"\n\
  DISPLAY_WIDTH: 0\n\
  DISPLAY_HEIGHT: 0\n\
NUM_GPUS: 1\n\
NUM_SHARDS: 1\n\
RNG_SEED: 0\n\
OUTPUT_DIR: "{cache}"'
    )

with open(f'{tools}/sf_ava.yaml', 'w') as yaml:
    yaml.write(
f'TRAIN:\n\
  ENABLE: False\n\
  DATASET: ava\n\
  BATCH_SIZE: 64\n\
  EVAL_PERIOD: 10\n\
  CHECKPOINT_PERIOD: 1\n\
  AUTO_RESUME: True\n\
  CHECKPOINT_FILE_PATH: "{tools}/sf/demo/AVA/SLOWFAST_32x2_R101_50_50.pkl" #path to pretrain model\n\
  CHECKPOINT_TYPE: pytorch\n\
DATA:\n\
  NUM_FRAMES: 20\n\
  SAMPLING_RATE: 3\n\
  TRAIN_JITTER_SCALES: [256, 320]\n\
  TRAIN_CROP_SIZE: 224\n\
  TEST_CROP_SIZE: 256\n\
  INPUT_CHANNEL_NUM: [3, 3]\n\
DETECTION:\n\
  ENABLE: True\n\
  ALIGNED: False\n\
AVA:\n\
  BGR: False\n\
  DETECTION_SCORE_THRESH: 0.8\n\
  TEST_PREDICT_BOX_LISTS: ["person_box_67091280_iou90/ava_detection_val_boxes_and_labels.csv"]\n\
SLOWFAST:\n\
  ALPHA: 4\n\
  BETA_INV: 8\n\
  FUSION_CONV_CHANNEL_RATIO: 2\n\
  FUSION_KERNEL_SZ: 5\n\
RESNET:\n\
  ZERO_INIT_FINAL_BN: True\n\
  WIDTH_PER_GROUP: 64\n\
  NUM_GROUPS: 1\n\
  DEPTH: 101\n\
  TRANS_FUNC: bottleneck_transform\n\
  STRIDE_1X1: False\n\
  NUM_BLOCK_TEMP_KERNEL: [[3, 3], [4, 4], [6, 6], [3, 3]]\n\
  SPATIAL_DILATIONS: [[1, 1], [1, 1], [1, 1], [2, 2]]\n\
  SPATIAL_STRIDES: [[1, 1], [2, 2], [2, 2], [1, 1]]\n\
NONLOCAL:\n\
  LOCATION: [[[], []], [[], []], [[6, 13, 20], []], [[], []]]\n\
  GROUP: [[1, 1], [1, 1], [1, 1], [1, 1]]\n\
  INSTANTIATION: dot_product\n\
  POOL: [[[2, 2, 2], [2, 2, 2]], [[2, 2, 2], [2, 2, 2]], [[2, 2, 2], [2, 2, 2]], [[2, 2, 2], [2, 2, 2]]]\n\
BN:\n\
  USE_PRECISE_STATS: False\n\
  NUM_BATCHES_PRECISE: 200\n\
  MOMENTUM: 0.1\n\
  WEIGHT_DECAY: 0.0\n\
SOLVER:\n\
  MOMENTUM: 0.9\n\
  WEIGHT_DECAY: 1e-7\n\
  OPTIMIZING_METHOD: sgd\n\
MODEL:\n\
  NUM_CLASSES: 80\n\
  ARCH: slowfast\n\
  LOSS_FUNC: bce\n\
  DROPOUT_RATE: 0.5\n\
TEST:\n\
  ENABLE: False\n\
  DATASET: ava\n\
  BATCH_SIZE: 8\n\
DATA_LOADER:\n\
  NUM_WORKERS: 2\n\
  PIN_MEMORY: True\n\
DEMO:\n\
  ENABLE: True\n\
  LABEL_FILE_PATH: "{tools}/sf/demo/AVA/ava.names"\n\
  DATA_SOURCE: "{cache}/{video}.incoming.mp4"\n\
  # DISPLAY_WIDTH: 640\n\
  # DISPLAY_HEIGHT: 480\n\
  DETECTRON2_OBJECT_DETECTION_MODEL_CFG: "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"\n\
  DETECTRON2_OBJECT_DETECTION_MODEL_WEIGHTS: "detectron2://COCO-Detection/faster_rcnn_R_50_FPN_3x/137849458/model_final_280758.pkl"\n\
NUM_GPUS: 1\n\
NUM_SHARDS: 1\n\
RNG_SEED: 0\n\
OUTPUT_DIR: "{cache}"'
    )
