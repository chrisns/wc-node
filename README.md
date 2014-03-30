WC4U backend application server
====================================

RESTful API built to run on GAE to service WC4U FE web app and any other end points


Install

-------

ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"

brew doctor

brew install node

curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -o - | python
sudo easy_install virtualenv
virtualenv --no-site-packages .
bin/easy_install zc.buildout
./bin/python bootstrap.py

npm install

gem install sass compass

npm install -g grunt-cli jshint bower karma-jasmine

grunt


apt-get install python-gvgen

Start
-----
grunt serve
../google_appengine/dev_appserver.py . 


Author
-------
Chris Nesbitt-Smith <chris@cns.me.uk>
