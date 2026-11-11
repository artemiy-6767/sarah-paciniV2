#!/usr/bin/env python3
"""Generates the redesigned static site into ../sarah-pacini-site"""
import json, os, shutil, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from products import load

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "sarah-pacini-site")

CONFIG = {
    "imgBase": "https://lady-blues.ru",   # '' если сайт будет лежать на lady-blues.ru
    "phone": "+7 912 664-30-06", "tel": "+79126643006",
    "email": "irina_shupova@mail.ru",
    "telegram": "https://t.me/+9qPt_0Mn9gw2MGFi",
    "max": "https://max.ru/u/f9LHodD0cOJoU7f1neCyUfe7MM_fpaE9rcEw2Eq0jK_FXXeBC4DmUqIfuSA",
    "instagram": "https://www.instagram.com/sarah_pacini_ekb/",
    "endpoints": {},   # сюда можно прописать URL серверных обработчиков форм: contact, oneclick, checkout, board, forgot
}
ADDR = "Екатеринбург, ул. Посадская, 28а, ТЦ «Универбыт», 2 этаж, бутик № 200"
IMG = lambda f: f"{CONFIG['imgBase']}/d/{f}"

ICONS = {
 "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
 "bag": '<path d="M5 8h14l-1 12H6L5 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "x": '<path d="M6 6l12 12M18 6 6 18"/>',
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A15 15 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
 "pin": '<path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
 "truck": '<path d="M2 6h11v10H2zM13 10h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
 "video": '<rect x="3" y="6" width="13" height="12" rx="1"/><path d="m16 10 5-3v10l-5-3"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "hanger": '<path d="M12 7a2 2 0 1 0-2-2"/><path d="M12 7v2l9 6a1 1 0 0 1-.6 1.8H3.6A1 1 0 0 1 3 15l9-6"/>',
 "award": '<circle cx="12" cy="9" r="5"/><path d="M8.5 13.5 7 21l5-3 5 3-1.5-7.5"/>',
 "cmp": '<rect x="4" y="4" width="6" height="16"/><rect x="14" y="4" width="6" height="16"/>',
 "trash": '<path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"/>',
 "grid": '<rect x="4" y="4" width="7" height="7"/><rect x="13" y="4" width="7" height="7"/><rect x="4" y="13" width="7" height="7"/><rect x="13" y="13" width="7" height="7"/>',
 "list": '<rect x="3" y="4" width="5" height="5"/><path d="M11 6.5h10"/><rect x="3" y="15" width="5" height="5"/><path d="M11 17.5h10"/>',
 "price": '<path d="M4 5h16M4 10h16M4 15h16M4 20h16"/>',
 "chev": '<path d="m9 6 6 6-6 6"/>', "chevl": '<path d="m15 6-6 6 6 6"/>',
 "check": '<path d="m5 12 5 5 9-10"/>', "filter": '<path d="M4 6h16M7 12h10M10 18h4"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="1"/><path d="m3 7 9 6 9-6"/>',
 "tg": '<path d="M21 4 3 11l5 2 2 6 3-4 5 3z"/>',
 "insta": '<rect x="4" y="4" width="16" height="16" rx="4"/><circle cx="12" cy="12" r="3.5"/><circle cx="17" cy="7" r=".6"/>',
 "chat": '<path d="M4 5h16v11H9l-5 4z"/>',
}
def ic(n, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[n]}</svg>'

LEAF = {"bryuki": "Брюки и леггинсы", "dgempera": "Джемпера / Кофты", "cardigany": "Кардиганы / Жакеты / Жилеты",
        "tuniki": "Футболки / Рубашки / Блузы", "topy": "Топы / Базы", "platya": "Платья", "yubki": "Юбки",
        "kurtki": "Верхняя одежда", "palantiny": "Палантины / Шарфы / Шапки", "sumki": "Сумки / Ремни", "ukrasheniya": "Украшения"}
CATS = [
    {"id": "odezhda", "t": "Каталог одежды", "kids": [{"id": k, "t": LEAF[k]} for k in
        ["bryuki", "dgempera", "cardigany", "tuniki", "topy", "platya", "yubki", "kurtki", "palantiny"]]},
    {"id": "aksessuary", "t": "Аксессуары", "kids": [{"id": "sumki", "t": "Сумки / Ремни"}, {"id": "ukrasheniya", "t": "Украшения"}]},
]
BRANDS = [
    {"id": "alpa", "t": "ALPA трикотаж", "facet": True}, {"id": "ag", "t": "ANNETTE GORTZ", "facet": True},
    {"id": "maxa", "t": "Maxa", "facet": True}, {"id": "pj", "t": "PJ Murano", "facet": True},
    {"id": "sp", "t": "Sarah Pacini", "facet": True}, {"id": "tr", "t": "TRANSIT Италия", "facet": True},
    {"id": "kn", "t": "KristenseN du Nord", "facet": False}, {"id": "ec", "t": "Европейская культура", "facet": False},
]
PRODUCTS = load()

def cl(**kw):
    return "@/catalog.html?" + "&".join(f"{k}={v}" for k, v in kw.items())

MENU = [
    ("Каталог одежды", cl(cat="odezhda"), [(LEAF[k], cl(cat=k)) for k in ["bryuki", "dgempera", "cardigany", "tuniki", "topy", "platya", "yubki", "kurtki", "palantiny"]], ""),
    ("Sarah Pacini", cl(brand="sp"), [("Весь каталог Sarah Pacini", cl(brand="sp")), ("Джемпера / Кофты / Свитера", cl(brand="sp", cat="dgempera")),
        ("Кардиганы", cl(brand="sp", cat="cardigany")), ("Базы / Топы", cl(brand="sp", cat="topy")), ("Туники / Рубашки / Блузы", cl(brand="sp", cat="tuniki")),
        ("Брюки и леггинсы", cl(brand="sp", cat="bryuki")), ("Платья", cl(brand="sp", cat="platya")), ("Юбки", cl(brand="sp", cat="yubki")),
        ("Аксессуары", cl(brand="sp", cat="aksessuary"))], ""),
    ("TRANSIT", cl(brand="tr"), [], ""),
    ("Annette Gortz", cl(brand="ag"), [], ""),
    ("Верхняя одежда", cl(cat="kurtki"), [], ""),
    ("Аксессуары", cl(cat="aksessuary"), [("Палантины / Шарфы / Шапки", cl(cat="palantiny")), ("Сумки / Ремни", cl(cat="sumki")), ("Украшения", cl(cat="ukrasheniya"))], ""),
    ("Kristensen du Nord", cl(brand="kn"), [], ""),
    ("Европейская культура", cl(brand="ec"), [], ""),
    ("Образы", "@/looks.html", [], ""),
    ("Распродажа", cl(sale="1"), [], "sale"),
]

TG_ICON = ic("tg")
def msgr(extra=""):
    return (f'<div class="msgr {extra}"><a href="{CONFIG["max"]}" target="_blank" rel="noopener"><img src="{IMG("max-messenger-sign-l.svg")}" alt="">MAX</a>'
            f'<a href="{CONFIG["telegram"]}" target="_blank" rel="noopener">{TG_ICON}Telegram</a>'
            f'<a href="tel:{CONFIG["tel"]}">{ic("phone")}{CONFIG["phone"]}</a></div>')

# ---------------------------------------------------------------- shell
def nav_html():
    out = []
    for t, href, kids, cls in MENU:
        dd = ""
        if kids:
            dd = '<div class="dd">' + "".join(f'<a href="{h}">{html.escape(n)}</a>' for n, h in kids) + "</div>"
        out.append(f'<li class="t {cls}"><a href="{href}">{html.escape(t)}</a>{dd}</li>')
    return '<ul class="top">' + "".join(out) + "</ul>"

def mob_menu():
    out = []
    for t, href, kids, cls in MENU:
        if kids:
            out.append(f'<details><summary>{html.escape(t)}{ic("chev")}</summary>' + "".join(f'<a href="{h}">{html.escape(n)}</a>' for n, h in kids) + "</details>")
        else:
            out.append(f'<a href="{href}">{html.escape(t)}</a>')
    out.append('<a href="@/o-kompanii.html">О компании</a><a href="@/brendy.html">Бренды</a><a href="@/kontakty.html">Контакты</a><a href="@/napishite-nam.html">Напишите нам</a>')
    return '<div class="mobmenu">' + "".join(out) + "</div>"

