#!/bin/bash

# Exit on error
set -e

# Scale the deployment to 3 replicas
kubectl scale deployment messaging-app-deployment --replicas=3

echo "Deployment scaled to 3 replicas."

# Wait for pods to be ready
kubectl rollout status deployment/messaging-app-deployment

# Get pods
kubectl get pods -o wide

echo "\nRunning load test with wrk..."
# Run wrk against the ClusterIP service (from inside the cluster)
# This assumes you have wrk installed and a way to access the service (e.g., via port-forward)
# Port-forward the service to localhost:8000 in the background
kubectl port-forward service/messaging-app-service 8000:8000 &
PF_PID=$!
sleep 3

# Run wrk for 10 seconds with 12 threads and 400 connections
wrk -t12 -c400 -d10s http://127.0.0.1:8000/

# Kill the port-forward process
kill $PF_PID

echo "\nResource usage (kubectl top pods):"
kubectl top pods 