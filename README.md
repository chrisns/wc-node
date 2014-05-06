# WC4U backend application server

RESTful API built to run on GAE to service WC4U FE web app and any other end points


## Install

OSX only to install node:

	ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
	brew doctor
	brew install node

All:

	npm install
	gem install sass compass
	npm install -g grunt-cli jshint bower karma-jasmine
	easy_install pylint WebTest

## Test
	grunt test

## Start
	grunt build
	../google_appengine/dev_appserver.py . 

## Develop
	grunt watch

## Author
	Chris Nesbitt-Smith <chris@cns.me.uk>