CAT_OPTIONS = '<option value="all">Все</option><option value="odezhda">Каталог одежды</option>' + "".join(f'<option value="{k}">» {v}</option>' for k, v in LEAF.items())
def adv_form():
    brands = "".join(f'<option value="{b["id"]}">{html.escape(b["t"])}</option>' for b in BRANDS if b["facet"])
    pp = "".join(f'<option{" selected" if n == 20 else ""}>{n}</option>' for n in [5, 20, 35, 50, 65, 80, 95])
    return f'''<form data-form="search" class="f two" novalidate>
<div class="fld full"><label for="a-name">Название</label><input id="a-name" name="name"></div>
<div class="fld"><label for="a-min">Цена от, ₽</label><input id="a-min" name="minp" inputmode="numeric"></div>
<div class="fld"><label for="a-max">Цена до, ₽</label><input id="a-max" name="maxp" inputmode="numeric"></div>
<div class="fld"><label for="a-art">Артикул</label><input id="a-art" name="art"></div>
<div class="fld"><label for="a-text">Текст в описании</label><input id="a-text" name="text"></div>
<div class="fld"><label for="a-cat">Категория</label><select id="a-cat" name="cat">{CAT_OPTIONS}</select></div>
<div class="fld"><label for="a-brand">Производитель</label><select id="a-brand" name="brand"><option value="">Все</option>{brands}</select></div>
<div class="fld"><label for="a-new">Новинка</label><select id="a-new" name="isnew"><option value="">Все</option><option value="1">Да</option><option value="0">Нет</option></select></div>
<div class="fld"><label for="a-sale">Спецпредложение</label><select id="a-sale" name="sale"><option value="">Все</option><option value="1">Да</option><option value="0">Нет</option></select></div>
<div class="fld"><label for="a-pp">Результатов на странице</label><select id="a-pp" name="pp">{pp}</select></div>
<div class="full"><button class="btn block" type="submit">Найти</button></div></form>'''

def header():
    return f'''<div class="ann"><div class="wrap"><span>Бесплатная доставка по всей России</span><div class="r"><span>Ежедневно с 10:00 до 20:00</span><a href="tel:{CONFIG["tel"]}">{CONFIG["phone"]}</a></div></div></div>
<header class="hdr"><div class="wrap hdr-in">
<div style="display:flex;align-items:center;gap:6px"><button class="ibtn burger" data-open="mob" aria-label="Меню">{ic("menu")}</button>
<a class="logo" href="@/index.html" aria-label="Sarah Pacini — на главную"><b>Sarah Pacini</b><i>Бутик итальянской одежды</i></a></div>
<form class="hdr-search" data-form="quick" role="search"><label class="sr" for="hq">Поиск по каталогу</label><input id="hq" name="q" placeholder="Что вы ищете?" autocomplete="off"><button aria-label="Найти" type="submit">{ic("search")}</button><button type="button" class="adv" data-open="search">Расширенный поиск</button></form>
<div class="hdr-act"><a class="hdr-phone" href="tel:{CONFIG["tel"]}">{CONFIG["phone"]}<small>Ежедневно 10:00–20:00</small></a>
<button class="ibtn only-m" data-open="search" aria-label="Поиск">{ic("search")}</button>
<button class="ibtn" data-open="login" aria-label="Вход в кабинет">{ic("user")}</button>
<a class="ibtn" href="@/compare.html" aria-label="Сравнение">{ic("cmp")}<span class="n" data-cmp-n data-n="0"></span></a>
<button class="ibtn" data-open="cart" aria-label="Корзина">{ic("bag")}<span class="n" data-cart-n data-n="0"></span></button></div>
</div><nav class="nav" aria-label="Каталог"><div class="wrap">{nav_html()}</div></nav></header>'''

def modals():
    return f'''<div class="veil" id="veil"></div>
<aside class="drawer left" id="mob" aria-label="Меню"><div class="drawer-h"><h3>Меню</h3><button class="ibtn" data-close aria-label="Закрыть">{ic("x")}</button></div><div class="drawer-b">{mob_menu()}</div></aside>
<aside class="drawer" id="cart" aria-label="Корзина"><div class="drawer-h"><h3>Корзина</h3><button class="ibtn" data-close aria-label="Закрыть">{ic("x")}</button></div>
<div class="drawer-b" id="miniItems"></div>
<div class="drawer-f" id="miniFoot" hidden><div style="display:flex;justify-content:space-between;margin-bottom:6px"><span>Итого</span><b id="miniSum"></b></div><p class="muted" style="font-size:13px;margin-bottom:14px">Цену, размеры и наличие подтвердит менеджер.</p><a class="btn block" href="@/cart.html">Оформить заказ</a></div></aside>
<div class="modal wide" id="search" role="dialog" aria-label="Расширенный поиск"><button class="x" data-close aria-label="Закрыть">{ic("x")}</button><h3>Расширенный поиск</h3><p class="muted">Заполните только то, что знаете.</p>{adv_form()}</div>
<div class="modal" id="login" role="dialog" aria-label="Вход в кабинет"><button class="x" data-close aria-label="Закрыть">{ic("x")}</button><h3>Вход в кабинет</h3>
<form data-form="login" class="f" novalidate><div class="fld"><label for="l-login">Логин или e-mail</label><input id="l-login" name="login" required autocomplete="username"><div class="em">Введите логин или e-mail</div></div>
<div class="fld"><label for="l-pass">Пароль</label><input id="l-pass" name="password" type="password" required autocomplete="current-password"><div class="em">Введите пароль</div></div>
<button class="btn block" type="submit">Войти</button><div style="display:flex;justify-content:space-between;font-size:14px"><a class="link" href="@/forgot-password.html">Забыли пароль?</a><a class="link" href="@/register.html">Регистрация</a></div></form></div>
<div class="modal" id="oneclick" role="dialog" aria-label="Купить в один клик"><button class="x" data-close aria-label="Закрыть">{ic("x")}</button><h3>Купить в один клик</h3><p class="muted" id="ocName"></p>
<div><form data-form="oneclick" id="ocForm" class="f" novalidate><div class="fld"><label for="oc-n">Ваше имя</label><input id="oc-n" name="name" required><div class="em">Укажите имя</div></div>
<div class="fld"><label for="oc-p">Телефон</label><input id="oc-p" name="phone" type="tel" required placeholder="+7"><div class="em">Укажите телефон с кодом</div></div>
<label class="chk"><input type="checkbox" required> Согласен на обработку персональных данных</label><button class="btn block" type="submit">Отправить заявку</button></form>
<div class="ok-box" hidden><b>Заявка готова.</b><p>Если почтовая программа не открылась, позвоните нам: <a class="link" href="tel:{CONFIG["tel"]}">{CONFIG["phone"]}</a> или напишите в мессенджер.</p></div></div></div>
<div class="cmpbar" id="cmpbar"><span>В сравнении: <b id="cmpbarN">0</b></span><a class="btn" href="@/compare.html">Сравнить</a><button class="c" id="cmpClear">Очистить</button></div>
<div class="float"><div class="opts"><a href="{CONFIG["max"]}" target="_blank" rel="noopener"><img src="{IMG("max-messenger-sign-l.svg")}" alt="">MAX</a><a href="{CONFIG["telegram"]}" target="_blank" rel="noopener">{TG_ICON}Telegram</a><a href="tel:{CONFIG["tel"]}">{ic("phone")}Позвонить</a></div>
<button class="fab" aria-label="Связаться с нами">{ic("chat")}</button></div>
<nav class="mobbar" aria-label="Быстрая навигация"><a href="@/catalog.html?cat=all">{ic("grid")}Каталог</a><button data-open="search">{ic("search")}Поиск</button><a href="tel:{CONFIG["tel"]}">{ic("phone")}Звонок</a><button data-open="cart">{ic("bag")}Корзина<span class="n" data-cart-n data-n="0"></span></button></nav>'''

