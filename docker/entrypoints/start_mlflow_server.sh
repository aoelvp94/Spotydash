#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail


poetry run mlflow server \
    --backend-store-uri "$DB_URI" \
    --host "$MLFLOW_SERVER_HOST" \
    --port "$MLFLOW_SERVER_PORT" \
    --default-artifact-root "$MLFLOW_ARTIFACT_ROOT"
