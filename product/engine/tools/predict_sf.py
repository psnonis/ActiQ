import os, sys

tools = os.environ.get('tools', '')
cache = os.environ.get('cache', '')
sfast = os.environ.get('sfast', '')

_     = sys.path.append(sfast)

import numpy   as np
import pandas  as pd
import cv2     as cv
import torch   as to

from detectron2        import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data   import MetadataCatalog

from slowfast.utils                  import logging
from slowfast.utils                  import misc
from slowfast.models                 import build_model

from slowfast.datasets.cv2_transform import scale, scale_boxes
from slowfast.config.defaults        import get_cfg

from time                            import time, sleep
from os.path                         import basename
from os                              import system

import slowfast.utils.checkpoint      as cu
import slowfast.utils.distributed     as du
import slowfast.utils.multiprocessing as mu

class VideoReader(object):

    def __init__(self, file) :

        self.cap     = cv.VideoCapture(file)

        if  not self.cap.isOpened():
            raise IOError(f'Unable to Locate Video File : {file}')

        self.video   = basename(file)
        self.video_w = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH ))
        self.video_h = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.video_c = int(self.cap.get(cv.CAP_PROP_FRAME_COUNT ))
        self.video_r = int(self.cap.get(cv.CAP_PROP_FPS         ))
        self.count   = 0
        self.ended   = False

    def __iter__(self) :

        return self

    def __next__(self) :

        was_read, frame = self.cap.read()

        if  not was_read : self.ended  = True
        else             : self.count += 1

        print(f'\r{self.video_w}x{self.video_h}@{self.video_r} fps : {self.count:>4} / {self.video_c} : {self.count / self.video_c * 100 : 5.1f} % = ', end = '')

        return was_read, frame

    def clean(self) :

        self.cap.release()

def predict(batch) :

    pass

def overlay_init() :

    if  cfg.DETECTION.ENABLE:
      # load object detector from detectron2
        dtron2_cfg_file = cfg.DEMO.DETECTRON2_OBJECT_DETECTION_MODEL_CFG
        dtron2_cfg      = get_cfg()
        dtron2_cfg.merge_from_file(model_zoo.get_config_file(dtron2_cfg_file))
        dtron2_cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = .5
        dtron2_cfg.MODEL.WEIGHTS = cfg.DEMO.DETECTRON2_OBJECT_DETECTION_MODEL_WEIGHTS
        object_predictor = DefaultPredictor(dtron2_cfg)
      # load the labels of AVA dataset
        with open(cfg.DEMO.LABEL_FILE_PATH) as f:
            labels = f.read().split('\n')[:-1]
        palette = np.random.randint(64, 128, (len(labels), 3)).tolist()
        boxes   = []

        mode    = 'Detection'

    else:
      # load the labels of Kinectics-400 dataset
        labels_df = pd.read_csv(cfg.DEMO.LABEL_FILE_PATH)
        labels    = labels_df['name'].values

        mode    = 'Classify'

def overlay(batch) :

    if  cfg.DETECTION.ENABLE and pred_labels and boxes.any():

        for box, box_labels in zip(boxes.astype(int), pred_labels):
            cv.rectangle(frame, tuple(box[:2]), tuple(box[2:]), (0, 255, 0), thickness=2)
            label_origin = box[:2]
            for label in box_labels:
                label_origin[-1] -= 5
                (label_width, label_height), _ = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, .5, 2)
                cv.rectangle(
                    frame, 
                    (label_origin[0], label_origin[1] + 5), 
                    (label_origin[0] + label_width, label_origin[1] - label_height - 5),
                    palette[labels.index(label)], -1
                )
                cv.putText(
                    frame, label, tuple(label_origin), 
                    cv.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1
                )
                label_origin[-1] -= label_height + 5

    if  not cfg.DETECTION.ENABLE:
        # display predicted labels to frame
        y_offset = 50
        cv.putText(frame, 'Action:', (10, y_offset), 
                            fontFace=cv.FONT_HERSHEY_SIMPLEX,
                            fontScale=.65, color=(0, 235, 0), thickness=2)        
        for pred_label in pred_labels:
            y_offset += 30
            cv.putText(frame, '{}'.format(pred_label), (20, y_offset), 
                        fontFace=cv.FONT_HERSHEY_SIMPLEX,
                        fontScale=.65, color=(0, 235, 0), thickness=2)

  # display prediction speed
    cv.putText(frame, f'Speed: {s:.2f}s', (10, 25), 
                fontFace  = cv.FONT_HERSHEY_SIMPLEX,
                fontScale = .65,
                color     = (0, 235, 0),
                thickness = 2)
  # display the frame
    cv.imwrite('', frame)   

