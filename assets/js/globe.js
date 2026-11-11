/* Grey Creatives Design: the logo globe. Drag to spin, hover to pop a logo forward, click to open it full size. */
(function(){
"use strict";
var stage = document.getElementById('glStage'), D = window.GCD, GC = window.GC;
if(!stage || !D || !GC) return;
var L = D.logos, N = L.length, ROOT = GC.ROOT, reduce = GC.reduce;
var field = stage.querySelector('.gl-field'), tip = stage.querySelector('.gl-tip');

/* even points on a sphere (Fibonacci) */
var P = [], GA = Math.PI * (3 - Math.sqrt(5));
for(var i = 0; i < N; i++){ var y = 1 - (i / (N - 1)) * 2, r = Math.sqrt(1 - y * y), th = GA * i; P.push({ x:Math.cos(th) * r, y:y, z:Math.sin(th) * r }); }

var els = L.map(function(l, i){
  var b = document.createElement('button'); b.type = 'button'; b.className = 'gl-tile'; b.setAttribute('aria-label', l.n + ' logo, open full size');
  b.style.background = l.bg;
  var im = document.createElement('img'); im.src = ROOT + 'assets/img/logos/' + l.f + '.webp'; im.alt = ''; im.width = 420; im.height = 420; im.decoding = 'async'; im.draggable = false;
  b.appendChild(im); field.appendChild(b); return { el:b, h:0, i:i, z:0, sx:0, sy:0, s:1 };
});

var W = 0, H = 0, R = 0, T = 64;
function size(){
  var r = stage.getBoundingClientRect(); W = r.width; H = r.height; R = Math.min(W, H) / 2 * 0.84; T = Math.max(50, Math.min(112, R * 0.33));
  els.forEach(function(o){ o.el.style.width = o.el.style.height = T + 'px'; o.el.style.marginLeft = o.el.style.marginTop = (-T / 2) + 'px'; });
}
size(); window.addEventListener('resize', size, { passive:true });

var yaw = 0.6, pitch = -0.28, vy = 0.0035, vp = 0, speed = 0.0035, hot = -1, drag = false, moved = 0, lx = 0, ly = 0, raf = 0, visible = false, lastT = 0;
function frame(now){
  raf = 0; if(!visible || document.hidden) return;
  var dt = Math.min(48, now - lastT) / 16.67; lastT = now;
  if(!drag){
    var target = (hot >= 0 || reduce) ? 0 : speed;
    vy += (target - vy) * 0.06 * dt; vp *= Math.pow(0.92, dt);
    yaw += vy * dt; pitch += vp * dt;
  }
  pitch = Math.max(-0.9, Math.min(0.9, pitch));
  var cy = Math.cos(yaw), sy = Math.sin(yaw), cp = Math.cos(pitch), sp = Math.sin(pitch);
  for(var i = 0; i < N; i++){
    var p = P[i], o = els[i];
    var x1 = p.x * cy + p.z * sy, z1 = -p.x * sy + p.z * cy;
    var y2 = p.y * cp - z1 * sp, z2 = p.y * sp + z1 * cp;
    o.z = z2;
    var depth = (z2 + 1) / 2;
    o.h += ((hot === i ? 1 : 0) - o.h) * 0.2 * dt;
    var s = (0.56 + 0.44 * depth) * (1 + 0.95 * o.h);
    o.sx = W / 2 + x1 * R; o.sy = H / 2 + y2 * R; o.s = s;
    o.el.style.transform = 'translate(' + o.sx.toFixed(1) + 'px,' + o.sy.toFixed(1) + 'px) scale(' + s.toFixed(3) + ') rotate(' + ((1 - o.h) * (x1 * 5)).toFixed(2) + 'deg)';
    o.el.style.opacity = (hot === i ? 1 : (0.34 + 0.66 * depth)).toFixed(2);
    o.el.style.zIndex = (hot === i ? 400 : Math.round(depth * 100));
    o.el.style.pointerEvents = z2 > -0.25 ? 'auto' : 'none';
  }
  if(hot >= 0 && tip){ var h = els[hot]; tip.style.transform = 'translate(' + (h.sx).toFixed(1) + 'px,' + (h.sy - T * h.s / 2 - 18).toFixed(1) + 'px) translate(-50%,-100%)'; }
  raf = requestAnimationFrame(frame);
}
function kick(){ if(!raf && visible && !document.hidden){ lastT = performance.now(); raf = requestAnimationFrame(frame); } }
if('IntersectionObserver' in window){ new IntersectionObserver(function(es){ visible = es[0].isIntersecting; if(visible){ kick(); } }, { rootMargin:'120px' }).observe(stage); } else { visible = true; kick(); }
document.addEventListener('visibilitychange', kick);

function setHot(i){
  if(i === hot) return; hot = i;
  if(tip){ if(i >= 0){ tip.textContent = L[i].n; tip.classList.add('on'); } else { tip.classList.remove('on'); } }
  if(reduce){ kick(); }
}
function idx(t){ for(var i = 0; i < els.length; i++){ if(els[i].el === t) return i; } return -1; }
field.addEventListener('pointerover', function(e){ if(drag || e.pointerType === 'touch') return; var t = e.target.closest('.gl-tile'); if(t){ setHot(idx(t)); } });
field.addEventListener('pointerout', function(e){ if(!e.relatedTarget || !e.relatedTarget.closest || !e.relatedTarget.closest('.gl-tile')){ setHot(-1); } });
field.addEventListener('focusin', function(e){ var t = e.target.closest('.gl-tile'); if(t){ setHot(idx(t)); } });
field.addEventListener('focusout', function(){ setHot(-1); });

/* drag to spin */
stage.addEventListener('pointerdown', function(e){ if(e.button > 0) return; drag = true; moved = 0; lx = e.clientX; ly = e.clientY; vy = 0; vp = 0; });
stage.addEventListener('pointermove', function(e){
  if(!drag) return; var dx = e.clientX - lx, dy = e.clientY - ly; lx = e.clientX; ly = e.clientY; moved += Math.abs(dx) + Math.abs(dy);
  if(moved > 6 && !stage.classList.contains('grab')){ stage.classList.add('grab'); try{ stage.setPointerCapture(e.pointerId); }catch(_){} }
  yaw += dx * 0.008; pitch += dy * 0.006; vy = dx * 0.008; vp = dy * 0.006; kick(); if(reduce && !raf){ raf = requestAnimationFrame(frame); }
});
function up(){ if(!drag) return; drag = false; stage.classList.remove('grab'); if(Math.abs(vy) < 0.002){ vy = speed; } }
stage.addEventListener('pointerup', up); stage.addEventListener('pointercancel', up);

field.addEventListener('click', function(e){ var t = e.target.closest('.gl-tile'); if(!t || moved > 6) return; GC.openLogo(idx(t)); });

window.GCGlobe = { spinTo:function(i){ setHot(i); } };
if(reduce){ visible = true; kick(); setTimeout(function(){ visible = false; }, 200); }
})();
