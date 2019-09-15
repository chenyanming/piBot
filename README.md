# PiBot

PiBot is a telegram bot which has the following features:

* Send a youtube link to Pibot, Pibot downloads the music and send back the sound file (Up to 50MB)
* Send a BT file to Pibot to trigger the server download
* send a pdf/mobi/epub/azw3 file to Pibot to backup the ebook to calibre library (Up to 20MB)
* send a message to Pibot, pibot will take it as a normal command and issue it. If you send it the python source codes, it will run it!
* send a formula to Pibot, start from a number or a parenthesis, you can use Built-in Functions as well
* send an hex (0x) or bin (0b) to Pibot
* Turn on/off Python Mode
* Check excahnge rates
* search duckduckgo
* Inline keyboard shortcuts:
  * Get the IP Address
  * Turn on/off Python Mode
  * Restart the Python Section
  * Check the lastest added Books
* Custom keyboard according to mode

<p align="center">
  <img src="./img/help.png" alt="help width="738">
</p>


## Functions

### /mode

Show mode status or change mode

```sh
/mode
```

<p align="center">
  <img src="./img/mode.png" alt="/mode" width="738">
</p>

```
/mode shell
```

<p align="center">
  <img src="./img/shell.png" alt="/mode shell" width="738">
</p>

You can issue normal linux commands to the server, just like terminal, e.g. pwd

```
pwd
```

<p align="center">
  <img src="./img/pwd.png" alt="pwd" width="300">
</p>

```
/mode python
```

<p align="center">
  <img src="./img/python.png" alt="python" width="738">
</p>

You can issue normal python commands to the server, just like python shell, e.g. calculate something...

```
343435*123434/0x34
```

<p align="center">
  <img src="./img/pythoncal.png" alt="python" width="738">
</p>

### /hkd, /cny, /usd, /jpy

Check the exchange rate

```sh
/hkd 100
```

<p align="center">
  <img src="./img/hkd.png" alt="hkd" width="738">
</p> 

###/search

Search the duckduckgo and get the summary of lastest 10 results.

<p align="center">
  <img src="./img/hkd.png" alt="search" width="738">
</p> 



###/preview

Search the duckduckgo and get the preview of lastest 10 results.

<p align="center">
  <img src="./img/hkd.png" alt="preview" width="300">
</p> 



###/py

run python commands in shell mode

<p align="center">
  <img src="./img/py.png" alt="py" width="738">
</p> 

###/booksearch

Search the calibre library

<p align="center">
  <img src="./img/booksearch.png" alt="/booksearch" width="738">
</p> 

### /bookshow

Get the specific book information

<p align="center">
  <img src="./img/bookshow.png" alt="/bookshow" width="738">
</p> 

###/bookexport

Export the book

<p align="center">
  <img src="./img/bookexport.png" alt="/bookexport" width="738">
</p> 

### Download BT

Send a bt file to pibot, it will trigger the aria2c server to download the bt file

<p align="center">
  <img src="./img/bt.png" alt="BT" width="738">
</p>

<p align="center">
  <img src="./img/bt2.png" alt="BT 2" width="738">
</p>

### Download Youtube audio

Send a youtube link to Pibot, it will send back the audio to you!

<p align="center">
  <img src="./img/audio.png" alt="audio" width="738">
</p> 

### Backup ebook

Send a ebook to Pibot, it will save to calibre library

<p align="center">
  <img src="./img/ebook.png" alt="audio" width="738">
</p> 