def process(cfg, video) :

    np.random.seed(cfg.RNG_SEED)
    to.manual_seed(cfg.RNG_SEED)

    model = build_model(cfg)

    if  cfg.TRAIN.CHECKPOINT_FILE_PATH != '' :

        cu.load_checkpoint(
            cfg.TRAIN.CHECKPOINT_FILE_PATH,
            model,
            cfg.NUM_GPUS > 1,
            None,
            inflation           = False,
            convert_from_caffe2 = cfg.TRAIN.CHECKPOINT_TYPE == 'caffe2',
        )

    else                                     : raise NotImplementedError('Unable to Locate Model Checkpoint')

    seq_len     = cfg.DATA.NUM_FRAMES * cfg.DATA.SAMPLING_RATE
    frames      = []
    pred_labels = []
    s           = 0.

    batch_count = 0
    batch       = []

    labels      = pd.read_csv(f'{tools}/sf-depends/kinetics/labels.csv')['name'].values
  
    system('clear')
    print(f'Starting Video Analysis')
    print(len(labels), cfg.DETECTION.ENABLE)

    for able_to_read, frame in video:

        if  not able_to_read:
          # when reaches the end frame, clear the buffer and continue to the next one.
            frames = []
            break

        if  len(frames) != seq_len :

            frame_processed = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            frame_processed = scale(cfg.DATA.TEST_CROP_SIZE, frame_processed)
            frames.append(frame_processed)

            if  cfg.DETECTION.ENABLE and len(frames) == seq_len // 2 - 1 :
                mid_frame = frame

        if  len(frames) == seq_len :

            start = time()

            if  cfg.DETECTION.ENABLE :

                outputs        = object_predictor(mid_frame)
                fields         = outputs['instances']._fields
                pred_classes   = fields['pred_classes']
                selection_mask = pred_classes == 0
              # acquire person boxes
                pred_classes   = pred_classes[selection_mask]
                pred_boxes     = fields['pred_boxes'].tensor[selection_mask]
                scores         = fields['scores'][selection_mask]
                boxes          = scale_boxes(cfg.DATA.TEST_CROP_SIZE, pred_boxes, video.video_h, video.video_w)
                boxes          = to.cat([to.full((boxes.shape[0], 1), float(0)).cuda(), boxes], axis = 1)

            inputs = to.as_tensor(frames).float()
            inputs = inputs / 255.0

            inputs = inputs - to.tensor(cfg.DATA.MEAN) # perform color normalization
            inputs = inputs / to.tensor(cfg.DATA.STD )

            inputs = inputs.permute(3, 0, 1, 2)        # T H W C -> C T H W  
            inputs = inputs.unsqueeze(0)               # 1 C T H W

          # sample frames for the fast pathway
            index  = to.linspace(0, inputs.shape[2] - 1, cfg.DATA.NUM_FRAMES).long()
            path_f = to.index_select(inputs, 2, index)

          # sample frames for the slow pathway
            index  = to.linspace(0, path_f.shape[2] - 1, path_f.shape[2] // cfg.SLOWFAST.ALPHA).long()
            path_s = to.index_select(path_f, 2, index)

          # print(f'fast_pathway.shape={path_f.shape}')
          # print(f'slow_pathway.shape={path_s.shape}')

          # transfer the data to the current GPU device

            inputs = [path_s, path_f]

            tprep  = time() - start
            start  = time()

            for n, path in enumerate(inputs) :
                inputs[n] = path.cuda(non_blocking = True)

            tload  = time() - start
            start  = time()

          # perform the forward pass.

            if  cfg.DETECTION.ENABLE :
                if  not len(boxes)   : pass # preds = to.tensor([])        # when there is nothing in the scene, use a dummy variable to disable all computations below
                else                 : pass # preds = model(inputs, boxes)
            else                     : preds = model(inputs)

            tpred  = time() - start

            print(f'prep {tprep:5.1f}, load {tload:5.1f}, pred {tpred:5.1f}')
            print(len(label_ids))

            label_ids   = to.nonzero(preds.squeeze() > .1).reshape(-1).cpu().detach().numpy()
            print(label_ids)
            pred_labels = labels[label_ids]

            print(*pred_labels, sep = ', ')


            #pred_labels = labels[label_ids]

            # if  cfg.DETECTION.ENABLE:
            #   # this post processing was intendedly assigned to the cpu since my laptop GPU
            #   # RTX 2080 runs out of its memory, if your GPU is more powerful, I'd recommend
            #   # to change this section to make CUDA does the processing
            #     preds = preds.cpu().detach().numpy()
            #     pred_masks = preds > .1
            #     label_ids = [np.nonzero(pred_mask)[0] for pred_mask in pred_masks]
            #     pred_labels = [
            #         [labels[label_id] for label_id in perbox_label_ids]
            #         for perbox_label_ids in label_ids
            #     ]
            #   # unsure how to detectron2 rescales boxes to image original size, so I use
            #   # input boxes of slowfast and rescale back it instead, it's safer and even if boxes
            #   # was not rescaled by cv2_transform.rescale_boxes, it still works
            #     boxes = boxes.cpu().detach().numpy()
            #     ratio = np.min(
            #         [video.video_h, video.video_w]
            #     ) / cfg.DATA.TEST_CROP_SIZE
            #     boxes = boxes[:, 1:] * ratio

            # else:

            #     # option 1: single label inference selected from the highest probability entry.
            #     # label_id = preds.argmax(-1).cpu()
            #     # pred_label = labels[label_id]
            #     # option 2: multi-label inferencing selected from probability entries > threshold

            #     label_ids   = to.nonzero(preds.squeeze() > .1).reshape(-1).cpu().detach().numpy()
            #     pred_labels = labels[label_ids]

            #   # logger.info(pred_labels)
            #     print(*pred_labels, sep = ', ')

            #     if  not list(pred_labels):
            #         pred_labels = ['Unknown']

            # # option 1: remove the oldest frame in the buffer to make place for the new one.
            # # frames.pop(0)
            # # option 2: empty the buffer

            frames = []
            s      = time() - start

      # overlay()

    video.clean()

def arg_parse() :

    from argparse import ArgumentParser, REMAINDER

    '''
    Parse the following arguments for the video training and testing pipeline.
    Args:
        shard_id (int): shard id for the current machine. Starts from 0 to
            num_shards - 1. If single machine is used, then set shard id to 0.
        num_shards (int): number of shards using by the job.
        init_method (str): initialization method to launch the job with multiple
            devices. Options includes TCP or shared file-system for
            initialization. details can be find in
            https://pyto.org/docs/stable/distributed.html#tcp-initialization
        cfg (str): path to the config file.
        opts (argument): provide addtional options from the command line, it
            overwrites the config loaded from file.
        '''

    par = ArgumentParser(
        description='Provide SlowFast video training, testing, and demo pipeline.'
    )

    par.add_argument(
        '--conf',
        dest    = f'conf',
        help    = f'Path to the config file',
        default = f'{sfast}/demo/Kinetics/SLOWFAST_8x8_R50.yaml',
        type    = str,
    )

    par.add_argument(
        '--file',
        dest    = f'file',
        help    = f'Path to the video file',
        default = f'{cache}/btTKApmxrtk.incoming.mp4',
        type    = str,
    )


    par.add_argument(
        'opts',
        help    ='See slowfast/config/defaults.py for all options',
        default = None,
        nargs   = REMAINDER,
    )

    return par.parse_args()

def cfg_load(arg):

    '''
    Given the arguemnts, load and initialize the configs.
    Args:
        arg (argument): `conf`, and `opts`.
    '''

  # setup cfg.

    cfg = get_cfg()

  # load config from cfg.

    if  arg.conf is not None:
        cfg.merge_from_file(arg.conf)
    
  # load config from command line, overwrite config from opts.

    if  arg.opts is not None:
        cfg.merge_from_list(arg.opts)

  # create the checkpoint dir.

    cu.make_checkpoint_dir(cfg.OUTPUT_DIR)

    return cfg

def main():

    arg = arg_parse()
    cfg = cfg_load(arg)

    mp4 = VideoReader(file = arg.file)

    process(cfg = cfg, video = mp4)

if  __name__ == '__main__':

  # to.multiprocessing.set_start_method('forkserver')

    main()
