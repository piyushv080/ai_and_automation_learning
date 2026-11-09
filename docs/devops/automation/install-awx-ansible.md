# Ansible AWX Setup on Ubuntu 24.04

This guide installs Docker, Minikube, `kubectl`, and Ansible AWX on an
Ubuntu 24.04 host. It then prepares Ubuntu and CentOS client machines
for SSH-based Ansible management.

> **Important:** This is a lab-style deployment using Minikube and
> Docker. For production, use a properly sized Kubernetes cluster,
> persistent storage, TLS, backups, and a supported AWX deployment
> design. Pin and review component versions before deploying.
>
> **Version note:** The AWX Operator version `2.19.0` is retained from
> the source procedure. Check the [AWX Operator
> releases](https://github.com/ansible/awx-operator/releases) and the
> AWX compatibility information before choosing a version.

## 1. Prerequisites

-   Ubuntu Server 24.04
-   A user with `sudo` privileges
-   Internet access
-   Virtualization/container resources appropriate for Minikube
-   Recommended lab allocation: **4 CPUs and 8 GB RAM** for Minikube, in
    addition to the host's own requirements

Update package metadata and install basic tools:

``` bash
sudo apt update
sudo apt install -y ca-certificates curl wget apt-transport-https git make
```

## 2. Install Docker Engine

### 2.1 Add Docker's official GPG key

``` bash
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

### 2.2 Add the Docker APT repository

``` bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 2.3 Install Docker

``` bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin
```

Enable and start Docker:

``` bash
sudo systemctl enable --now docker
sudo systemctl status docker
```

Add your current user to the `docker` group:

``` bash
sudo usermod -aG docker "$USER"
```

Apply the new group membership by logging out and back in, or run:

``` bash
newgrp docker
```

Verify the installation:

``` bash
docker --version
docker run hello-world
```

> **Security note:** Membership in the `docker` group effectively grants
> root-level control of the host. Add only trusted users.

## 3. Install Minikube and kubectl

### 3.1 Update the system and install dependencies

``` bash
sudo apt update
sudo apt install -y curl wget apt-transport-https
```

### 3.2 Download and install Minikube

``` bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
rm -f minikube-linux-amd64
```

Verify:

``` bash
minikube version
```

### 3.3 Install kubectl

Download the latest stable Linux AMD64 client:

``` bash
KUBECTL_VERSION="$(curl -L -s https://dl.k8s.io/release/stable.txt)"
curl -LO "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
rm -f kubectl
```

Verify:

``` bash
kubectl version --client -o yaml
```

## 4. Start Minikube with Docker

Minikube should be run as your regular, non-root user. Confirm Docker
works for that user before starting the cluster.

For a lab host with sufficient resources, configure Minikube with 4 CPUs
and 8 GB RAM:

``` bash
minikube config set cpus 4
minikube config set memory 8192
```

If you already have a Minikube cluster and want to recreate it with the
new settings, delete it first. **This removes the existing Minikube
cluster and its workloads.**

``` bash
minikube delete
```

Start Minikube with the Docker driver and ingress add-on:

``` bash
minikube start --driver=docker --addons=ingress
```

Check the cluster:

``` bash
minikube status
kubectl cluster-info
kubectl get nodes
kubectl get pods -A
docker stats
```

If your host cannot provide 4 CPUs and 8 GB RAM, set lower values that
fit your available resources. AWX may take longer to initialize with
less memory or CPU.

## 5. Install the AWX Operator

Install Git and Make if they are not already present:

``` bash
sudo apt install -y git make
```

Clone the AWX Operator repository and check out the version used in this
guide:

``` bash
git clone https://github.com/ansible/awx-operator.git
cd awx-operator
git checkout 2.19.0
```

Set the Kubernetes namespace and deploy the operator:

``` bash
export NAMESPACE=ansible-awx
make deploy
```

Check the operator pods:

``` bash
kubectl get pods -n ansible-awx
```

## 6. Create and deploy the AWX instance

Copy the demo custom resource file:

``` bash
cp awx-demo.yml awx-ubuntu.yml
```

Edit `awx-ubuntu.yml`:

``` bash
vi awx-ubuntu.yml
```

Use the following manifest (ensure the indentation is preserved):

``` yaml
---
apiVersion: awx.ansible.com/v1beta1
kind: AWX
metadata:
  name: awx-ubuntu
spec:
  service_type: nodeport
```

Create the AWX instance:

``` bash
kubectl create -f awx-ubuntu.yml -n ansible-awx
```

Monitor the pods and services:

``` bash
kubectl get pods -n ansible-awx
kubectl get services -n ansible-awx
```

Follow the operator logs while AWX is being provisioned:

``` bash
kubectl logs -f deployment/awx-operator-controller-manager \
  -c awx-manager -n ansible-awx
```

AWX deployment can take several minutes. Wait until the AWX web and task
components are ready before trying to sign in.

## 7. Access the AWX dashboard

### 7.1 Access from the Ubuntu host

Ask Minikube for the service URL:

``` bash
minikube service awx-ubuntu-service --url -n ansible-awx
```

Open the URL returned by the command in a browser. Do not assume the IP
or port will always be the same.

### 7.2 Access from another machine

Start a port-forward listener on all host interfaces:

``` bash
kubectl port-forward service/awx-ubuntu-service \
  -n ansible-awx --address 0.0.0.0 10445:80
```

Keep this terminal/session running while accessing AWX. Then open:

``` text
http://<UBUNTU_HOST_IP>:10445
```

Only expose this port on a trusted network. For anything beyond a
temporary lab, configure authenticated access and TLS rather than
exposing an unsecured HTTP endpoint.

### 7.3 Retrieve the AWX administrator password

List likely password secrets:

``` bash
kubectl get secrets -n ansible-awx | grep -i password
```

Decode the AWX admin password:

``` bash
kubectl get secret awx-ubuntu-admin-password \
  -o jsonpath='{.data.password}' -n ansible-awx | base64 --decode
echo
```

Sign in with username `admin` and the retrieved password. Change the
password after the first login.

## 8. Prepare the managed client machines

This procedure uses: - Client 1: Ubuntu - Client 2: CentOS

Record each client's IP address and ensure the AWX environment can reach
it over the network. Replace all example usernames and IP addresses with
your actual values.

### 8.1 Ubuntu client

On the Ubuntu client:

``` bash
ip -br address
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
sudo systemctl status ssh
```

Confirm the client is reachable from the AWX host:

``` bash
ping <UBUNTU_CLIENT_IP>
```

If ICMP is blocked, test SSH connectivity instead:

``` bash
ssh <CLIENT_USERNAME>@<UBUNTU_CLIENT_IP>
```

### 8.2 CentOS client

On the CentOS client:

``` bash
ip -br address
sudo systemctl enable --now sshd
sudo systemctl status sshd
```

If the SSH server package is missing, install it using the package
manager for that CentOS release. For CentOS Stream/RHEL-family systems,
this is commonly:

``` bash
sudo dnf install -y openssh-server
sudo systemctl enable --now sshd
```

Check connectivity from the AWX host:

``` bash
ping <CENTOS_CLIENT_IP>
```

If ICMP is blocked, test SSH connectivity instead:

``` bash
ssh <CLIENT_USERNAME>@<CENTOS_CLIENT_IP>
```

### 8.3 Configure sudo access on CentOS (if required)

Use `visudo` to safely edit sudoers:

``` bash
sudo visudo
```

Add a rule for the actual automation account:

``` text
<CLIENT_USERNAME> ALL=(ALL) NOPASSWD: ALL
```

Replace `<CLIENT_USERNAME>` with the real account name. This grants
passwordless sudo and should be used only for a trusted automation
account. A more restrictive sudo rule is preferable where practical.

Test the account:

``` bash
sudo -l
```

## 9. Configure SSH key authentication

### Important distinction for AWX

A successful SSH test from the Ubuntu host proves that the host can
connect to the clients. AWX jobs normally connect from an AWX execution
environment (container/pod), not from an interactive shell on the Ubuntu
host.

For AWX job execution, the recommended approach is to create a **Machine
credential** in the AWX web interface and provide the private key there.
The matching public key must be present in the target user's
`~/.ssh/authorized_keys` file on each client.

### 9.1 Generate a dedicated SSH key pair

You can generate a dedicated key pair on a secure administration
machine:

``` bash
ssh-keygen -t ed25519 -C "awx-automation"
```

Choose a protected location for the key. If AWX must use the key
non-interactively, configure the private key as an AWX Machine
credential and protect access to that credential. Do not commit private
keys to Git or paste them into playbooks.

### 9.2 Install the public key on both clients

For the Ubuntu client:

``` bash
ssh-copy-id <CLIENT_USERNAME>@<UBUNTU_CLIENT_IP>
```

For the CentOS client:

``` bash
ssh-copy-id <CLIENT_USERNAME>@<CENTOS_CLIENT_IP>
```

Enter the target user's password when prompted. The command appends the
public key to the target user's `~/.ssh/authorized_keys`.

On each client, verify the authorized keys file and permissions:

``` bash
ls -la ~/.ssh
cat ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

### 9.3 Test SSH from the key-owning machine

``` bash
ssh <CLIENT_USERNAME>@<UBUNTU_CLIENT_IP> "hostname"
ssh <CLIENT_USERNAME>@<CENTOS_CLIENT_IP> "hostname"
```

Additional checks:

``` bash
ssh <CLIENT_USERNAME>@<UBUNTU_CLIENT_IP> "cat /etc/os-release"
ssh <CLIENT_USERNAME>@<CENTOS_CLIENT_IP> "uname -a"
```

The first connection may ask you to verify the remote host key. Confirm
the fingerprint through a trusted channel before accepting it.

### 9.4 Add the Machine credential in AWX

In the AWX web interface:

1.  Open **Resources → Credentials**.
2.  Select **Add**.
3.  Choose **Machine** as the credential type.
4.  Enter a descriptive name.
5.  Set the username to the managed client account.
6.  Paste the matching private key into the SSH Private Key field.
7.  Supply the key passphrase if one was configured.
8.  Save the credential.

Use this credential when configuring the inventory or job template. If
the two clients use different usernames or keys, create separate
credentials or otherwise configure the inventory and credentials to
match each host.

## 10. Quick verification checklist

Run these checks on the Ubuntu AWX host:

``` bash
docker --version
docker run hello-world
minikube status
kubectl get nodes
kubectl get pods -n ansible-awx
kubectl get services -n ansible-awx
```

In AWX, verify that: - The AWX web interface is reachable. - The admin
login works and the password has been changed. - An inventory contains
both managed hosts. - The correct Machine credential is attached to the
job template. - A test playbook can gather facts from both clients.

Example test playbook:

``` yaml
---
- name: Verify managed hosts
  hosts: all
  gather_facts: true
  tasks:
    - name: Display managed host name
      ansible.builtin.debug:
        msg: "Connected to {{ inventory_hostname }}"
```

## 11. Troubleshooting notes

-   **Docker permission denied:** Log out and back in after adding your
    user to the `docker` group, or run `newgrp docker`.
-   **Minikube fails to start:** Check Docker access, available CPU/RAM,
    and `minikube logs`.
-   **AWX pods remain pending or restart:** Check
    `kubectl describe pod -n ansible-awx <POD_NAME>`,
    `kubectl get events -n ansible-awx --sort-by=.lastTimestamp`, and
    operator logs.
-   **AWX service URL does not work remotely:** The Minikube service
    address may be reachable only from the host. Use the port-forward
    method for a lab, and restrict network access.
-   **SSH authentication fails:** Confirm the username, client IP, SSH
    service, firewall rules, `authorized_keys`, and AWX Machine
    credential.
-   **Privilege escalation fails:** Confirm the account's sudo policy
    and configure the job template's privilege escalation settings as
    appropriate.

## 12. Replace these example values

  Placeholder            Replace with
  ---------------------- -----------------------------------------------
  `<UBUNTU_HOST_IP>`     IP address of the Ubuntu AWX host
  `<UBUNTU_CLIENT_IP>`   IP address of the Ubuntu managed client
  `<CENTOS_CLIENT_IP>`   IP address of the CentOS managed client
  `<CLIENT_USERNAME>`    User account configured on the managed client

------------------------------------------------------------------------

**End of guide**
