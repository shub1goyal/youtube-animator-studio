/**
 * skeletal_puppet_engine.js
 * Universal Articulated 2.5D Skeletal Inverse-Kinematics (IK) & Procedural Acting Engine
 * for Broadcast-Grade OverSimplified & Historical Animated Characters in HTML5 Canvas.
 *
 * BROADCAST STANDARDS:
 * 1. Broadcast Character Scale: 45%-52% of 1080p canvas (~470px-500px standing height, grounded at Y ~ 890-910px).
 * 2. High-Contrast Limbs: Garment sleeves/trousers (width=24px) wrapped in bold #050608 ink border (width=32px).
 * 3. White Hands: Distinct white circular hands (r=15px, stroke #050608 width=4.5px) for 100% gesture readability.
 * 4. Articulated Joint Hierarchy: Root -> Pelvis -> Torso -> Neck -> Head + Shoulder -> Elbow -> Hand + Hip -> Knee -> Foot.
 * 5. Analytical 2-Bone IK Solver for aiming arms at focal targets.
 * 6. Role Wardrobe & Headwear: Peaked cap, diplomat tie, spectacles, and distinct era accessories.
 * 7. Audio-Driven Lip-Sync Visemes: closed, slight_open, wide_ah, round_oh, teeth_ee.
 */

class SkeletalPuppet {
  constructor(config = {}) {
    this.name = config.name || "Actor";
    this.x = config.x || 960;
    this.y = config.y || 890;
    this.scale = config.scale || 1.0;
    this.facing = config.facing || 1; // 1 = right, -1 = left

    // Wardrobe & Styling
    this.skinColor = config.skinColor || "#fae3cb";
    this.coatColor = config.coatColor || "#1e293b";
    this.vestColor = config.vestColor || "#cbd5e1";
    this.pantsColor = config.pantsColor || "#0f172a";
    this.tieColor = config.tieColor || "#dc2626";
    this.hatType = config.hatType || null; // e.g. "peaked_cap", "spectacles", "tie", "helmet"
    this.hasGlasses = config.hasGlasses || (config.hatType === "spectacles");
    this.rimColor = config.rimColor || "#fbbf24";
    this.rimSide = config.rimSide || "right";

    // Broadcast Proportions (Height ~ 480px at scale = 1.0)
    // Head ~ 150px, Torso ~ 170px, Legs ~ 160px -> Total ~ 480px (45% of 1080p)
    const s = this.scale;
    this.torsoWidth = 100 * s;
    this.torsoHeight = 160 * s;
    this.upperArmLength = 76 * s;
    this.forearmLength = 70 * s;
    this.thighLength = 80 * s;
    this.shinLength = 76 * s;
    this.headRadiusX = 64 * s;
    this.headRadiusY = 72 * s;

    // Joint Angles (in radians)
    this.torsoAngle = 0;
    this.headAngle = 0;
    this.leftArm = { shoulder: 0.25, elbow: 0.35 };
    this.rightArm = { shoulder: -0.25, elbow: 0.35 };
    this.leftLeg = { hip: 0.05, knee: 0.05 };
    this.rightLeg = { hip: -0.05, knee: 0.05 };

    // Micro-Physics States
    this.blinkTimer = 0;
    this.isBlinking = false;
    this.mouthViseme = "closed";
    this.activeExpression = config.expression || "neutral";
    this.walkCycle = 0;
    this.verticalBob = 0;
    this.shakeAmount = 0;
  }

