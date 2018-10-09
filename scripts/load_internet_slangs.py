#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convert and load the file "internet-slangs.json" to Anki.

Slangs was retrieved from Wikipedia.

# Input

This program accepts a JSON file containing the list of slangs in this format:

{
  "slang": "AAF",
  "meaning": "As A Friend",
}

# Output

The program creates multiple flashcards like this:

===========================================================
<div>
  (Internet Slang)
  <b>AAF</b>
</div>
-----------------------------------------------------------
<div lang="en">
  <b>AAF</b>: As A Friend.
</div>
===========================================================

Note: all created flashcards have the tag "Slang"

# Running

Note: We consider a deck named "Slang" already exists.

$ python load_internet_slangs.py -d Slang \
    $PWD/resources/internet-slangs.json \
    AnkiTest/User\ 1/
"""

import os, sys, json, re

def load_slangs(input_file, col, deck):

    # We read the input file
    with open(input_file) as f:
        data = json.load(f)

        for entry in data:

            slang = entry["slang"]
            meaning = entry["meaning"]

            # Card 1: French -> English
            card_front = """
<div>
  (Internet Slang)
  <b>%s</b>
</div>
""" % slang

            card_back = """
<div lang="en">
  <b>%s</b>: %s
</div>
""" % (slang, meaning)

            add_flashcard(col, deck, card_front, card_back)


def add_flashcard(col, deck, front, back):
    """
    We hide the Anki API details inside this model.
    Each call create a new note of type Basic in the given deck.
    """

    # Instantiate the new note
    note = col.newNote()
    note.model()['did'] = deck['id']

    # Set the ordered fields as defined in Anki note type
    fields = {}
    fields["Front"] = front
    fields["Back"] = back
    anki_fields = ["Front", "Back"]
    for field, value in fields.items():
        note.fields[anki_fields.index(field)] = value


    # Set the tags
    tags = "Slang"
    note.tags = col.tags.canonify(col.tags.split(tags))
    m = note.model()
    m['tags'] = note.tags
    col.models.save(m)

    # Add the note
    col.addNote(note)



if __name__ == "__main__":

    # Add Anki source to path
    sys.path.append("../../anki")
    from anki.storage import Collection
    from anki.sched import Scheduler

    import argparse, glob

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="JSON file containing the connectors")
    parser.add_argument("anki_home", help="Home of your Anki installation")
    parser.add_argument("-d", "--deck", help="Name of the deck in which to create the flashcards", default="English")
    parser.add_argument("-v", "--verbose", help="Enable verbose mode", action='store_true')
    parser.set_defaults(verbose=False)
    args = parser.parse_args()

    print("-------------------------------")
    print("Connectors Loader -------------")
    print("-------------------------------")
    print("Anki home: %s\n" % args.anki_home)

    # Load the anki collection
    cpath = os.path.join(args.anki_home, "collection.anki2")
    col = Collection(cpath, log=True)

    # Set the model
    modelBasic = col.models.byName('Basic')
    deck = col.decks.byName(args.deck)
    col.decks.select(deck['id'])
    col.decks.current()['mid'] = modelBasic['id']

    # Parse input file
    load_slangs(args.input_file, col, deck)

    # Save the changes to DB
    col.save()