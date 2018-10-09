# anki-packages-generator

Scripts used to create flashcards programmatically. (see under folder `scripts/`)

## Dependencies

** Python 3.x
** Virtualenv

## Installing

```
$ git clone <anki-packages-generator>
$ cd anki-packages-generator
$ git submodule add https://github.com/dae/anki.git # Use a tag if error happens with latest version
$ virtualenv -p python3 env
$ pip install -r requirements.txt
```

## Running

First, make sure to enable virtualenv:

```
$ source env/bin/activate
```

Then, create a valid Anki installation that will be populated with generated flashcards.
(Important: use a clean installation to avoid corrupting our Anki database!)

On Linux:

```
$ cp -R AnkiModel AnkiTest
$ anki -b AnkiTest
# Anki installation will be written to ./AnkiTest/User\ 1/
```

On MacOS:

```
$ cp -R AnkiModel AnkiTest
$ open /Applications/Anki.app --args -b ./AnkiTest
# Anki installation will be written to /Applications/Anki.app/Contents/Resources/AnkiTest/User\ 1/
```

With Anki running, create the target deck and the required custom note type(s). Once done, close Anki.

Select the script to launch it:
```
$ cd scripts/
$ python load_XXX.py -d English \
    $PWD/resources/XXX.json \
    AnkiTest/User\ 1/
```

Note: Check each script Python docstring for further documentation.

Reopen Anki using the same command as used above and export the populated deck as an Anki package. To finish, open Anki without argument and import the exported package. That's it.

