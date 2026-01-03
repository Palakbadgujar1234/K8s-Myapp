# Kubernetes Setup Guide for Flask App
## Simple K8s Deployment with Complete Explanations

Complete beginner-friendly guide to deploy your Flask app (app1.py) on Kubernetes with detailed explanations of every concept.

---

## What is Kubernetes? 🤔

**Simple Explanation:**
Kubernetes (K8s) is like a smart manager for your containers. Instead of manually running Docker containers, K8s automatically:
- Runs multiple copies of your app (for reliability)
- Restarts crashed containers automatically
- Distributes traffic across containers
- Scales up/down based on load
- Manages updates without downtime

**Real-world analogy:**
- **Docker:** You manually hire and manage one employee
- **Kubernetes:** You have an HR manager who automatically hires, trains, and manages multiple employees

---

## Why Use Kubernetes for Your App? 🚀

### Without Kubernetes (Current Setup):
```
Your App (Docker)
├─ 1 container running
├─ If it crashes → App is down
├─ Manual restart needed
├─ No load balancing
└─ Manual scaling
```

### With Kubernetes:
```
Your App (Kubernetes)
├─ 2+ containers running (replicas)
├─ If one crashes → Others still work
├─ Auto restart
├─ Auto load balancing
└─ Auto scaling
```

### Benefits for Your Flask App:
1. **High Availability:** If one pod crashes, others keep running
2. **Auto Healing:** K8s automatically restarts failed pods
3. **Load Balancing:** Traffic distributed across multiple pods
4. **Easy Scaling:** Scale from 2 to 10 pods with one command
5. **Rolling Updates:** Update app without downtime
6. **Better Management:** Declarative configuration (YAML files)

---

## Kubernetes Concepts Explained Simply

### 1. Pod 🎯
**What:** Smallest unit in K8s, wraps your Docker container
**Analogy:** A pod is like a wrapper around your container
**Example:** Your Flask app runs inside a pod

### 2. Deployment 📦
**What:** Manages multiple pods (replicas)
**Analogy:** Like a factory that creates and manages workers
**Example:** Creates 2 pods of your Flask app

### 3. Service 🌐
**What:** Exposes your pods to the network
**Analogy:** Like a receptionist who directs visitors to available workers
**Example:** Routes traffic to your Flask app pods

### 4. Replica 👥
**What:** Multiple copies of your app
**Analogy:** Having backup employees
**Example:** 2 replicas = 2 pods running your app

### 5. Node 🖥️
**What:** Physical or virtual machine running K8s
**Analogy:** The office building where workers work
**Example:** Your EC2 instance is a node

---

## Files Created for Kubernetes

### 1. app1.py
```python
# Your Flask application
# Same as app.py but renamed to avoid confusion
# Shows "Running in Kubernetes Pod ☸️"
```

### 2. Dockerfile.k8s
```dockerfile
# Instructions to build Docker image
# Uses app1.py instead of app.py
# Creates image: flask-app:latest
```

### 3. k8s-deployment.yaml
```yaml
# Tells K8s how to run your app
# Creates 2 replicas (2 pods)
# Sets resource limits
# Configures health checks
```

### 4. k8s-service.yaml
```yaml
# Exposes your app to outside world
# Type: NodePort (accessible via node IP)
# Port: 30000 (external access)
```

---

## Step-by-Step Setup

### Prerequisites

1. **Install Minikube (Lightweight K8s for learning)**

```bash
# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Verify installation
minikube version
```

2. **Install kubectl (K8s command-line tool)**

```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verify installation
kubectl version --client
```

---

## Part 1: Start Kubernetes Cluster

### Step 1: Start Minikube

```bash
# Start Minikube (creates a K8s cluster)
minikube start --driver=docker

# This will:
# - Download K8s components
# - Create a virtual cluster
# - Configure kubectl
# Takes 2-5 minutes first time
```

**What happens:**
- Minikube creates a mini Kubernetes cluster on your machine
- Uses Docker as the driver (runs K8s in Docker)
- Sets up networking and storage

### Step 2: Verify Cluster is Running

