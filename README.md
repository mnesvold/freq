# freq
Feature request tracking

## Getting started locally

You'll need [Docker](https://docs.docker.com/mac/) and [Docker
Compose](https://docs.docker.com/compose/install/). If you don't want to
install the latter yourself, but do have Python's `virtualenv` tool available,
there's a utility script in this repo to set up Docker Compose in a virtual
environment.

Once you've cloned this repo and `cd`'d into the working directory, this will
get you set up running locally:

```bash
$ ./bin/mkvenv # (optional -- installs docker-compose to a virtual env.)
$ source venv/bin/activate # (optional -- activates the virtual env.)
$ docker-compose run --rm web python manage.py migrate
$ docker-compose run --rm web python manage.py loaddata /srv/fixtures/dev.json
$ docker-compose run --rm web python manage.py collectstatic --noinput
$ docker-compose up
```

Your local Freq instance should be running on your localhost's port `8000`. The
dev fixture (`/srv/fixtures/dev.json`) imports a single superuser, `admin`,
whose password is also `admin`. (Needless to say, **don't import this fixture
in production**.)
