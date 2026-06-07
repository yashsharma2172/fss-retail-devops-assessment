#!/bin/bash
# Task 2: Create EKS cluster with namespace murali-ns, RBAC, and deploy k8s-manifests

eksctl create cluster \
  --name fss-cluster \
  --region ap-south-2 \
  --nodegroup-name fss-nodes \
  --node-type t3.small \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed

aws eks update-kubeconfig --name fss-cluster --region ap-south-2

kubectl create namespace murali-ns
kubectl create namespace argocd

kubectl create serviceaccount fss-sa -n murali-ns

kubectl create clusterrolebinding fss-admin \
  --clusterrole=cluster-admin \
  --serviceaccount=murali-ns:fss-sa

# Enable OIDC for EBS CSI Driver (from Notes file)
eksctl utils associate-iam-oidc-provider \
  --region ap-south-2 \
  --cluster fss-cluster \
  --approve

kubectl apply -f k8s-manifests/

kubectl get nodes
kubectl get pods -n murali-ns
kubectl get svc -n murali-ns
