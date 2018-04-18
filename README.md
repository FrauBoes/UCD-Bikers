# UCD-Bikers

Web application for Dublin Bikes with latest updates and past occupancy trends



## Quick Start

Run the application:

    make run

And open it in the browser at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)



## Prerequisites

The application is built to be used with Python 3. Update `Makefile` to switch to Python 2 if needed.

Some Flask dependencies are compiled during installation, so `gcc` and Python header files need to be present.
For example, on Ubuntu:

    apt install build-essential python3-dev



## Development environment and release process

 - create virtualenv with Flask and UCD-Bikers installed into it (latter is installed in
   [develop mode](http://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode) which allows
   modifying source code directly without a need to re-install the app): `make venv`

 - run development server in debug mode: `make run`; Flask will restart if source code is modified

 - run tests: `make test` (see also: [Testing Flask Applications](http://flask.pocoo.org/docs/0.12/testing/))

 - create source distribution: `make sdist` (will run tests first)

 - to remove virtualenv and built distributions: `make clean`

 - to add more python dependencies: add to `install_requires` in `setup.py`

 - to modify configuration in development environment: edit file `settings.cfg`; this is a local configuration file
   and it is *ignored* by Git - make sure to put a proper configuration file to a production environment when
   deploying


## Deployment

Check out [Deploying with Fabric](http://flask.pocoo.org/docs/0.12/patterns/fabric/#fabric-deployment) on one of the
possible ways to automate the deployment.

- Build a package (`make sdist`)

- deliver it to a server and install it (`pip install bikers.tar.gz`)

- ensure that configuration file exists and `BIKERS_SETTINGS` environment variable points to it

- ensure that user has access to the working directory to create and write log files in it

- run a [WSGI container](http://flask.pocoo.org/docs/0.12/deploying/wsgi-standalone/) with the application.
And, most likely, it will also run behind a [reverse proxy](http://flask.pocoo.org/docs/0.12/deploying/wsgi-standalone/#proxy-setups).


## Built With

* [Flask](http://http://flask.pocoo.org/) - The web framework used
* [jQuery](https://jquery.com/) - JavaScript library
* [Bootstrap](https://getbootstrap.com/) - Front-end library
* [PyMySQL](https://github.com/PyMySQL/PyMySQL) - Python MySQL client
* [Google Charts](https://developers.google.com/chart/) - Gallery of interactive charts
* [Jupyter Notebook](http://jupyter.org/) - Web application used for data analysis


## Authors

* **Julia Boes** - *Initial work* - [PurpleBooth](https://github.com/FrauBoes)
* **Daragh O'Farrell** - *Initial work* - [PurpleBooth](https://github.com/Basschops)
* **Wu Di** - *Initial work* - [PurpleBooth](https://github.com/derekwu90)


## License

This project is licensed under the MIT License - see the [LICENSE.md]()LICENSE.md file for details


## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
