#!/usr/bin/env python3
# -*- coding: utf-8 -*-

PHONETIC_DICTIONARY = {
    # Pronouns and Articles
    'não': 'nãu',
    'nao': 'nãu',
    'olá': 'oi',
    'ate': 'té',
    'alguém': 'auguêin',
    'alguem': 'auguêin',
    'ninguém': 'ninguêin',
    'ninguem': 'ninguêin',
    'aquilo': 'akilu',
    'aquele': 'akêli',
    'aqueles': 'akêlis',
    'aquela': 'akéla',
    'aquelas': 'akélas',
    'daquilo': 'dakilu',
    'daquele': 'dakêli',
    'daqueles': 'dakêlis',
    'daquela': 'dakéla',
    'daquelas': 'dakélas',
    'naquilo': 'nakilu',
    'naquele': 'nakêli',
    'naqueles': 'nakêlis',
    'naquela': 'nakéla',
    'naquelas': 'nakélas',
    'ela': 'éla',
    'elas': 'élas',
    'ele': 'êli',
    'eles': 'êlis',
    'eli': 'êli',
    'essa': 'éssa',
    'essas': 'éssas',
    'esse': 'êssi',
    'esses': 'êssis',
    'esta': 'ésta',
    'estas': 'éstas',
    'este': 'êsti',
    'estes': 'êstis',
    'eu': 'eu',
    'meu': 'mêu',
    'nesta': 'néssa',
    'nestas': 'néssas',
    'neste': 'nêssi',
    'nestes': 'nêssis',
    'nossa': 'nóssa',
    'nossas': 'nóssas',
    'nosso': 'nóssu',
    'nossos': 'nóssus',
    'quais': 'kuais',
    'quaisquer': 'kuauké',
    'qual': 'kuau',
    'qualquer': 'kuauké',
    'quando': 'cuandu',
    'quem': 'kêyn',
    'seu': 'teu',
    'seus': 'teus',
    'sua': 'tua',
    'suas': 'tuas',
    'te': 'ti',
    'tao': 'tãu',
    'ta': 'tá',
    'me': 'mi',
    'lhe': 'ly',
    'lhes': 'lys',
    'nos': 'nus',
    'o': 'u',
    'os': 'us',
    'voce': 'você',
    'voces': 'vocêis',

    # Adverbs
    'demais': 'dimais',
    'devagar': 'divagá',

    # Prepositions and Conjunctions
    'à': 'a',
    'às': 'as',
    'com': 'cu',
    'sem': 'sêyn',
    'e': 'i',
    'em': 'in',
    'mas': 'máys',
    'para': 'pra',
    'pela': 'pela',
    'pelas': 'pelas',
    'pelo': 'pelu',
    'pelos': 'pelus',
    'por': 'pur',
    'porque': 'purkê',
    'porquê': 'purkê',
    'de': 'di',
    'dele': 'dêli',
    'deles': 'dêlis',
    'desta': 'déssa',
    'destas': 'déssas',
    'deste': 'dêssi',
    'destes': 'dêssis',
    'dessa': 'déssa',
    'dessas': 'déssas',
    'desse': 'dêssi',
    'desses': 'dêssis',

    # Tech Terms
    'app': 'épi',
    'apps': 'épis',
    'celular': 'celulá',
    'email': 'imêiu',
    'facebook': 'feicibúqui',
    'google': 'gugou',
    'instagram': 'instagran',
    'internet': 'internéti',
    'link': 'linki',
    'links': 'linkis',
    'mouse': 'mauzi',
    'site': 'sáiti',
    'sites': 'sáitis',
    'smartphone': 'ysmartifôni',
    'tablet': 'tábleti',
    'tiktok': 'tikitóki',
    'twitter': 'tuíter',
    'whatsapp': 'uatizápi',
    'wifi': 'uaifai',
    'youtube': 'iutiúbi',
    'chat': 'chati',
    'ipad': 'aipédi',

    # Common Words and Expressions
    'aí': 'aí',
    'ali': 'alí',
    'aqui': 'akí',
    'atrás': 'atráyz',
    'bem': 'beyn',
    'depois': 'dipois',
    'empresa': 'impreza',
    'empresas': 'imprezas',
    'então': 'entãum',
    'juntos': 'juntu',
    'lá': 'lá',
    'mais': 'máys',
    'muito': 'mūtu',
    'muita': 'mūta',
    'muitas': 'mūtas',
    'muitos': 'mūtus',
    'obrigada': 'brigada',
    'obrigado': 'brigadu',
    'que': 'ki',
    'sempre': 'seynpri',
    'também': 'tãmbêin',
    'tambem': 'tãmbêin',
    'teatro': 'tiatru',
    'teatros': 'tiatrus',
    'última': 'útima',
    'últimas': 'útimas',
    'último': 'útimu',
    'últimos': 'útimus',
    'dormir': 'durmí',
    'dormiu': 'durmíu',
    'dormiram': 'durmíram',
    'atual': 'atuau',
    'atualmente': 'atuaumêinti',
    'agora': 'agóra',
    'hoje': 'ôji',
    'mes': 'mêys',
    'meses': 'mêzis',
    'menos': 'menus',
    'menor': 'menór',
    'menores': 'menoris',
    'pouco': 'pôcu',
    'poucos': 'pôcus',
    'pouca': 'pôca',
    'poucas': 'pôcas',
    'bonito': 'bunitu',
    'bonita': 'bunita',
    'bonitas': 'bunitas',
    'bonitos': 'bunitus',
    'olho': 'ôliu',
    'olhos': 'ôlius',
    'menino': 'mininu',
    'menina': 'minina',
    'meninas': 'mininas',
    'meninos': 'mininus'
}