from argparse import ArgumentParser, REMAINDER
from os.path  import basename, splitext
from time     import time, sleep
from sys      import path
from os       import environ, system

path += ['/work/ActIQ/product/engine/tools/sf']

import pandas as pd
import numpy  as np
import torch  as to
import cv2    as cv

from slowfast.config.defaults        import get_cfg as get_cfg_sf
from slowfast.models                 import build_model
from slowfast.utils.misc             import log_model_info
from slowfast.utils.checkpoint       import load_checkpoint
from slowfast.datasets.cv2_transform import scale, scale_boxes

from detectron2        import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg as get_cfg_d2
from detectron2.data   import MetadataCatalog

class FrameProvider(object) :

    def __init__(self, file) :

        self.cap     = cv.VideoCapture(file)

        if  not self.cap.isOpened():
            raise IOError(f'Unable to Locate Video File : {file}')

        self.video   = splitext(basename(file))[0]
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

        if  not was_read : self.ended  = True ; frame = None
        else             : self.count += 1

        print(f'\r{self.video_w}x{self.video_h}@{self.video_r} fps : {self.count:>4} / {self.video_c} : {self.count / self.video_c * 100 : 5.1f} % = ', end = '')

        return frame

    def clean(self) :

        self.cap.release()

def overlay(config, labels, frame , predict_labels, boxes, palette, s, output) :

    if  config.DETECTION.ENABLE and predict_labels and boxes.any() :

        for box, box_labels in zip(boxes.astype(int), predict_labels) :

            cv.rectangle(frame, tuple(box[:2]), tuple(box[2:]), (0, 255, 0), thickness=2)
            label_origin = box[:2]

            for label in box_labels:
                label_origin[-1] -= 5
                (label_width, label_height), _ = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, .5, 2)
                cv.rectangle(frame, (label_origin[0], label_origin[1] + 5), (label_origin[0] + label_width, label_origin[1] - label_height - 5), palette[labels.index(label)], -1)
                cv.putText(frame, label, tuple(label_origin), cv.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1)
                label_origin[-1] -= label_height + 5

    if  not config.DETECTION.ENABLE :
      # display predicted labels to frame
        y_offset = 50
        cv.putText(frame, 'Action:', (10, y_offset), fontFace = cv.FONT_HERSHEY_SIMPLEX, fontScale = .65, color = (0, 235, 0), thickness = 2)

        for predict_label in predict_labels :
            y_offset += 30
            cv.putText(frame, f'{predict_label}', (20, y_offset), fontFace = cv.FONT_HERSHEY_SIMPLEX, fontScale = .65, color = (0, 235, 0), thickness = 2)

  # display prediction speed
    cv.putText(frame, 'Speed: {:.2f}s'.format(s), (10, 25), fontFace = cv.FONT_HERSHEY_SIMPLEX, fontScale = .65, color = (0, 235, 0), thickness = 2)
  # display the frame
    cv.imwrite(output, frame)

