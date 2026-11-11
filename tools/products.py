# slug | name | brand | price (0 = по запросу) | image file on lady-blues.ru/d/ | description
RAW = """
dzhemper-sarah-pacini-26211100-02|Джемпер Sarah Pacini 26211100-53|sp|0|26211100-53.jpg|Свитер с рукавом 3/4 из стрейч мохера с круглым вырезом и боковыми прорезями
dzhemper-sarah-pacini-26211014-02|Джемпер Sarah Pacini 26211100-02|sp|0|26211100.jpg|Свитер с рукавом 3/4 из стрейч мохера с круглым вырезом и боковыми прорезями
trikotazhnye-bryuki-sarah-pacini-24111019-05-2|Трикотажные брюки Sarah Pacini 26211021-02|sp|0|26211021.jpg|Широкие брюки из структурированной стрейч вискозы из комфортного трикотажа с эластичным поясом
zhilet-sarah-pacini-26113001-12|Жилет Sarah Pacini 26211018-02|sp|0|26211018.jpg|Жилет из стрейч вискозы трикотажный
dzhemper-sarah-pacini-26211013-02|Джемпер Sarah Pacini 26211014-02|sp|0|26211014.jpg|Джемпер с длинными рукавами из гладкой стрейч вискозы с вырезом лодочки с декоративной молнией
kofta-sarah-pacini-2521113-1|Джемпер Sarah Pacini 26211013-02|sp|0|26211013.jpg|Джемпер с рукавами 3/4 и молнией на ней из стрейч вискозы с ребристыми рукавами
bazovaya-vodolazka-sarah-pacini-24112511-v-assortimente|Базовая водолазка Sarah Pacini 109308-02|sp|0|109308-02.jpg|Базовая водолазка из модала
palantin-sarah-pacini-10963009-00|Палантин Sarah Pacini 22114002-43|sp|19241|22114002-43-00-1.jpg|Воздушный палантин
palantin-sarah-pacini-24114504-43|Палантин Sarah Pacini 10963009-00|sp|33770|10963009-00-5.jpg|Воздушный палантин
dlinnoe-plate-sarah-pacini-26113593-02-99913593-1|Платье Sarah Pacini 25113035-22|sp|41300|img_8895.jpg|
rubashka-sarah-pacini-26111003-02|Рубашка Sarah Pacini 25113054|sp|35230|img_8892.jpg|Легкая рубашка
letnij-sviter-s-kapyushonom-sarah-pacini-26111107-02-1|Рубашка Sarah Pacini 26111003-02|sp|39754|img_8747.jpg|Легкая рубашка
bryuki-sarah-pacini-26113004-12|Брюки Sarah Pacini 26133012-12|sp|36680|26133012-12-2.jpg|Повседневные брюки. Универсальные брюки из эластичного хлопка
bryuki-sarah-pacini-26113004-03|Брюки Sarah Pacini 26113004-12|sp|35410|26113004-12-2.jpg|Широкие брюки из фактурного хлопково-полиамидного материала, подчеркнутые декоративной строчкой. Лаконичный, свободный крой сочетает в себе комфорт и современность
trikotazhnye-bryuki-sarah-pacini-24111019-05-1|Брюки Sarah Pacini 26113004-03|sp|35410|26113004-03-2.jpg|Широкие брюки из фактурного хлопково-полиамидного материала, подчеркнутые декоративной строчкой. Лаконичный, свободный крой сочетает в себе комфорт и современность
zhilet-sarah-pacini-26113001-03|Жилет Sarah Pacini 26113001-12|sp|33740|26113001-12.jpg|Жилет без рукавов из фактурной хлопково-полиамидной ткани: широкие проймы, накладные карманы и застежки на кнопках
letnij-sviter-s-korotkim-rukavom-sarah-pacini-26111106-25|Жилет Sarah Pacini 26113001-03|sp|33740|26113001-03.jpg|Жилет без рукавов из фактурной хлопково-полиамидной ткани: широкие проймы, накладные карманы и застежки на кнопках
kardigan-sarah-pacini-26111108-02|Кардиган Sarah Pacini 26111108-25|sp|41040|26111108-25.jpg|Кардиган на молнии с высоким воротником
letnij-sviter-s-kapyushonom-sarah-pacini-26111107-25|Кардиган Sarah Pacini 26111108-02|sp|41040|26111108-02.jpg|Кардиган на молнии с высоким воротником
letnij-sviter-s-kapyushonom-sarah-pacini-26111107-02|Летний свитер с капюшоном Sarah Pacini 26111107-25|sp|41040|26111107-25.jpg|Свободный летний свитер с капюшоном
letnij-sviter-s-korotkim-rukavom-sarah-pacini-26111106-02-1|Летний свитер с капюшоном Sarah Pacini 26111107-02|sp|41040|26111107-02.jpg|Свободный летний свитер с капюшоном
letnij-sviter-s-korotkim-rukavom-sarah-pacini-26111106-02|Летний свитер с коротким рукавом Sarah Pacini 26111106-25|sp|29510|26111106-25.jpg|Свитер без рукавов из льна и нейлона
sviter-s-korotkim-rukavom-sarah-pacini-26111086-15|Летний свитер с коротким рукавом Sarah Pacini 26111106-02|sp|29510|26111106-02.jpg|Свитер без рукавов из льна и нейлона
sviter-s-korotkim-rukavom-sarah-pacini-26111086-1|Свитер с коротким рукавом Sarah Pacini 26111086-15|sp|26400|26111086-15.jpg|Свитер без рукавов из органического хлопка, нейлона и льна с двухцветным узором, сочетающим матовые и глянцевые эффекты
legginsy-sarah-pacini-109320-v-assortimente|Юбка с высокой талией Sarah Pacini 26113006-02|sp|39800|26113006-02.jpg|Юбка с высокой талией из эластичного вискозного полиамида в стиле корсета со съемной бретелькой
letnij-sviter-oversajz-sarah-pacini-26111093-02|Летний свитер оверсайз Sarah Pacini 26111093-33|sp|39800|26111093-33.jpg|Свитер оверсайз, связанный без швов из льна, полиамида и хлопка, сочетает в себе прочность и тонкую вязку. Изысканный и воздушный, он воплощает современную и экологичную эстетику
besshovnyj-azhurnyj-sviter-sarah-pacini-26111092-33|Летний свитер оверсайз Sarah Pacini 26111093-02|sp|39800|26111093-02.jpg|Свитер оверсайз, связанный без швов из льна, полиамида и хлопка, сочетает в себе прочность и тонкую вязку. Изысканный и воздушный, он воплощает современную и экологичную эстетику
besshovnyj-azhurnyj-sviter-sarah-pacini-26111092-02|Бесшовный ажурный свитер Sarah Pacini 26111092-33|sp|36300|26111092-33.jpg|Свитер с вырезом-лодочкой и изящным ажурным узором связан из льна, полиамида и хлопка
sviter-s-korotkim-rukavom-sarah-pacini-26111087|Бесшовный ажурный свитер Sarah Pacini 26111092-02|sp|36300|26111092-02.jpg|Свитер с вырезом-лодочкой и изящным ажурным узором связан из льна, полиамида и хлопка
sviter-s-korotkim-rukavom-sarah-pacini-26111086|Свитер с коротким рукавом Sarah Pacini 26111087|sp|34600|26111087.jpg|Свитер без рукавов из органического хлопка, нейлона и льна с двухцветным узором, сочетающим матовые и глянцевые эффекты
dlinnoe-plate-sarah-pacini-26113593-02-99913593|Рубашка Sarah Pacini 26111003|sp|39800|26111003-03.jpg|Вязаная хлопковая рубашка. Легкая и изысканная: укороченная трикотажная рубашка из хлопка Mako с полупрозрачной ребристой текстурой выгодно подчеркивает фигуру
legginsy-sarah-pacini-20211060-46-1|Леггинсы Sarah Pacini 109320 в ассортименте|sp|16800|109320-02.jpg|Практичные и городские длинные леггинсы прекрасно дополнят туники, юбки и платья этого сезона. Возьмите их с собой в любое приключение
sumka-sarah-pacini-99934614-1|Сумка Sarah Pacini 99934617|sp|39800|99934617.jpg|Сумка через плечо из натуральной кожи. Мягкая кожаная сумочка для всего необходимого. Компактный дизайн: два стильных передних кармана и внутренние отделения
dlinnoe-plate-sarah-pacini-26113593|Длинное платье Sarah Pacini 26113593-02, 99913593|sp|35300|99913593-02.jpg|Длинное платье без рукавов. Струящееся, красиво драпируется и не мнется. Карман-мешок на шнурке можно регулировать для создания плиссированного силуэта
plate-sarah-pacini-20213018-02-1|Длинное платье Sarah Pacini 26113593|sp|35300|26113593-2.jpg|Длинное платье без рукавов. Струящееся, красиво драпируется и не мнется. Карман-мешок на шнурке можно регулировать для создания плиссированного силуэта
bazovyj-top-sarah-pacini-24112504-v-assortimente-1|Базовый топ Sarah Pacini 26112504 в ассортименте|sp|12970|26112504.jpg|Базовый топ из модала
myagkij-sviter-sarah-pacini-23211075-1|Мягкий свитер Sarah Pacini 99211514-06|sp|37520|img_8393.jpg|Мягкий свитер из тонкой шерсти
myagkij-sviter-sarah-pacini-23211075|Мягкий шарф Sarah Pacini 23211078|sp|19890|img_8379.jpg|Мягкий шарф из тонкой шерсти с люрексом
myagkij-sviter-sarah-pacini-24211514-96|Мягкий свитер Sarah Pacini 23211075|sp|30164|img_8372.jpg|Мягкий свитер из тонкой шерсти с люрексом
myagkij-kardigan-sarah-pacini-23211106|Мягкий свитер Sarah Pacini 24211514-96|sp|37520|img_8366_898692.jpg|Мягкий свитер из тонкой шерсти
zhaket-pidzhak-iz-viskozy-transit-cfdtrwt290-05|Брюки из вискозы TRANSIT CFDTRWT291-05|tr|32130|cfdtrwt290-05-11.jpg|
zhaket-pidzhak-iz-lna-i-iskusstvennogo-shelka-transit-cfdtrtb110-1|Жакет (пиджак) из вискозы TRANSIT CFDTRWT290-05|tr|42930|cfdtrwt290-05-13.jpg|
udlinennyj-lnyanoj-zhilet-transit-cfdtrdb116-11|Шарф женский тонкий TRANSIT SCADTRC2000|tr|7700|scadtrc2000-4.jpg|
lnyanoj-zhilet-transit-cfdtrda102-102|Удлиненный льняной жилет TRANSIT CFDTRDB116-11|tr|27500|cfdtrdb116-11-8.jpg|
hlopkovye-bryuki-transit-cfdtrcb115-04|Льняные брюки TRANSIT CFDTRDA103-102|tr|23980|cfdtrda102-102-1.jpg|
futbolka-bez-rukavov-transit-cfdtrcv313-02|Льняной жилет TRANSIT CFDTRDA102-102|tr|18040|cfdtrda102-102-2.jpg|
futbolka-bez-rukavov-transit-cfdtrcv313-04|Футболка без рукавов TRANSIT CFDTRCV313-02|tr|12100|cfdtrcv313-02-3.jpg|
rubashka-iz-iskusstvennogo-shelka-transit-cfdtrcv310-04|Рубашка из искусственного шелка TRANSIT CFDTRCV310-10|tr|25300|20260705_110412.jpg|
futbolka-transit-cfdtrck201|Футболка TRANSIT CFDTRCK201-25|tr|15180|cfdtrck201-25.jpg|
rubashka-iz-iskusstvennogo-shelka-transit-cfdtrcv310-14|Рубашка из искусственного шелка TRANSIT CFDTRCV310-04|tr|25300|cfdtrcv310-04.jpg|
myagkij-shelkovyj-zhilet-transit-cfdtrcv317-02|Мягкий шелковый жилет TRANSIT CFDTRCV317-04|tr|34540|cfdtrcv317-04.jpg|
dvubortnyj-trench-s-poyasom-iz-shelka-transit-cfdtrcv316|Мягкий шелковый жилет TRANSIT CFDTRCV317-02|tr|34540|cfdtrcv317-02_01_t_7768e63c-ff62-4dae-9506-ee8c2bc22d36_600x.jpg|
zhaket-pidzhak-iz-lna-i-iskusstvennogo-shelka-transit-cfdtrtb110|Двубортный тренч с поясом из шелка TRANSIT CFDTRCV316|tr|50600|cfdtrcv316-12_01_f_600x.jpg|
lnyanoe-plate-transit-135-15|Платье TRANSIT CFDTRCV315-05|tr|29700|cfdtrcv315-05_01_t_600x.jpg|
bryuki-transit-cfdtrng-163-04|Брюки TRANSIT CFDTRCV314-04|tr|23980|cfdtrcv314-04_01_t_600x.jpg|
futbolka-bez-rukavov-transit-cfdtrck200-1|Футболка без рукавов TRANSIT CFDTRCV313-04|tr|12100|cfdtrcv313-04_01_s_600x.jpg|
rubashka-iz-lna-i-iskusstvennogo-shelka-transit-cfdtrtb113-1|Рубашка из искусственного шелка TRANSIT CFDTRCV310-14|tr|25300|cfdtrcv310-14_01_s_600x.jpg|
futbolka-bez-rukavov-transit-cfdtrck200|Футболка TRANSIT CFDTRCK201|tr|15180|cfdtrck201-16_01_t_600x.jpg|
futbolka-transit-cfdtrcj192|Футболка без рукавов TRANSIT CFDTRCK200|tr|12100|cfdtrck200-10_01_s_600x.jpg|
lnyanye-bryuki-transit-cfdtrtd138-15|Хлопковые брюки TRANSIT CFDTRCB115-04|tr|21780|cfdtrcb115-04-4.jpg|
bryuki-transit-g163-04|Брюки TRANSIT CFDTRNG 163-04|tr|30322|img_9057.jpg|
rubashka-iz-lna-i-iskusstvennogo-shelka-transit-cfdtrtb113|Жакет (пиджак) из льна и искусственного шелка TRANSIT CFDTRTB110|tr|34510|img_9034.jpg|
lnyanaya-rubashka-transit-cfdtrce144-11|Рубашка из льна и искусственного шелка TRANSIT CFDTRTB113|tr|42602|img_9045.jpg|
bryuki-transit-cfdtrcc121|Льняные брюки TRANSIT CFDTRTD138-15|tr|17300|img_8999.jpg|
lnyanoj-zhaket-transit-cfdtrcc122|Льняной жакет TRANSIT CFDTRTD136-15|tr|27980|img_9004.jpg|
lnyanoe-plate-transit-135-4010-1|Льняное платье TRANSIT 135-15|tr|27900|img_8981.jpg|
lnyanaya-rubashka-transit-cfdtrce144-00-1|Льняная рубашка TRANSIT CFDTRCE144-11|tr|27300|img_8943.jpg|
bryuki-transit-cfdtrcc121-12-1|Брюки TRANSIT CFDTRCC121|tr|25300|img_8924.jpg|
lnyanoj-zhaket-rubashka-transit-cfdtrcd130-1|Льняной жакет TRANSIT CFDTRCC122|tr|30100|img_8921.jpg|
lnyanaya-rubashka-transit-cfdtrce144-00|Льняная рубашка TRANSIT CFDTRWD130|tr|33750|img_8919.jpg|
lnyanaya-rubashka-transit-cfdtrce144-10|Льняная рубашка TRANSIT CFDTRCE144-00|tr|27300|img_8876.jpg|
lnyanaya-rubashka-transit-cfdtrce142-11|Льняная рубашка TRANSIT CFDTRCE144-10|tr|27300|img_8827.jpg|
lnyanaya-rubashka-transit-cfdtrce142-10|Льняная рубашка TRANSIT CFDTRCE142-11|tr|21800|img_8849.jpg|
lnyanaya-rubashka-transit-cfdtrce142-00-1|Льняная рубашка TRANSIT CFDTRCE142-10|tr|21800|img_8813.jpg|
futbolka-transit-cfdtrcj190|Футболка TRANSIT CFDTRCJ192|tr|15250|img_8799.jpg|
lnyanoj-zhaket-rubashka-transit-cfdtrcd130|Льняная рубашка TRANSIT CFDTRWE141|tr|21060|img_8678.jpg|
lnyanoj-zhaket-rubashka-transit-cfdtrcd1301|Льняной жакет/рубашка TRANSIT CFDTRCD130|tr|25300|img_8612.jpg|
"""