```bash
# Check cluster status
minikube status

# You should see:
# minikube: Running
# kubelet: Running
# apiserver: Running

# Check nodes
kubectl get nodes

# You should see:
# NAME       STATUS   ROLE           AGE   VERSION
# minikube   Ready    control-plane  1m    v1.28.3
```

---

## Part 2: Build Docker Image

### Step 1: Build Image for Kubernetes

```bash
# Use Minikube's Docker daemon (important!)
eval $(minikube docker-env)

# Build Docker image using Dockerfile.k8s
docker build -f Dockerfile.k8s -t flask-app:latest .

# Verify image is built
docker images | grep flask-app
```

**Why use Minikube's Docker?**
- Minikube runs in its own Docker environment
- Images built in your local Docker won't be visible to Minikube
- `eval $(minikube docker-env)` switches to Minikube's Docker

### Step 2: Verify Image

```bash
# List images in Minikube
minikube ssh docker images | grep flask-app

# You should see:
# flask-app   latest   abc123   2 minutes ago   150MB
```

---

## Part 3: Deploy to Kubernetes

### Step 1: Apply Deployment Configuration

```bash
# Create deployment (creates pods)
kubectl apply -f k8s-deployment.yaml

# You should see:
# deployment.apps/flask-app-deployment created
```

**What happens:**
- K8s reads k8s-deployment.yaml
- Creates 2 pods (replicas: 2)
- Each pod runs your Flask app
- Assigns resources (CPU, memory)
- Sets up health checks

### Step 2: Verify Deployment

```bash
# Check deployment status
kubectl get deployments

# You should see:
# NAME                   READY   UP-TO-DATE   AVAILABLE   AGE
# flask-app-deployment   2/2     2            2           30s

# Check pods
kubectl get pods

# You should see:
# NAME                                    READY   STATUS    RESTARTS   AGE
# flask-app-deployment-abc123-xyz        1/1     Running   0          30s
# flask-app-deployment-def456-uvw        1/1     Running   0          30s
```

**Understanding the output:**
- `READY 2/2`: 2 out of 2 pods are ready
- `STATUS Running`: Pods are running successfully
- `RESTARTS 0`: No crashes (good!)

### Step 3: Check Pod Details

```bash
# Get detailed info about pods
kubectl describe pods

# Check logs from a pod
kubectl logs <pod-name>

# Example:
kubectl logs flask-app-deployment-abc123-xyz

# You should see Flask startup logs:
# * Running on http://0.0.0.0:3000
```

---

## Part 4: Expose App with Service

### Step 1: Create Service

```bash
# Create service (exposes pods)
kubectl apply -f k8s-service.yaml

# You should see:
# service/flask-app-service created
```

**What happens:**
- K8s creates a service
- Service finds pods with label "app: flask-app"
- Exposes them on port 30000
- Load balances traffic across pods

### Step 2: Verify Service

```bash
# Check service
kubectl get services

# You should see:
# NAME                TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
# flask-app-service   NodePort   10.96.123.45    <none>        3000:30000/TCP   30s

# Get service details
kubectl describe service flask-app-service
```

**Understanding the output:**
- `TYPE NodePort`: Accessible via node IP
- `PORT(S) 3000:30000`: Internal port 3000, external port 30000
- `CLUSTER-IP`: Internal IP (used within cluster)

---

## Part 5: Access Your App

### Method 1: Using Minikube Service (Easiest)

```bash
# Open app in browser automatically
minikube service flask-app-service

# This will:
# - Get the service URL
# - Open it in your default browser
```

### Method 2: Get URL Manually

```bash
# Get Minikube IP
minikube ip

# Example output: 192.168.49.2

# Get service port
kubectl get service flask-app-service

# Access app at:
# http://MINIKUBE_IP:30000
# Example: http://192.168.49.2:30000
```

### Method 3: Port Forwarding (For Testing)

```bash
# Forward local port to service
kubectl port-forward service/flask-app-service 3000:3000

# Access at: http://localhost:3000
# Press Ctrl+C to stop
```

---

## Part 6: Verify Everything Works

### Check 1: Pods are Running

```bash
kubectl get pods

# All pods should show:
# STATUS: Running
# READY: 1/1
```

### Check 2: Service is Accessible

