WC4U backend application server
====================================

RESTful API built to run on GAE to service WC4U FE web app and any other end points


Install

-------

ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
brew doctor
brew install node
npm install
gem install sass --pre
npm install -g grunt-cli
grunt sass
grunt uglify
grunt watch

apt-get install python-gvgen

Start
-----
npm start


Author
-------
Chris Nesbitt-Smith <chris@cns.me.uk>