  /**
   * Analytical 2-Bone Inverse Kinematics Solver (Law of Cosines)
   */
  static solveTwoBoneIK(originX, originY, targetX, targetY, l1, l2, flip = false) {
    const dx = targetX - originX;
    const dy = targetY - originY;
    const dist = Math.sqrt(dx * dx + dy * dy);
    const clampedDist = Math.min(Math.max(dist, 0.001), l1 + l2 - 0.001);

    const baseAngle = Math.atan2(dy, dx);
    const cosAngle1 = (l1 * l1 + clampedDist * clampedDist - l2 * l2) / (2 * l1 * clampedDist);
    const angle1 = Math.acos(Math.min(Math.max(cosAngle1, -1), 1));

    const cosAngle2 = (l1 * l1 + l2 * l2 - clampedDist * clampedDist) / (2 * l1 * l2);
    const angle2 = Math.acos(Math.min(Math.max(cosAngle2, -1), 1));

    const sign = flip ? -1 : 1;
    const bone1Angle = baseAngle + sign * angle1;
    const bone2Angle = bone1Angle + Math.PI - sign * angle2;

    return {
      bone1: bone1Angle,
      bone2: bone2Angle,
      jointX: originX + Math.cos(bone1Angle) * l1,
      jointY: originY + Math.sin(bone1Angle) * l1
    };
  }

  /**
   * Point hand at focal coordinate using IK
   */
  pointAt(targetX, targetY, armSide = "front") {
    const s = this.scale;
    const shoulderX = this.x + (armSide === "front" ? 32 * this.facing * s : -32 * this.facing * s);
    const shoulderY = this.y - 210 * s + this.verticalBob;

    const ik = SkeletalPuppet.solveTwoBoneIK(
      shoulderX, shoulderY, targetX, targetY,
      this.upperArmLength, this.forearmLength,
      this.facing < 0
    );

    if (armSide === "front") {
      this.rightArm.shoulder = ik.bone1;
      this.rightArm.elbow = ik.bone2 - ik.bone1;
    } else {
      this.leftArm.shoulder = ik.bone1;
      this.leftArm.elbow = ik.bone2 - ik.bone1;
    }

    // Look slightly toward target
    const angleToTarget = Math.atan2(targetY - (this.y - 280 * s), targetX - this.x);
    this.headAngle = Math.max(-0.35, Math.min(0.35, angleToTarget * 0.4));
  }

