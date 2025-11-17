#!/usr/bin/env bash
set -euo pipefail

# === БАЗОВІ ЗМІННІ (частину з них будемо передавати з GitHub Actions) ===
AWS_REGION=${AWS_REGION:-us-east-1}
AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID:?AWS_ACCOUNT_ID is required}
ECR_REPO_NAME=${ECR_REPO_NAME:-articlehub-new}
CLUSTER=${ECS_CLUSTER:-articlehub-new-cluster}
SERVICE=${ECS_SERVICE:-articlehub-new-svc}
TASK_FAMILY=${ECS_TASK_FAMILY:-articlehub-new-task}

echo "Deploying to ECS cluster=${CLUSTER}, service=${SERVICE}, repo=${ECR_REPO_NAME}"

# === 1) ЛОГІН В ECR ===
aws ecr get-login-password --region "${AWS_REGION}" \
  | docker login --username AWS --password-stdin "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

# === 2) BUILD + PUSH ARM64 ОБРАЗУ ===
IMAGE_TAG="${GITHUB_SHA:-local}-arm64"
IMAGE_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}"

echo "Building image: ${IMAGE_URI}"

docker buildx create --use 2>/dev/null || true
docker buildx build --platform linux/arm64 \
  -t "${IMAGE_URI}" \
  --push .

# === 3) ОНОВИТИ task definition З НОВИМ IMAGE_URI ===
#   Припускаємо, що в task-def-articlehub.json вже є правильна структура,
#   тільки треба поміняти поле image в containerDefinitions.
TMP_TD=task-def-articlehub.rendered.json

jq --arg IMAGE "${IMAGE_URI}" '
  .containerDefinitions |=
    (map(if .name == "api" or .name == "worker" or .name == "beat"
         then .image = $IMAGE
         else .
         end))
' task-def-articlehub.json > "${TMP_TD}"

# === 4) РЕЄСТРАЦІЯ НОВОЇ РЕВІЗІЇ TASK DEFINITION ===
TD_ARN=$(aws ecs register-task-definition \
  --cli-input-json "file://${TMP_TD}" \
  --query 'taskDefinition.taskDefinitionArn' \
  --output text \
  --region "${AWS_REGION}")

echo "Registered task definition: ${TD_ARN}"

# === 5) ОНОВИТИ СЕРВІС (force new deployment) ===
aws ecs update-service \
  --cluster "${CLUSTER}" \
  --service "${SERVICE}" \
  --task-definition "${TD_ARN}" \
  --force-new-deployment \
  --region "${AWS_REGION}"

echo "Deployment triggered successfully."
