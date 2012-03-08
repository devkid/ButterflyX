#!/bin/bash

xgettext --force --files-from po/POTFILES.in --output po/MESSAGES.pot

for f in po/*.po
do
	msgmerge --update --no-fuzzy-matching --backup=off $f po/MESSAGES.pot
	msgfmt $f --output `dirname "$f"`/`basename "$f" .po`.mo
done