```bash
# Get service URL
minikube service flask-app-service --url

# Test with curl
curl $(minikube service flask-app-service --url)

# You should see HTML output
```

### Check 3: Load Balancing Works

```bash
# Watch which pod handles requests
kubectl logs -f <pod-name-1> &
kubectl logs -f <pod-name-2> &

# Make requests
for i in {1..10}; do
  curl $(minikube service flask-app-service --url)
done

# You'll see logs from BOTH pods (load balancing!)
```

---

## Understanding Your Kubernetes Setup

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│  Your Computer / EC2 Instance                           │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Minikube (Kubernetes Cluster)                    │ │
│  │                                                   │ │
│  │  ┌─────────────────────────────────────────────┐ │ │
│  │  │  Service (flask-app-service)                │ │ │
│  │  │  - Type: NodePort                           │ │ │
│  │  │  - Port: 30000                              │ │ │
│  │  │  - Load Balancer                            │ │ │
│  │  └──────────────┬──────────────────────────────┘ │ │
│  │                 │                                 │ │
│  │                 │ (Routes traffic)                │ │
│  │                 │                                 │ │
│  │        ┌────────┴────────┐                       │ │
│  │        │                 │                       │ │
│  │        ▼                 ▼                       │ │
│  │  ┌──────────┐      ┌──────────┐                │ │
│  │  │  Pod 1   │      │  Pod 2   │                │ │
│  │  │          │      │          │                │ │
│  │  │ ┌──────┐ │      │ ┌──────┐ │                │ │
│  │  │ │Flask │ │      │ │Flask │ │                │ │
│  │  │ │App   │ │      │ │App   │ │                │ │
│  │  │ │Port  │ │      │ │Port  │ │                │ │
│  │  │ │3000  │ │      │ │3000  │ │                │ │
│  │  │ └──────┘ │      │ └──────┘ │                │ │
│  │  └──────────┘      └──────────┘                │ │
│  │                                                 │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
└─────────────────────────────────────────────────────────┘
         │
         │ Access via: http://MINIKUBE_IP:30000
         │
         ▼
    Your Browser 🌐
```

### Traffic Flow

```
1. User → http://MINIKUBE_IP:30000
         │
         ▼
2. Service (flask-app-service)
   - Receives request on port 30000
   - Selects a pod (load balancing)
         │
         ▼
3. Pod (flask-app-deployment-xxx)
   - Receives request on port 3000
   - Flask app processes request
         │
         ▼
4. Response ← Flask app
         │
         ▼
5. User ← HTML page with animations
```

---

## Kubernetes Management Commands

### View Resources

```bash
# View all resources
kubectl get all

# View deployments
kubectl get deployments

# View pods
kubectl get pods

# View services
kubectl get services

# View with more details
kubectl get pods -o wide
```

### Describe Resources (Detailed Info)

```bash
# Describe deployment
kubectl describe deployment flask-app-deployment

# Describe pod
kubectl describe pod <pod-name>

# Describe service
kubectl describe service flask-app-service
```

### View Logs

```bash
# View logs from a pod
kubectl logs <pod-name>

# Follow logs (real-time)
kubectl logs -f <pod-name>

# View logs from all pods
kubectl logs -l app=flask-app

# View last 50 lines
kubectl logs <pod-name> --tail=50
```

### Execute Commands in Pod

```bash
# Open shell in pod
kubectl exec -it <pod-name> -- /bin/bash

# Run single command
kubectl exec <pod-name> -- ls -la

# Check Flask app is running
kubectl exec <pod-name> -- curl localhost:3000
```

---

## Scaling Your App

### Scale Up (More Replicas)

```bash
# Scale to 5 replicas
kubectl scale deployment flask-app-deployment --replicas=5

# Verify
kubectl get pods

# You should see 5 pods running
```

**What happens:**
- K8s creates 3 more pods
- Service automatically includes them in load balancing
- More capacity to handle traffic

### Scale Down

```bash
# Scale to 1 replica
kubectl scale deployment flask-app-deployment --replicas=1

# Verify
kubectl get pods

# You should see 1 pod running
```

**What happens:**
- K8s terminates extra pods gracefully
- Keeps 1 pod running
- Saves resources

### Auto-Scaling (Advanced)

```bash
# Auto-scale based on CPU usage
kubectl autoscale deployment flask-app-deployment --min=2 --max=10 --cpu-percent=80

