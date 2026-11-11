/* Grey Creatives Design: homepage behaviour (hero collage, open book, services, enquiry form) */
(function(){
"use strict";
var doc = document, D = window.GCD, GC = window.GC; if(!D || !GC) return;
var ROOT = GC.ROOT, esc = GC.esc, reduce = GC.reduce;
function $(id){ return doc.getElementById(id); }
var fine = window.matchMedia('(hover:hover) and (pointer:fine)').matches;

/* ---------- hero collage: the pieces drift a little with the pointer ---------- */
(function(){
  var hero = $('top'), cl = hero && hero.querySelectorAll('.cl'); if(!cl || !cl.length || reduce || !fine) return;
  var raf = 0, mx = 0, my = 0;
  function apply(){ raf = 0; cl.forEach(function(el){ var d = +el.getAttribute('data-d') || 1; el.style.setProperty('--px', (mx * d * 14).toFixed(1) + 'px'); el.style.setProperty('--py', (my * d * 14).toFixed(1) + 'px'); }); }
  hero.addEventListener('pointermove', function(e){ var r = hero.getBoundingClientRect(); mx = (e.clientX - r.left) / r.width - 0.5; my = (e.clientY - r.top) / r.height - 0.5; if(!raf){ raf = requestAnimationFrame(apply); } }, { passive:true });
  hero.addEventListener('pointerleave', function(){ mx = my = 0; if(!raf){ raf = requestAnimationFrame(apply); } });
})();

/* ---------- services: the fan of mockups follows the row you pick ---------- */
(function(){
  var items = doc.querySelectorAll('.svc-item'), pics = doc.querySelectorAll('.svc-pic'); if(!items.length) return;
  function set(i){ items.forEach(function(it, k){ var on = k === i; it.classList.toggle('on', on); var b = it.querySelector('.svc-row'); if(b){ b.setAttribute('aria-expanded', on ? 'true' : 'false'); } }); pics.forEach(function(p, k){ p.classList.toggle('on', k === i); }); }
  items.forEach(function(it, i){
    var b = it.querySelector('.svc-row');
    b.addEventListener('click', function(){ set(i); });
    b.addEventListener('pointerenter', function(e){ if(e.pointerType === 'mouse'){ set(i); } });
    b.addEventListener('focus', function(){ set(i); });
  });
  set(0);
})();

/* ---------- the open book ---------- */
(function(){
  var root = $('book'), W = D.projects; if(!root || !W.length) return;
  var n = W.length, cur = 0, busy = false;
  var mobile = window.matchMedia('(max-width:820px)');
  var ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  var BACK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>';
  function p2(x){ return ('0' + x).slice(-2); }
  function leftInner(i){
    var p = W[i];
    return '<div class="bk-meta"><span><b>' + p2(i + 1) + '</b> of ' + p2(n) + '</span><span class="bk-sector">' + esc(p.sector) + '</span></div>' +
      '<h3 class="bk-h">' + esc(p.title) + '</h3><p class="bk-tagline">' + esc(p.tagline) + '</p><p class="bk-focus">' + esc(p.short) + '</p>' +
      '<div class="bk-pal" aria-hidden="true">' + p.palette.map(function(c){ return '<i style="background:' + c[1] + '"></i>'; }).join('') + '</div>' +
      '<div class="bk-actions"><a class="bk-open" href="' + ROOT + p.href + '">See the full identity ' + ARROW + '</a></div><span class="bk-no">' + (i * 2 + 2) + '</span>';
  }
  function rightInner(i){
    var p = W[i], src = ROOT + p.cover;
    return '<div class="bk-fig" style="--tone:' + p.tone + '"><div class="bg" style="background-image:url(' + src + ')"></div><img src="' + src + '" alt="' + esc(p.coverAlt) + '" decoding="async" draggable="false"></div>' +
      '<p class="bk-cap">' + p.count + ' images in the gallery</p><span class="bk-no">' + (i * 2 + 3) + '</span>';
  }
  root.innerHTML =
    '<div class="bk-board"><div class="bk-spread" id="bkSpread" tabindex="0" role="group" aria-roledescription="book" aria-label="Brand identities. Use the left and right arrow keys to turn the page.">' +
      '<div class="bk-page bk-left bk-sl"></div><div class="bk-page bk-right bk-sr"></div>' +
      '<i class="bk-spine" aria-hidden="true"></i><i class="bk-ribbon" aria-hidden="true"></i>' +
      '<button type="button" class="bk-corner pv" aria-label="Previous brand" tabindex="-1"></button><button type="button" class="bk-corner nx" aria-label="Next brand" tabindex="-1"></button>' +
    '</div></div>' +
    '<div class="bk-ctrl"><button type="button" class="bk-arrow" data-d="-1" aria-label="Previous brand">' + BACK + '</button>' +
      '<div class="bk-dots" role="group" aria-label="Choose a brand">' + W.map(function(p, i){ return '<button type="button" data-i="' + i + '" aria-label="' + esc(p.title) + '">' + p2(i + 1) + '</button>'; }).join('') + '</div>' +
      '<button type="button" class="bk-arrow" data-d="1" aria-label="Next brand">' + ARROW + '</button></div>' +
    '<p class="bk-hint">Turn the page with the corners, the arrows or a swipe.</p><div class="bk-live" aria-live="polite"></div>';
  var spread = $('bkSpread'), sl = spread.querySelector('.bk-sl'), sr = spread.querySelector('.bk-sr');
  var pv = spread.querySelector('.bk-corner.pv'), nx = spread.querySelector('.bk-corner.nx');
  var arrows = root.querySelectorAll('.bk-arrow'), dots = root.querySelectorAll('.bk-dots button'), live = root.querySelector('.bk-live');
  function chrome(){
    pv.disabled = arrows[0].disabled = cur === 0; nx.disabled = arrows[1].disabled = cur === n - 1;
    dots.forEach(function(d, i){ if(i === cur){ d.setAttribute('aria-current', 'true'); } else { d.removeAttribute('aria-current'); } });
    live.textContent = 'Brand ' + (cur + 1) + ' of ' + n + ': ' + W[cur].title;
  }
  function paint(i){ sl.innerHTML = leftInner(i); sr.innerHTML = rightInner(i); }
  function page(cls, inner, face){ var d = doc.createElement('div'); d.className = 'bk-face ' + face + ' bk-page ' + cls; d.innerHTML = inner; return d; }
  function go(to){
    if(busy || to === cur || to < 0 || to > n - 1) return;
    var dir = to > cur ? 1 : -1, from = cur;
    if(reduce){ cur = to; paint(cur); chrome(); return; }
    if(mobile.matches){
      busy = true; cur = to; paint(cur); chrome();
      spread.classList.remove('turn-n', 'turn-p'); void spread.offsetWidth; spread.classList.add(dir > 0 ? 'turn-n' : 'turn-p');
      setTimeout(function(){ busy = false; }, 500); return;
    }
    busy = true;
    var leaf = doc.createElement('div'); leaf.className = 'bk-leaf' + (dir < 0 ? ' prev' : '');
    if(dir > 0){ sr.innerHTML = rightInner(to); leaf.appendChild(page('bk-right', rightInner(from), 'f')); leaf.appendChild(page('bk-left', leftInner(to), 'b')); }
    else { sl.innerHTML = leftInner(to); leaf.appendChild(page('bk-left', leftInner(from), 'f')); leaf.appendChild(page('bk-right', rightInner(to), 'b')); }
    spread.appendChild(leaf); void leaf.offsetWidth; leaf.classList.add('go');
    var done = false;
    function end(){ if(done) return; done = true; cur = to; paint(cur); leaf.remove(); chrome(); busy = false; }
    leaf.addEventListener('transitionend', function(e){ if(e.target === leaf && e.propertyName === 'transform'){ end(); } });
    setTimeout(end, 1150);
  }
  paint(0); chrome();
  nx.addEventListener('click', function(){ go(cur + 1); }); pv.addEventListener('click', function(){ go(cur - 1); });
  arrows.forEach(function(b){ b.addEventListener('click', function(){ go(cur + (+b.getAttribute('data-d'))); }); });
  dots.forEach(function(b){ b.addEventListener('click', function(){ go(+b.getAttribute('data-i')); }); });
  spread.addEventListener('keydown', function(e){ if(e.key === 'ArrowRight'){ e.preventDefault(); go(cur + 1); } else if(e.key === 'ArrowLeft'){ e.preventDefault(); go(cur - 1); } });
  var sx = 0, sy = 0, tracking = false;
  spread.addEventListener('pointerdown', function(e){ if(e.target.closest('a, button')) return; tracking = true; sx = e.clientX; sy = e.clientY; });
  spread.addEventListener('pointerup', function(e){ if(!tracking) return; tracking = false; var dx = e.clientX - sx, dy = e.clientY - sy; if(Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.4){ go(cur + (dx < 0 ? 1 : -1)); } });
  spread.addEventListener('pointercancel', function(){ tracking = false; });
  if('IntersectionObserver' in window && !reduce){
    var io = new IntersectionObserver(function(es){ if(es[0].isIntersecting){ io.disconnect(); root.classList.add('opened'); } }, { threshold:0.25 });
    io.observe(root);
  } else { root.classList.add('opened'); }
})();

/* ---------- enquiry form: builds a message and opens WhatsApp or email ---------- */
(function(){
  var f = $('enqForm'); if(!f) return;
  function message(){
    var name = ($('enqName').value || '').trim(), msg = ($('enqMsg').value || '').trim(), picks = [];
    f.querySelectorAll('input[name="need"]:checked').forEach(function(c){ picks.push(c.value); });
    var t = 'Hello Grey Creatives Design' + (name ? ', my name is ' + name : '') + '.';
    if(picks.length){ t += ' I am looking for: ' + picks.join(', ') + '.'; }
    if(msg){ t += ' ' + msg; }
    return t;
  }
  $('enqWa').addEventListener('click', function(){ window.open(D.waLink.split('?')[0] + '?text=' + encodeURIComponent(message()), '_blank', 'noopener'); });
  $('enqMail').addEventListener('click', function(){ window.location.href = 'mailto:' + D.email + '?subject=' + encodeURIComponent('Brand enquiry') + '&body=' + encodeURIComponent(message()); });
  f.addEventListener('submit', function(e){ e.preventDefault(); });
})();
})();