EXTRA = {  # known extra data from the original product page
    "palantin-sarah-pacini-10963009-00": {
        "material": "85% модал хлопок, 15% шелк",
        "images": ["22114002-43-00-1.jpg", "22114002-43-00.jpg", "22114002-43-00-2.jpg"],
        "tags": ["аксессуары", "шарф Sarah Pacini"],
    }
}


def category(name):
    n = name.lower()
    rules = [
        ("sumki", ["сумка"]),
        ("palantiny", ["палантин", "шарф", "шапк"]),
        ("platya", ["платье"]),
        ("yubki", ["юбка"]),
        ("bryuki", ["брюки", "леггинсы"]),
        ("kurtki", ["тренч", "пальто", "куртка"]),
        ("cardigany", ["жилет", "кардиган", "жакет"]),
        ("tuniki", ["футболка", "рубашка", "блуз"]),
        ("topy", ["топ ", "водолазка"]),
        ("dgempera", ["джемпер", "свитер", "кофта"]),
    ]
    for slug, keys in rules:
        if any(k in n for k in keys):
            return slug
    return "tuniki"


def load():
    items = []
    for line in RAW.strip().splitlines():
        slug, name, brand, price, img, desc = line.split("|")
        p = {
            "id": slug, "name": name, "brand": brand, "price": int(price),
            "img": img, "desc": desc, "cat": category(name), "isNew": True, "sale": False,
            "model": name.split(" ")[-1] if name.split(" ")[-1][0].isdigit() or name.split(" ")[-1].isupper() else "",
        }
        p.update(EXTRA.get(slug, {}))
        items.append(p)
    return items
