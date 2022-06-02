


## **ANISQ** - Download Anime Movies and TV Series with albanian subtitles.

Better implementation of [Filma24-CLI] written in Python, and made for albanian anime.

### Table of Contents

- [Install](#Installation)
- [Usage](#Usage)
- [Disclaimer](#Disclaimer)

## Installation: <a name="Installation"></a>

`pip install anisq`

- Make sure to install MPV player if you are planning to Stream content.
- If You are having issues installing this package on Android [Termux] try installing these dependencies first

      pkg install libxml2 libxslt libiconv

## Usage: <a name="Usage"></a>

### Download a movie or tv series

      anisq [Title or URL]

### Downloads without asking for a choice

      anisq -a [Title]

### Watch

      anisq -w [Title]

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

You can also use arguments such as -m or -t to make the script only search for movies or tv series. Make sure to write the title after the arguments.

      anisq -m [title]
      anisq -t [title] -s [nr] -e [nr]

### Using a List

You can use a txt file filled with names or url's and use that as input. The script will go over all of them.

- If you add a custom season, the script will download the same season number for all elements on the list. Same thing will happen for a custom episode.

---

## Disclaimer: <a name="Disclaimer"></a>

This script was made to make it easier to download movies and tv series through web scraping instead of doing so manually. Every content that is being downloaded is hosted by third parties, as mentioned in the webpage that is used for scraping. <br>
Use it at your own risk. Make sure to look up your country's laws before proceeding. <br>
<br>
Any Copyright Infridgement should be directed towards the scraped website or hosts inside it.
