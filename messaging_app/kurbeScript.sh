#!/bin/bash

# Exit on error
set -e

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Ensure minikube is installed
if command_exists minikube; then
    echo "Minikube is already installed."
else
    echo "Minikube not found. Installing..."
    # Install minikube (for Linux)
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube
    rm minikube-linux-amd64
    echo "Minikube installed."
fi

# Ensure kubectl is installed
if command_exists kubectl; then
    echo "kubectl is already installed."
else
    echo "kubectl not found. Installing..."
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    rm kubectl
    echo "kubectl installed."
fi

# Start minikube
minikube start

# Verify cluster is running
kubectl cluster-info

# Get available pods
kubectl get pods -A 