def footer():
    return f'''<footer class="ftr"><div class="wrap"><div class="cols">
<div><a class="logo" href="@/index.html"><b>Sarah Pacini</b><i>Бутик итальянской одежды</i></a><p>Одежда из натуральных тканей от европейских брендов. Более 20 лет работаем для вас в Екатеринбурге.</p>
<div class="soc"><a href="{CONFIG["max"]}" target="_blank" rel="noopener" aria-label="MAX"><img src="{IMG("max-messenger-sign-l.svg")}" alt=""></a><a href="{CONFIG["telegram"]}" target="_blank" rel="noopener" aria-label="Telegram">{ic("tg")}</a><a href="{CONFIG["instagram"]}" target="_blank" rel="noopener" aria-label="Instagram">{ic("insta")}</a></div></div>
<div><h4>Каталог</h4><ul><li><a href="@/catalog.html?cat=all">Смотреть всё</a></li><li><a href="@/catalog.html?brand=sp">Sarah Pacini</a></li><li><a href="@/catalog.html?brand=tr">TRANSIT</a></li><li><a href="@/catalog.html?cat=aksessuary">Аксессуары</a></li><li><a href="@/looks.html">Образы</a></li><li><a href="@/catalog.html?sale=1">Распродажа</a></li></ul></div>
<div><h4>Компания</h4><ul><li><a href="@/index.html">Главная</a></li><li><a href="@/o-kompanii.html">О компании</a></li><li><a href="@/brendy.html">Бренды</a></li><li><a href="@/kontakty.html">Контакты</a></li><li><a href="@/napishite-nam.html">Напишите нам</a></li><li><a href="@/karta-sayta.html">Карта сайта</a></li><li><a href="@/doska-obyavleniy.html">Доска объявлений</a></li></ul></div>
<div><h4>Контакты</h4><ul><li><a href="tel:{CONFIG["tel"]}">{CONFIG["phone"]}</a></li><li>Ежедневно с 10:00 до 20:00</li><li>{ADDR}</li><li><a href="mailto:{CONFIG["email"]}">{CONFIG["email"]}</a></li></ul></div></div>
<div class="bot"><span>© 2017–2026 Sarah Pacini · ООО «Леди Блюз»</span><span>Цены на сайте носят информационный характер и не являются публичной офертой.</span></div></div></footer>'''

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600&family=Prata&display=swap&subset=cyrillic" rel="stylesheet">'

def page(path, title, desc, body, base="", extra_head=""):
    doc = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc, quote=True)}"><meta name="format-detection" content="telephone=no">
{FONTS}<link rel="stylesheet" href="@/assets/style.css">{extra_head}</head>
<body data-root="{base}">{header()}<main id="main">{body}</main>{footer()}{modals()}
<script src="@/assets/data.js"></script><script src="@/assets/app.js" defer></script></body></html>'''
    doc = doc.replace("@/", base)
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(doc)

def crumbs(items):
    parts = []
    for i, (t, h) in enumerate(items):
        parts.append(f'<a href="{h}">{html.escape(t)}</a>' if h else f'<b style="font-weight:500;color:var(--ink)">{html.escape(t)}</b>')
    return '<nav class="crumbs" aria-label="Хлебные крошки"><div class="wrap">' + "<span>/</span>".join(parts) + "</div></nav>"

def slider(slides):
    sl = []
    for img, cap, href in slides:
        c = f'<span class="cap">{html.escape(cap)}{ic("chev")}</span>' if cap else ""
        alt = html.escape(cap or "Фото")
        tag = f'<a class="slide" href="{href}">' if href else '<div class="slide">'
        end = "</a>" if href else "</div>"
        sl.append(f'{tag}<img src="{IMG(img)}" alt="{alt}" {"loading=lazy" if sl else ""}>{c}{end}')
    return (f'<div class="slider" aria-roledescription="carousel"><div class="slides">{"".join(sl)}</div>'
            f'<button class="sl-btn p" aria-label="Назад">{ic("chevl")}</button><button class="sl-btn n" aria-label="Вперёд">{ic("chev")}</button><div class="dots"></div></div>')

def addr_box():
    return f'<div class="store">{ic("pin")}<b>Примерить и купить — в нашем бутике</b><span>{ADDR}. Ежедневно с 10:00 до 20:00.</span></div>'

SP_TEXT = ("Коллекция одежды Sarah Pacini — это видение, эволюция, адаптация: одежда колдует над силой переосмысления себя. "
           "Позитивное мышление побуждает нас видеть дальше и вдохновлять окружающих. Откройте для себя коллекцию — осознание самого себя и творчество.")
SP_TEXT2 = ("Новые грани себя — натуральность и естественность. Одежда в коллекции преимущественно выполнена из натуральных материалов. "
            "Внимание на детали и текстуры. Геометрические узоры и другие графические элементы вызывают беззаботность и свободу мыслей и мечтаний.")
TR_TEXT = ("Итальянская марка TRANSIT была создана в 1986 году как фирма по пошиву женской одежды высокого качества. Одежда шьётся на фабрике, "
           "которая осуществляет полный процесс производства изделий и является семейным бизнесом. Высококачественное сырьё, невычурная элегантность, "
           "индивидуальность, свобода и соотношение цены и качества — так TRANSIT подходит и к одежде, и к жизни.")
LEGAL = ('Цена, указанная на сайте, носит исключительно информационно-рекламный характер и не является офертой или публичной офертой '
         'в соответствии со статьёй 435 и пунктом 2 статьи 437 Гражданского кодекса Российской Федерации. Указанные на сайте цены не являются '
         'окончательной ценой договора, возможны скидки постоянным клиентам и акции. Цену уточняйте по телефону 8-912-664-30-06.')

# ---------------------------------------------------------------- home
def home():
    first = {}
    for p in PRODUCTS:
        first.setdefault(p["cat"], p)
    def tile(cat, label, big=False):
        p = first[cat]
        return f'<a class="tile{" big" if big else ""}" href="@/catalog.html?cat={cat}"><img src="{IMG(p["img"])}" alt="{label}" loading="lazy"><span>{label}</span></a>'
    slides = [("slajd_1_431212.jpg", "Sarah Pacini, коллекция 2026", cl(brand="sp")), ("slajd_1.jpg", "TRANSIT, лето 2026", cl(brand="tr")),
              ("slajd_kristensen_na_glavnuyu.jpg", "Kristensen du Nord", cl(brand="kn")), ("tranzit_zima_22.png", "TRANSIT", cl(brand="tr")),
              ("slajd_aksessuary.jpg", "Аксессуары", cl(cat="aksessuary")), ("ukrasheniya.jpg", "Украшения PJ Murano", cl(cat="ukrasheniya")),
              ("slayd_filosofiya.jpg", "Философия бренда Sarah Pacini", "@/brendy/sarah-pacini.html")]
    looks = ["h4_13.jpg", "look_17_donna.jpg", "h3_17.jpg", "look_15_donna-683x1024.jpg", "h3_04.jpg", "look_16_donna-683x1024.jpg", "h3_11.jpg", "cfdtrce141-10_01_t_600x.jpg"]
    body = f'''<div class="wrap"><div class="hero-t"><h1>Итальянская одежда Sarah Pacini и Transit</h1>
