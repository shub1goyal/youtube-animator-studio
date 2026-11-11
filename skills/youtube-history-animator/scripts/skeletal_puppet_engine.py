"""
skeletal_puppet_engine.py
Python companion module for Skeletal IK Puppet configurations,
bounding boxes, and behavior sequence generator.
"""

import math


class SkeletalPuppetPython:
    """Python-side representation of skeletal character rig for metadata & layout."""

    def __init__(self, name="Actor", x=960, y=820, scale=1.0, facing=1):
        self.name = name
        self.x = x
        self.y = y
        self.scale = scale
        self.facing = facing

    @staticmethod
    def solve_two_bone_ik(origin_x, origin_y, target_x, target_y, l1, l2, flip=False):
        dx = target_x - origin_x
        dy = target_y - origin_y
        dist = math.sqrt(dx * dx + dy * dy)
        clamped_dist = min(max(dist, 0.001), l1 + l2 - 0.001)

        base_angle = math.atan2(dy, dx)
        cos_angle1 = (l1 * l1 + clamped_dist * clamped_dist - l2 * l2) / (2 * l1 * clamped_dist)
        angle1 = math.acos(min(max(cos_angle1, -1), 1))

        cos_angle2 = (l1 * l1 + l2 * l2 - clamped_dist * clamped_dist) / (2 * l1 * l2)
        angle2 = math.acos(min(max(cos_angle2, -1), 1))

        sign = -1 if flip else 1
        bone1_angle = base_angle + sign * angle1
        bone2_angle = bone1_angle + math.pi - sign * angle2

        return {
            "bone1": bone1_angle,
            "bone2": bone2_angle,
            "joint_x": origin_x + math.cos(bone1_angle) * l1,
            "joint_y": origin_y + math.sin(bone1_angle) * l1
        }

