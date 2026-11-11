/* Grey Creatives Design: shared behaviour (theme, menu, lightbox, command palette, copy). No sound. */
(function(){
"use strict";
var doc = document, root = doc.documentElement;
var ROOT = root.getAttribute('data-root') || '';
var D = window.GCD || { projects:[], logos:[], email:'', wa:'' };
var GC = window.GC = window.GC || {};
var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function $(id){ return doc.getElementById(id); }
function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return { '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;' }[c]; }); }
GC.esc = esc; GC.ROOT = ROOT; GC.reduce = reduce;
function store(k, v){ try{ if(v === undefined){ return localStorage.getItem(k); } localStorage.setItem(k, v); }catch(e){} return null; }

/* ---------- toast + copy ---------- */
var toastEl, toastT;
GC.toast = function(msg){
  if(!toastEl){ toastEl = doc.createElement('div'); toastEl.className = 'toast'; toastEl.setAttribute('role', 'status'); doc.body.appendChild(toastEl); }
  toastEl.textContent = msg; toastEl.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(function(){ toastEl.classList.remove('on'); }, 2200);
};
GC.copy = function(text, msg){
  function done(){ GC.toast(msg || 'Copied'); }
  function fallback(){
    var t = doc.createElement('textarea'); t.value = text; t.setAttribute('readonly', ''); t.style.cssText = 'position:fixed;opacity:0;top:0;left:0';
    doc.body.appendChild(t); t.select(); try{ doc.execCommand('copy'); done(); }catch(e){ GC.toast(text); } doc.body.removeChild(t);
  }
  if(navigator.clipboard && window.isSecureContext){ navigator.clipboard.writeText(text).then(done, fallback); } else { fallback(); }
};
doc.addEventListener('click', function(e){
  var b = e.target.closest('[data-copy]'); if(!b) return;
  GC.copy(b.getAttribute('data-copy'), b.getAttribute('data-msg') || 'Copied');
});

/* ---------- theme ---------- */
function setTheme(t){
  if(t === 'dark'){ root.setAttribute('data-theme', 'dark'); } else { root.removeAttribute('data-theme'); }
  var m = doc.querySelector('meta[name="theme-color"]'); if(m){ m.setAttribute('content', t === 'dark' ? '#0E0E0D' : '#FAFAF8'); }
  var b = $('themeToggle'); if(b){ b.setAttribute('aria-pressed', t === 'dark' ? 'true' : 'false'); b.setAttribute('aria-label', t === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'); }
}
GC.toggleTheme = function(){ var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'; setTheme(next); store('gcd-theme', next); return next; };
setTheme(root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light');
var tt = $('themeToggle'); if(tt){ tt.addEventListener('click', GC.toggleTheme); }

/* ---------- mobile menu ---------- */
(function(){
  var nav = $('navLinks'), tg = $('navToggle'), cl = $('navClose'); if(!nav || !tg) return;
  function set(open){
    nav.classList.toggle('open', open); doc.body.classList.toggle('nav-open', open); tg.setAttribute('aria-expanded', open ? 'true' : 'false');
    if(open && cl){ setTimeout(function(){ cl.focus({ preventScroll:true }); }, 50); } else if(!open && doc.activeElement && nav.contains(doc.activeElement)){ tg.focus({ preventScroll:true }); }
  }
  tg.addEventListener('click', function(){ set(!nav.classList.contains('open')); });
  if(cl){ cl.addEventListener('click', function(){ set(false); }); }
  nav.querySelectorAll('a').forEach(function(a){ a.addEventListener('click', function(){ set(false); }); });
  doc.addEventListener('keydown', function(e){ if(e.key === 'Escape' && nav.classList.contains('open')){ set(false); } });
  window.addEventListener('resize', function(){ if(window.innerWidth > 960 && nav.classList.contains('open')){ set(false); } });
})();

/* ---------- highlight the section you are in (home page) ---------- */
(function(){
  var nav = $('navLinks'); if(!nav || !('IntersectionObserver' in window)) return;
  var map = {}, home = nav.querySelector('[data-k="home"]');
  nav.querySelectorAll('a[data-sec]').forEach(function(a){ map[a.getAttribute('data-sec')] = a; });
  var ids = Object.keys(map).filter(function(id){ return $(id); }); if(!ids.length || !home || !home.classList.contains('is-cur')) return;
  var io = new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting) return;
      nav.querySelectorAll('a.is-cur').forEach(function(a){ a.classList.remove('is-cur'); });
      (map[e.target.id] || home).classList.add('is-cur');
    });
  }, { rootMargin:'-45% 0px -50% 0px' });
  ids.forEach(function(id){ io.observe($(id)); });
  var top = $('top'); if(top){ io.observe(top); }
})();