<div class="r"><p class="lead">Бутик в Екатеринбурге. Доставляем по всей России бесплатно. Если вы в другом городе — пришлём видеообзор и сделаем замеры любой вещи.</p>
<div class="cta-row"><a class="btn" href="#new">Смотреть новинки</a><a class="btn ghost" href="@/kontakty.html">Как нас найти</a></div></div></div>
{slider(slides)}</div>
<div class="wrap" style="margin-top:36px"><div class="benefits">
<div>{ic("truck")}<p><b>Бесплатная доставка</b><span>По всей России, без порога заказа</span></p></div>
<div>{ic("video")}<p><b>Видеообзор и замеры</b><span>Покажем вещь и снимем мерки, если вы не в Екатеринбурге</span></p></div>
<div>{ic("hanger")}<p><b>Примерка в бутике</b><span>Универбыт, 2 этаж, бутик № 200</span></p></div>
<div>{ic("award")}<p><b>Более 20 лет с вами</b><span>Многие модели — в единственном экземпляре</span></p></div></div></div>
<section class="sec" id="new"><div class="wrap"><div class="sec-h"><h2>Новинки</h2>
<div class="cta-row" data-tabs-for="newGrid"><button class="btn sm on" data-brand="" style="">Все</button><button class="btn sm ghost" data-brand="sp">Sarah Pacini</button><button class="btn sm ghost" data-brand="tr">Transit</button></div></div>
<div class="grid" id="newGrid" data-grid data-mix="1" data-limit="12"></div>
<p style="margin-top:44px;text-align:center"><a class="btn" href="@/catalog.html?cat=all">Весь каталог</a></p></div></section>
<section class="sec alt"><div class="wrap"><div class="sec-h"><h2>Что вы ищете</h2><a class="link" href="@/catalog.html?cat=all">Весь каталог</a></div>
<div class="tiles">{tile("platya", "Платья", True)}{tile("bryuki", "Брюки и леггинсы")}{tile("dgempera", "Джемпера и кофты")}{tile("tuniki", "Рубашки и футболки")}{tile("cardigany", "Жакеты и жилеты")}</div></div></section>
<section class="sec tight"><div class="duo">
<a class="b" href="@/brendy/sarah-pacini.html"><div class="txt"><div><img class="logo-img" src="{IMG("logo-white.jpg")}" alt="Sarah Pacini"><h3>Одежда как отражение души</h3><p style="margin-top:12px">Изящные женственные коллекции из дорогих тканей и сдержанных цветов. Мохер, который не скатывается, и ткани с бамбуком и крапивой.</p></div><span class="link" style="align-self:flex-start">О бренде</span></div><img class="ph" src="{IMG("h3_09.jpg")}" alt="" loading="lazy"></a>
<a class="b" href="@/brendy/transit.html"><div class="txt"><div><img class="logo-img" src="{IMG("logotip1.jpg")}" alt="TRANSIT"><h3>Свобода в простоте</h3><p style="margin-top:12px">Семейная фабрика с 1986 года. Лён, шёлк, монохромные комплекты в оттенках бетона, стали и брезента.</p></div><span class="link" style="align-self:flex-start">О бренде</span></div><img class="ph" src="{IMG("1_link_editoriali_18_1200x.jpg")}" alt="" loading="lazy"></a></div>
<div class="wrap"><div class="brandrow"><span class="muted" style="font-family:var(--sans);font-size:15px">Также в бутике:</span><a href="@/brendy/european-culture.html">European Culture</a><a href="@/brendy/pj-murano.html">PJ Murano</a><a href="@/brendy/urbahia.html">Urbahia</a><a href="@/catalog.html?brand=kn">Kristensen du Nord</a></div></div></section>
<section class="sec alt"><div class="wrap"><div class="sec-h"><h2>Любимые образы</h2><a class="link" href="@/looks.html">Все образы</a></div>
<div class="mosaic m4">{"".join(f'<a href="{IMG(f)}" data-lb="home"><img src="{IMG(f)}" alt="Образ" loading="lazy"></a>' for f in looks)}</div></div></section>
<section class="sec"><div class="wrap band"><div><h2>Уважаемые покупатели</h2>
<p class="lead" style="margin-bottom:16px">В нашем магазине Sarah Pacini представлен большой ассортимент одежды, произведённой в Италии. На сайте показаны не все модели новых коллекций и не вся цветовая гамма.</p>
<p style="margin-bottom:12px"><b>Напишите нам — проведём видеообзор любой коллекции.</b></p><p class="muted" style="margin-bottom:24px">Одежда продаётся в нескольких экземплярах, поэтому наличие нужно уточнять.</p>{msgr()}</div>
<div class="note"><b style="display:block;color:var(--ink);margin-bottom:6px">Комфорт и стиль от бутика Sarah Pacini</b>Здесь вы найдёте бренды <a class="link" href="@/brendy/sarah-pacini.html">Sarah Pacini (Италия)</a> и <a class="link" href="@/brendy/transit.html">TRANSIT (Италия)</a>. Примерить и купить можно в магазине, доставляем по всей России.</div></div></section>
<section class="sec dark"><div class="wrap band"><div><h2>Ждём вас в Универбыте</h2><p style="margin:14px 0 24px;opacity:.85;max-width:48ch">{ADDR}. Ежедневно с 10:00 до 20:00.</p>
<div class="cta-row" style="margin-bottom:22px"><a class="btn light" href="https://yandex.ru/maps/?text=%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3%2C%20%D0%9F%D0%BE%D1%81%D0%B0%D0%B4%D1%81%D0%BA%D0%B0%D1%8F%2028%D0%B0" target="_blank" rel="noopener">Построить маршрут</a><a class="btn ghost" style="color:#fff;border-color:#fff" href="@/kontakty.html">Все контакты</a></div>{msgr()}</div>
<img src="{IMG("univerbyt_novye_foto.jpg")}" alt="Торговый центр Универбыт" loading="lazy" style="width:100%;max-height:420px;object-fit:cover"></div></section>'''
    page("index.html", "Sarah Pacini и Transit — итальянская одежда в Екатеринбурге",
         "Бутик женской одежды Sarah Pacini (Италия) и TRANSIT (Италия) в Екатеринбурге. Примерка в магазине, бесплатная доставка по России.", body)

# ---------------------------------------------------------------- catalog
def catalog():
    pr = "".join(f'<button class="chip" data-price="{a}-{b}">{t}</button>' for a, b, t in [("", "15000", "до 15 000"), ("15000", "30000", "15–30 тыс."), ("30000", "", "от 30 000")])
    pp = "".join(f'<option>{n}</option>' for n in [5, 20, 35, 50, 65, 80, 95])
    body = crumbs([("Главная", "@/index.html"), ("Каталог", None)]).replace("Каталог</b>", '<span id="catCrumb">Каталог</span></b>') + f'''
<div class="wrap"><div class="pagehead"><h1 id="catTitle">Каталог</h1>
<div id="catIntro" class="prose lead" hidden style="margin-top:18px"><p><b>Лабиринт. Коллекция осень–зима 2024–25.</b> Лабиринт — отправная точка сезона Sarah Pacini. Это жизнь, лабиринт возможностей, предлагающий нам множество путей. Путь, а не гонка, который может изменить нас в зависимости от нашего выбора.</p></div></div>
<div class="cat-layout" id="catalog"><aside class="filters" id="filters" aria-label="Фильтры"><div style="display:flex;justify-content:space-between;align-items:center" class="fgrp"><h3 style="font-size:22px">Фильтр</h3><button class="fbtn ibtn" data-close aria-label="Закрыть">{ic("x")}</button></div>
<div class="fgrp"><h4>Цена, ₽</h4><div class="prange"><input id="fmin" placeholder="от" inputmode="numeric" aria-label="Цена от"><input id="fmax" placeholder="до" inputmode="numeric" aria-label="Цена до"></div><div class="chips" style="margin:12px 0 0">{pr}</div></div>
<div class="fgrp"><h4>Производитель</h4><div id="fbrands"></div></div>
<div class="fgrp"><div class="chk"><label><input type="checkbox" id="fnew"><span>Новинки</span></label></div><div class="chk"><label><input type="checkbox" id="fsale"><span>Спецпредложение</span></label></div></div>
<div class="fgrp"><h4>Разделы</h4><div class="catlist" id="fcats"></div></div>
<div class="fgrp" style="display:flex;gap:10px;border:0"><button class="btn ghost sm" id="freset">Сбросить</button><button class="btn sm" id="fshow" style="flex:1">Показать</button></div></aside>
<div><div class="toolbar"><div class="grp"><button class="btn ghost sm fbtn" data-open="filters">{ic("filter")}Фильтры</button><span class="muted" id="catCount"></span></div>
<div class="grp"><label class="sr" for="sort">Сортировка</label><select id="sort"><option value="">Не сортировать</option><option value="p1">Цена: по возрастанию</option><option value="p2">Цена: по убыванию</option><option value="n1">Название: А–Я</option><option value="n2">Название: Я–А</option></select>
<label class="sr" for="pp">Товаров на странице</label><select id="pp" title="Товаров на странице">{pp}</select>
<div class="views" role="group" aria-label="Вид"><button data-view="grid" title="Витрина" aria-label="Витрина">{ic("grid")}</button><button data-view="list" title="Список" aria-label="Список">{ic("list")}</button><button data-view="price" title="Прайс-лист" aria-label="Прайс-лист">{ic("price")}</button></div></div></div>
<div class="chips" id="chips"></div><div id="items" class="grid"></div><div class="pager" id="pager"></div>
<div class="seo-note"><p>Женскую одежду Sarah Pacini можно купить в Екатеринбурге в нашем бутике: ул. Посадская, 28а, ТЦ «Универбыт», 2 этаж, бутик № 200.</p><p style="margin-top:10px">{LEGAL}</p></div></div></div></div>'''
    page("catalog.html", "Каталог — Sarah Pacini, Екатеринбург", "Каталог женской одежды Sarah Pacini и TRANSIT: джемперы, брюки, платья, рубашки, жакеты и аксессуары.", body)

# ---------------------------------------------------------------- product pages
def product_pages():
    names = {"sp": "Sarah Pacini", "tr": "TRANSIT Италия"}
    for p in PRODUCTS:
        imgs = p.get("images", [p["img"]])
        th = "".join(f'<button type="button" data-src="{IMG(f)}" class="{"on" if i == 0 else ""}" aria-label="Фото {i+1}"><img src="{IMG(f)}" alt="" loading="lazy"></button>' for i, f in enumerate(imgs)) if len(imgs) > 1 else ""
        price = f'<div class="price">{p["price"]:,}&nbsp;₽</div>'.replace(",", "&nbsp;") if p["price"] else '<div class="price ask">Цена по запросу</div>'
        brand_link = cl(brand=p["brand"])
        spec = f'<dt>Производитель</dt><dd><a class="link" href="{brand_link}">{names[p["brand"]]}</a></dd>'
        if p["model"]: spec += f'<dt>Модель</dt><dd>{html.escape(p["model"])}</dd>'
        spec += f'<dt>Раздел</dt><dd>{LEAF[p["cat"]]}</dd>'
        if p.get("material"): spec += f'<dt>Материал</dt><dd>{html.escape(p["material"])}</dd>'
        brand_txt = (SP_TEXT + "</p><p>" + SP_TEXT2) if p["brand"] == "sp" else TR_TEXT
        desc = f'<p>{html.escape(p["desc"])}</p>' if p["desc"] else ""
        tags = p.get("tags") or [LEAF[p["cat"]], names[p["brand"]]]
        tagh = "".join(f'<a href="{cl(q=t.replace(" ", "+"))}">{html.escape(t)}</a>' for t in tags)
        title = p["name"]
        body = crumbs([("Главная", "@/index.html"), ("Смотреть всё", cl(cat="all")), (title, None)]).replace("@/", "../@/").replace("../@/", "@/") + f'''
