"""
skills/youtube-history-animator/scripts/skeletal_puppet_engine.py
Python companion module for Skeletal IK Puppet configurations,
bounding boxes, and behavior sequence generator matching broadcast OverSimplified standards.
"""

import math


class SkeletalPuppetPython:
    """Python-side representation of skeletal character rig for layout & scene composition."""

    def __init__(self, name="Actor", x=960, y=890, scale=1.0, facing=1, hat_type=None):
        self.name = name
        self.x = x
        self.y = y
        self.scale = scale
        self.facing = facing
        self.hat_type = hat_type

        # Broadcast proportions (~480px total height)
        s = self.scale
        self.torso_width = 100 * s
        self.torso_height = 160 * s
        self.upper_arm_length = 76 * s
        self.forearm_length = 70 * s
        self.thigh_length = 80 * s
        self.shin_length = 76 * s
        self.head_radius_x = 64 * s
        self.head_radius_y = 72 * s

    @staticmethod
    def solve_two_bone_ik(origin_x, origin_y, target_x, target_y, l1, l2, flip=False):
        """Analytical 2-bone IK solver using Law of Cosines."""
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
