/* Grey Creatives Design: Work filters, logo pinboard, deep links */
(function(){
"use strict";
var doc = document, GC = window.GC, D = window.GCD; if(!GC || !D) return;

/* ---------- Work page filters: the staggered layout re-flows for the visible pieces ---------- */
(function(){
  var wrap = doc.getElementById('mosaic'), bar = doc.getElementById('filters'); if(!wrap || !bar) return;
  var cards = [].slice.call(wrap.querySelectorAll('.wc'));
  function layout(){ var k = 0; cards.forEach(function(c){ if(!c.hidden){ c.setAttribute('data-p', k % 4); k++; } }); }
  bar.addEventListener('click', function(e){
    var b = e.target.closest('button'); if(!b) return;
    bar.querySelectorAll('button').forEach(function(x){ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    var f = b.getAttribute('data-f');
    cards.forEach(function(c){ c.hidden = !(f === 'all' || (c.getAttribute('data-tags') || '').split('|').indexOf(f) > -1); });
    layout();
  });
  layout();
})();

/* ---------- Logo pinboard ---------- */
(function(){
  var pins = doc.querySelectorAll('[data-logo]'); if(!pins.length) return;
  pins.forEach(function(p){ p.addEventListener('click', function(){ GC.openLogo(+p.getAttribute('data-logo')); }); });
  function slug(n){ return n.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''); }
  function fromHash(){
    var h = (location.hash || '').replace('#', ''); if(!h) return;
    for(var i = 0; i < D.logos.length; i++){ if(slug(D.logos[i].n) === h){ GC.openLogo(i); return; } }
  }
  fromHash(); window.addEventListener('hashchange', fromHash);
})();
})();
