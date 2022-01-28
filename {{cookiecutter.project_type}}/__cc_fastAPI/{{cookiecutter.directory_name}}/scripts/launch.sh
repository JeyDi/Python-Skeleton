#Launch the application using gunicorn backend
#gunicorn -w 4 -b 0.0.0.0:${APP_ENDPOINT_PORT:-8045} app.main:app
gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:${APP_ENDPOINT_PORT:-8000} --preload --log-level ${VERBOSITY:-INFO} app.main:app
#python ./app/main.py