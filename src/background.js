import { rand, hsla } from './utils.js';

export class Background {
  constructor(w, h) {
    this.w = w; this.h = h;
    this.t = 0;
    this.groundH = 90;
    this.stars = Array.from({ length: 90 }, () => ({
      x: rand(0, w), y: rand(0, h * 0.7), r: rand(0.5, 2), tw: rand(0, Math.PI * 2), s: rand(0.2, 1.2)
    }));
    this.buildingsFar = this.makeBuildings(18, h * 0.45, h * 0.7, 30, 80);
    this.buildingsNear = this.makeBuildings(12, h * 0.55, h * 0.78, 50, 120);
    this.motes = Array.from({ length: 25 }, () => ({ x: rand(0, w), y: rand(0, h), r: rand(1, 2.5), vx: rand(-8, -2), hue: rand(170, 320) }));
  }
  makeBuildings(n, minY, maxY, minW, maxW) {
    const arr = [];
    let x = 0;
    for (let i = 0; i < n; i++) {
      const w = rand(minW, maxW);
      const h = rand(this.h - maxY, this.h - minY);
      arr.push({ x, w, h, hue: rand(180, 320) });
      x += w + rand(4, 20);
    }
    arr.totalW = x + 200;
    return arr;
  }
  resize(w, h) { this.w = w; this.h = h; this.groundH = Math.max(70, h * 0.1); }
  update(dt, speed) {
    this.t += dt;
    for (const m of this.motes) {
      m.x += (m.vx - speed * 0.05) * dt;
      if (m.x < -10) { m.x = this.w + 10; m.y = rand(0, this.h); }
    }
  }
  drawSky(ctx) {
    const g = ctx.createLinearGradient(0, 0, 0, this.h);
    g.addColorStop(0, '#02040f');
    g.addColorStop(0.45, '#090424');
    g.addColorStop(0.75, '#12062e');
    g.addColorStop(1, '#050814');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, this.w, this.h);

    // sun/moon glow
    const sx = this.w * 0.7, sy = this.h * 0.28, sr = this.h * 0.13;
    const sun = ctx.createRadialGradient(sx, sy, sr * 0.1, sx, sy, sr);
    sun.addColorStop(0, 'rgba(255, 0, 200, 0.35)');
    sun.addColorStop(0.5, 'rgba(255, 0, 120, 0.12)');
    sun.addColorStop(1, 'rgba(255, 0, 120, 0)');
    ctx.fillStyle = sun;
    ctx.beginPath(); ctx.arc(sx, sy, sr, 0, Math.PI * 2); ctx.fill();

    // stars
    ctx.save();
    for (const s of this.stars) {
      const tw = 0.4 + 0.6 * (0.5 + 0.5 * Math.sin(this.t * (1 + s.s) + s.tw));
      ctx.fillStyle = `rgba(200, 240, 255, ${tw})`;
      ctx.shadowColor = 'rgba(0,255,255,0.8)';
      ctx.shadowBlur = 6 * tw;
      ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2); ctx.fill();
    }
    ctx.restore();
  }
  drawGrid(ctx, offset) {
    const horizon = this.h * 0.62;
    ctx.save();
    ctx.strokeStyle = 'rgba(255, 0, 200, 0.18)';
    ctx.lineWidth = 1;
    ctx.shadowColor = 'rgba(255,0,200,0.5)';
    ctx.shadowBlur = 6;
    // horizontal receding lines
    for (let i = 0; i < 12; i++) {
      const p = i / 12;
      const y = horizon + Math.pow(p, 1.7) * (this.h - this.groundH - horizon);
      ctx.globalAlpha = 0.15 + p * 0.5;
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(this.w, y); ctx.stroke();
    }
    // verticals
    ctx.globalAlpha = 0.25;
    const cx = this.w / 2;
    const spacing = 60;
    const off = (offset * 0.3) % spacing;
    for (let x = -this.w; x < this.w * 2; x += spacing) {
      const xx = x - off;
      ctx.beginPath(); ctx.moveTo(cx + (xx - cx) * 0.05, horizon); ctx.lineTo(xx, this.h - this.groundH); ctx.stroke();
    }
    ctx.restore();
  }
  drawBuildingLayer(ctx, buildings, offset, baseY, colorA, alpha) {
    const total = buildings.totalW;
    const off = ((offset % total) + total) % total;
    ctx.save();
    ctx.fillStyle = colorA;
    ctx.globalAlpha = alpha;
    for (let k = -1; k <= 2; k++) {
      for (const b of buildings) {
        const x = b.x - off + k * total;
        if (x > this.w + 100 || x + b.w < -100) continue;
        const y = this.h - this.groundH - b.h * (baseY);
        ctx.fillRect(x, y, b.w, b.h * baseY + this.groundH);
      }
    }
    ctx.restore();
  }
  draw(ctx, camX) {
    this.drawSky(ctx);
    this.drawBuildingLayer(ctx, this.buildingsFar, camX * 0.2, 0.7, '#0a0520', 1);
    this.drawGrid(ctx, camX);
    this.drawBuildingLayer(ctx, this.buildingsNear, camX * 0.45, 1, '#060317', 1);
    // neon outlines on near buildings
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    const total = this.buildingsNear.totalW;
    const off = ((camX * 0.45 % total) + total) % total;
    for (let k = -1; k <= 2; k++) {
      for (const b of this.buildingsNear) {
        const x = b.x - off + k * total;
        if (x > this.w + 100 || x + b.w < -100) continue;
        const y = this.h - this.groundH - b.h;
        ctx.strokeStyle = hsla(b.hue, 100, 60, 0.25);
        ctx.shadowColor = hsla(b.hue, 100, 60, 0.8);
        ctx.shadowBlur = 10;
        ctx.lineWidth = 1.5;
        ctx.strokeRect(x, y, b.w, b.h);
      }
    }
    ctx.restore();

    // motes
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    for (const m of this.motes) {
      ctx.fillStyle = hsla(m.hue, 100, 70, 0.35);
      ctx.shadowColor = hsla(m.hue, 100, 60, 0.8);
      ctx.shadowBlur = 8;
      ctx.beginPath(); ctx.arc(m.x, m.y, m.r, 0, Math.PI * 2); ctx.fill();
    }
    ctx.restore();
  }
  drawGround(ctx, camX) {
    const y = this.h - this.groundH;
    const g = ctx.createLinearGradient(0, y, 0, this.h);
    g.addColorStop(0, '#0b0620');
    g.addColorStop(1, '#03010a');
    ctx.fillStyle = g;
    ctx.fillRect(0, y, this.w, this.groundH);
    // neon top line
    ctx.save();
    ctx.shadowColor = '#00ffff';
    ctx.shadowBlur = 18;
    ctx.strokeStyle = '#00ffff';
    ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(this.w, y); ctx.stroke();
    ctx.restore();
    // scrolling segments
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    const seg = 40;
    const off = (camX % seg);
    for (let x = -seg; x < this.w + seg; x += seg) {
      const xx = x - off;
      ctx.strokeStyle = 'rgba(255,0,200,0.35)';
      ctx.shadowColor = 'rgba(255,0,200,0.7)';
      ctx.shadowBlur = 8;
      ctx.beginPath(); ctx.moveTo(xx, y); ctx.lineTo(xx - 20, this.h); ctx.stroke();
    }
    ctx.restore();
  }
}
