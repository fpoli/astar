# Progetto Intelligenza Artificiale 2015/2016

Vindinium (http://vindinium.org/)

[![Build Status](https://magnum.travis-ci.com/fpoli/ia1516.svg?token=XpqKLcynjTRxpC4xqqri)](https://magnum.travis-ci.com/fpoli/ia1516)

## Relazione

Il comando `make report` genera la relazione:

- HTML(5) `report/report.html` (personalizzabile con CSS e template)
- PDF `report/report.pdf`

## Utilizzo

Per far partire il client: `python3 src/main.py <la-key-del-bot>`

## Documentazione

Il comando `make docs` genera la documentazione html, visibile alla pagina `docs/build/html/index.html`.

## Dipendenze

Per installare le dipendenze su `Ubuntu 14.04` ho usato:
```
sudo apt-get install python3-pip python3-sphinx
sudo pip3 install -r requirements.txt
```

## License

The code is based on [https://github.com/renatopp/vindinium-python]

Copyright 2015
GPL version 3, see [LICENSE.txt](LICENSE.txt)

