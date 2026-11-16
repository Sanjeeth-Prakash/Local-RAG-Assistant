export class AudioManager {
  constructor() {
    this.ctx = null;
    this.muted = false;
  }

  ensure() {
    if (this.muted) return null;
    if (!this.ctx) {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return null;
      this.ctx = new AC();
    }
    if (this.ctx.state === 'suspended') this.ctx.resume().catch(() => {});
    return this.ctx;
  }

  toggle() {
    this.muted = !this.muted;
    return this.muted;
  }

  beep({ freq = 440, freq2, dur = 0.08, type = 'sine', gain = 0.06, delay = 0 }) {
    const ctx = this.ensure();
    if (!ctx) return;
    const t0 = ctx.currentTime + delay;
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, t0);
    if (freq2) osc.frequency.exponentialRampToValueAtTime(Math.max(1, freq2), t0 + dur);
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(gain, t0 + 0.01);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    osc.connect(g).connect(ctx.destination);
    osc.start(t0);
    osc.stop(t0 + dur + 0.02);
  }

  flap() {
    this.beep({ freq: 420, freq2: 720, dur: 0.09, type: 'sine', gain: 0.05 });
  }

  score() {
    this.beep({ freq: 660, freq2: 990, dur: 0.07, type: 'triangle', gain: 0.045 });
    this.beep({ freq: 880, freq2: 1320, dur: 0.09, type: 'triangle', gain: 0.04, delay: 0.05 });
  }

  hit() {
    this.beep({ freq: 220, freq2: 55, dur: 0.35, type: 'sawtooth', gain: 0.06 });
    this.beep({ freq: 140, freq2: 40, dur: 0.4, type: 'square', gain: 0.03 });
  }
}