<div class="wrap"><div class="pdp"><div class="gal"><div class="th">{th}</div><a class="main" data-lb="pdp" href="{IMG(imgs[0])}"><img src="{IMG(imgs[0])}" alt="{html.escape(title)}">{'<span class="badge">Новинка</span>' if p["isNew"] else ''}</a></div>
<div class="info"><a class="muted" style="font-size:14px" href="{brand_link}">{names[p["brand"]]}</a><h1>{html.escape(title)}</h1>
<div class="meta">{f'<span>Модель: {html.escape(p["model"])}</span>' if p["model"] else ''}<span>Оценок пока нет</span></div>{price}
<p class="muted" style="font-size:14px">{"Мы подберём размер и назовём точную цену." if not p["price"] else "Цену, размеры и наличие подтвердит менеджер."}</p>
<div class="buyrow"><div class="qty" data-qtybox><button type="button" data-step="-1" aria-label="Меньше">−</button><input value="1" aria-label="Количество" inputmode="numeric"><button type="button" data-step="1" aria-label="Больше">+</button></div>
<button class="btn" data-add="{p["id"]}">Добавить в корзину</button></div>
<div class="buyrow" style="margin-top:0"><button class="btn ghost" data-oneclick="{html.escape(title, quote=True)}">Купить в один клик</button><button class="btn ghost" data-cmp="{p["id"]}">{ic("cmp")}К сравнению</button></div>
<div class="lines"><div>{ic("hanger")}<p><b>Примерка в бутике</b><span>{ADDR}</span></p></div><div>{ic("truck")}<p><b>Бесплатная доставка по России</b><span>Одежда продаётся в нескольких экземплярах — наличие уточняйте</span></p></div><div>{ic("video")}<p><b>Видеообзор и замеры</b><span>Покажем вещь и снимем мерки, если вы в другом городе</span></p></div></div>
<div class="ask-row"><a class="btn sm ghost" href="tel:{CONFIG["tel"]}">{ic("phone")}Позвонить</a><a class="btn sm ghost" href="{CONFIG["telegram"]}" target="_blank" rel="noopener">{TG_ICON}Telegram</a><a class="btn sm ghost" href="{CONFIG["max"]}" target="_blank" rel="noopener"><img src="{IMG("max-messenger-sign-l.svg")}" width="18" height="18" alt="">MAX</a></div></div></div>
<div class="tabs"><div class="tl" role="tablist"><button class="on" data-tab="t1">Параметры</button><button data-tab="t2">Описание</button><button data-tab="t3">Отзывы</button></div>
<div class="pn on" id="t1"><dl class="spec">{spec}</dl></div>
<div class="pn prose" id="t2">{desc}<p>{brand_txt}</p><p>Примерить и купить одежду {names[p["brand"]]} можно в <a href="@/kontakty.html">нашем магазине</a>: {ADDR}. Будем рады видеть вас!</p></div>
<div class="pn" id="t3"><p style="max-width:56ch;margin-bottom:8px"><b>Авторизуйтесь, чтобы оставить комментарий.</b></p><p class="muted" style="margin-bottom:10px">Если вы уже зарегистрированы на сайте, войдите. Забыли пароль — <a class="link" href="@/forgot-password.html">восстановите его</a>.</p><button class="btn" data-open="login">Войти</button></div>
<div class="tags">{tagh}</div><p class="legal">{LEGAL}</p>{addr_box()}</div>
<section class="sec tight" style="padding-top:0"><div class="sec-h"><h2>Похожие вещи</h2><a class="link" href="{cl(cat=p["cat"])}">Все в разделе</a></div><div class="grid" data-grid data-cat="{p["cat"]}" data-exclude="{p["id"]}" data-limit="4"></div></section></div>'''
        body = body.replace('data-root', 'data-root')
        page(f"product/{p['id']}.html", f"{title} — купить в Екатеринбурге", (p["desc"] or title) + ". Бутик Sarah Pacini, Екатеринбург.", body, base="../")

# ---------------------------------------------------------------- content pages
def cart_page():
    body = crumbs([("Главная", "@/index.html"), ("Корзина", None)]) + f'''
<div class="wrap" id="cartPage"><div class="pagehead"><h1>Корзина</h1></div>
<div id="cartEmpty" class="empty" hidden><h3>Корзина пуста</h3><p style="margin-bottom:20px">Добавьте вещи из каталога — мы подтвердим наличие и размеры.</p><a class="btn" href="@/catalog.html?cat=all">Перейти в каталог</a></div>
<div class="ct" id="cartFull" hidden><div><div id="cartRows"></div><p style="margin-top:14px"><button class="link" id="cartClear" style="color:var(--steel)">Очистить корзину</button></p>
<h2 style="margin:48px 0 4px;font-size:30px">Оформление заказа</h2><p class="muted">Менеджер свяжется с вами, подтвердит наличие, размеры и итоговую цену.</p>
<form id="checkoutForm" data-form="checkout" class="f two" novalidate>
<div class="fld"><label for="c-n">Имя</label><input id="c-n" name="name" required autocomplete="name"><div class="em">Укажите имя</div></div>
<div class="fld"><label for="c-p">Телефон</label><input id="c-p" name="phone" type="tel" required autocomplete="tel" placeholder="+7"><div class="em">Укажите телефон с кодом</div></div>
<div class="fld"><label for="c-e">E-mail</label><input id="c-e" name="email" type="email" autocomplete="email"><div class="em">Проверьте адрес почты</div></div>
<div class="fld"><label for="c-v">Как с вами связаться</label><select id="c-v" name="via"><option>Телефон</option><option>Telegram</option><option>MAX</option><option>E-mail</option></select></div>
<div class="fld full"><label for="c-a">Город и адрес доставки</label><input id="c-a" name="addr" autocomplete="street-address"></div>
<div class="fld full"><label for="c-c">Комментарий</label><textarea id="c-c" name="comment" style="min-height:90px"></textarea></div>
<label class="chk full"><input type="checkbox" required> Согласен на обработку персональных данных</label></form>
<div id="orderDone" class="ok-box" hidden style="margin-top:24px"><h3>Заказ готов к отправке</h3><p style="margin:8px 0 14px">Отправьте его удобным способом — менеджер ответит в рабочее время с 10:00 до 20:00.</p>
<textarea id="orderText" readonly style="width:100%;min-height:200px;padding:12px;border:1px solid var(--concrete);background:#fff"></textarea>
<div class="cta-row" style="margin-top:14px"><a class="btn" id="orderMail" href="#">Отправить по e-mail</a><button class="btn ghost" id="orderCopy" type="button">Скопировать заказ</button><a class="btn ghost" href="{CONFIG["telegram"]}" target="_blank" rel="noopener">В Telegram</a><a class="btn ghost" href="{CONFIG["max"]}" target="_blank" rel="noopener">В MAX</a></div></div></div>
<aside class="sumbox"><h3 style="margin-bottom:14px">Ваш заказ</h3><div class="ln"><span>Товаров</span><b id="cartCnt">0</b></div><div class="ln"><span>Доставка по России</span><b>Бесплатно</b></div><p id="cartAsk" class="muted" style="font-size:14px" hidden>Ещё <span></span> поз. — цена по запросу, её назовёт менеджер.</p>
<div class="tot"><span>Итого</span><b id="cartSum" style="font-weight:400"></b></div><button class="btn block" form="checkoutForm" type="submit" style="margin-top:22px">Оформить заказ</button><p class="legal" style="font-size:12px">{LEGAL}</p></aside></div></div>'''
    page("cart.html", "Корзина — Sarah Pacini", "Корзина и оформление заказа в бутике Sarah Pacini.", body)

def compare_page():
    body = crumbs([("Главная", "@/index.html"), ("Сравнение", None)]) + '''
