# maklai-internship-test-task

## How to run

You can run this project either locally or using Docker. 

Regardless of the option you choose, you need to clone this repo and change your current working directory to cloned project's root directory.

### Running locally

1. Install project's dependencies with:
    ```bash
    pip install -r requirements.txt
    ```

    Additionally, you can install test dependencies to be able to run tests:
    ```bash
    pip install -r requirements-test.txt
    ```
2. Execute one of the following commands:
    
    2.1 Run application itself:
    ```bash
    uvicorn main:app
    ```
    After that application can be accessed at http://localhost:8000.

    2.2 Or, optionally, run tests with:
    ```bash
    pytest -v
    ```

### Running using Docker

Use `docker compose` to run application:
```bash
docker compose up -d
```
After that application can be accessed at http://localhost:8000.

Optionally, to run tests use the following commands:
```bash
docker build -f Dockerfile.test -t <image-name>:<image-tag> .
docker run --rm <image-name>:<image-tag>
```