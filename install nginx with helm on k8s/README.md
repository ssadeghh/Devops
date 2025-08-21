# Kubernetes Cluster with kubeadm + Helm Deployment

This repository documents my practice in setting up a Kubernetes cluster using `kubeadm` and deploying applications with `Helm`.  
The cluster consists of **one master node** and **one worker node**. Finally, I deployed a simple `nginx` application with Helm and practiced `upgrade` and `rollback`.

---

## 📌 Prerequisites
- Two Linux machines (Ubuntu 22.04 recommended) with at least:
  - 2 vCPUs
  - 4 GB RAM
  - 20 GB Disk (important!)
- Installed packages:
  ```bash
  sudo apt update && sudo apt install -y curl apt-transport-https ca-certificates
  ```

- Installed ```kubeadm```, ```kubelet```, and ```kubectl```

## 🚀 Setup Steps
### 1. Initialize the Kubernetes cluster
On the master node:
```bash
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
```

Configure kubectl for your user:
```bash
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
```

Install a CNI plugin (Flannel in this case):
```bash
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml
```

On the worker node, join the cluster using the kubeadm join ... command that was generated on the master.

### 2. Verify nodes
```bash
kubectl get nodes -o wide
```

### 3. Install Helm
On the master node:
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### 4. Deploy an application with Helm
For testing, I used the official nginx Helm chart:
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install my-nginx bitnami/nginx
```

### 5. Manage the application with Helm
- Check installed releases:
```bash
helm list
```

- Upgrade release:
```bash
helm upgrade my-nginx bitnami/nginx --set service.type=NodePort
```

- Rollback to previous revision:
```bash
helm rollback my-nginx 1
```

- Uninstall release:
```bash
helm uninstall my-nginx
```
