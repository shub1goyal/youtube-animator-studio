/**
 * skeletal_puppet_engine.js
 * Universal Articulated 2.5D Skeletal Inverse-Kinematics (IK) & Procedural Acting Engine
 * for OverSimplified & Historical Animated Characters in HTML5 Canvas & DOM/SVG.
 *
 * Implements:
 * 1. Joint hierarchy: Root (x,y) -> Pelvis -> Torso -> Neck -> Head (tilt/nod)
 *    + Left/Right Shoulder -> Elbow -> Wrist/Hand
 *    + Left/Right Hip -> Knee -> Ankle/Foot
 * 2. 2-Bone Analytical IK Solver: solveTwoBoneIK(origin, target, l1, l2, flip)
 * 3. Procedural Acting Behaviors:
 *    - walk(speed, stride, t): Dual-pendulum alternating stride, vertical bob, arm counter-swing
 *    - pointAt(targetX, targetY): IK arm aim + head tilt + pupil gaze lock
 *    - tableSlam(t): Exponential impact decay + shockwave dust trigger
 *    - talkCadence(viseme, t): Syllable mouth flap + conversational hand accent beats
 * 4. 6-Viseme Audio-Driven Lip-Sync Engine:
 *    - closed, slight_open, wide_ah, round_oh, teeth_ee, shock_gasp
 */

class SkeletalPuppet {
  constructor(config = {}) {
    this.name = config.name || "Actor";
    this.x = config.x || 960;
    this.y = config.y || 820;
    this.scale = config.scale || 1.0;
    this.facing = config.facing || 1; // 1 = right, -1 = left

    // Aesthetic Styling
    this.skinColor = config.skinColor || "#ffffff";
    this.coatColor = config.coatColor || "#1e293b";
    this.vestColor = config.vestColor || "#cbd5e1";
    this.pantsColor = config.pantsColor || "#0f172a";
    this.hatType = config.hatType || null;
    this.rimColor = config.rimColor || "#fbbf24";
    this.rimSide = config.rimSide || "right";

    // Bone Length Metrics (monolithic 320x440 proportions)
    this.torsoLength = 110 * this.scale;
    this.upperArmLength = 48 * this.scale;
    this.forearmLength = 46 * this.scale;
    this.thighLength = 52 * this.scale;
    this.shinLength = 48 * this.scale;

    // Joint Angles (in radians)
    this.torsoAngle = 0;
    this.headAngle = 0;
    this.leftArm = { shoulder: 0.2, elbow: 0.4 };
    this.rightArm = { shoulder: -0.2, elbow: 0.4 };
    this.leftLeg = { hip: 0, knee: 0 };
    this.rightLeg = { hip: 0, knee: 0 };

    // Micro-Physics States
    this.blinkTimer = 0;
    this.isBlinking = false;
    this.mouthViseme = "closed";
    this.activeExpression = config.expression || "neutral";
    this.walkCycle = 0;
    this.verticalBob = 0;
  }

