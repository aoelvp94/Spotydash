#!/usr/bin/env bash

# Read env vars
parent_dir="$(dirname "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)")"
if [ -f "$parent_dir/.env"  ]; then
    set -a
    # shellcheck disable=SC1091
    source "$parent_dir/.env"
    set +a
else
    echo ".env file is not in project root"
    exit 1
fi


if [[ -n "$2" ]]; then
    artifact="$2"
fi



function pg_connect {
    pgcli -h localhost -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB"
}

# Execution of base container (defined in Dockerfile)
function exec_base {
    docker container exec -ti "$COMPOSE_PROJECT_NAME"_base_1 /bin/bash
}

# Check users list of Airflow
function airflow_ls {
    echo 'Checking users list of Airflow..'
    docker exec -it "$COMPOSE_PROJECT_NAME"_airflow-webserver_1 poetry run airflow users list
}


# Create an admin user in Superset
function superset_create_admin {
    echo 'Creating an admin user..'
    docker exec -it "$COMPOSE_PROJECT_NAME"_superset_1 superset-init
}

# Check users list of Superset
function superset_ls {
    echo 'Checking users list of Superset..'
    docker exec -it "$COMPOSE_PROJECT_NAME"_superset_1 flask fab list-users
}

# Export all dashboards/datasources defined in Superset service. It requires an argument to export that.
function superset_export () {
    case "$artifact" in
        *"dashboards"*)
            echo 'Creating directory for dashboards..'
            mkdir -p "$SUPERSET_DASHBOARDS_PATH"
            echo 'Exporting dashboards..'
            docker exec "$COMPOSE_PROJECT_NAME"_superset_1 superset export_dashboards -f "$SUPERSET_DASHBOARDS_PATH"/dashboard.json
            echo "All the dashboards in Superset were exported."
            ;;
        *"datasources"*)
            echo 'Creating directory for datasources..'
            mkdir -p "$SUPERSET_DATASOURCES_PATH"
            echo 'Exporting datasources..'
            docker exec "$COMPOSE_PROJECT_NAME"_superset_1 superset export_datasources -f "$SUPERSET_DATASOURCES_PATH"/datasources.yaml
            echo "All the datasources in Superset were exported."
            ;;
        *)
            printf "ERROR: Missing command. Available commands: \n  dashboards, datasources \n"
            exit 1
            ;;
    esac
}


case "$1" in
    pg_connect)
        pg_connect
        ;;
    exec_base)
        exec_base
        ;;
    airflow_ls)
        airflow_ls
        ;;
    superset_create_admin)
        superset_create_admin
        ;;
    superset_ls)
        superset_ls
        ;;
    superset_export)
        superset_export
        ;;
    *)
        printf "ERROR: Missing command. Available commands: \n  pg_connect, exec_base, airflow_ls, superset_create_admin, superset_ls, superset_export\n"
        exit 1
        ;;
esac
