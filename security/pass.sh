#! /bin/sh

CLEAR=~/pass.txt
CRYPT=~/pass.crypt
CIPHER=AES256

gpg --output $CLEAR --decrypt $CRYPT 2>/dev/null && vi $CLEAR

case "$1" in
	"edit")
		gpg --output $CRYPT --symmetric --cipher-algo $CIPHER $CLEAR 2>/dev/null
		;;
	*)
		;;
esac

shred --remove $CLEAR
