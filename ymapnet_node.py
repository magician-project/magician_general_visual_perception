#!/usr/bin/env python3
"""ROS2 node: subscribes to a camera image topic, runs Y-MAP-Net pose
estimation, and publishes keypoint results as JSON and an annotated image."""

import json
import os
import sys

# Y-MAP-Net lives next to this scripts/ directory.
# YMAPNet.__init__ resolves all model paths relative to cwd, so we chdir first.
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
YMAP_NET_DIR = os.path.abspath(os.path.join(_SCRIPTS_DIR, '..', 'Y-MAP-Net'))
os.chdir(YMAP_NET_DIR)
sys.path.insert(0, YMAP_NET_DIR)

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String


class YMAPNetNode(Node):
    def __init__(self):
        super().__init__('ymapnet_node')

        self.declare_parameter('input_topic', '/camera/image_raw')
        self.declare_parameter('threshold', 84.0)
        self.declare_parameter('depth_iterations', 10)
        self.declare_parameter('vram_limit', 4800)

        input_topic = self.get_parameter('input_topic').value
        threshold = float(self.get_parameter('threshold').value)
        depth_iterations = int(self.get_parameter('depth_iterations').value)
        vram_limit = int(self.get_parameter('vram_limit').value)

        self.bridge = CvBridge()

        self.get_logger().info(f'Loading Y-MAP-Net from {YMAP_NET_DIR}')
        from YMAPNet import YMAPNet
        self.estimator = YMAPNet(
            modelPath='2d_pose_estimation',
            threshold=int(threshold),
            keypoint_threshold=threshold,
            engine='tensorflow',
            profiling=False,
            illustrate=False,
            pruneTokens=False,
            monitor=[],
            window_arrangement=[],
            screen_w=1920,
            screen_h=1080,
            depth_iterations=depth_iterations,
            estimate_person_id=True,
            resolve_skeleton=True,
            vram_limit=vram_limit,
            compileModel=False,
            show=False,
        )
        self.get_logger().info('Y-MAP-Net model loaded.')

        self.pub_poses = self.create_publisher(String, 'ymapnet/poses', 10)
        self.pub_image = self.create_publisher(Image, 'ymapnet/image', 10)
        self.sub = self.create_subscription(Image, input_topic, self._image_cb, 10)
        self.get_logger().info(f'Subscribed to {input_topic}')

    def _image_cb(self, msg: Image):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'cv_bridge conversion failed: {e}')
            return

        self.estimator.process(frame, static_frame_threshold=0.0)
        self.pub_poses.publish(String(data=json.dumps(self._build_result())))

        vis = frame.copy()
        try:
            self.estimator.visualize(vis, show=False, save=False)
        except Exception as e:
            self.get_logger().warn(f'visualize error (non-fatal): {e}')

        try:
            img_msg = self.bridge.cv2_to_imgmsg(vis, encoding='bgr8')
            img_msg.header = msg.header
            self.pub_image.publish(img_msg)
        except Exception as e:
            self.get_logger().error(f'image publish failed: {e}')

    def _build_result(self) -> dict:
        e = self.estimator
        result = {
            'frame': e.frameNumber,
            'keypoints': [],
            'skeletons': [],
        }

        if e.keypoint_results is not None:
            for i, kp_list in enumerate(e.keypoint_results):
                name = e.keypoint_names[i] if i < len(e.keypoint_names) else str(i)
                depth = (float(e.keypoint_depths[i])
                         if (e.keypoint_depths and i < len(e.keypoint_depths)) else 0.0)
                for x, y, conf in kp_list:
                    result['keypoints'].append({
                        'name': name,
                        'x': float(x),
                        'y': float(y),
                        'confidence': float(conf),
                        'depth': depth,
                    })

        if e.skeletons is not None:
            for i in range(len(e.skeletons)):
                try:
                    result['skeletons'].append(e.encodeSkeletonAsDict(i))
                except Exception:
                    pass

        return result


def main():
    rclpy.init()
    node = YMAPNetNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