def predict(config, labels, frames, csv, stime, etime, enabled) :

    np.random.seed(config.RNG_SEED)
    to.manual_seed(config.RNG_SEED)

  # print(config)

    np.random.seed(config.RNG_SEED)
    to.manual_seed(config.RNG_SEED)

    model = build_model(config)
    model.eval()

  # log_model_info(model)

    if  config.TRAIN.CHECKPOINT_FILE_PATH != '' :

        load_checkpoint(
            config.TRAIN.CHECKPOINT_FILE_PATH,
            model,
            config.NUM_GPUS > 1,
            None,
            inflation           = False,
            convert_from_caffe2 = config.TRAIN.CHECKPOINT_TYPE == 'caffe2',
        )

    else                                        : raise NotImplementedError('Unable to Locate Model Checkpoint')

    if  config.DETECTION.ENABLE :

      # load object detector from detectron2
        cfg_d2                                   = get_cfg_d2()
        cfg_d2.merge_from_file(model_zoo.get_config_file('COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml'))
        cfg_d2.MODEL.ROI_HEADS.SCORE_THRESH_TEST = .5
        cfg_d2.MODEL.WEIGHTS                     = 'detectron2://COCO-Detection/faster_rcnn_R_50_FPN_3x/137849458/model_final_280758.pkl'
        object_predictor                         = DefaultPredictor(cfg_d2)

      # load the labels of AVA dataset
        labels  = pd.read_csv(labels)['name'].values.tolist()
    else :
      # load the labels of Kinectics-400 dataset
        labels  = pd.read_csv(labels)['name'].values

    threshold      = .01
    boxes          = []
    palette        = np.random.randint(64, 128, (len(labels), 3)).tolist()
    segment_number = 0
    segment_length = config.DATA.NUM_FRAMES * config.DATA.SAMPLING_RATE
    segment_frames = []
    predict_labels = []

    rows           = []

    for frame in frames :

        if  frame is None :
            break

        if  len(segment_frames) != segment_length : # collect segment frames

            frame_processed = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            frame_processed = scale(config.DATA.TEST_CROP_SIZE, frame_processed)
            segment_frames.append(frame_processed)

            if  config.DETECTION.ENABLE and len(segment_frames) == segment_length // 2 - 1 :

                frame_mid = frame
            
        if  len(segment_frames) == segment_length : # predict segment

            start = time()

            if  config.DETECTION.ENABLE :

                output         = object_predictor(frame_mid)
                fields         = output['instances']._fields
                pred_classes   = fields['pred_classes']
                selection_mask = pred_classes == 0
              # acquire person boxes
                pred_classes   = pred_classes[selection_mask]
                pred_boxes     = fields['pred_boxes'].tensor[selection_mask]
                scores         = fields['scores'    ][selection_mask]
                boxes          = scale_boxes(config.DATA.TEST_CROP_SIZE, pred_boxes, frames.video_h, frames.video_w)
                boxes          = to.cat([to.full((boxes.shape[0], 1), float(0)).cuda(), boxes], axis = 1)

            inputs = to.as_tensor(segment_frames).float()
            inputs = inputs / 255.0
            inputs = inputs - to.tensor(config.DATA.MEAN) # perform color normalization
            inputs = inputs / to.tensor(config.DATA.STD)
            inputs = inputs.permute(3, 0, 1, 2)           # T H W C -> C T H W
            inputs = inputs.unsqueeze(0)                  # 1 C T H W

            index  = to.linspace(0,  inputs.shape[2] - 1, config.DATA.NUM_FRAMES                  ).long() # sample frames for the fast pathway
            fast_p = to.index_select(inputs, 2, index)

            index  = to.linspace(0,  fast_p.shape[2] - 1, fast_p.shape[2] // config.SLOWFAST.ALPHA).long() # sample frames for the slow pathway
            slow_p = to.index_select(fast_p, 2, index)

          # print(f'fast_p.shape={fast_p.shape}')
          # print(f'slow_p.shape={slow_p.shape}')

          # transfer the data to the current GPU device

            inputs = [slow_p, fast_p]

            for i in range(len(inputs)) :
                inputs[i] = inputs[i].cuda(non_blocking = True)

          # perform the forward pass

            if  config.DETECTION.ENABLE :
                if not len(boxes) : predict_score = to.tensor([])        # when there is nothing in the scene, use a dummy variable to disable all computations below
                else              : predict_score = model(inputs, boxes)
            else                  : predict_score = model(inputs)

            if  config.DETECTION.ENABLE :

              # this post processing was intendedly assigned to the cpu since my laptop GPURTX 2080 runs out of its memory, if your GPU is more powerful, I'd recommend to change this section to make CUDA does the processing.
                predict_score = predict_score.cpu().detach().numpy()
                predict_masks = predict_score > threshold                                         # predicted probs > threshold

                predict_probs = [pbox[mask] for pbox, mask in zip(predict_score, predict_masks) ] # predicted probs
                predict_pflat = [prob       for pbox in predict_probs for prob in pbox          ] # predicted probs flat

                predict_index = [np.nonzero(predict_mask)[0] for predict_mask in predict_masks  ] # predicted class index
                predict_class = [[labels[id] for id in box_clids] for box_clids in predict_index] # predicted class label
                predict_cflat = [ labels[id] for box_clids in predict_index for id in box_clids ] # predicted class label flat
                predict_iflat = [        id  for box_clids in predict_index for id in box_clids ] # predicted class index flat

              # unsure how to detectron2 rescales boxes to image original size, so use input boxes of slowfast and rescale back it instead, it's safer and even if boxes was not rescaled by cv2_transform.rescale_boxes, it still works
                boxes = boxes.cpu().detach().numpy()
                ratio = np.min([frames.video_h, frames.video_w]) / config.DATA.TEST_CROP_SIZE
                boxes = boxes[:, 1:] * ratio

            else :

                predict_index = to.nonzero(predict_score.squeeze() > threshold).reshape(-1).cpu().detach().numpy()
                predict_probs = \
                predict_pflat = predict_score[predict_score > threshold].cpu().detach().numpy()
                predict_cflat = \
                predict_class = labels[predict_index]

            micros  = int(frames.count / frames.video_r * 10 ** 6)
            ranked  = [f'{c}:{p}' for p, c in sorted(zip(predict_pflat, predict_cflat), reverse = True)][:10]
            ranked  = ranked + ['unknown:0.0'] * (10 - len(ranked))
            rows   += [[micros] + ranked]

            pd.DataFrame(rows).to_csv(csv, index = False, header = False)

            print(f'{micros} uS')
            for n, x in enumerate(ranked) :
                print(n, x)
            print()

            if  enabled :
                overlay(config, labels, frame, predict_class, boxes, palette, time() - start, f'{csv.split(".classify")[0]}.overlays.{frames.count:04d}.jpg')

            segment_frames  = []
            segment_number += 1

            if  int(frames.count / frames.video_r) >= etime :
                break

    frames.clean()

if  __name__ == '__main__' :

    parser = ArgumentParser(description = 'ActIQ SlowFast Prediction Pipeline')

    parser.add_argument('--config' , dest = f'config' , default =    '',  type =       str)
    parser.add_argument('--labels' , dest = f'labels' , default =    '',  type =       str)
    parser.add_argument('--overlay', dest = f'overlay', default = False,  type =      bool)
    parser.add_argument('--video'  , dest = f'video'  , default =  None,  type =       str)
    parser.add_argument('--csv'    , dest = f'csv'    , default =    '',  type =       str)
    parser.add_argument('--stime'  , dest = f'stime'  , default =     0,  type =       int)
    parser.add_argument('--etime'  , dest = f'etime'  , default =   120,  type =       int)    
    parser.add_argument(  'option' ,                    default =  None, nargs = REMAINDER)

    parsed = parser.parse_args()
    config = get_cfg_sf()
    frames = FrameProvider(parsed.video)

    if  parsed.config : config.merge_from_file(parsed.config)
    if  parsed.option : config.merge_from_list(parsed.option)

    labels = parsed.config.replace('.yaml', '.csv') if not parsed.labels else \
             parsed.labels

    csv    = parsed.video.replace('.incoming.mp4', f'.classify.{"av" if config.DETECTION.ENABLE else "ki"}.csv') if not parsed.csv else \
             parsed.csv

    predict(config = config, labels = labels, frames = frames, csv = csv, stime = parsed.stime, etime = parsed.etime, enabled = parsed.overlay)
