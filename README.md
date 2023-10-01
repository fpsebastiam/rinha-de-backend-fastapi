A FastAPI solution to the [rinha de backend](https://github.com/zanfranceschi/rinha-de-backend-2023-q3/blob/main/INSTRUCOES.md) challenge, just to practice a bit of Python.

Heavily inspired by [iancambrea's solution](https://github.com/iancambrea/rinha-python-sanic/tree/main) in Sanic.

## Stress Testing
The current implementation achieves a count of 23891, without using the `network_mode: host` config. Below is a summary of the stress test:

![Gatling Results](image.png)

## TODO
- Try some caching
- See if bulk inserts help
- Optimize sqlalchemy and postgres configs
- Try `network_mode: host`