<div class="wrap" id="cmpPage"><div class="pagehead"><h1>Сравнение товаров</h1></div>
<div id="cmpEmpty" class="empty" hidden><h3>Пока нечего сравнивать</h3><p style="margin-bottom:20px">Нажмите значок сравнения на карточке товара — можно выбрать до четырёх вещей.</p><a class="btn" href="@/catalog.html?cat=all">Перейти в каталог</a></div>
<div class="cmp-wrap" id="cmpTable" hidden></div></div>'''
    page("compare.html", "Сравнение товаров — Sarah Pacini", "Сравнение товаров в интернет-магазине Sarah Pacini.", body)

def about():
    gal = ["butik_univerbyt-18.jpg", "butik_univerbyt-6.jpg", "butik_univerbyt-20.jpg", "butik_univerbyt-17_1.jpg", "butik_univerbyt-8.jpg", "img_7915.jpg", "img_7905.jpg", "img_7256.jpg", "img_7258.jpg", "img_7255.jpg"]
    body = crumbs([("Главная", "@/index.html"), ("О компании", None)]) + f'''
<div class="wrap"><div class="pagehead"><h1>Рады приветствовать вас в бутике Sarah Pacini</h1></div>
{slider([("magazin_2.jpg", "", None), ("slajd_kontakty-4.png", "", "@/kontakty.html"), ("slajd_kontakty-2.png", "", None), ("slajd_kontakty.png", "", None)])}
<div class="facts" style="margin-top:48px"><div><b>20+ лет</b><span>Работаем для вас</span></div><div><b>1 вещь</b><span>Многие модели есть в одном размере и экземпляре</span></div><div><b>Вся Россия</b><span>Доставляем бесплатно</span></div></div></div>
<section class="sec"><div class="wrap split"><div class="prose"><p class="lead" style="margin-bottom:1em">Бутик итальянской одежды Сара Пачини — большой выбор качественной натуральной и стильной одежды европейских брендов.</p>
<p>Вы можете подобрать одежду эксклюзивных брендов <a href="@/brendy/sarah-pacini.html">Sarah Pacini</a> и <a href="@/brendy/transit.html">Transit (Италия)</a>.</p>
<p>Закончить образ помогут аксессуары: качественные сумки и бижутерия от Sarah Pacini, дизайнерские украшения от PJ Murano (муранское стекло) и Krikos.</p>
<p>Мы искренне верим, что одежда должна соответствовать мироощущению и приносить радость и удовлетворение каждому.</p></div>
<div class="prose"><h3>Почему вещи эксклюзивны</h3><p>Многие модели представлены в одном размере и единственном экземпляре. Это позволяет владелице быть особенной и сводит к минимуму возможность встретить рядом такой же наряд.</p>
<p>Модели отшиваются в нескольких экземплярах, поэтому размеры могут отличаться от стандартных. Вещь можно отложить на сайте и прийти примерить её в магазин. На сайте представлены далеко не все модели — ждём вас в бутике.</p></div></div></section>
<section class="sec alt"><div class="wrap"><div class="sec-h"><h2>Наш бутик</h2></div><div class="mosaic m4">{"".join(f'<a href="{IMG(f)}" data-lb="about"><img src="{IMG(f)}" alt="Бутик Sarah Pacini" loading="lazy"></a>' for f in gal)}</div></div></section>
<section class="sec"><div class="wrap band"><div><h2>Ждём вас в Универбыте</h2><p class="lead" style="margin:14px 0 22px">{ADDR}</p>{msgr()}</div><div class="cta-row"><a class="btn" href="@/kontakty.html">Контакты и маршрут</a><a class="btn ghost" href="@/catalog.html?cat=all">Смотреть каталог</a></div></div></section>'''
    page("o-kompanii.html", "О магазине брендовой одежды Sarah Pacini", "Бутик Sarah Pacini в Екатеринбурге: итальянские бренды, эксклюзивные модели, примерка и доставка по России.", body)

def brands():
    cards = [("Sarah Pacini", "Италия. Изящные женственные коллекции из дорогих тканей.", "bezymyannyj_847421.png", "@/brendy/sarah-pacini.html"),
             ("TRANSIT", "Италия. Семейная фабрика с 1986 года, лён и шёлк.", "slajd_1.jpg", "@/brendy/transit.html"),
             ("European Culture", "Италия. Одежда в стиле милитари с устойчивым цветом.", "slajd_evropejskaya_kultura.jpg", "@/brendy/european-culture.html"),
             ("Urbahia", "Франция. Верхняя одежда из водонепроницаемой ткани.", "urbahia.png", "@/brendy/urbahia.html"),
             ("PJ Murano", "Италия. Украшения из муранского стекла.", "murano_slayd.jpg", "@/brendy/pj-murano.html")]
    c = "".join(f'<a class="bcard" href="{h}"><div class="ph"><img src="{IMG(i)}" alt="{t}" loading="lazy"></div><div class="tx"><h3>{t}</h3><p>{d}</p><span class="link" style="align-self:flex-start">Читать о бренде</span></div></a>' for t, d, i, h in cards)
    c += f'<div class="bcard" style="background:var(--ink);color:#e9e7e0"><div class="tx" style="justify-content:center;padding:32px"><h3>Не нашли нужную модель?</h3><p>Индивидуально сделаем видеообзор и замеры всех вещей, если вы в другом городе.</p>{msgr("")}</div></div>'
    body = crumbs([("Главная", "@/index.html"), ("Бренды", None)]) + f'''
<div class="wrap"><div class="pagehead"><h1>Итальянские бренды женской одежды</h1><p class="lead" style="margin-top:14px">Бутик Сара Пачини знакомит покупателей с европейскими брендами.</p></div>
<div class="bcards">{c}</div>
<div class="note" style="margin:48px 0 80px"><b style="color:var(--ink)">Внимание.</b> Одежда продаётся в нескольких экземплярах, наличие уточняйте. Лично примерить и купить можно только в нашем магазине: {ADDR}.</div></div>'''
    page("brendy.html", "Бренды — итальянская женская одежда Sarah Pacini и Transit", "Бренды бутика Sarah Pacini в Екатеринбурге: Sarah Pacini, Transit, European Culture, Urbahia, PJ Murano.", body)

def brand_page(fn, title, slides, paras, cta, gal=None, brand=None, extra="", meta=""):
    ps = "".join(f"<p>{x}</p>" for x in paras)
    g = f'<div class="mosaic" style="margin-top:40px">{"".join(f"<a href=\"{IMG(f)}\" data-lb=\"b\"><img src=\"{IMG(f)}\" alt=\"\" loading=\"lazy\"></a>" for f in gal)}</div>' if gal else ""
    grid = f'<section class="sec alt"><div class="wrap"><div class="sec-h"><h2>Из коллекции</h2><a class="link" href="{cta[1]}">Весь каталог</a></div><div class="grid" data-grid data-brand="{brand}" data-limit="4"></div></div></section>' if brand else ""
    body = crumbs([("Главная", "@/index.html"), ("Бренды", "@/brendy.html"), (title.split(" бренда ")[-1] if "бренда" in title else title, None)]) + f'''
