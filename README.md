# ChatbotBackend

```shell
    python -m uvicorn main:app --host '0.0.0.0' --port 8000 --reload
    gunicorn main:app -b 0.0.0.0:8000  -w 4 -k uvicorn.workers.UvicornH11Worker --daemon
```
