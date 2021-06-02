#!/bin/bash
# Script that allows the user and connection creation for Superset service. Also it would allow us to import dashboards/datasources.
if [ "$SUPERSET_CREATE_USER" = true ]; then
    echo "Creating superset user..."
    superset-init --username "$SUPERSET_USER" --password "$SUPERSET_PASSWORD" --firstname "$SUPERSET_FIRSTNAME" --lastname "$SUPERSET_LASTNAME" --email "$SUPERSET_EMAIL"
    superset set_database_uri -d "$POSTGRES_DB" -u postgresql+psycopg2://"$POSTGRES_USER":"$POSTGRES_PASSWORD"@"$COMPOSE_PROJECT_NAME"_"$POSTGRES_HOST"_1:5432/"$POSTGRES_DB"
fi

if [ "$SUPERSET_IMPORT_DASHBOARD_DATASOURCES" = true ]; then
    DASHBOARDS_FILE="$SUPERSET_DASHBOARDS_PATH/dashboard.json"
    DATASOURCES_FILE="$SUPERSET_DATASOURCES_PATH/datasources.yaml"

    echo 'Checking if datasources file exists..'
    if [ -f "$DATASOURCES_FILE" ]; then
        echo "Importing datasources in '$DATASOURCES_FILE'.."
        superset import_datasources -p "$DATASOURCES_FILE"
        echo "All the datasources in Superset were imported."
    else
        echo "You don't have the datasources file, please export the datasources defined in Superset service."
    fi

    echo 'Checking if dashboards file exists..'
    if [ -f "$DASHBOARDS_FILE" ]; then
        echo "Importing dashboards in '$DASHBOARDS_FILE'.."
        superset import_dashboards -p "$DASHBOARDS_FILE"
        echo "All the dashboards in Superset were imported."
    else
        echo "You don't have the dashboards file, please export the dashboards defined in Superset service."
    fi
fi

gunicorn --bind 0.0.0.0:"$SUPERSET_PORT" -w 10 --timeout 120 "superset.app:create_app()"
