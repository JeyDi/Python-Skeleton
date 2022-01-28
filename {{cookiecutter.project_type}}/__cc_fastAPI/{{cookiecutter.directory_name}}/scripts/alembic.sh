export PYTHONPATH=$(pwd)
#create the revision for the changed (first revision)
alembic revision --autogenerate -m "first init"
#commit the migration
alembic upgrade head