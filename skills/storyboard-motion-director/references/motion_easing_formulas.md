# Motion Easing Formulas & Animation Kinetics

Professional motion design reference for After Effects, Cavalry, and code-based animations.

---

## 1. The Core Easing Principles for Educational History Animations

Linear motion feels robotic and amateur. Professional YouTube animators (OverSimplified, Johnny Harris, Kurzgesagt) use exponential ease-out curves and overshoot bounces to give 2D vectors weight, impact, and charm.

### The Standard Cubic-Bezier Curves
- **Snappy Pop-In (Objects, Price Tags, Icons)**:
  `cubic-bezier(0.175, 0.885, 0.32, 1.275)` (Slight overshoot bounce)
- **Smooth Territory Reveal (Trim Paths)**:
  `cubic-bezier(0.16, 1, 0.3, 1)` (Ultra-fast start, long cinematic decelerating tail)
- **Camera Whip-Pan**:
  `cubic-bezier(0.7, 0, 0.3, 1)` (Rapid acceleration into maximum velocity, sharp deceleration into rest)

---

## 2. After Effects Expression Snippets

### A. Automatic Inertial Bounce / Overshoot
Paste this expression onto the `Scale` or `Position` property of a layer to create an automatic, organic bounce without hand-keyframing:

```javascript
// Inertial Bounce for Scale or Position
n = 0;
if (numKeys > 0){
  n = nearestKey(time).index;
  if (key(n).time > time){
    n--;
  }
}
if (n == 0){
  t = 0;
} else {
  t = time - key(n).time;
}
if (n > 0 && t < 1){
  v = velocityAtTime(key(n).time - ((thisComp.frameDuration)?thisComp.frameDuration:0.001));
  amp = 0.05; // Amplitude of bounce
  freq = 4.0; // Frequency of bounce
  decay = 8.0; // Decay rate
  value + v*amp*Math.sin(freq*t*2*Math.PI)/Math.exp(decay*t);
} else {
  value;
}
```

### B. Subtle Organic Breathing / Idling Expression
Apply to the `Scale` property of static characters to keep them subtly alive during long voiceover segments:

```javascript
// 2D Breathing / Idle Pulse
x = value[0] + Math.sin(time * 3) * 1.5;
y = value[1] - Math.sin(time * 3) * 1.5;
[x, y];
```

### C. Hand-Drawn Wiggle / Boil Effect (History Matters Style)
Apply to a `Posterize Time` adjustment layer or layer `Transform` to mimic traditional frame-by-frame slight line jitter:

```javascript
// Subtle Hand-Drawn Boil
posterizeTime(8); // Limit to 8 or 12 fps
wiggle(4, 2);
```

---

## 3. Kinetic Typography & Subtitle Synchronization

For 9:16 Shorts and high-impact 16:9 moments, text must be synchronized with voice syllables:
1. **Word Chunking**: Display 1 to 3 words at a time. Never show a long paragraph of text.
2. **Placement**:
   - 9:16 Shorts: Position at Y = 62% to 68% of screen height (below the main character focal plane, above YouTube's bottom title/sound UI elements).
   - 16:9 Long-Form: Lower third, centered, with high-contrast semi-transparent backdrop or solid 3px dark stroke.
3. **Color Coding**:
   - Standard words: `#FFFFFF`
   - Key historical names: `#38BDF8` (Bright Sky Blue)
   - Danger / Conflict words: `#EF4444` (Vibrant Red)
   - Dollar amounts / Gold: `#FACC15` (Vibrant Gold)

