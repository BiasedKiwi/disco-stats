<h1 align="center">📈 Disco Stats</h1>

<div align="center">

<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![DeepSource](https://deepsource.io/gh/BiasedKiwi/disco-stats.svg/?label=active+issues&show_trend=true&token=poQIOnCKk20c7Kt_tPx40Gwc)](https://deepsource.io/gh/BiasedKiwi/disco-stats/?ref=repository-badge)
![discord.py](https://img.shields.io/github/pipenv/locked/dependency-version/biasedkiwi/disco-stats/discord.py)
![LICENSE](https://img.shields.io/github/license/biasedkiwi/disco-stats)
![Open Issues](https://img.shields.io/github/issues/biasedkiwi/disco-stats)

</div>

## 🖥️ Self-hosting

For a more detailed summary, check the the end of the steps below.

* To run Disco Stats on your own machine, you will first need a bot token, to get one head over to <a href="https://discord.com/developers">discord.com/developers</a> and create a new app and a bot associated to it and it's token.

* Setup an instance of <a href="https://www.postgresql.org/download/">PostgreSQL</a>.

* After that, install the latest Python interpreter at <a href="https://python.org/downloads">python.org/downloads</a>.

* Using your newly installed tools, run `pip install -r requirements.txt` inside Disco Stats' root directory to install it's dependencies.

* Then, set your environments variables inside `.env`:
  - `DISCO_TOKEN`: Your Discord bot token
  - `POSTGRES_USER`: Your postgres installation user
  - `POSTGRES_PASSWORD`: Your postgres installation password

* Finally, you can run `launcher.py` and the bot will launch.

<details>
<summary>Detailed Summary</summary>
    Coming soon!
</details>