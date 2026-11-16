import { rand, TAU, hsla } from './utils.js';

class Particle {
  constructor() { this.alive = false; }
  init(x, y, vx, vy, life, size, hue, type = 'dot') {
    this.x = x; this.y = y; this.vx = vx; this.vy = vy;
    this.life = life; this.maxLife = life; this.size = size;
    this.hue = hue; this.type = type; this.alive = true;
    this.drag = type === 'ring' ? 1 : 0.985;
    this.gravity = type === 'spark' ? 500 : (type === 'puff' ? -20 : 0);
  }
  update(dt) {
    if (!this.alive) return;
    this.life -= dt;
    if (this.life <= 0) { this.alive = false; return; }
    this.vx *= this.drag;
    this.vy = this.vy * this.drag + this.gravity * dt;
    this.x += this.vx * dt;
    this.y += this.vy * dt;
  }
  draw(ctx) {
    if (!this.alive) return;
    const t = this.life / this.maxLife;
    const alpha = Math.max(0, t);
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    if (this.type === 'ring') {
      const r = this.size * (1.8 - t);
      ctx.lineWidth = 2 + 2 * t;
      ctx.strokeStyle = hsla(this.hue, 100, 65, alpha * 0.9);
      ctx.shadowColor = hsla(this.hue, 100, 60, 0.9);
      ctx.shadowBlur = 18;
      ctx.beginPath(); ctx.arc(this.x, this.y, r, 0, TAU); ctx.stroke();
    } else {
      const r = this.size * (0.4 + 0.8 * t);
      ctx.fillStyle = hsla(this.hue, 100, 70, alpha);
      ctx.shadowColor = hsla(this.hue, 100, 60, 0.9);
      ctx.shadowBlur = 14;
      ctx.beginPath(); ctx.arc(this.x, this.y, r, 0, TAU); ctx.fill();
    }
    ctx.restore();
  }
}

export class ParticleSystem {
  constructor(max = 500) {
    this.pool = Array.from({ length: max }, () => new Particle());
  }
  spawn(x, y, vx, vy, life, size, hue, type) {
    const p = this.pool.find(pp => !pp.alive);
    if (p) p.init(x, y, vx, vy, life, size, hue, type);
  }
  emitFlap(x, y) {
    for (let i = 0; i < 10; i++) {
      const a = rand(Math.PI * 0.6, Math.PI * 1.4);
      const s = rand(30, 140);
      this.spawn(x, y, Math.cos(a) * s, Math.sin(a) * s, rand(0.2, 0.5), rand(1.5, 4), rand(170, 200), 'puff');
    }
  }
  emitScore(x, y) {
    this.spawn(x, y, 0, 0, 0.5, 18, 140, 'ring');
    for (let i = 0; i < 18; i++) {
      const a = rand(0, TAU);
      const s = rand(60, 220);
      this.spawn(x, y, Math.cos(a) * s, Math.sin(a) * s, rand(0.3, 0.7), rand(1.5, 3.5), rand(120, 170), 'dot');
    }
  }
  emitHit(x, y) {
    this.spawn(x, y, 0, 0, 0.6, 24, 320, 'ring');
    for (let i = 0; i < 40; i++) {
      const a = rand(0, TAU);
      const s = rand(80, 420);
      const hue = Math.random() < 0.5 ? rand(300, 330) : rand(180, 200);
      this.spawn(x, y, Math.cos(a) * s, Math.sin(a) * s - 60, rand(0.4, 1.0), rand(1.5, 4), hue, 'spark');
    }
  }
  update(dt) { for (const p of this.pool) p.update(dt); }
  draw(ctx) { for (const p of this.pool) p.draw(ctx); }
}
