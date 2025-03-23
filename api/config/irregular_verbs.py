
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

IRREGULAR_VERBS = {
    "estar": "tá",
    "estou": "tô",
    "estás": "tá",
    "está": "tá",
    "estamos": "tam",
    "estão": "tãum",
    "estive": "tivi",
    "esteve": "tevi",
    "estivemos": "tivimu",
    "estiveram": "tiverã",
    "estava": "tava",
    "estavamos": "tavamu",
    "estavam": "tavã",
    "ser": "sê",
    "sou": "sô",
    "é": "é",
    "somos": "sômu",
    "são": "sãu",
    "fui": "fui",
    "foi": "fôi",
    "fomos": "fomu",
    "foram": "forãu",
    "ter": "tê",
    "tenho": "tenhu",
    "tem": "tein",
    "temos": "temu",
    "têm": "têim",
    "tive": "tivi",
    "teve": "tevi",
    "tivemos": "tivemu",
    "tiveram": "tiveraum",
    "tinha": "tinha",
    "tinhamos": "tinhamu",
    "tinham": "tinhaum",
    "fazer": "fazê",
    "faco": "fassu",
    "faço": "fassu",
    "faz": "fais",
    "fazemos": "fazêmu",
    "fazem": "fázeim",
    "fiz": "fis",
    "fez": "fêiz",
    "fizemos": "fizemu",
    "fizeram": "fizérã",
    "fazia": "fazia",
    "faziamos": "faziamu",
    "faziam": "faziãu",
    "faria": "fazia",
    "fariam": "faziãu",
    "ir": "ih",
    "vou": "vô",
    "vai": "vai",
    "vamos": "vã",
    "vão": "vãun",
    "vir": "vim",
    "venho": "venhu",
    "vem": "vêin",
    "vimos": "vimu",
    "vêm": "vêin",
    "dizer": "dizê",
    "digo": "digu",
    "diz": "dis",
    "dizemos": "dizemu",
    "dizem": "dizeim",
    "disse": "dissi",
    "dissemos": "dissêmu",
    "disseram": "dissérãu",
    "diria": "diria",
    "diríamos": "diríamus",
    "diriam": "diriãu",
    "diga": "diz",
    "digamos": "digãmu",
    "digam": "digãu",
    "pedir": "pedí",
    "peço": "péssu",
    "pedi": "pédi",
    "pedimos": "pedímu",
    "pedem": "pédeim",
    "dar": "dá",
    "dou": "dô",
    "dá": "dá",
    "damos": "dãmu",
    "dão": "dãu",
    "dei": "dêi",
    "deu": "dêu",
    "demos": "démus",
    "deram": "déraum",
    "querer": "kerê",
    "quero": "kéru",
    "quer": "ké",
    "queremos": "kerêmu",
    "querem": "kéreym",
    "quis": "kis",
    "quisemos": "kizemu",
    "quiseram": "kizeraum",
    "poder": "podê",
    "posso": "póssu",
    "pode": "pódi",
    "podemos": "podêmu",
    "podem": "pódeym",
    "pude": "pudi",
    "pudemos": "pudemu",
    "puderam": "puderaum",
    "ver": "vê",
    "vejo": "veju",
    "vê": "vê",
    "ve": "vê",
    "vemos": "vemu",
    "veem": "veem",
    "vi": "vi",
    "viu": "viu",
    "viram": "viraum",
    "saber": "sabê",
    "sei": "sei",
    "soube": "sóbe",
    "soubemos": "sobemos",
    "souberam": "soberam",
    "trazer": "trazê",
    "trago": "trago",
    "traz": "traz",
    "trazemos": "traizemu",
    "trazem": "traizeym",
    "trocar": "troca",
    "trocamos": "trocamu",
    "trocam": "trocaum",
    "trocaram": "trocaum",
    "mentir": "menti",
    "minto": "minto",
    "mente": "meinti",
    "mentimos": "mintimos",
    "mentem": "mentem",
    "mentia": "mintia",
    "mentiamos": "mintiamos",
    "mentiam": "mintiam",
    "mentiram": "mintiram",
    "ler": "lê",
    "leio": "lêiu",
    "lê": "lê",
    "lemos": "lêmus",
    "olhar": "oliá",
    "olho": "óliu",
    "olhamos": "oliamus",
    "olham": "oliam",
    "olharam": "olharam",
    "errar": "erra",
    "erro": "erro",
    "erramos": "erramu",
    "erram": "erram",
    "errou": "errou",
    "erraram": "erraram",
    "experimentar": "isprimentá",
    "experimento": "isprimentu",
    "experimenta": "isprimenta",
    "experimentamos": "isprimentãmu",
    "experimentam": "isprimentam",
    "experimentei": "isprimentei",
    "experimentou": "isprimentou",
    "experimentaram": "isprimentaram"
}