# This will:
# - Keep minimum 2 pods
# - Scale up to 10 pods if CPU > 80%
# - Scale down if CPU < 80%
```

---

## Updating Your App

### Method 1: Update Image

```bash
# Make changes to app1.py
nano app1.py

# Rebuild image
eval $(minikube docker-env)
docker build -f Dockerfile.k8s -t flask-app:v2 .

# Update deployment to use new image
kubectl set image deployment/flask-app-deployment flask-app=flask-app:v2

# Watch rollout
kubectl rollout status deployment/flask-app-deployment
```

**What happens:**
- K8s performs rolling update
- Creates new pods with v2
- Terminates old pods gradually
- Zero downtime!

### Method 2: Edit Deployment

```bash
# Edit deployment directly
kubectl edit deployment flask-app-deployment

# Change image tag or other settings
# Save and exit

# K8s automatically applies changes
```

### Rollback if Something Goes Wrong

```bash
# Rollback to previous version
kubectl rollout undo deployment/flask-app-deployment

# Check rollout history
kubectl rollout history deployment/flask-app-deployment

# Rollback to specific revision
kubectl rollout undo deployment/flask-app-deployment --to-revision=2
```

---

## Testing High Availability

### Test 1: Delete a Pod (Auto-Healing)

```bash
# Get pod name
kubectl get pods

# Delete one pod
kubectl delete pod <pod-name>

# Immediately check pods again
kubectl get pods

# You'll see:
# - Deleted pod is terminating
# - New pod is being created automatically
# - Total pods always = 2 (replicas)
```

**What this proves:**
- K8s automatically maintains desired state
- If a pod crashes/dies, K8s creates a new one
- Your app stays available

### Test 2: Simulate High Load

```bash
# Install Apache Bench (load testing tool)
sudo apt install apache2-utils -y

# Send 1000 requests with 10 concurrent connections
ab -n 1000 -c 10 $(minikube service flask-app-service --url)/

# Watch pods handle the load
kubectl top pods

# You'll see:
# - Load distributed across pods
# - CPU/Memory usage
# - All pods working together
```

### Test 3: Rolling Update (Zero Downtime)

```bash
# Terminal 1: Continuously send requests
while true; do
  curl $(minikube service flask-app-service --url)
  sleep 0.5
done

# Terminal 2: Update deployment
kubectl set image deployment/flask-app-deployment flask-app=flask-app:v2

# Watch Terminal 1:
# - Requests keep succeeding
# - No downtime during update
# - Seamless transition
```

---

## Monitoring and Debugging

### Check Pod Health

```bash
# Check if pods are healthy
kubectl get pods

# Check pod events
kubectl describe pod <pod-name>

# Check pod resource usage
kubectl top pods
```

### Common Issues and Solutions

#### Issue 1: Pod is Pending

```bash
# Check why
kubectl describe pod <pod-name>

# Common causes:
# - Not enough resources
# - Image pull error
# - Node not ready
```

#### Issue 2: Pod is CrashLoopBackOff

```bash
# Check logs
kubectl logs <pod-name>

# Common causes:
# - App error in code
# - Missing dependencies
# - Port already in use
```

#### Issue 3: Can't Access Service

```bash
# Check service
kubectl get service flask-app-service

# Check endpoints
kubectl get endpoints flask-app-service

# Test from inside cluster
kubectl run test-pod --image=busybox -it --rm -- wget -O- http://flask-app-service:3000
```

---

## Cleanup

### Delete Everything

```bash
# Delete service
kubectl delete -f k8s-service.yaml

# Delete deployment
kubectl delete -f k8s-deployment.yaml

# Verify everything is deleted
kubectl get all

# Stop Minikube
minikube stop

# Delete Minikube cluster (if needed)
minikube delete
```

---

## Comparison: Docker vs Kubernetes

### Docker (Current Setup)

```bash
# Start app
docker run -p 3000:3000 flask-app

Pros:
✅ Simple
✅ Fast to start
✅ Easy to understand

