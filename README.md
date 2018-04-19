# UCD-Bikers

Web application for Dublin Bikes with latest updates and past occupancy trends.


![Dublin Bikes image](https://user-images.githubusercontent.com/28864823/38957163-ba9fb094-4351-11e8-8a96-3871ca201a09.jpg)

(Photograph: Aidan Crawley/Bloomberg)


## Prerequisites

The application is built to be used with Python 3. Update `Makefile` to switch to Python 2 if needed.

Some Flask dependencies are compiled during installation, so `gcc` and Python header files need to be present.
For example, on Ubuntu:

    apt install build-essential python3-dev
    pip install virtualenv


## Quick Start

        git clone https://github.com/FrauBoes/UCD-Bikers.git
        
Go to UCD-Bikers/bikers. To run the application from the terminal:

    make run

And open it in the browser at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).


## Development environment and release process

 - Create virtualenv with Flask and UCD-Bikers installed into it (latter is installed in
   [develop mode](http://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode) which allows
   modifying source code directly without a need to re-install the app): `make venv`

 - Run development server in debug mode: `make run`; Flask will restart if source code is modified

 - Run tests: `make test` (see also: [Testing Flask Applications](http://flask.pocoo.org/docs/0.12/testing/))

 - Create source distribution: `make sdist` (will run tests first)

 - To remove virtualenv and built distributions: `make clean`

 - To add more python dependencies: add to `install_requires` in `setup.py`

 - To modify configuration in development environment: edit file `settings.cfg`; this is a local configuration file
   and it is *ignored* by Git - make sure to put a proper configuration file to a production environment when
   deploying


## Deployment

Check out [Deploying with Fabric](http://flask.pocoo.org/docs/0.12/patterns/fabric/#fabric-deployment) on one of the
possible ways to automate the deployment.

- Build a package (`make sdist`)

- Deliver it to a server and install it (`pip install bikers.tar.gz`)

- Ensure that configuration file exists and `BIKERS_SETTINGS` environment variable points to it

- Ensure that user has access to the working directory to create and write log files in it

- Run a [WSGI container](http://flask.pocoo.org/docs/0.12/deploying/wsgi-standalone/) with the application.
And, most likely, it will also run behind a [reverse proxy](http://flask.pocoo.org/docs/0.12/deploying/wsgi-standalone/#proxy-setups).


## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used
* [jQuery](https://jquery.com/) - JavaScript library
* [Bootstrap](https://getbootstrap.com/) - Front-end library
* [PyMySQL](https://github.com/PyMySQL/PyMySQL) - Python MySQL client
* [Google Charts](https://developers.google.com/chart/) - Gallery of interactive charts
* [Google Maps](https://developers.google.com/maps/) - Real-time information for mapping and navigation
* [Jupyter Notebook](http://jupyter.org/) - Web application used for data analysis


## Data Used

* [Open Weather Map](https://openweathermap.org/) - Current weather and forecasts
* [JCDecaux](https://developer.jcdecaux.com/) - Self-service bicyles


## Authors

* **Julia Boes** - [GitHub](https://github.com/FrauBoes)
* **Daragh O'Farrell** - [GitHub](https://github.com/Basschops)
* **Wu Di** - [GitHub](https://github.com/derekwu90)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