/* ---------- lightbox ---------- */
var LB = (function(){
  var items = [], cur = 0, last = null;
  var el = doc.createElement('div'); el.className = 'lb'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-modal', 'true'); el.setAttribute('aria-label', 'Image viewer');
  var X = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';
  el.innerHTML = '<span class="lb-count"></span><button type="button" class="lb-x">' + X + 'Close</button>' +
    '<button type="button" class="lb-nav pv" aria-label="Previous image"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M11 6l-6 6 6 6"/></svg></button>' +
    '<figure><img alt=""><figcaption></figcaption></figure>' +
    '<button type="button" class="lb-nav nx" aria-label="Next image"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>';
  doc.body.appendChild(el);
  var img = el.querySelector('img'), cap = el.querySelector('figcaption'), cnt = el.querySelector('.lb-count'), pv = el.querySelector('.pv'), nx = el.querySelector('.nx');
  function show(i){
    cur = (i + items.length) % items.length; var it = items[cur];
    img.style.animation = 'none'; void img.offsetWidth; img.style.animation = '';
    img.src = it.src; img.alt = it.alt || ''; cap.textContent = it.cap || it.alt || '';
    cnt.textContent = items.length > 1 ? (cur + 1) + ' / ' + items.length : '';
    pv.style.display = nx.style.display = items.length > 1 ? '' : 'none';
    [cur + 1, cur - 1].forEach(function(k){ var n = items[(k + items.length) % items.length]; if(n){ var p = new Image(); p.src = n.src; } });
  }
  function open(list, i){ items = list; last = doc.activeElement; el.classList.add('open'); doc.body.classList.add('lb-open'); show(i || 0); el.querySelector('.lb-x').focus({ preventScroll:true }); }
  function close(){ if(!el.classList.contains('open')) return; el.classList.remove('open'); doc.body.classList.remove('lb-open'); if(last && last.focus){ try{ last.focus({ preventScroll:true }); }catch(e){} } }
  pv.addEventListener('click', function(){ show(cur - 1); }); nx.addEventListener('click', function(){ show(cur + 1); });
  el.querySelector('.lb-x').addEventListener('click', close);
  el.addEventListener('click', function(e){ if(e.target === el || e.target.tagName === 'FIGURE'){ close(); } });
  doc.addEventListener('keydown', function(e){
    if(!el.classList.contains('open')) return;
    if(e.key === 'Escape'){ close(); } else if(e.key === 'ArrowRight'){ show(cur + 1); } else if(e.key === 'ArrowLeft'){ show(cur - 1); }
  });
  var sx = 0, sy = 0;
  el.addEventListener('touchstart', function(e){ sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive:true });
  el.addEventListener('touchend', function(e){ var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy; if(Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.4){ show(cur + (dx < 0 ? 1 : -1)); } }, { passive:true });
  return { open:open, close:close, isOpen:function(){ return el.classList.contains('open'); } };
})();
GC.lightbox = LB;

/* gallery images: any [data-lb] button opens its group */
doc.addEventListener('click', function(e){
  var b = e.target.closest('[data-lb]'); if(!b) return;
  var g = b.getAttribute('data-lb'), list = [], idx = 0;
  doc.querySelectorAll('[data-lb="' + g + '"]').forEach(function(n, i){ list.push({ src:n.getAttribute('data-full'), alt:n.getAttribute('data-alt') || '', cap:n.getAttribute('data-alt') || '' }); if(n === b){ idx = i; } });
  LB.open(list, idx);
});