<div class="wrap"><div class="pagehead"><h1>{title}</h1></div>{slider(slides)}
<div class="sec tight"><div class="prose">{ps}<p style="margin-top:1.6em"><a class="btn" href="{cta[1]}">{cta[0]}</a></p></div>{g}{extra}</div></div>{grid}
<section class="sec"><div class="wrap">{addr_box()}</div></section>'''
    page(f"brendy/{fn}.html", meta or title, paras[0][:150], body, base="../")

def brands_pages():
    brand_page("sarah-pacini", "История создания бренда Sarah Pacini",
        [("slajd_1_431212.jpg", "", cl(brand="sp")), ("novaya_kollekciya4_0.jpg", "", None), ("slajd_aksessuary.jpg", "", cl(cat="aksessuary"))],
        ["История бренда <b>Sarah Pacini</b> (Сара Пачини) началась более 20 лет назад в Бельгии. За эти годы были созданы коллекции, приносящие в мир изящество, легкость и элегантность. Сегодня одежда представлена в более чем 50 монобрендовых бутиках и более чем в 1500 мультибрендах. В России компания также заняла особое место.",
         "Философия бренда — «одежда как отражение души» — проявляется в изящных женственных коллекциях благодаря уникальному сочетанию дорогих тканей и сдержанных цветовых решений. Для каждой женщины, которая дорожит собственной неповторимостью, ценит не только стиль, но и комфорт и верит, что мода — это искусство жить.",
         "И отдельные модели, и их сочетания создают ясные и точные силуэты. Одежда Sarah Pacini достаточно креативна, но из неё легко собрать комплект для офиса. Это «умный креатив», который делает женщину красивой.",
         "Ткани для марки выпускают по спецзаказу. Мохер не скатывается и годами не теряет вида. Sarah Pacini одной из первых начала использовать ткани с добавлением волокон бамбука и крапивы. Продукция производится только на фабриках Италии и Франции."],
        ("Смотреть коллекцию Sarah Pacini", cl(brand="sp")), ["h3_09.jpg", "26114504.jpg"], "sp", meta="История появления итальянского бренда женской одежды Сара Пачини")
    brand_page("transit", "Информация о бренде TRANSIT",
        [("slajd_1.jpg", "", cl(brand="tr")), ("rubashka_141.jpg", "", None), ("frame_71.jpg", "", None)],
        ["Итальянская марка <b>TRANSIT</b> (Транзит) создана в 1986 году как фирма по пошиву женской одежды высокого качества. Одежда шьётся на фабрике полного цикла, это семейный бизнес и своего рода «ручная работа». Высококачественное сырьё, невычурная элегантность, индивидуальность, свобода и соотношение цены и качества — так TRANSIT подходит и к одежде, и к жизни.",
         "В намеренном упрощении образов дизайнеры видят свободу: клиенты предпочитают облегающему костюму монохромный комплект из брюк и однобортного пиджака с мягкими плечами и необработанными швами. Палитра скромна: бетонный, стальной, антрацитовый и брезентовый оттенки. Пыльные и «закатные» цвета лучше подчёркивают текстуру натуральных тканей, которые семья Козза производит на собственной фабрике.",
         "<b>Примерить и купить одежду бренда Транзит можно в нашем магазине.</b>"],
        ("Смотреть коллекцию TRANSIT", cl(brand="tr")), ["1_link_editoriali_18_1200x.jpg", "1_link_editoriali_48_1200x.jpg", "donna_1200x1800_fw25-26_32_1200.jpg"], "tr", meta="Купить брендовую одежду TRANSIT Италия в Екатеринбурге")
    brand_page("european-culture", "Женская одежда бренда Европейская Культура", [("slajd_evropejskaya_kultura.jpg", "", cl(brand="ec"))],
        ["Итальянский бренд <b>European Culture</b> создан в 1999 году. Под маркой выпускается женская, мужская и детская одежда, известная высоким качеством и выполненная в стиле «милитари».",
         "Все модели — образцы изысканного и инновационного дизайна. Новейшие технологии окраски тканей дают особую устойчивость цвета, поэтому вещи подходят людям, ведущим активный образ жизни.",
         "Одежду окрашивают инновационным способом: готовые изделия полностью погружают в ёмкости со специальным раствором с красящим веществом и выдерживают четыре часа при очень высокой температуре. Ткань приобретает уникальный оттенок. Эта технология применяется до сих пор.",
         "Сегодня это практичность, безупречный пошив, роскошь и простота. В последних коллекциях дизайнеры смешивают фактуры и стили и постоянно экспериментируют. В моделях нет вычурности, лишнего блеска и обилия страз, но они необычайно удобны и красивы."],
        ("Смотреть коллекцию European Culture", cl(brand="ec")), None, None, meta="Бренд Европейская Культура в Екатеринбурге")
    brand_page("pj-murano", "Бусы и колье PJ Murano из муранского стекла", [("murano_slayd.jpg", "", cl(cat="ukrasheniya")), ("murano_slayd-1.jpg", "", cl(cat="ukrasheniya"))],
        ["<b>PJ Murano</b> — бренд стильных оригинальных украшений из муранского стекла, венецианского стекла с итальянского острова Мурано.",
         "Аксессуары из муранского стекла никого не оставят равнодушным: лёгкие, интересные, красивые, качественные. Хочется покупать их снова и снова — или завести одно самое любимое украшение.",
         "Украшения PJ Murano безупречны в дизайне, качестве и деталях. Это всегда свежие и актуальные тренды."],
        ("Смотреть коллекцию PJ Murano", cl(cat="ukrasheniya")), ["140995535_image__9_.jpg"], None, meta="Купить бусы и аксессуары бренда PJ Murano в Екатеринбурге")
    brand_page("urbahia", "Верхняя одежда Urbahia в Екатеринбурге", [("urbahia.png", "", None)],
        ["Верхняя одежда французского производителя <b>Urbahia</b> отличается стилем и материалами.",
         "Сочетание шика и водонепроницаемой ткани позволяет выглядеть прекрасно в дождливые и сырые осенне-весенние дни. В качестве утеплителя используется холлофайбер: он прекрасно греет без лишних объёмов.",
         "Прямой ровный крой сочетается с длиной наряда и создаёт правильный силуэт. В коллекциях есть пальто классической длины и укороченные модели, а широкая цветовая гамма позволяет выбрать и яркую, и нейтральную вещь.",
         "Посмотреть, примерить и купить одежду Urbahia можно по адресу: ул. Малышева, 16, ТК «Гермес Плаза», 2 этаж, бутик № 213."],
        ("Смотреть верхнюю одежду", cl(cat="kurtki")), None, None, meta="Купить верхнюю одежду из Франции Urbahia в Екатеринбурге")

def contacts():
    body = crumbs([("Главная", "@/index.html"), ("Контакты", None)]) + f'''
<div class="wrap"><div class="pagehead"><h1>Адрес и контакты магазина итальянской одежды Sarah Pacini</h1></div>
{slider([(f, "", None) for f in ["slajd_kontakty-4.png", "slajd_kontakty-2.png", "slajd_kontakty.png", "slajd_kontakty-3.png", "slajd_kontakty-1.jpg"]])}
<div class="contact-grid" style="margin-top:56px"><div class="cinfo">
<div>{ic("phone")}<p><small>Телефон и MAX</small><b><a href="tel:{CONFIG["tel"]}">{CONFIG["phone"]}</a></b></p></div>
<div>{ic("clock")}<p><small>Режим работы</small><b>Ежедневно с 10:00 до 20:00</b></p></div>
<div>{ic("pin")}<p><small>Адрес</small><b>{ADDR}</b></p></div>
<div>{ic("mail")}<p><small>E-mail</small><b><a href="mailto:{CONFIG["email"]}">{CONFIG["email"]}</a></b></p></div>
<div>{ic("chat")}<p><small>Реквизиты</small><b>ООО «Леди Блюз»</b></p></div>
<div style="border:0;flex-direction:column;gap:14px"><small>Напишите нам</small>{msgr()}<div class="msgr"><a href="{CONFIG["instagram"]}" target="_blank" rel="noopener">{ic("insta")}Instagram</a></div></div></div>
<div><div class="mosaic"><a href="{IMG("univerbyt_novye_foto.jpg")}" data-lb="c" style="grid-column:span 3;aspect-ratio:16/10"><img src="{IMG("univerbyt_novye_foto.jpg")}" alt="Торговый центр Универбыт"></a>
<a href="{IMG("univerbyt_novye_foto-1.jpg")}" data-lb="c" style="grid-column:span 2;aspect-ratio:4/3"><img src="{IMG("univerbyt_novye_foto-1.jpg")}" alt="Вход"></a><a href="{IMG("univerbyt_novye_foto-2.jpg")}" data-lb="c" style="aspect-ratio:auto"><img src="{IMG("univerbyt_novye_foto-2.jpg")}" alt="Этаж"></a></div>
<div class="cta-row" style="margin-top:24px"><a class="btn" href="https://yandex.ru/maps/?text=%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3%2C%20%D0%9F%D0%BE%D1%81%D0%B0%D0%B4%D1%81%D0%BA%D0%B0%D1%8F%2028%D0%B0" target="_blank" rel="noopener">Маршрут в Яндекс Картах</a><a class="btn ghost" href="https://2gis.ru/ekaterinburg/search/%D0%9F%D0%BE%D1%81%D0%B0%D0%B4%D1%81%D0%BA%D0%B0%D1%8F%2028%D0%B0" target="_blank" rel="noopener">Открыть в 2ГИС</a></div></div></div>
<p class="lead" style="margin:56px 0 80px">Мы будем очень рады видеть вас в нашем магазине.</p></div>'''
    page("kontakty.html", "Контакты бутика брендовой одежды Sarah Pacini", "Адрес, телефон и схема проезда в бутик Sarah Pacini в Екатеринбурге, ТЦ Универбыт.", body)

def form_page(fn, title, h1, intro, kind, fields, ok_text, extra_after=""):
    body = crumbs([("Главная", "@/index.html"), (h1, None)]) + f'''