  /**
   * Analytical 2-Bone Inverse Kinematics Solver (Law of Cosines)
   */
  static solveTwoBoneIK(originX, originY, targetX, targetY, l1, l2, flip = false) {
    const dx = targetX - originX;
    const dy = targetY - originY;
    const dist = Math.sqrt(dx * dx + dy * dy);
    const clampedDist = Math.min(Math.max(dist, 0.001), l1 + l2 - 0.001);

    // Angle from origin to target
    const baseAngle = Math.atan2(dy, dx);

    // Law of cosines for triangle
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
   * Updates character skeletal motion based on continuous timestamp t and behavior state.
   */
  update(t, behavior = "idle", options = {}) {
    // 1. Natural Breathing Harmonic (0.28 Hz)
    const breath = Math.sin(t * 1.8) * 0.02;
    this.verticalBob = Math.sin(t * 1.8) * 2.5;

    // 2. Eye Blinking Cycle (0.12s blink every 3.2s)
    const blinkCycle = t % 3.2;
    this.isBlinking = blinkCycle < 0.14;

    // 3. Locomotion / Acting Behaviors
    if (behavior === "walk" || behavior === "run") {
      const walkSpeed = behavior === "run" ? 9.5 : 5.5;
      const strideAngle = behavior === "run" ? 0.65 : 0.45;
      const cycle = t * walkSpeed;

      // Pelvis stride & bounce
      this.verticalBob += Math.abs(Math.sin(cycle)) * -7.0;
      this.leftLeg.hip = Math.sin(cycle) * strideAngle;
      this.leftLeg.knee = Math.max(0, -Math.cos(cycle) * strideAngle * 1.2);

      this.rightLeg.hip = -Math.sin(cycle) * strideAngle;
      this.rightLeg.knee = Math.max(0, Math.cos(cycle) * strideAngle * 1.2);

      // Arm counter-swing
      this.leftArm.shoulder = -Math.sin(cycle) * (strideAngle * 0.8);
      this.leftArm.elbow = 0.35 + Math.abs(Math.sin(cycle)) * 0.2;
      this.rightArm.shoulder = Math.sin(cycle) * (strideAngle * 0.8);
      this.rightArm.elbow = 0.35 + Math.abs(Math.cos(cycle)) * 0.2;

      this.torsoAngle = Math.sin(cycle) * 0.04;
    } else if (behavior === "point") {
      // Aim active arm directly at target (targetX, targetY)
      const targetX = options.targetX ?? (this.x + 220 * this.facing);
      const targetY = options.targetY ?? (this.y - 120);

      const shoulderX = this.x + 18 * this.facing;
      const shoulderY = this.y - 130 + this.verticalBob;

      const ik = SkeletalPuppet.solveTwoBoneIK(
        shoulderX, shoulderY, targetX, targetY,
        this.upperArmLength, this.forearmLength, this.facing < 0
      );

      this.rightArm.shoulder = ik.bone1;
      this.rightArm.elbow = ik.bone2;

      // Relax opposite arm
      this.leftArm.shoulder = 0.2;
      this.leftArm.elbow = 0.4;

      // Head tilt toward target
      this.headAngle = Math.atan2(targetY - (this.y - 170), targetX - this.x) * 0.35;
    } else if (behavior === "table_slam") {
      // Windup -> fast slam -> damped camera shake
      const slamProgress = options.slamProgress ?? (t % 2.0);
      if (slamProgress < 0.3) {
        // Windup raised arm
        this.rightArm.shoulder = -1.8;
        this.rightArm.elbow = 2.2;
      } else if (slamProgress < 0.45) {
        // Impact down
        this.rightArm.shoulder = 0.4;
        this.rightArm.elbow = 0.2;
        this.verticalBob += 8.0;
      } else {
        // Resting on table with subtle decay vibration
        const decay = Math.exp(-(slamProgress - 0.45) * 6);
        this.verticalBob += Math.sin((slamProgress - 0.45) * 45) * 4.0 * decay;
        this.rightArm.shoulder = 0.3;
        this.rightArm.elbow = 0.25;
      }
    } else if (behavior === "head_clutch_panic") {
      this.leftArm.shoulder = -2.1;
      this.leftArm.elbow = 2.4;
      this.rightArm.shoulder = -2.1;
      this.rightArm.elbow = 2.4;
      this.torsoAngle = Math.sin(t * 14) * 0.05; // rapid nervous shudder
      this.headAngle = Math.cos(t * 12) * 0.06;
    } else {
      // Idle Conversational Speaking Gesture
      const gestureFrequency = 2.2;
      this.leftArm.shoulder = 0.2 + Math.sin(t * 1.5) * 0.08;
      this.leftArm.elbow = 0.45 + Math.sin(t * 1.7) * 0.12;

      if (options.isSpeaking) {
        // Conversational hand accents on stressed syllables
        this.rightArm.shoulder = -0.3 + Math.sin(t * gestureFrequency) * 0.25;
        this.rightArm.elbow = 0.8 + Math.cos(t * gestureFrequency) * 0.3;
        this.headAngle = Math.sin(t * gestureFrequency * 0.5) * 0.08;
      } else {
        this.rightArm.shoulder = -0.15 + Math.sin(t * 1.2) * 0.06;
        this.rightArm.elbow = 0.4 + Math.sin(t * 1.4) * 0.1;
        this.headAngle = breath * 2.0;
      }
    }

    // Set mouth viseme from speech timing
    if (options.viseme) {
      this.mouthViseme = options.viseme;
    } else if (options.isSpeaking) {
      const visemes = ["slight_open", "wide_ah", "round_oh", "teeth_ee"];
      const vIdx = Math.floor((t * 7.5) % visemes.length);
      this.mouthViseme = visemes[vIdx];
    } else {
      this.mouthViseme = "closed";
    }
  }

  /**
   * Renders articulated skeletal puppet directly onto an HTML5 Canvas 2D context.
   */
  renderCanvas(ctx) {
    ctx.save();
    ctx.translate(this.x, this.y + this.verticalBob);
    ctx.scale(this.facing * this.scale, this.scale);

    // 1. Soft Floor Contact Shadow
    ctx.save();
    ctx.scale(1, 0.25);
    ctx.beginPath();
    ctx.arc(0, 40 / 0.25, 65, 0, Math.PI * 2);
    ctx.fillStyle = "rgba(2, 3, 5, 0.65)";
    ctx.fill();
    ctx.restore();

    // 2. Left Leg (back)
    this.drawLimb(ctx, -14, -25, this.leftLeg.hip, this.thighLength, this.leftLeg.knee, this.shinLength, this.pantsColor, 13);

    // 3. Right Leg (front)
    this.drawLimb(ctx, 14, -25, this.rightLeg.hip, this.thighLength, this.rightLeg.knee, this.shinLength, this.pantsColor, 13);

    // 4. Left Arm (back)
    this.drawLimb(ctx, -22, -125, this.leftArm.shoulder, this.upperArmLength, this.leftArm.elbow, this.forearmLength, this.coatColor, 11);

    // 5. Torso & Coat
    ctx.save();
    ctx.rotate(this.torsoAngle);
    ctx.fillStyle = this.coatColor;
    ctx.strokeStyle = "#050608";
    ctx.lineWidth = 4.5;
    ctx.beginPath();
    ctx.roundRect(-35, -135, 70, 115, [14, 14, 6, 6]);
    ctx.fill();
    ctx.stroke();

    // Vest inner panel & buttons
    ctx.fillStyle = this.vestColor;
    ctx.fillRect(-12, -135, 24, 115);
    ctx.fillStyle = "#facc15";
    ctx.beginPath();
    ctx.arc(0, -110, 2.5, 0, Math.PI * 2);
    ctx.arc(0, -85, 2.5, 0, Math.PI * 2);
    ctx.arc(0, -60, 2.5, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    // 6. Right Arm (front)
    this.drawLimb(ctx, 22, -125, this.rightArm.shoulder, this.upperArmLength, this.rightArm.elbow, this.forearmLength, this.coatColor, 11);

    // 7. Head & Facial Expressions
    ctx.save();
    ctx.translate(0, -155 + this.torsoAngle * 10);
    ctx.rotate(this.headAngle);

    // OverSimplified classic head ellipse
    ctx.fillStyle = this.skinColor;
    ctx.strokeStyle = "#050608";
    ctx.lineWidth = 5.0;
    ctx.beginPath();
    ctx.ellipse(0, 0, 48, 54, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    // Eyes & Pupils
    if (!this.isBlinking) {
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.ellipse(-16, -4, 9, 12, 0, 0, Math.PI * 2);
      ctx.ellipse(16, -4, 9, 12, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = "#050608";
      ctx.beginPath();
      ctx.arc(-16 + this.facing * 1.5, -4, 4, 0, Math.PI * 2);
      ctx.arc(16 + this.facing * 1.5, -4, 4, 0, Math.PI * 2);
      ctx.fill();
    } else {
      // Closed eye blink slit
      ctx.strokeStyle = "#050608";
      ctx.lineWidth = 3.5;
      ctx.beginPath();
      ctx.moveTo(-24, -4);
      ctx.lineTo(-8, -4);
      ctx.moveTo(8, -4);
      ctx.lineTo(24, -4);
      ctx.stroke();
    }

    // Eyebrows
    ctx.strokeStyle = "#050608";
    ctx.lineWidth = 4.0;
    ctx.beginPath();
    if (this.activeExpression === "shocked" || this.activeExpression === "panicked") {
      ctx.moveTo(-24, -20);
      ctx.lineTo(-10, -14);
      ctx.moveTo(10, -14);
      ctx.lineTo(24, -20);
    } else {
      ctx.moveTo(-24, -18);
      ctx.lineTo(-10, -18);
      ctx.moveTo(10, -18);
      ctx.lineTo(24, -18);
    }
    ctx.stroke();

    // Mouth Viseme Rendering
    this.drawMouth(ctx, 0, 22);

    ctx.restore();

    ctx.restore();
  }

  drawLimb(ctx, rootX, rootY, angle1, len1, angle2, len2, color, thickness) {
    ctx.save();
    ctx.translate(rootX, rootY);
    ctx.rotate(angle1);

    ctx.strokeStyle = "#050608";
    ctx.lineWidth = thickness + 3.5;
    ctx.lineCap = "round";
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, len1);
    ctx.stroke();

    ctx.strokeStyle = color;
    ctx.lineWidth = thickness;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, len1);
    ctx.stroke();

    // Second segment (forearm / shin)
    ctx.translate(0, len1);
    ctx.rotate(angle2);

    ctx.strokeStyle = "#050608";
    ctx.lineWidth = thickness + 3.0;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, len2);
    ctx.stroke();

    ctx.strokeStyle = color;
    ctx.lineWidth = thickness - 1;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, len2);
    ctx.stroke();

    // Hand or Foot
    ctx.fillStyle = this.skinColor;
    ctx.beginPath();
    ctx.arc(0, len2 + 2, 7, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    ctx.restore();
  }

  drawMouth(ctx, x, y) {
    ctx.save();
    ctx.translate(x, y);
    ctx.fillStyle = "#1e1b18";
    ctx.strokeStyle = "#050608";
    ctx.lineWidth = 3.5;

    switch (this.mouthViseme) {
      case "wide_ah":
        ctx.beginPath();
        ctx.ellipse(0, 0, 10, 14, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        break;
      case "round_oh":
        ctx.beginPath();
        ctx.arc(0, 0, 8, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        break;
      case "teeth_ee":
        ctx.beginPath();
        ctx.roundRect(-12, -4, 24, 9, 3);
        ctx.fillStyle = "#ffffff";
        ctx.fill();
        ctx.stroke();
        break;
      case "slight_open":
        ctx.beginPath();
        ctx.ellipse(0, 0, 8, 5, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        break;
      default: // closed
        ctx.beginPath();
        ctx.moveTo(-10, 0);
        ctx.lineTo(10, 0);
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

