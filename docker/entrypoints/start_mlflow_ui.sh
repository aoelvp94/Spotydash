#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail


poetry run mlflow ui \
    --backend-store-uri "$DB_URI" \
    --host "$MLFLOW_UI_HOST" \
    --port "$MLFLOW_UI_PORT" \
    --default-artifact-root "$MLFLOW_ARTIFACT_ROOT"