  /**
   * Updates character skeletal motion based on continuous timestamp t and behavior state.
   */
  update(t, behavior = "idle", options = {}) {
    const s = this.scale;

    // 1. Natural Breathing Harmonic (0.28 Hz)
    const breath = Math.sin(t * 1.8) * 0.02;
    this.verticalBob = Math.sin(t * 1.8) * 3.0;

    // 2. Eye Blinking Cycle (0.14s blink every 3.2s)
    const blinkCycle = t % 3.4;
    this.isBlinking = blinkCycle > 3.26;

    // 3. Audio Lip-Sync Modulation
    if (options.isSpeaking) {
      const flap = Math.sin(t * 16.0);
      const flap2 = Math.cos(t * 9.5);
      if (flap > 0.5) {
        this.mouthViseme = flap2 > 0 ? "wide_ah" : "round_oh";
      } else if (flap > -0.1) {
        this.mouthViseme = "slight_open";
      } else if (flap > -0.6) {
        this.mouthViseme = "teeth_ee";
      } else {
        this.mouthViseme = "closed";
      }
    } else {
      this.mouthViseme = "closed";
    }

    // 4. Procedural Acting Behaviors
    if (behavior === "talk" || (behavior === "idle" && options.isSpeaking)) {
      this.torsoAngle = breath + Math.sin(t * 3.5) * 0.035;
      this.headAngle = Math.sin(t * 3.5) * 0.055;

      // Conversational hand gesture accents
      const gPhase = t * 4.0;
      this.rightArm.shoulder = -0.55 + Math.sin(gPhase) * 0.22;
      this.rightArm.elbow = 0.95 + Math.cos(gPhase) * 0.28;
      this.leftArm.shoulder = 0.28 + Math.cos(gPhase * 0.5) * 0.12;
      this.leftArm.elbow = 0.45;

      this.leftLeg.hip = 0.05;
      this.leftLeg.knee = 0.05;
      this.rightLeg.hip = -0.05;
      this.rightLeg.knee = 0.05;

    } else if (behavior === "point") {
      const tx = options.targetX || (this.x + this.facing * 420);
      const ty = options.targetY || (this.y - 240);
      this.pointAt(tx, ty, "front");
      this.leftArm.shoulder = 0.35;
      this.leftArm.elbow = 0.55;

    } else if (behavior === "head_clutch_panic" || this.activeExpression === "panicked") {
      this.torsoAngle = Math.sin(t * 18.0) * 0.025; // Terror shiver
      this.headAngle = Math.sin(t * 12.0) * 0.04 - 0.1;

      // Both hands clutching sides of head
      this.rightArm.shoulder = -2.1;
      this.rightArm.elbow = 2.4;
      this.leftArm.shoulder = -2.1;
      this.leftArm.elbow = -2.4;

      this.mouthViseme = "wide_ah";

    } else if (behavior === "table_slam") {
      const impactTime = options.triggerTime || 0.0;
      const relT = t - impactTime;
      if (relT < 0.25) {
        // Wind-up arm raised high
        this.rightArm.shoulder = -2.2;
        this.rightArm.elbow = 1.1;
        this.torsoAngle = -0.15;
      } else if (relT < 0.45) {
        // High-velocity downward slam
        this.rightArm.shoulder = 0.45;
        this.rightArm.elbow = 0.25;
        this.torsoAngle = 0.18;
      } else {
        // Table resting vibration
        const decay = Math.exp(-(relT - 0.45) * 5.0);
        this.torsoAngle = Math.sin(relT * 30.0) * 0.04 * decay;
        this.rightArm.shoulder = 0.25;
        this.rightArm.elbow = 0.65;
      }

    } else if (behavior === "walk") {
      const walkSpeed = 6.0;
      this.walkCycle += 0.06;
      const stride = Math.sin(t * walkSpeed);
      this.leftLeg.hip = stride * 0.42;
      this.leftLeg.knee = Math.max(0, -stride * 0.55);
      this.rightLeg.hip = -stride * 0.42;
      this.rightLeg.knee = Math.max(0, stride * 0.55);

      // Arm counter-swing
      this.leftArm.shoulder = -stride * 0.45;
      this.leftArm.elbow = 0.45;
      this.rightArm.shoulder = stride * 0.45;
      this.rightArm.elbow = 0.45;

      this.verticalBob = Math.abs(Math.sin(t * walkSpeed)) * -10.0;
      this.torsoAngle = stride * 0.04;

    } else {
      // Idle / Listening
      this.torsoAngle = breath;
      if (options.isListening) {
        this.headAngle = -0.09 + Math.sin(t * 1.6) * 0.03; // angled toward speaker
        this.rightArm.shoulder = 0.35;
        this.rightArm.elbow = 1.35; // hand thoughtfully placed near chin
        this.leftArm.shoulder = -0.22;
        this.leftArm.elbow = 0.45;
      } else {
        this.headAngle = -breath * 0.5;
        this.leftArm.shoulder = 0.22 + Math.sin(t * 1.5) * 0.04;
        this.leftArm.elbow = 0.35;
        this.rightArm.shoulder = -0.22 - Math.sin(t * 1.5) * 0.04;
        this.rightArm.elbow = 0.35;
      }
      this.leftLeg.hip = 0.05;
      this.leftLeg.knee = 0.04;
      this.rightLeg.hip = -0.05;
      this.rightLeg.knee = 0.04;
    }
  }

