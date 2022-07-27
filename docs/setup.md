1. Install Docker for your distro
1. Copy `.env.sample` to a new file called `.env`
1. `make dev` runs docker-compose and then runs database migrations
1. `docker ps` confirm that you have two containers running: `kaizen_db` and `kaizen_pgadmin`