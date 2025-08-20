# Kubernetes Cluster Setup with kubeadm (1 Master + 1 Worker)
This guide explains how to install Kubernetes using **kubeadm** on a bare metal environment with one **master** node and one **worker** node.
It also covers how to reset an existing cluster and how to deploy a sample service with **NodePort.**

## 1. Reset an Existing Cluster
If you already have a running cluster and want to start fresh:

```bash
# On all nodes (master + workers)
sudo kubeadm reset -f
sudo systemctl stop kubelet
sudo systemctl stop containerd
sudo rm -rf /etc/cni/net.d /var/lib/cni /var/lib/kubelet /var/lib/etcd /etc/kubernetes

# Restart services
sudo systemctl restart containerd
sudo systemctl restart kubelet
```

## 2. Prerequisites (on all nodes)
Make sure each node has:
- Ubuntu 20.04+ (or any modern Linux distro)
- At least 2 GB RAM (master), 1 GB RAM (worker)
- Swap disabled:
    ```bash
    sudo swapoff -a
    sudo sed -i '/ swap / s/^/#/' /etc/fstab
    ```
- Container runtime installed (e.g., containerd or Docker)
- ```kubeadm```, ```kubelet```, and ```kubectl``` installed
Example installation (containerd + Kubernetes tools):

```bash
sudo apt update && sudo apt install -y apt-transport-https curl

# Add Kubernetes repo
sudo curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list

# Install
sudo apt update
sudo apt install -y kubelet kubeadm kubectl containerd
sudo apt-mark hold kubelet kubeadm kubectl
```

## 3. Initialize the Master Node
On the **master node:**
```bash
sudo kubeadm init --pod-network-cidr=192.168.0.0/16
```
After success, copy the ```kubeadm join ...``` command (you’ll need it for the worker).

Set up ```kubectl``` access for your user:

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

## 4. Install a Pod Network Addon
For networking, install **Calico:**
```bash
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
```

## 5. Join the Worker Node
On the worker node, run the ```kubeadm join``` command given by the master.
It looks like this (your token/hash will differ):
```bash
sudo kubeadm join <MASTER_IP>:6443 --token <TOKEN> --discovery-token-ca-cert-hash sha256:<HASH>
```
Verify from the master:
```bash
kubectl get nodes -o wide
```

## 6. Deploy a Sample NodePort Service

Since this is bare metal, we use NodePort to expose applications.

### Create a Deployment
```bash
kubectl create deployment nginx --image=nginx
```

### Expose it as a NodePort Service
```bash
kubectl expose deployment nginx --port=80 --type=NodePort
```

Check the assigned NodePort:
```bash
kubectl get svc nginx
```

Example output:
```bash
NAME    TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
nginx   NodePort   10.96.23.145   <none>        80:31234/TCP   1m
```

Now you can access Nginx via:
```bash
http://<NODE_IP>:31234
```

Where ```<NODE_IP>``` is the IP of either the master or worker node.