/* logos as lightbox items */
GC.logoItems = function(){ return D.logos.map(function(l){ return { src:ROOT + 'assets/img/logos/' + l.f + '-lg.webp', alt:l.n + ' logo', cap:l.n }; }); };
GC.openLogo = function(i){ LB.open(GC.logoItems(), i); };

/* ---------- command palette ---------- */
(function(){
  var isMac = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent || '');
  var KEY = isMac ? '⌘K' : 'Ctrl K';
  var box = doc.createElement('div'); box.className = 'cp'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-label', 'Search the site');
  box.innerHTML = '<div class="cp-scrim" data-close></div><div class="cp-box"><div class="cp-top"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>' +
    '<input class="cp-input" id="cpInput" type="text" placeholder="Search pages, brands, logos, actions" autocomplete="off" spellcheck="false" role="combobox" aria-expanded="true" aria-controls="cpList" aria-autocomplete="list"><kbd>esc</kbd></div>' +
    '<div class="cp-list" id="cpList" role="listbox"></div><div class="cp-foot"><span><kbd>↑</kbd> <kbd>↓</kbd> move</span><span><kbd>↵</kbd> open</span><span><kbd>esc</kbd> close</span></div></div>';
  doc.body.appendChild(box);
  var input = $('cpInput'), list = $('cpList'), items = [], shown = [], act = 0, last = null;
  function I(p){ return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + p + '</svg>'; }
  var ic = { page:I('<path d="M5 12h14M13 6l6 6-6 6"/>'), act:I('<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>') };
  function slug(n){ return n.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''); }
  function build(){
    items = [];
    [['Home', 'index.html', 'start top'], ['Work', 'work.html', 'projects brand identities case studies'], ['Logos', 'logos.html', 'logo design globe'], ['Services', 'index.html#services', 'what we design'], ['Contact', '#contact', 'email whatsapp hire quote']].forEach(function(p){
      items.push({ g:'Pages', icon:ic.page, label:p[0], kw:p[2], run:function(){ location.href = p[1].charAt(0) === '#' ? p[1] : ROOT + p[1]; } });
    });
    D.projects.forEach(function(p){ items.push({ g:'Brand identities', icon:'<img src="' + ROOT + p.thumb + '" alt="">', label:p.title, sub:p.sector, kw:p.slug + ' ' + p.tags.join(' '), run:function(){ location.href = ROOT + p.href; } }); });
    D.logos.forEach(function(l, i){ items.push({ g:'Logos', icon:'<img src="' + ROOT + 'assets/img/logos/' + l.f + '.webp" alt="">', label:l.n, sub:'Logo', kw:'logo mark ' + l.n, run:function(){ if(doc.body.getAttribute('data-page') === 'logos'){ GC.openLogo(i); } else { location.href = ROOT + 'logos.html#' + slug(l.n); } } }); });
    items.push({ g:'Actions', icon:ic.act, label:'Switch light or dark theme', kw:'theme dark light mode', run:function(){ GC.toast(GC.toggleTheme() === 'dark' ? 'Dark mode' : 'Light mode'); } });
    items.push({ g:'Actions', icon:ic.act, label:'Copy email address', sub:D.email, kw:'mail contact copy', run:function(){ GC.copy(D.email, 'Email copied'); } });
    items.push({ g:'Actions', icon:ic.act, label:'Chat on WhatsApp', sub:D.phone, kw:'message whatsapp contact', run:function(){ window.open(D.waLink, '_blank', 'noopener'); } });
    items.push({ g:'Actions', icon:ic.act, label:'Send an email', sub:D.email, kw:'mail contact', run:function(){ location.href = 'mailto:' + D.email; } });
  }
  function score(q, it){
    if(!q) return 1; var s = (it.label + ' ' + (it.kw || '')).toLowerCase(), i = s.indexOf(q);
    if(i > -1) return 200 - i; var j = 0; for(var k = 0; k < s.length && j < q.length; k++){ if(s[k] === q[j]) j++; } return j === q.length ? 20 : 0;
  }
  function render(){
    var q = input.value.trim().toLowerCase();
    var c = items.map(function(it){ return { it:it, s:score(q, it) }; }).filter(function(x){ return x.s > 0; });
    if(q){ c.sort(function(a, b){ return b.s - a.s; }); }
    shown = c.map(function(x){ return x.it; });
    if(q){ shown = shown.slice(0, 30); }
    if(!shown.length){ list.innerHTML = '<div class="cp-empty">Nothing matches “' + esc(input.value) + '”. Try a brand, a logo or a page name.</div>'; return; }
    var html = '', gi = '';
    shown.forEach(function(it, i){
      if(!q && it.g !== gi){ gi = it.g; html += '<div class="cp-group" role="presentation">' + esc(gi) + '</div>'; }
      html += '<button type="button" class="cp-item" role="option" id="cpo' + i + '" data-i="' + i + '"><span class="ic">' + it.icon + '</span><span class="lb2">' + esc(it.label) + (it.sub ? '<small>' + esc(it.sub) + '</small>' : '') + '</span></button>';
    });
    list.innerHTML = html; act = 0; mark();
  }
  function mark(){
    var els = list.querySelectorAll('.cp-item');
    for(var i = 0; i < els.length; i++){ var on = i === act; els[i].classList.toggle('on', on); els[i].setAttribute('aria-selected', on ? 'true' : 'false'); if(on){ input.setAttribute('aria-activedescendant', els[i].id); els[i].scrollIntoView({ block:'nearest' }); } }
  }
  function pick(i){ var it = shown[i]; if(!it) return; close(true); setTimeout(function(){ it.run(); }, 40); }
  function open(){
    if(box.classList.contains('open')) return; if(!items.length) build();
    last = doc.activeElement; box.classList.add('open'); doc.body.classList.add('cp-open'); input.value = ''; render(); setTimeout(function(){ input.focus(); }, 10);
  }
  function close(silent){ if(!box.classList.contains('open')) return; box.classList.remove('open'); doc.body.classList.remove('cp-open'); if(!silent && last && last.focus){ try{ last.focus({ preventScroll:true }); }catch(e){} } }
  GC.palette = { open:open, close:close };
  input.addEventListener('input', render);
  input.addEventListener('keydown', function(e){
    if(e.key === 'ArrowDown'){ e.preventDefault(); act = Math.min(shown.length - 1, act + 1); mark(); }
    else if(e.key === 'ArrowUp'){ e.preventDefault(); act = Math.max(0, act - 1); mark(); }
    else if(e.key === 'Enter'){ e.preventDefault(); pick(act); }
    else if(e.key === 'Tab'){ e.preventDefault(); }
  });
  list.addEventListener('click', function(e){ var b = e.target.closest('.cp-item'); if(b){ pick(+b.getAttribute('data-i')); } });
  list.addEventListener('pointermove', function(e){ var b = e.target.closest('.cp-item'); if(b && +b.getAttribute('data-i') !== act){ act = +b.getAttribute('data-i'); mark(); } });
  box.addEventListener('click', function(e){ if(e.target.hasAttribute('data-close')){ close(); } });
  doc.addEventListener('keydown', function(e){
    var k = (e.key || '').toLowerCase();
    if((e.ctrlKey || e.metaKey) && k === 'k'){ e.preventDefault(); box.classList.contains('open') ? close() : open(); return; }
    if(k === 'escape' && box.classList.contains('open')){ e.preventDefault(); close(); return; }
    if(k === '/' && !e.ctrlKey && !e.metaKey && !e.altKey){ var t = e.target; if(t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return; e.preventDefault(); open(); }
  });
  var sb = $('searchBtn'); if(sb){ sb.setAttribute('title', 'Search (' + KEY + ')'); sb.addEventListener('click', open); }
})();

/* ---------- header shadow on scroll ---------- */
(function(){
  var hd = $('siteHeader'); if(!hd) return;
  function on(){ hd.classList.toggle('scrolled', window.scrollY > 12); }
  window.addEventListener('scroll', on, { passive:true }); on();
})();
})();