<div class="wrap"><div class="pagehead"><h1>{h1}</h1><p class="lead" style="margin-top:14px">{intro}</p></div>
<div class="band" style="align-items:start;margin-bottom:80px"><div style="max-width:620px"><form data-form="{kind}" class="f" novalidate>{fields}</form>
<div class="ok-box" hidden><b>Готово.</b><p>{ok_text}</p></div></div><div class="note"><b style="color:var(--ink)">Быстрее — в мессенджере</b><p style="margin:8px 0 14px">Ответим в рабочее время, ежедневно с 10:00 до 20:00.</p>{msgr()}{extra_after}</div></div></div>'''
    page(fn, title, intro, body)

def small_pages():
    ag = '<label class="chk"><input type="checkbox" required> Согласен на обработку персональных данных</label>'
    form_page("napishite-nam.html", "Напишите нам — Sarah Pacini", "Напишите нам", "Спросите о наличии, размерах или попросите видеообзор — мы ответим.", "contact",
        f'''<div class="fld"><label for="w-n">Ваше имя или название организации</label><input id="w-n" name="name" required><div class="em">Укажите имя</div></div>
<div class="fld"><label for="w-c">Ваш e-mail или телефон</label><input id="w-c" name="contact" required data-contact="1"><div class="em">Укажите корректный e-mail или телефон</div></div>
<div class="fld"><label for="w-t">Сообщение</label><textarea id="w-t" name="text" required></textarea><div class="em">Напишите сообщение</div></div>{ag}<button class="btn" type="submit">Отправить сообщение</button>''',
        "Если почтовая программа не открылась, напишите нам в мессенджер или позвоните.")
    form_page("doska-obyavleniy.html", "Доска объявлений — Sarah Pacini", "Доска объявлений", "Оставьте сообщение для других посетителей и команды магазина.", "board",
        f'''<div class="fld"><label for="b-n">Имя</label><input id="b-n" name="name" required><div class="em">Укажите имя</div></div><div class="fld"><label for="b-e">E-mail</label><input id="b-e" name="email" type="email"><div class="em">Проверьте адрес почты</div></div>
<div class="fld"><label for="b-t">Текст</label><textarea id="b-t" name="text" required></textarea><div class="em">Напишите текст</div></div><button class="btn" type="submit">Отправить</button>''',
        "Сообщение передано на модерацию.", '<p class="muted" style="margin-top:20px;font-size:14px">Опубликованных объявлений пока нет.</p>')
    form_page("forgot-password.html", "Восстановление пароля — Sarah Pacini", "Восстановление пароля", "Укажите e-mail, который использовали при регистрации.", "forgot",
        '''<div class="fld"><label for="f-e">E-mail</label><input id="f-e" name="email" type="email" required><div class="em">Укажите корректный e-mail</div></div><button class="btn" type="submit">Восстановить пароль</button>''',
        "Мы передали запрос. Если ответа нет, свяжитесь с нами по телефону.")
    body = crumbs([("Главная", "@/index.html"), ("Регистрация", None)]) + f'''<div class="wrap"><div class="pagehead"><h1>Регистрация</h1></div><div class="band" style="margin-bottom:80px"><div><p class="lead">Регистрация на сайте закрыта. По вопросам обращайтесь к администрации сайта.</p><p style="margin-top:20px"><a class="btn" href="@/napishite-nam.html">Написать администрации</a></p></div><div class="note">Заказать можно и без регистрации: добавьте вещи в корзину и оформите заказ.</div></div></div>'''
    page("register.html", "Регистрация — Sarah Pacini", "Регистрация на сайте закрыта.", body)

def looks():
    f = ["h4_13.jpg", "look_17_donna.jpg", "h3_17.jpg", "look_15_donna-683x1024.jpg", "h3_04.jpg", "look_16_donna-683x1024.jpg", "h3_11.jpg", "scadtrc2000-04_01_t_600x.jpg",
         "cfdtrcd1301-01_01_t_361ef2b2-27e9-4be4-b6b5-7038de5e9c58_600x.jpg", "cfdtrce141-10_01_t_600x.jpg", "26111093-33-2.jpg", "26111086-2.jpg", "26113006-02-2.jpg", "cfdtrcc121-12_01_t_600x.jpg"]
    body = crumbs([("Главная", "@/index.html"), ("Образы", None)]) + f'''<div class="wrap"><div class="pagehead"><h1>Любимые образы</h1><p class="lead" style="margin-top:14px">Готовые сочетания вещей Sarah Pacini и Transit. Понравился образ — напишите, подберём размеры.</p></div>
<div class="looks">{"".join(f'<a href="{IMG(x)}" data-lb="l"><img src="{IMG(x)}" alt="Образ {i+1}" loading="lazy"></a>' for i, x in enumerate(f))}</div>
<p style="margin:48px 0 80px"><a class="btn" href="@/catalog.html?cat=all">Смотреть каталог</a></p></div>'''
    page("looks.html", "Образы — Sarah Pacini", "Любимые образы бутика Sarah Pacini: сочетания вещей Sarah Pacini и Transit.", body)

def sitemap():
    cats = "".join(f'<li><a href="{h}">{html.escape(t)}</a></li>' for t, h in [(LEAF[k], cl(cat=k)) for k in LEAF])
    body = crumbs([("Главная", "@/index.html"), ("Карта сайта", None)]) + f'''<div class="wrap smap"><div class="pagehead"><h1>Карта сайта</h1></div><div class="split" style="align-items:start;margin-bottom:80px"><div>
<ul><li><a href="@/index.html">Главная</a></li><li><a href="@/o-kompanii.html">О компании</a></li><li><a href="@/brendy.html">Бренды</a><ul><li><a href="@/brendy/sarah-pacini.html">Sarah Pacini</a></li><li><a href="@/brendy/transit.html">TRANSIT</a></li><li><a href="@/brendy/european-culture.html">Европейская культура</a></li><li><a href="@/brendy/urbahia.html">URBAHIA</a></li><li><a href="@/brendy/pj-murano.html">PJ Murano</a></li></ul></li>
<li><a href="@/kontakty.html">Контакты</a></li><li><a href="@/napishite-nam.html">Напишите нам</a></li><li><a href="@/karta-sayta.html">Карта сайта</a></li><li><a href="@/doska-obyavleniy.html">Доска объявлений</a></li><li><a href="@/looks.html">Образы</a></li><li><a href="@/cart.html">Корзина</a></li><li><a href="@/compare.html">Сравнение</a></li></ul></div>
<div><h3 style="margin-top:0">Интернет-магазин</h3><ul><li><a href="@/catalog.html?cat=all">Смотреть всё</a></li><li><a href="@/catalog.html?cat=odezhda">Каталог одежды</a><ul>{cats}</ul></li><li><a href="@/catalog.html?brand=sp">Sarah Pacini</a></li><li><a href="@/catalog.html?brand=tr">TRANSIT</a></li><li><a href="@/catalog.html?brand=ag">Annette Gortz</a></li><li><a href="@/catalog.html?brand=kn">Kristensen du Nord</a></li><li><a href="@/catalog.html?brand=ec">Европейская культура</a></li><li><a href="@/catalog.html?sale=1">Распродажа</a></li></ul></div></div></div>'''
    page("karta-sayta.html", "Карта сайта — Sarah Pacini", "Карта сайта бутика Sarah Pacini.", body)

def not_found():
    body = f'''<div class="wrap"><div class="empty" style="padding:120px 0"><h1>Такой страницы нет</h1><p style="margin:14px 0 24px">Возможно, ссылка устарела. Перейдите в каталог или на главную.</p><div class="cta-row" style="justify-content:center"><a class="btn" href="/catalog.html?cat=all">Каталог</a><a class="btn ghost" href="/index.html">На главную</a></div></div></div>'''
    page("404.html", "Страница не найдена — Sarah Pacini", "Страница не найдена", body)

# ---------------------------------------------------------------- run
def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    for f in ("style.css", "app.js"):
        shutil.copy(os.path.join(HERE, "assets", f), os.path.join(OUT, "assets", f))
    data = {"config": CONFIG, "products": PRODUCTS, "cats": CATS, "brands": BRANDS, "icons": ICONS, "leaf": LEAF}
    open(os.path.join(OUT, "assets", "data.js"), "w", encoding="utf-8").write("window.SP=" + json.dumps(data, ensure_ascii=False) + ";")
    home(); catalog(); product_pages(); cart_page(); compare_page(); about(); brands(); brands_pages(); contacts(); small_pages(); looks(); sitemap(); not_found()
    # tools for regeneration
    tools = os.path.join(OUT, "tools"); os.makedirs(os.path.join(tools, "assets"))
    for f in ("build.py", "products.py"): shutil.copy(os.path.join(HERE, f), tools)
    for f in ("style.css", "app.js"): shutil.copy(os.path.join(HERE, "assets", f), os.path.join(tools, "assets"))
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    print("files:", n, "products:", len(PRODUCTS))

if __name__ == "__main__":
    main()
