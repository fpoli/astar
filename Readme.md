# Progetto Intelligenza Artificiale 2015/2016

Vindinium (http://vindinium.org/)

[![Build Status](https://magnum.travis-ci.com/fpoli/ia1516.svg?token=XpqKLcynjTRxpC4xqqri)](https://magnum.travis-ci.com/fpoli/ia1516)


## Relazione

Il comando `make report` genera la relazione:

- HTML(5) `report/report.html` (personalizzabile con CSS e template)
- PDF `report/report.pdf`


## Utilizzo

Crea un file `bot.key` contentente la key del bot:

	echo la-key-del-bot > bot.key

Successivamente, per far partire il client:

	make start


## Documentazione

Per generare la documentazione html:

	make docs

Sarà visibile alla pagina `docs/build/html/index.html`.


## Test automatici

Per eseguire linter e test:

	make linter
	make test


## Alcune misurazioni

Per eseguire una partita con il profiling attivo:

       make profile

Per analizzare i risultati (il file `main.calltree`) è molto comodo usare
`kcachegrind` (con il comando `kcachegrind main.calltree`).

Per misura la velocità del server, del simulatore o di certi bot:

       make benchmark


## Dipendenze

Per installare le dipendenze su `Ubuntu 14.04`:

	sudo apt-get install python3-pip python3-sphinx
	sudo pip3 install -r requirements.txt


## License

The code is based on [renatopp/vindinium-python](https://github.com/renatopp/vindinium-python).

Copyright 2015.

Distributed under the GNU GPL version 3, see [LICENSE.txt](LICENSE.txt)
