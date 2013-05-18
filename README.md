# GroupStatus

GroupStatus tries to make it easier to keep track of what everybody is
up to.  It consists of an IRC bot that listens to status updates on
channels, and a web frontend that publishes what the bot learned.

## Database

Status updates are stored in a postgresql database.

## IRC Bot

The IRC part implemented is a [supybot](http://supybot.com/) plugin.

## Web UI

The web-site is a django application.  It only needs read-only
access to the database.

