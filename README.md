
## **ANISQ** - Download Anime Movies and TV Series with albanian subtitles.

Better implementation of [Filma24-CLI] written in Python, and made for albanian anime.

### Table of Contents

- [Install](#Installation)
- [Usage](#Usage)
- [Disclaimer](#Disclaimer)

## Installation: <a name="Installation"></a>

`pip install anisq`

## Usage: <a name="Usage"></a>

### Download a movie or tv series

      anisq [Title or URL]

### Download in automatic mode

      anisq -a [Movie Title]

### Watch

      anisq -w [Movie Title]

### Watch a movie, but let the script choose automatically

      anisq -wa [Movie Title]

---

### Watch first episode of a custom season

      anisq -w [Series Title] -s [Season Nr]

### Watch a custom episode of a custom season

      anisq -w -s [Season Nr] -e [Episode Nr] [Series Title]

---

### Custom Output Directory

      anisq [options] [query] -o [directory path]

---

### Using a List

You can use a txt file filled with names or url's and use that as input. The script will go over all of them.

- If you add a custom season, the script will download the same season number for all elements on the list. Same thing will happen for a custom episode.

---

## Disclaimer: <a name="Disclaimer"></a>

This script was made to make it easier to download movies and tv series through web scraping instead of doing so manually. Every content that is being downloaded is hosted by third parties, as mentioned in the webpage that is used for scraping. <br>
Use it at your own risk. Make sure to look up your country's laws before proceeding. <br>
<br>
Any Copyright Infridgement should be directed towards the scraped website or hosts inside it.
