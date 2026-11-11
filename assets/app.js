/* Sarah Pacini — front-end logic: cart, compare, catalog, forms. No backend required. */
(function () {
  'use strict';
  var SP = window.SP, C = SP.config;
  var ROOT = document.body.dataset.root || '';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var BY = {}; SP.products.forEach(function (p) { BY[p.id] = p; });
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var fmt = function (n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); };
  var ico = function (n, c) { return '<svg class="' + (c || 'ico') + '" viewBox="0 0 24 24" aria-hidden="true">' + (SP.icons[n] || '') + '</svg>'; };
  var img = function (f) { return C.imgBase + '/d/' + f; };
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  var priceText = function (p) { return p.price ? fmt(p.price) + ' ₽' : 'Цена по запросу'; };
  var brandName = function (id) { return (SP.brands.filter(function (b) { return b.id === id; })[0] || {}).t || ''; };
  var leafName = function (id) { return SP.leaf[id] || ''; };

  /* ---------- toast ---------- */
  var toastEl, toastT;
  function toast(msg) {
    if (!toastEl) { toastEl = document.createElement('div'); toastEl.className = 'toast'; toastEl.setAttribute('role', 'status'); document.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add('on'); clearTimeout(toastT);
    toastT = setTimeout(function () { toastEl.classList.remove('on'); }, 2600);
  }

  /* ---------- overlays ---------- */
  var veil = $('#veil');
  function openO(id) { var el = document.getElementById(id); if (!el) return; closeAll(); el.classList.add('on'); veil.classList.add('on'); document.body.style.overflow = 'hidden'; var f = $('input,button.x', el); if (f && id !== 'mob') setTimeout(function () { try { f.focus(); } catch (e) {} }, 80); }
  function closeAll() { $$('.drawer.on,.modal.on,.filters.on').forEach(function (e) { e.classList.remove('on'); }); veil.classList.remove('on'); document.body.style.overflow = ''; }
  document.addEventListener('click', function (e) {
    var o = e.target.closest('[data-open]');
    if (o) { e.preventDefault(); if (o.dataset.open === 'cart') renderMini(); openO(o.dataset.open); return; }
    if (e.target.closest('[data-close]') || e.target === veil) { closeAll(); }
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeAll(); closeLB(); } });

  /* ---------- cart ---------- */
  var cart = store.get('sp_cart', {});
  function saveCart() { store.set('sp_cart', cart); badges(); }
  function cartCount() { return Object.keys(cart).reduce(function (a, k) { return a + cart[k]; }, 0); }
  function cartTotals() {
    var t = 0, ask = 0;
    Object.keys(cart).forEach(function (k) { var p = BY[k]; if (!p) return; if (p.price) t += p.price * cart[k]; else ask += cart[k]; });
    return { sum: t, ask: ask };
  }
  function addCart(id, q) { if (!BY[id]) return; cart[id] = Math.min(99, (cart[id] || 0) + (q || 1)); saveCart(); toast('Добавлено в корзину: ' + BY[id].name); renderMini(); }
  function setQty(id, q) { if (q < 1) delete cart[id]; else cart[id] = Math.min(99, q); saveCart(); renderMini(); if (window.__renderCart) window.__renderCart(); }
  function badges() {
    var n = cartCount(), c = (store.get('sp_cmp', [])).length;
    $$('[data-cart-n]').forEach(function (e) { e.textContent = n || ''; e.dataset.n = n; });
    $$('[data-cmp-n]').forEach(function (e) { e.textContent = c || ''; e.dataset.n = c; });
  }
  function renderMini() {
    var box = $('#miniItems'); if (!box) return;
    var ids = Object.keys(cart).filter(function (k) { return BY[k]; });
    if (!ids.length) { box.innerHTML = '<div class="empty"><h3>Корзина пуста</h3><p>Добавьте вещи из каталога — мы уточним наличие и размеры.</p><p style="margin-top:20px"><a class="btn" href="' + ROOT + 'catalog.html?cat=all">Смотреть каталог</a></p></div>'; $('#miniFoot').hidden = true; return; }
    $('#miniFoot').hidden = false;
    box.innerHTML = ids.map(function (k) {
      var p = BY[k];
      return '<div class="mini"><a href="' + ROOT + 'product/' + p.id + '.html"><img src="' + img(p.img) + '" alt="" loading="lazy"></a><div><h4>' + esc(p.name) + '</h4><div class="p">' + priceText(p) + '</div>' +
        '<div class="qty" style="margin-top:10px"><button data-q="' + p.id + '" data-d="-1" aria-label="Меньше">−</button><input value="' + cart[k] + '" readonly aria-label="Количество"><button data-q="' + p.id + '" data-d="1" aria-label="Больше">+</button></div></div>' +
        '<button class="rm" data-rm="' + p.id + '" aria-label="Удалить">' + ico('trash') + '</button></div>';
    }).join('');
    var t = cartTotals();
    $('#miniSum').textContent = (t.sum ? fmt(t.sum) + ' ₽' : '—') + (t.ask ? ' + ' + t.ask + ' по запросу' : '');
  }
  document.addEventListener('click', function (e) {
    var q = e.target.closest('[data-q]');
    if (q) { setQty(q.dataset.q, (cart[q.dataset.q] || 0) + Number(q.dataset.d)); return; }
    var r = e.target.closest('[data-rm]');
    if (r) { setQty(r.dataset.rm, 0); return; }
    var a = e.target.closest('[data-add]');
    if (a) {
      var qty = 1, box = a.closest('[data-qtybox]'); if (box) qty = Number($('input', box).value) || 1;
      addCart(a.dataset.add, qty); return;
    }
    var c = e.target.closest('[data-cmp]');
    if (c) { toggleCmp(c.dataset.cmp); return; }
  });
  /* plain qty steppers (pdp) */
  document.addEventListener('click', function (e) {
    var s = e.target.closest('[data-step]'); if (!s) return;
    var inp = $('input', s.closest('.qty')); inp.value = Math.max(1, Math.min(99, (Number(inp.value) || 1) + Number(s.dataset.step)));
  });

  /* ---------- compare ---------- */
  function toggleCmp(id) {
    var l = store.get('sp_cmp', []), i = l.indexOf(id);
    if (i > -1) { l.splice(i, 1); toast('Убрано из сравнения'); }
    else { if (l.length >= 4) { toast('В сравнении может быть до 4 товаров'); return; } l.push(id); toast('Добавлено к сравнению'); }
    store.set('sp_cmp', l); badges(); markCmp(); cmpBar(); if (window.__renderCmp) window.__renderCmp();
  }
  function markCmp() { var l = store.get('sp_cmp', []); $$('[data-cmp]').forEach(function (b) { var on = l.indexOf(b.dataset.cmp) > -1; b.classList.toggle('on', on); b.setAttribute('aria-pressed', on); }); }
  function cmpBar() {
    var l = store.get('sp_cmp', []), bar = $('#cmpbar'); if (!bar) return;
    bar.classList.toggle('on', l.length > 0 && !/compare\.html/.test(location.pathname));
    $('#cmpbarN').textContent = l.length;
  }
  $('#cmpClear') && $('#cmpClear').addEventListener('click', function () { store.set('sp_cmp', []); badges(); markCmp(); cmpBar(); });

  /* ---------- product card ---------- */
  function card(p, view) {
    var href = ROOT + 'product/' + p.id + '.html';
    var pr = '<div class="pr' + (p.price ? '' : ' ask') + '">' + priceText(p) + '</div>';
    var cmpb = '<button class="cmp" data-cmp="' + p.id + '" aria-label="Добавить к сравнению" title="К сравнению">' + ico('cmp') + '</button>';
    var badge = p.isNew ? '<span class="badge">Новинка</span>' : '';
    var buy = '<div class="buy"><button class="btn" data-add="' + p.id + '">В корзину</button></div>';
    if (view === 'list') {
      return '<article class="card row"><a class="im" href="' + href + '" style="position:relative"><img src="' + img(p.img) + '" alt="' + esc(p.name) + '" loading="lazy">' + badge + '</a>' +
        '<div class="body"><div class="br">' + esc(brandName(p.brand)) + '</div><h3 class="nm"><a href="' + href + '">' + esc(p.name) + '</a></h3><p class="d">' + esc(p.desc) + '</p>' + pr +
        '<div class="buy"><button class="btn" data-add="' + p.id + '">Добавить в корзину</button><button class="btn ghost" data-cmp="' + p.id + '">К сравнению</button></div></div></article>';
    }
    return '<article class="card"><a class="im" href="' + href + '"><img src="' + img(p.img) + '" alt="' + esc(p.name) + '" loading="lazy">' + badge + '</a>' + cmpb +
      '<h3 class="nm"><a href="' + href + '">' + esc(p.name) + '</a></h3><div class="br">' + esc(brandName(p.brand)) + '</div>' + pr + buy + '</article>';
  }

  /* ---------- static grids (home, brand pages, related) ---------- */
  $$('[data-grid]').forEach(function (g) {
    var brand = g.dataset.brand, cat = g.dataset.cat, ex = g.dataset.exclude, lim = Number(g.dataset.limit) || 8;
    var list = SP.products.filter(function (p) { return (!brand || p.brand === brand) && (!cat || p.cat === cat) && p.id !== ex; });
    if (g.dataset.mix) { var a = list.filter(function (p) { return p.brand === 'sp'; }), b = list.filter(function (p) { return p.brand === 'tr'; }), m = []; for (var i = 0; i < Math.max(a.length, b.length); i++) { if (a[i]) m.push(a[i]); if (b[i]) m.push(b[i]); } list = m; }
    g.innerHTML = list.slice(0, lim).map(function (p) { return card(p); }).join('');
  });
  $$('[data-tabs-for]').forEach(function (t) {
    t.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      $$('button', t).forEach(function (x) { x.classList.toggle('on', x === b); });
      var g = document.getElementById(t.dataset.tabsFor); g.dataset.brand = b.dataset.brand || ''; g.innerHTML = '';
      var list = SP.products.filter(function (p) { return !b.dataset.brand || p.brand === b.dataset.brand; });
      g.innerHTML = list.slice(0, Number(g.dataset.limit) || 8).map(function (p) { return card(p); }).join('');
      markCmp();
    });
  });

  /* ---------- catalog ---------- */
  var catEl = $('#catalog');
  if (catEl) {
    var P = new URLSearchParams(location.search);
    var st = {
      cat: P.get('cat') || 'all', brand: P.get('brand') || '', brands: (P.get('brands') || '').split(',').filter(Boolean),
      q: P.get('q') || '', name: P.get('name') || '', art: P.get('art') || '', text: P.get('text') || '',
      minp: P.get('minp') || '', maxp: P.get('maxp') || '', isnew: P.get('isnew') || '', sale: P.get('sale') || '',
      pp: Number(P.get('pp')) || 20, sort: P.get('sort') || '', view: store.get('sp_view', 'grid'), page: Number(P.get('page')) || 1
    };
    if (st.brand && !st.brands.length) st.brands = [st.brand];
    var groupCats = function (c) {
      if (c === 'all') return null;
      if (c === 'odezhda') return ['bryuki', 'dgempera', 'cardigany', 'tuniki', 'topy', 'platya', 'yubki', 'kurtki', 'palantiny'];
      if (c === 'aksessuary') return ['palantiny', 'sumki', 'ukrasheniya'];
      return [c];
    };
    var filtered = function (skipBrand) {
      var gc = groupCats(st.cat);
      var q = (st.q || st.name).toLowerCase(), art = st.art.toLowerCase(), tx = st.text.toLowerCase();
      var lo = Number(st.minp) || 0, hi = Number(st.maxp) || 0;
      return SP.products.filter(function (p) {
        if (gc && gc.indexOf(p.cat) < 0) return false;
        if (!skipBrand && st.brands.length && st.brands.indexOf(p.brand) < 0) return false;
        if (q && p.name.toLowerCase().indexOf(q) < 0) return false;
        if (art && (p.model || '').toLowerCase().indexOf(art) < 0 && p.name.toLowerCase().indexOf(art) < 0) return false;
        if (tx && (p.desc + ' ' + (p.material || '')).toLowerCase().indexOf(tx) < 0) return false;
        if (lo && (!p.price || p.price < lo)) return false;
        if (hi && (!p.price || p.price > hi)) return false;
        if (st.isnew === '1' && !p.isNew) return false; if (st.isnew === '0' && p.isNew) return false;
        if (st.sale === '1' && !p.sale) return false; if (st.sale === '0' && p.sale) return false;
        return true;
      });
    };
    var sorted = function (l) {
      var r = l.slice();
      if (st.sort === 'p1') r.sort(function (a, b) { return (a.price || 9e9) - (b.price || 9e9); });
      if (st.sort === 'p2') r.sort(function (a, b) { return (b.price || -1) - (a.price || -1); });
      if (st.sort === 'n1') r.sort(function (a, b) { return a.name.localeCompare(b.name, 'ru'); });
      if (st.sort === 'n2') r.sort(function (a, b) { return b.name.localeCompare(a.name, 'ru'); });
      return r;
    };
    var findCat = function (id) { var r = null; SP.cats.forEach(function (c) { if (c.id === id) r = c.t; (c.kids || []).forEach(function (k) { if (k.id === id && !r) r = k.t; }); }); return r; };
    var url = function (over) {
      var s = Object.assign({}, st, over || {}), o = new URLSearchParams();
      ['cat', 'q', 'name', 'art', 'text', 'minp', 'maxp', 'isnew', 'sale', 'sort'].forEach(function (k) { if (s[k] && !(k === 'cat' && s[k] === 'all')) o.set(k, s[k]); });
      if (s.brands.length) o.set('brands', s.brands.join(','));
      if (s.pp !== 20) o.set('pp', s.pp); if (s.page > 1) o.set('page', s.page);
      var q = o.toString(); return location.pathname + (q ? '?' + q : '');
    };
    var render = function () {
      var all = sorted(filtered()), per = st.pp, pages = Math.max(1, Math.ceil(all.length / per));
      if (st.page > pages) st.page = pages;
      var slice = all.slice((st.page - 1) * per, st.page * per);
      /* title */
      var oneBrand = st.brands.length === 1 ? brandName(st.brands[0]) : '';
      var title = st.cat !== 'all' ? findCat(st.cat) : (oneBrand ? 'Женская одежда ' + oneBrand : 'Каталог');
      if (st.cat === 'all' && !oneBrand) title = (st.q || st.name || st.art || st.text) ? 'Результаты поиска' : 'Смотреть всё';
      if (st.cat !== 'all' && oneBrand) title += ' ' + oneBrand;
      $('#catTitle').textContent = title; $('#catCrumb').textContent = title; document.title = title + ' — Sarah Pacini, Екатеринбург';
      $('#catCount').textContent = all.length + ' ' + (all.length % 10 === 1 && all.length % 100 !== 11 ? 'товар' : (all.length % 10 > 1 && all.length % 10 < 5 && (all.length % 100 < 10 || all.length % 100 >= 20) ? 'товара' : 'товаров'));
      var intro = $('#catIntro'); intro.hidden = !(st.brands.length === 1 && st.brands[0] === 'sp' && st.cat === 'all');
      /* chips */
      var ch = [];
      st.brands.forEach(function (b) { ch.push(['brands', brandName(b) || b, b]); });
      if (st.q) ch.push(['q', 'Поиск: ' + st.q]); if (st.name) ch.push(['name', 'Название: ' + st.name]); if (st.art) ch.push(['art', 'Артикул: ' + st.art]); if (st.text) ch.push(['text', 'Текст: ' + st.text]);
      if (st.minp || st.maxp) ch.push(['price', 'Цена: ' + (st.minp || '0') + '–' + (st.maxp || '∞')]);
      if (st.isnew) ch.push(['isnew', st.isnew === '1' ? 'Новинки' : 'Не новинки']); if (st.sale) ch.push(['sale', st.sale === '1' ? 'Спецпредложение' : 'Без спецпредложения']);
      if (st.cat !== 'all') ch.push(['cat', findCat(st.cat) || st.cat]);
      $('#chips').innerHTML = ch.map(function (c) { return '<button class="chip" data-chip="' + c[0] + '" data-v="' + esc(c[2] || '') + '">' + esc(c[1]) + ' ' + ico('x', 'ico" style="width:14px;height:14px') + '</button>'; }).join('') + (ch.length ? '<button class="chip" data-chip="all">Сбросить всё</button>' : '');
      /* list */
      var out = $('#items'), view = st.view;
      if (!slice.length) {
        out.className = ''; out.innerHTML = '<div class="empty"><h3>Здесь пока нет вещей на сайте</h3><p style="max-width:48ch;margin:0 auto 20px">На сайте показаны не все модели. Напишите нам — пришлём видеообзор и расскажем, что есть в наличии в бутике.</p><div class="cta-row" style="justify-content:center"><a class="btn" href="' + C.telegram + '" target="_blank" rel="noopener">Написать в Telegram</a><a class="btn ghost" href="' + ROOT + 'catalog.html?cat=all">Смотреть весь каталог</a></div></div>';
      } else if (view === 'price') {
        out.className = ''; out.innerHTML = '<table class="pl"><thead><tr><th></th><th>Название</th><th class="hide-s">Производитель</th><th>Цена</th><th></th></tr></thead><tbody>' + slice.map(function (p) {
          return '<tr><td><a href="' + ROOT + 'product/' + p.id + '.html"><img src="' + img(p.img) + '" alt="" loading="lazy"></a></td><td class="nm"><a href="' + ROOT + 'product/' + p.id + '.html">' + esc(p.name) + '</a></td><td class="hide-s muted">' + esc(brandName(p.brand)) + '</td><td>' + priceText(p) + '</td><td style="text-align:right"><button class="btn sm" data-add="' + p.id + '">В корзину</button></td></tr>';
        }).join('') + '</tbody></table>';
      } else {
        out.className = view === 'list' ? '' : 'grid';
        out.innerHTML = slice.map(function (p) { return card(p, view); }).join('');
      }
      /* pager */
      var pg = '';
      if (pages > 1) { for (var i = 1; i <= pages; i++) pg += '<button data-pg="' + i + '" class="' + (i === st.page ? 'on' : '') + '">' + i + '</button>'; }
      $('#pager').innerHTML = pg;
      /* controls */
      $('#sort').value = st.sort; $('#pp').value = st.pp;
      $$('.views button').forEach(function (b) { b.classList.toggle('on', b.dataset.view === st.view); });
      $('#fmin').value = st.minp; $('#fmax').value = st.maxp; $('#fnew').checked = st.isnew === '1'; $('#fsale').checked = st.sale === '1';
      /* brand facet */
      var base = filtered(true); var counts = {}; base.forEach(function (p) { counts[p.brand] = (counts[p.brand] || 0) + 1; });
      $('#fbrands').innerHTML = SP.brands.filter(function (b) { return b.facet; }).map(function (b) {
        return '<div class="chk"><label><input type="checkbox" value="' + b.id + '"' + (st.brands.indexOf(b.id) > -1 ? ' checked' : '') + '><span>' + esc(b.t) + '</span><span class="cnt">' + (counts[b.id] || 0) + '</span></label></div>';
      }).join('');
      $('#fshow').textContent = 'Показать (' + all.length + ')';
      $('#fcats').innerHTML = SP.cats.filter(function (c) { return c.kids && c.id !== 'sp' && c.id !== 'aksessuary'; }).map(function (c) {
        return c.kids.map(function (k) { return '<a href="' + ROOT + 'catalog.html?cat=' + k.id + '" class="' + (st.cat === k.id ? 'on' : '') + '">' + esc(k.t) + '</a>'; }).join('');
      }).join('');
      markCmp(); cmpBar();
      history.replaceState(null, '', url());
    };
    var upd = function (o) { Object.assign(st, o); st.page = o && o.page ? o.page : 1; render(); };
    $('#sort').addEventListener('change', function (e) { upd({ sort: e.target.value }); });
    $('#pp').addEventListener('change', function (e) { upd({ pp: Number(e.target.value) }); });
    $$('.views button').forEach(function (b) { b.addEventListener('click', function () { store.set('sp_view', b.dataset.view); upd({ view: b.dataset.view }); }); });
    $('#fbrands').addEventListener('change', function () { upd({ brands: $$('input:checked', $('#fbrands')).map(function (i) { return i.value; }) }); });
    ['fmin', 'fmax'].forEach(function (id) { $('#' + id).addEventListener('change', function () { upd({ minp: $('#fmin').value, maxp: $('#fmax').value }); }); });
    $('#fnew').addEventListener('change', function (e) { upd({ isnew: e.target.checked ? '1' : '' }); });
    $('#fsale').addEventListener('change', function (e) { upd({ sale: e.target.checked ? '1' : '' }); });
    $('#freset').addEventListener('click', function () { upd({ brands: [], minp: '', maxp: '', isnew: '', sale: '', q: '', name: '', art: '', text: '' }); });
    $('#fshow').addEventListener('click', closeAll);
    $$('[data-price]').forEach(function (b) { b.addEventListener('click', function () { var r = b.dataset.price.split('-'); upd({ minp: r[0], maxp: r[1] }); }); });
    $('#pager').addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) { upd({ page: Number(b.dataset.pg) }); window.scrollTo({ top: catEl.offsetTop - 120, behavior: 'smooth' }); } });
    $('#chips').addEventListener('click', function (e) {
      var b = e.target.closest('[data-chip]'); if (!b) return; var k = b.dataset.chip;
      if (k === 'all') return upd({ brands: [], minp: '', maxp: '', isnew: '', sale: '', q: '', name: '', art: '', text: '', cat: 'all' });
      if (k === 'brands') return upd({ brands: st.brands.filter(function (x) { return x !== b.dataset.v; }) });
      if (k === 'price') return upd({ minp: '', maxp: '' });
      if (k === 'cat') return upd({ cat: 'all' });
      var o = {}; o[k] = ''; upd(o);
    });
    render();
  }

  /* ---------- cart page ---------- */
  var cartPage = $('#cartPage');
  if (cartPage) {
    window.__renderCart = function () {
      var ids = Object.keys(cart).filter(function (k) { return BY[k]; });
      $('#cartEmpty').hidden = ids.length > 0; $('#cartFull').hidden = !ids.length;
      $('#cartRows').innerHTML = ids.map(function (k) {
        var p = BY[k];
        return '<div class="ct-row"><a href="' + ROOT + 'product/' + p.id + '.html"><img src="' + img(p.img) + '" alt=""></a><div><div class="nm"><a href="' + ROOT + 'product/' + p.id + '.html">' + esc(p.name) + '</a></div><div class="muted" style="font-size:14px">' + esc(brandName(p.brand)) + ' · ' + priceText(p) + '</div></div>' +
          '<div class="qty"><button data-q="' + p.id + '" data-d="-1" aria-label="Меньше">−</button><input value="' + cart[k] + '" readonly><button data-q="' + p.id + '" data-d="1" aria-label="Больше">+</button></div>' +
          '<div class="sum">' + (p.price ? fmt(p.price * cart[k]) + ' ₽' : 'по запросу') + '</div><button class="rm" data-rm="' + p.id + '" aria-label="Удалить">' + ico('trash') + '</button></div>';
      }).join('');
      var t = cartTotals();
      $('#cartCnt').textContent = cartCount(); $('#cartSum').textContent = t.sum ? fmt(t.sum) + ' ₽' : '—';
      $('#cartAsk').hidden = !t.ask; $('#cartAsk span').textContent = t.ask;
    };
    window.__renderCart();
    $('#cartClear').addEventListener('click', function () { cart = {}; saveCart(); window.__renderCart(); renderMini(); });
  }
  function orderText() {
    var lines = [], t = cartTotals();
    Object.keys(cart).forEach(function (k) { var p = BY[k]; if (p) lines.push('• ' + p.name + ' — ' + cart[k] + ' шт. — ' + (p.price ? fmt(p.price * cart[k]) + ' ₽' : 'цена по запросу')); });
    return lines.join('\n') + '\n\nИтого по указанным ценам: ' + (t.sum ? fmt(t.sum) + ' ₽' : '—') + (t.ask ? ' (+ ' + t.ask + ' поз. по запросу)' : '');
  }

  /* ---------- compare page ---------- */
  var cmpPage = $('#cmpPage');
  if (cmpPage) {
    window.__renderCmp = function () {
      var l = store.get('sp_cmp', []).filter(function (k) { return BY[k]; });
      $('#cmpEmpty').hidden = l.length > 0; $('#cmpTable').hidden = !l.length;
      if (!l.length) return;
      var row = function (lab, fn) { return '<tr><th>' + lab + '</th>' + l.map(function (k) { return '<td>' + fn(BY[k]) + '</td>'; }).join('') + '</tr>'; };
      $('#cmpTable').innerHTML = '<table class="cmp-t"><tbody>' +
        row('', function (p) { return '<a href="' + ROOT + 'product/' + p.id + '.html"><img src="' + img(p.img) + '" alt=""></a>'; }) +
        row('Название', function (p) { return '<a class="link" href="' + ROOT + 'product/' + p.id + '.html">' + esc(p.name) + '</a>'; }) +
        row('Производитель', function (p) { return esc(brandName(p.brand)); }) +
        row('Категория', function (p) { return esc(leafName(p.cat)); }) +
        row('Цена', function (p) { return '<b>' + priceText(p) + '</b>'; }) +
        row('Материал', function (p) { return esc(p.material || 'Уточняйте у менеджера'); }) +
        row('Описание', function (p) { return esc(p.desc || '—'); }) +
        row('', function (p) { return '<button class="btn sm" data-add="' + p.id + '">В корзину</button><br><button class="link" style="margin-top:12px;color:var(--steel)" data-cmp="' + p.id + '">Убрать</button>'; }) +
        '</tbody></table>';
      markCmp();
    };
    window.__renderCmp();
  }

  /* ---------- product page ---------- */
  var pdp = $('.pdp');
  if (pdp) {
    $$('.gal .th button').forEach(function (b) {
      b.addEventListener('click', function () { $('.gal .main img').src = b.dataset.src; $$('.gal .th button').forEach(function (x) { x.classList.toggle('on', x === b); }); });
    });
    $$('.tabs .tl button').forEach(function (b) {
      b.addEventListener('click', function () { $$('.tabs .tl button').forEach(function (x) { x.classList.toggle('on', x === b); }); $$('.tabs .pn').forEach(function (p) { p.classList.toggle('on', p.id === b.dataset.tab); }); });
    });
    var oc = $('[data-oneclick]');
    oc && oc.addEventListener('click', function () { $('#ocName').textContent = oc.dataset.oneclick; $('#ocForm').dataset.product = oc.dataset.oneclick; openO('oneclick'); });
  }

  /* ---------- slider ---------- */
  $$('.slider').forEach(function (s) {
    var tr = $('.slides', s), n = $$('.slide', s).length, i = 0, dots = $('.dots', s), timer;
    if (dots) dots.innerHTML = Array.apply(null, Array(n)).map(function (_, k) { return '<button aria-label="Слайд ' + (k + 1) + '"></button>'; }).join('');
    var go = function (k) { i = (k + n) % n; tr.style.transform = 'translateX(' + (-100 * i) + '%)'; $$('.dots button', s).forEach(function (d, j) { d.classList.toggle('on', j === i); }); };
    var auto = function () { clearInterval(timer); if (!matchMedia('(prefers-reduced-motion:reduce)').matches) timer = setInterval(function () { go(i + 1); }, 6000); };
    $('.sl-btn.p', s).addEventListener('click', function () { go(i - 1); auto(); });
    $('.sl-btn.n', s).addEventListener('click', function () { go(i + 1); auto(); });
    dots && dots.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) { go($$('button', dots).indexOf(b)); auto(); } });
    var x0 = null; s.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    s.addEventListener('touchend', function (e) { if (x0 == null) return; var d = e.changedTouches[0].clientX - x0; if (Math.abs(d) > 40) { go(i + (d < 0 ? 1 : -1)); auto(); } x0 = null; });
    go(0); auto();
  });

  /* ---------- lightbox ---------- */
  var lb, lbList = [], lbI = 0;
  function showLB(i) { lbI = (i + lbList.length) % lbList.length; $('img', lb).src = lbList[lbI]; }
  function closeLB() { lb && lb.classList.remove('on'); }
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-lb]'); if (!a) return; e.preventDefault();
    var grp = $$('[data-lb="' + a.dataset.lb + '"]'); lbList = grp.map(function (x) { return x.getAttribute('href') || x.dataset.full || $('img', x).src; });
    if (!lb) { lb = document.createElement('div'); lb.className = 'lb'; lb.innerHTML = '<img alt=""><button class="c" aria-label="Закрыть">×</button><button class="pv" aria-label="Назад">‹</button><button class="nx" aria-label="Вперёд">›</button>'; document.body.appendChild(lb);
      lb.addEventListener('click', function (ev) { if (ev.target.classList.contains('pv')) showLB(lbI - 1); else if (ev.target.classList.contains('nx')) showLB(lbI + 1); else closeLB(); }); }
    lb.classList.add('on'); showLB(grp.indexOf(a));
  });

  /* ---------- floating contact ---------- */
  var fl = $('.float .fab'); fl && fl.addEventListener('click', function () { fl.parentNode.classList.toggle('on'); });

  /* ---------- forms ---------- */
  function validate(form) {
    var ok = true;
    $$('.fld', form).forEach(function (f) {
      var i = $('input,textarea', f); if (!i) return; var bad = false;
      if (i.required && !i.value.trim()) bad = true;
      if (i.type === 'email' && i.value && !/^\S+@\S+\.\S+$/.test(i.value)) bad = true;
      if (i.dataset.contact && i.value && !(/^\S+@\S+\.\S+$/.test(i.value) || i.value.replace(/\D/g, '').length >= 10)) bad = true;
      if (i.type === 'tel' && i.value && i.value.replace(/\D/g, '').length < 10) bad = true;
      f.classList.toggle('err', bad); if (bad) ok = false;
    });
    var ag = $('input[type=checkbox][required]', form); if (ag && !ag.checked) { ok = false; toast('Подтвердите согласие на обработку персональных данных'); }
    return ok;
  }
  function send(kind, subject, body, form) {
    var ep = C.endpoints && C.endpoints[kind];
    var done = function () { var ok = $('.ok-box', form.parentNode); form.hidden = true; if (ok) ok.hidden = false; };
    if (ep) {
      var fd = new FormData(form); fd.append('subject', subject); fd.append('body', body);
      fetch(ep, { method: 'POST', body: fd }).then(function (r) { if (!r.ok) throw 0; done(); }).catch(function () { toast('Не удалось отправить. Напишите нам в Telegram или позвоните.'); });
    } else {
      location.href = 'mailto:' + C.email + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      done();
    }
  }
  var val = function (form, name) { var el = form.elements[name]; return el ? el.value.trim() : ''; };
  document.addEventListener('submit', function (e) {
    var form = e.target.closest('form[data-form]'); if (!form) return; e.preventDefault();
    var kind = form.dataset.form;
    if (kind === 'search') { var q = new URLSearchParams(new FormData(form)); Array.from(q.keys()).forEach(function (k) { if (!q.get(k)) q.delete(k); }); location.href = ROOT + 'catalog.html' + (q.toString() ? '?' + q.toString() : ''); return; }
    if (kind === 'quick') { var v = val(form, 'q'); location.href = ROOT + 'catalog.html' + (v ? '?q=' + encodeURIComponent(v) : ''); return; }
    if (!validate(form)) return;
    if (kind === 'login') { toast('Личный кабинет подключается к серверной части сайта. Пока напишите нам или позвоните.'); return; }
    if (kind === 'forgot') { send('forgot', 'Восстановление пароля', 'Прошу восстановить доступ для: ' + val(form, 'email'), form); return; }
    if (kind === 'contact') { send('contact', 'Сообщение с сайта от ' + val(form, 'name'), 'Имя / организация: ' + val(form, 'name') + '\nКонтакт: ' + val(form, 'contact') + '\n\n' + val(form, 'text'), form); return; }
    if (kind === 'oneclick') { send('oneclick', 'Купить в один клик: ' + (form.dataset.product || ''), 'Товар: ' + (form.dataset.product || '') + '\nИмя: ' + val(form, 'name') + '\nТелефон: ' + val(form, 'phone'), form); return; }
    if (kind === 'board') { send('board', 'Сообщение на доске объявлений', 'Имя: ' + val(form, 'name') + '\nE-mail: ' + val(form, 'email') + '\n\n' + val(form, 'text'), form); return; }
    if (kind === 'checkout') {
      if (!Object.keys(cart).length) { toast('Корзина пуста'); return; }
      var body = 'Заказ с сайта\n\n' + orderText() + '\n\nИмя: ' + val(form, 'name') + '\nТелефон: ' + val(form, 'phone') + '\nE-mail: ' + val(form, 'email') + '\nГород и адрес: ' + val(form, 'addr') + '\nСвязь: ' + val(form, 'via') + '\nКомментарий: ' + val(form, 'comment');
      var ok = $('#orderDone'); window.__lastOrder = body;
      var ep = C.endpoints && C.endpoints.checkout;
      var finish = function () { form.hidden = true; ok.hidden = false; $('#orderText').value = body; $('#orderMail').href = 'mailto:' + C.email + '?subject=' + encodeURIComponent('Заказ с сайта') + '&body=' + encodeURIComponent(body); window.scrollTo({ top: 0, behavior: 'smooth' }); };
      if (ep) { var fd = new FormData(form); fd.append('order', body); fetch(ep, { method: 'POST', body: fd }).then(function (r) { if (!r.ok) throw 0; cart = {}; saveCart(); renderMini(); finish(); }).catch(function () { toast('Не удалось отправить заказ. Отправьте его по e-mail или в мессенджер.'); finish(); }); }
      else finish();
    }
  });
  $$('input,textarea').forEach(function (i) { i.addEventListener('input', function () { var f = i.closest('.fld'); f && f.classList.remove('err'); }); });
  var cp = $('#orderCopy'); cp && cp.addEventListener('click', function () { var t = $('#orderText'); t.select(); try { navigator.clipboard.writeText(t.value); } catch (e) { document.execCommand('copy'); } toast('Заказ скопирован — вставьте его в чат'); });

  /* ---------- init ---------- */
  badges(); markCmp(); cmpBar(); renderMini();
  if (location.hash === '#cart') { renderMini(); openO('cart'); }
})();
