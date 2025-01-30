# ACME ANALYTICS DATA PLATFORM

## Pre-Requirements 
- git
- Docker with at least 4GB of RAM and Docker Compose v1.27.0 or later
- IDE

## Run Project
- From the root directory
```
# spins up all the docker containers
make up 

# registers topics with Debezium
make connector 

```


## Improvement 
- Manage secrets with a third party tool such as vault
- Add CI/CD
- Add unit tests
- Add Integration tests
- configure pre-commit
- logging