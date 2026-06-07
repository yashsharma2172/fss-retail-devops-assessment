#!/bin/bash
# Task 3: Install ArgoCD, configure access, onboard fss-retail-app, and validate deployment

kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

kubectl create namespace murali-ns

kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'

echo "Waiting for ArgoCD server to be ready..."
kubectl wait --for=condition=available deployment/argocd-server -n argocd --timeout=120s

argocd admin initial-password -n argocd

kubectl apply -f k8s-manifests/argocd-application.yaml

kubectl get applications -n argocd
kubectl get pods -n murali-ns
kubectl get svc -n murali-ns
