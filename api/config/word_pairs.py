
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

WORD_PAIRS = {
    "bem estar": "bein-está",
    "a gente": "agenti",
    "por que": "purkê",
    "por quê": "purkê",
    "para que": "prakê",
    "para quê": "prakê",
    "vamos embora": "vambóra",
    "vamo embora": "vambóra",
    "com você": "cucê",
    "com vocês": "cucêis",
    "com voce": "cucê",
    "com voces": "cucêis",
    "sem você": "sêin ucê",
    "sem vocês": "sêin ucêis",
    "sem voce": "sêin ucê",
    "sem voces": "sêin ucêis",
    "para você": "prucê",
    "pra você": "prucê",
    "para vocês": "prucêis",
    "pra vocês": "prucêis",
    "para voce": "prucê",
    "para voces": "prucêis",
    "pra voce": "prucê",
    "pra voces": "prucêis",
    "de voce": "ducê",
    "de voces": "ducêis",
    "de você": "ducê",
    "de vocês": "ducêis",
    "em um": "num",
    "em uns": "nuns",
    "em uma": "numa",
    "em umas": "numas",
    "em ele": "nêli",
    "em eles": "nêlis",
    "em ela": "néla",
    "em elas": "nélas",
    "em eles": "nêlis",
    "com um": "cum",
    "com uma": "cuma",
    "com umas": "cumas",
    "com uns": "cuns",
    "com a": "cua",
    "com as": "cuas",
    "com o": "cuo",
    "com os": "cus",
    "com ele": "cuêli",
    "com eles": "cuêlis",
    "com ela": "cuéla",
    "com elas": "cuélas",
    "com você": "cucê",
    "com vocês": "cucêis",
    "com voce": "cucê",
    "com voces": "cucêis",
    "como você": "comucê",
    "como vocês": "comucêis",
    "como voce": "comucê",
    "como voces": "comucêis",
    "que eu": "keu",
    "que é": "ké",
    "esse é": "êssé",
    "essa é": "éssé",
    "está você": "cê tá",
    "está voce": "cê tá",
    "esta você": "cê tá",
    "ta voce": "cê tá",
    "tá você": "cê tá",
    "tá voce": "cê tá",
    "ta você": "cê tá",
    "estão vocês": "cêys tãum",
    "estão voces": "cêys tãum",
    "estao vocês": "cêys tãum",
    "estao voces": "cêys tãum",
    "tão vocês": "cêys tãum",
    "tão voces": "cêys tãum",
    "tao voces": "cêys tãum",
    "tao vocês": "cêys tãum",
    "e você": "iucê",
    "onde você": "ond'cê",
    "onde vocês": "ond'cêys",
    "onde voce": "ond'cê",
    "onde voces": "ond'cêys",
    "para de": "para di",
    "vai voce": "cê vai",
    "vai você": "cê vai",
    "vao voces": "cêys vãu",
    "vão vocês": "cêys vãu",
    "vao vocês": "cêys vãu",
    "vão voces": "cêys vãu",
    "esta voce": "cê tá",
    "está voce": "cê tá",
    "esta você": "cê tá",
    "está você": "cê tá",
    "ta voce": "cê tá",
    "tá voce": "cê tá",
    "ta você": "cê tá",
    "tá você": "cê tá",
    "estao voces": "cêys tãu",
    "estão voces": "cêys tãu",
    "estao vocês": "cêys tãu",
    "estão vocês": "cêys tãu",
    "tão voces": "cêys tãu",
    "tão vocês": "cêys tãu",
    "tao voces": "cêys tãu",
    "tao vocês": "cêys tãu",
    "anda voce": "cê ãnda",
    "anda você": "cê ãnda",
    "andam voces": "cêys andãu",
    "andam vocês": "cêys andãu",
    "do outro": "dôtru",
    "de outro": "dôtru",
    "da outra": "dôtra",
    "dos outros": "dôtrus",
    "das outras": "dôtras",
    "em outro": "nôtru",
    "em outra": "nôtra",
    "em outros": "nôtrus",
    "em outras": "nôtras"
}