  /**
   * Renders the complete articulated OverSimplified puppet onto HTML5 Canvas.
   */
  renderCanvas(ctx) {
    const s = this.scale;
    ctx.save();
    ctx.translate(this.x, this.y + this.verticalBob);
    ctx.scale(this.facing, 1);

    // 1. Soft Ground Contact Shadow
    ctx.fillStyle = "rgba(2, 4, 8, 0.65)";
    ctx.beginPath();
    ctx.ellipse(0, 4, 110 * s, 24 * s, 0, 0, Math.PI * 2);
    ctx.fill();

    // 2. Back Legs
    this.drawLimb(ctx, -24 * s, -155 * s, this.leftLeg.hip, this.thighLength, this.leftLeg.knee, this.shinLength, this.pantsColor, 22 * s, true);

    // 3. Back Arm
    this.drawLimb(ctx, -32 * s, -280 * s, this.leftArm.shoulder, this.upperArmLength, this.leftArm.elbow, this.forearmLength, this.coatColor, 22 * s, false);

    // 4. Front Leg
    this.drawLimb(ctx, 24 * s, -155 * s, this.rightLeg.hip, this.thighLength, this.rightLeg.knee, this.shinLength, this.pantsColor, 24 * s, true);

    // 5. Articulated Torso with Suit/Vest & Tie
    ctx.save();
    ctx.translate(0, -155 * s);
    ctx.rotate(this.torsoAngle);

    // Outer Torso Jacket (Coat)
    ctx.fillStyle = this.coatColor;
    ctx.strokeStyle = "#050608";
    ctx.lineWidth = 6.0 * s;
    ctx.beginPath();
    ctx.roundRect(-this.torsoWidth / 2, -this.torsoHeight, this.torsoWidth, this.torsoHeight, [22 * s, 22 * s, 10 * s, 10 * s]);
    ctx.fill();
    ctx.stroke();

    // Inner Vest / Shirt Panel
    ctx.fillStyle = this.vestColor;
    ctx.fillRect(-18 * s, -this.torsoHeight, 36 * s, this.torsoHeight);

    // Tie / Neckwear
    if (this.hatType === "peaked_cap" || this.hatType === "military" || this.hatType === "diplomat") {
      ctx.fillStyle = this.tieColor;
      ctx.beginPath();
      ctx.moveTo(-10 * s, -this.torsoHeight + 10 * s);
      ctx.lineTo(10 * s, -this.torsoHeight + 10 * s);
      ctx.lineTo(14 * s, -this.torsoHeight + 90 * s);
      ctx.lineTo(0, -this.torsoHeight + 115 * s);
      ctx.lineTo(-14 * s, -this.torsoHeight + 90 * s);
      ctx.closePath();
      ctx.fill();
      ctx.strokeStyle = "#050608";
      ctx.lineWidth = 3.5 * s;
      ctx.stroke();
    } else {
      // Golden Suit Buttons
      ctx.fillStyle = "#facc15";
      ctx.beginPath();
      ctx.arc(0, -this.torsoHeight + 45 * s, 3.5 * s, 0, Math.PI * 2);
      ctx.arc(0, -this.torsoHeight + 85 * s, 3.5 * s, 0, Math.PI * 2);
      ctx.arc(0, -this.torsoHeight + 125 * s, 3.5 * s, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.restore();

    // 6. Front Arm (high contrast sleeves)
    this.drawLimb(ctx, 32 * s, -280 * s, this.rightArm.shoulder, this.upperArmLength, this.rightArm.elbow, this.forearmLength, this.coatColor, 24 * s, false);

    // 7. Expressive OverSimplified Head & Facial Features
    ctx.save();
    ctx.translate(0, -325 * s + this.torsoAngle * 15 * s);
    ctx.rotate(this.headAngle);

    // Head Base (Clean OverSimplified egg/oval with zero side ovals)
    ctx.fillStyle = this.skinColor;
    ctx.strokeStyle = "#050608";
    ctx.lineWidth = 7.0 * s;
    ctx.beginPath();
    ctx.ellipse(0, 0, this.headRadiusX, this.headRadiusY, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    // Eyes (OverSimplified Large expressive whites)
    if (!this.isBlinking) {
      const eyeR_X = 14 * s;
      const eyeR_Y = 18 * s;
      const pupilR = 6.5 * s;
      const pupilShift = this.facing * 3.0 * s;

      // Left Eye
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = "#050608";
      ctx.lineWidth = 4.5 * s;
      ctx.beginPath();
      ctx.ellipse(-24 * s, -4 * s, eyeR_X, eyeR_Y, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Right Eye
      ctx.beginPath();
      ctx.ellipse(24 * s, -4 * s, eyeR_X, eyeR_Y, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Left Pupil
      ctx.fillStyle = "#050608";
      ctx.beginPath();
      ctx.arc(-24 * s + pupilShift, -4 * s, pupilR, 0, Math.PI * 2);
      ctx.fill();
      // Pupil Catchlight
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(-26 * s + pupilShift, -7 * s, 2.2 * s, 0, Math.PI * 2);
      ctx.fill();

      // Right Pupil
      ctx.fillStyle = "#050608";
      ctx.beginPath();
      ctx.arc(24 * s + pupilShift, -4 * s, pupilR, 0, Math.PI * 2);
      ctx.fill();
      // Pupil Catchlight
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(22 * s + pupilShift, -7 * s, 2.2 * s, 0, Math.PI * 2);
      ctx.fill();

      // Spectacles if enabled
      if (this.hasGlasses) {
        ctx.strokeStyle = "#050608";
        ctx.lineWidth = 4.0 * s;
        ctx.beginPath();
        ctx.ellipse(-24 * s, -4 * s, eyeR_X + 4 * s, eyeR_Y + 4 * s, 0, 0, Math.PI * 2);
        ctx.ellipse(24 * s, -4 * s, eyeR_X + 4 * s, eyeR_Y + 4 * s, 0, 0, Math.PI * 2);
        ctx.moveTo(-6 * s, -4 * s);
        ctx.lineTo(6 * s, -4 * s);
        ctx.stroke();
      }

    } else {
      // Closed Eye Blink Slit
      ctx.strokeStyle = "#050608";
      ctx.lineWidth = 4.5 * s;
      ctx.beginPath();
      ctx.moveTo(-36 * s, -4 * s);
      ctx.lineTo(-12 * s, -4 * s);
      ctx.moveTo(12 * s, -4 * s);
      ctx.lineTo(36 * s, -4 * s);
      ctx.stroke();
    }

    // Bold Eyebrows
    ctx.strokeStyle = "#050608";
    ctx.lineWidth = 6.0 * s;
    ctx.lineCap = "round";
    ctx.beginPath();
    if (this.activeExpression === "panicked" || this.activeExpression === "shocked") {
      ctx.moveTo(-36 * s, -32 * s);
      ctx.lineTo(-14 * s, -22 * s);
      ctx.moveTo(14 * s, -22 * s);
      ctx.lineTo(36 * s, -32 * s);
    } else if (this.activeExpression === "thinking") {
      ctx.moveTo(-36 * s, -34 * s);
      ctx.lineTo(-14 * s, -24 * s);
      ctx.moveTo(14 * s, -28 * s);
      ctx.lineTo(36 * s, -28 * s);
    } else {
      ctx.moveTo(-34 * s, -26 * s);
      ctx.lineTo(-14 * s, -26 * s);
      ctx.moveTo(14 * s, -26 * s);
      ctx.lineTo(34 * s, -26 * s);
    }
    ctx.stroke();

    // Audio Lip-Sync Mouth
    this.drawMouth(ctx, 0, 32 * s);

    // Optional Role Headwear: Peaked Military / Commander Cap
    if (this.hatType === "peaked_cap" || this.hatType === "military") {
      ctx.save();
      ctx.translate(0, -this.headRadiusY + 12 * s);
      // Cap Crown
      ctx.fillStyle = this.coatColor;
      ctx.strokeStyle = "#050608";
      ctx.lineWidth = 5.5 * s;
      ctx.beginPath();
      ctx.moveTo(-68 * s, 0);
      ctx.lineTo(-76 * s, -45 * s);
      ctx.quadraticCurveTo(0, -65 * s, 76 * s, -45 * s);
      ctx.lineTo(68 * s, 0);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      // Gold Band
      ctx.fillStyle = "#facc15";
      ctx.fillRect(-68 * s, -12 * s, 136 * s, 14 * s);
      ctx.strokeStyle = "#050608";
      ctx.lineWidth = 3.5 * s;
      ctx.strokeRect(-68 * s, -12 * s, 136 * s, 14 * s);

      // Gold Cockade / Insignia
      ctx.fillStyle = "#ef4444";
      ctx.beginPath();
      ctx.arc(0, -22 * s, 8 * s, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Black Visor
      ctx.fillStyle = "#090a0f";
      ctx.beginPath();
      ctx.moveTo(-62 * s, 2 * s);
      ctx.quadraticCurveTo(0, 24 * s, 62 * s, 2 * s);
      ctx.quadraticCurveTo(0, 10 * s, -62 * s, 2 * s);
      ctx.fill();
      ctx.stroke();
      ctx.restore();
    }

    ctx.restore(); // Head restore
    ctx.restore(); // Character restore
  }

  /**
   * Draws a 2-segment articulated limb with high-contrast colored garment & bold ink outer border.
   */
  drawLimb(ctx, rootX, rootY, angle1, len1, angle2, len2, color, thickness, isLeg = false) {
    const s = this.scale;
    ctx.save();
    ctx.translate(rootX, rootY);
    ctx.rotate(angle1);

    // Segment 1 (Upper Arm / Thigh) - Outer Ink Border
    ctx.strokeStyle = "#050608";
    ctx.lineWidth = thickness + 8.0 * s;
    ctx.lineCap = "round";
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, len1);
    ctx.stroke();

    // Segment 1 - Garment Fill
    ctx.strokeStyle = color;
    ctx.lineWidth = thickness;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, len1);
    ctx.stroke();

    // Segment 2 (Forearm / Shin)
    ctx.translate(0, len1);
    ctx.rotate(angle2);

    // Segment 2 - Outer Ink Border
    ctx.strokeStyle = "#050608";
    ctx.lineWidth = thickness + 7.0 * s;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, len2);
    ctx.stroke();

    // Segment 2 - Garment Fill
    ctx.strokeStyle = color;
    ctx.lineWidth = thickness - 1.5 * s;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, len2);
    ctx.stroke();

    if (isLeg) {
      // Rounded Shoe / Boot
      ctx.fillStyle = "#090b10";
      ctx.strokeStyle = "#050608";
      ctx.lineWidth = 4.5 * s;
      ctx.beginPath();
      ctx.ellipse(8 * s, len2 + 4 * s, 24 * s, 12 * s, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    } else {
      // Crisp White Circular Hand
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = "#050608";
      ctx.lineWidth = 4.5 * s;
      ctx.beginPath();
      ctx.arc(0, len2 + 4 * s, 15 * s, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    }

    ctx.restore();
  }

  /**
   * Draws 6-viseme lip-sync mouth shape.
   */
  drawMouth(ctx, x, y) {
    const s = this.scale;
    ctx.save();
    ctx.translate(x, y);
    ctx.fillStyle = "#1e1b18";
    ctx.strokeStyle = "#050608";
    ctx.lineWidth = 4.0 * s;

    switch (this.mouthViseme) {
      case "wide_ah":
        ctx.beginPath();
        ctx.ellipse(0, 0, 15 * s, 20 * s, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        // Inner tongue
        ctx.fillStyle = "#f43f5e";
        ctx.beginPath();
        ctx.arc(0, 10 * s, 8 * s, 0, Math.PI);
        ctx.fill();
        break;

      case "round_oh":
        ctx.beginPath();
        ctx.arc(0, 0, 13 * s, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        break;

      case "teeth_ee":
        ctx.fillStyle = "#ffffff";
        ctx.beginPath();
        ctx.roundRect(-18 * s, -6 * s, 36 * s, 14 * s, 4 * s);
        ctx.fill();
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(-18 * s, 1 * s);
        ctx.lineTo(18 * s, 1 * s);
        ctx.stroke();
        break;

      case "slight_open":
        ctx.beginPath();
        ctx.ellipse(0, 0, 12 * s, 8 * s, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        break;

      default: // closed
        ctx.lineCap = "round";
        ctx.beginPath();
        ctx.moveTo(-14 * s, 0);
        ctx.lineTo(14 * s, 0);
        ctx.stroke();
        break;
    }
    ctx.restore();
  }
}

// Export for Node/CommonJS or Browser global
if (typeof module !== "undefined" && module.exports) {
  module.exports = { SkeletalPuppet };
} else if (typeof window !== "undefined") {
  window.SkeletalPuppet = SkeletalPuppet;
}
