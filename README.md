# Ghost Reader: Autonomously Reading Images and Texts

## Welcome to Ghost Reader.

An easy-to-use solution for extracting text from images and further converting them into raw audios. Ghost Readers offers a high-level API where requests can be made via JSON to accomplish such features. Please, follow along with the next sections in order to learn more about this excellent tool.

Ghost Reader is compatible with: **Python 3.6+**.

---

## Package guidelines

1. The very first information you need is in the very **next** section.
2. **Installing** is also easy if you wish to read the code and bump yourself into, follow along.
3. Note that there might be some **additional** steps in order to use our solutions.
4. If there is a problem, please do not **hesitate**. Call us.

---

## Getting started: 60 seconds with Ghost Reader

First of all. Code is commented. Yes, everything is commented. Just browse to any file, chose your subpackage, and follow it. We have high-level code for most tasks we could think.

Alternatively, if you wish to learn even more, please take a minute:

Ghost Reader source files are based on the following structure, and you should pay attention to its tree:

```yaml
- ghost_reader
    - decorators
        - authentication
    - handlers
        - base
        - convert
        - extract
        - login
        - register
    - models
        - conversion
        - extraction
        - user
    - processors
        - base
        - convert
        - extract
    - utils
        - constants
        - database
        - loader
        - process_manager
        - server
        - speecher
```

### Decorators

Each decorator is responsible for performing additional verifications that must be made before computing requests.

### Handlers

A package that is used to handle any route within this API.

### Models

Models are NoSQL definitions used to persist data across interactions.

### Processors

The processors are responsible for invoking and consuming the task queues, providing a callback when the task has been invoked, consumed, and finished.

### Utils

A utility package stands for everyday things shared across the application. It is better to implement once and use it as you wish than re-implementing the same thing repeatedly.

---

## Installation

Remember that you need to adjust `.env.example` according to your needs and make sure that `docker-compose` is installed and accessible from the command line.

### Docker-Compose

First of all, you need to build the container's image, as follows:

```
docker-compose build
```

After the build process is finished, you can run the container in detached mode:

```
docker-compose up -d
```

If you ever need to perform maintenance or update the repository, please put the container down:

```
docker-compose down
```

---

## Environment configuration

Note that sometimes, there is a need for additional implementation. If needed, from here, you will be the one to know all of its details.

### Ubuntu

No specific additional commands are needed.

### Windows

No specific additional commands are needed.

### MacOS

No specific additional commands are needed.

---

## Support

We know that we do our best, but it is inevitable to acknowledge that we make mistakes. If you ever need to report a bug, report a problem, talk to us, please do so! We will be available at our bests at this repository.

---