Cons:
❌ Single container (no redundancy)
❌ Manual restart if crashes
❌ No load balancing
❌ Manual scaling
❌ Downtime during updates
```

### Kubernetes (New Setup)

```bash
# Start app
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml

Pros:
✅ Multiple replicas (high availability)
✅ Auto-restart if crashes
✅ Built-in load balancing
✅ Easy scaling (one command)
✅ Zero-downtime updates
✅ Self-healing
✅ Better for production

Cons:
❌ More complex
❌ Requires learning
❌ More resources needed
```

---

## When to Use Kubernetes?

### Use Kubernetes When:
- ✅ App needs high availability
- ✅ Expecting high traffic
- ✅ Need auto-scaling
- ✅ Want zero-downtime updates
- ✅ Running multiple services
- ✅ Learning DevOps/Cloud

### Stick with Docker When:
- ✅ Simple app
- ✅ Low traffic
- ✅ Learning basics
- ✅ Development environment
- ✅ Limited resources

---

## Cost Comparison

### Docker Only (Current)
```
Resources:
- 1 container
- 128 MB RAM
- 0.1 CPU

Cost: Minimal
```

### Kubernetes (Minikube)
```
Resources:
- Minikube cluster: 2 GB RAM, 2 CPUs
- 2 pods: 256 MB RAM each, 0.2 CPU each
- Total: ~2.5 GB RAM, 2.5 CPUs

Cost: Higher (but worth it for learning!)
```

### Recommendation for Learning:
- **Start with Docker** (simple, cheap)
- **Learn Kubernetes** (valuable skill)
- **Use Minikube** (free, local)
- **Production:** Use managed K8s (EKS, GKE, AKS)

---

## Next Steps

### 1. Basic Practice
```bash
# Deploy app
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml

# Scale up/down
kubectl scale deployment flask-app-deployment --replicas=3

# Update app
# (make changes to app1.py, rebuild, update)

# Check logs
kubectl logs -f <pod-name>
```

### 2. Advanced Topics (Future Learning)
- ConfigMaps (configuration management)
- Secrets (sensitive data)
- Persistent Volumes (data storage)
- Ingress (advanced routing)
- Helm (package manager)
- Monitoring (Prometheus, Grafana)

### 3. Production Deployment
- AWS EKS (Elastic Kubernetes Service)
- Google GKE (Google Kubernetes Engine)
- Azure AKS (Azure Kubernetes Service)

---

## Quick Reference Commands

```bash
# Cluster Management
minikube start                    # Start cluster
minikube stop                     # Stop cluster
minikube status                   # Check status
minikube dashboard                # Open web UI

# Deployment
kubectl apply -f <file>           # Create/update resource
kubectl delete -f <file>          # Delete resource
kubectl get all                   # View all resources

# Pods
kubectl get pods                  # List pods
kubectl describe pod <name>       # Pod details
kubectl logs <pod-name>           # View logs
kubectl exec -it <pod> -- bash    # Shell into pod

# Scaling
kubectl scale deployment <name> --replicas=3

# Updates
kubectl set image deployment/<name> <container>=<image>
kubectl rollout status deployment/<name>
kubectl rollout undo deployment/<name>

# Service
kubectl get services              # List services
kubectl describe service <name>   # Service details
minikube service <name>           # Open service in browser
```

---

## Summary

### What You've Learned:
1. ✅ What Kubernetes is and why it's useful
2. ✅ How to install Minikube and kubectl
3. ✅ How to deploy Flask app to K8s
4. ✅ How to scale your app
5. ✅ How to update without downtime
6. ✅ How to monitor and debug
7. ✅ Difference between Docker and K8s

### Your App Now Has:
- ✅ 2 replicas (high availability)
- ✅ Auto-restart (self-healing)
- ✅ Load balancing
- ✅ Easy scaling
- ✅ Zero-downtime updates
- ✅ Better management

### Files Created:
- ✅ app1.py (Flask app)
- ✅ Dockerfile.k8s (Docker image)
- ✅ k8s-deployment.yaml (Deployment config)
- ✅ k8s-service.yaml (Service config)

**Congratulations! You now have a production-ready Kubernetes deployment! 🎉☸️**

---

**Made with ❤️ by Bob**

**Welcome to the world of Kubernetes! 🚀**