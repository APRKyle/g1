import numpy as np
import math
from .utils import xywh2xyxy, nms, sigmoid
import cv2


class PostProcessor:
    def __init__(self, iou_threshold, class_threshold,
                 input_height, input_width, img_height, img_width,
                  num_masks = 32):
        self.iou_threshold = iou_threshold
        self.clas_threshold = class_threshold
        self.num_masks = num_masks
        self.input_height = input_height
        self.input_width = input_width
        self.img_height = img_height
        self.img_width = img_width



    def process(self, output):

        boxes_data = output[1]
        masks_data = output[0]

        boxes_data = np.reshape(boxes_data, (1, 116, 2730))
        masks_data = np.reshape(masks_data, (1,32,104,80))

        boxes, scores, class_id, mask_predictions = self._process_boxes(boxes_data)


        masks = self._process_masks(mask_predictions, masks_data, boxes)


        return boxes, masks, class_id



    def _process_boxes(self, boxes_data):

        predictions = np.squeeze(boxes_data).T
        num_classes = boxes_data.shape[1] - self.num_masks - 4
        print(f' n_classes: {num_classes}')
        scores = np.max(predictions[:, 4:4 + num_classes], axis=1)
        print(f' scores: {scores}')
        predictions = predictions[scores > self.clas_threshold, :]
        scores = scores[scores > self.clas_threshold]
        box_predictions = predictions[..., :num_classes + 4]
        mask_predictions = predictions[..., num_classes + 4:]
        class_ids = np.argmax(box_predictions[:, 4:], axis=1)


        boxes = self._extract_boxes(box_predictions)

        indices = nms(boxes, scores, self.iou_threshold)

        boxes = boxes[indices]
        scores = scores[indices]
        class_ids = class_ids[indices]

        mask_predictions = mask_predictions[indices]

        return boxes, scores, class_ids, mask_predictions


    def _process_masks(self, mask_predictions, mask_data, boxes):
        mask_output = np.squeeze(mask_data)

        # Calculate the mask maps for each box
        num_mask, mask_height, mask_width = mask_output.shape  # CHW
        masks = sigmoid(mask_predictions @ mask_output.reshape((num_mask, -1)))
        masks = masks.reshape((-1, mask_height, mask_width))

        # Downscale the boxes to match the mask size
        scale_boxes = self._rescale_boxes(boxes,
                                          (self.img_height, self.img_width),
                                          (mask_height, mask_width))

        # For every box/mask pair, get the mask map
        mask_maps = np.zeros((len(scale_boxes), self.img_height, self.img_width))
        blur_size = (int(self.img_width / mask_width), int(self.img_height / mask_height))
        for i in range(len(scale_boxes)):
            scale_x1 = int(math.floor(scale_boxes[i][0]))
            scale_y1 = int(math.floor(scale_boxes[i][1]))
            scale_x2 = int(math.ceil(scale_boxes[i][2]))
            scale_y2 = int(math.ceil(scale_boxes[i][3]))

            x1 = int(math.floor(boxes[i][0]))
            y1 = int(math.floor(boxes[i][1]))
            x2 = int(math.ceil(boxes[i][2]))
            y2 = int(math.ceil(boxes[i][3]))

            scale_crop_mask = masks[i][scale_y1:scale_y2, scale_x1:scale_x2]
            crop_mask = cv2.resize(scale_crop_mask,
                                   (x2 - x1, y2 - y1),
                                   interpolation=cv2.INTER_CUBIC)

            crop_mask = cv2.blur(crop_mask, blur_size)

            crop_mask = (crop_mask > 0.5).astype(np.uint8)
            mask_maps[i, y1:y2, x1:x2] = crop_mask



        return mask_maps

    def _extract_boxes(self, box_predictions):
        boxes = box_predictions[:, :4]
        boxes = self._rescale_boxes(boxes,
                                   (self.input_height, self.input_width),
                                   (self.img_height, self.img_width))
        boxes = xywh2xyxy(boxes)
        boxes[:, 0] = np.clip(boxes[:, 0], 0, self.img_width)
        boxes[:, 1] = np.clip(boxes[:, 1], 0, self.img_height)
        boxes[:, 2] = np.clip(boxes[:, 2], 0, self.img_width)
        boxes[:, 3] = np.clip(boxes[:, 3], 0, self.img_height)

        return boxes


    def _rescale_boxes(self, boxes, input_shape, img_shape):
        input_shape = np.array([input_shape[1], input_shape[0],
                                input_shape[1], input_shape[0]])
        boxes = np.divide(boxes, input_shape, dtype=np.float32)
        boxes *= np.array([img_shape[1], img_shape[0],
                           img_shape[1], img_shape[0]])
        return boxes


