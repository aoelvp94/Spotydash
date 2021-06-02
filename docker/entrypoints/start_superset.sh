#!/bin/bash
# Script that allows the user and connection creation for Superset service. Also it would allow us to import dashboards/datasources.
if [ "$SUPERSET_CREATE_USER" = true ]; then
    echo "Creating superset user..."
    superset-init --username "$SUPERSET_USER" --password "$SUPERSET_PASSWORD" --firstname "$SUPERSET_FIRSTNAME" --lastname "$SUPERSET_LASTNAME" --email "$SUPERSET_EMAIL"
    superset set_database_uri -d "$POSTGRES_DB" -u postgresql+psycopg2://"$POSTGRES_USER":"$POSTGRES_PASSWORD"@"$POSTGRES_HOST":"$POSTGRES_PORT"/"$POSTGRES_DB"
fi

gunicorn --bind 0.0.0.0:"$SUPERSET_PORT" -w 10 --timeout 120 "superset.app:create_app()"
