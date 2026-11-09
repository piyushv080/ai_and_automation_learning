# Kubernetes Guide

Kubernetes is an open-source orchestration platform for deploying and managing containerized applications across a cluster of machines. It provides scheduling, service discovery, scaling, rolling updates, rollback, and self-healing capabilities.

## 1. Why Kubernetes

Kubernetes grew out of Google's internal Borg and Omega systems and was open-sourced in 2014. It is now maintained by the Cloud Native Computing Foundation (CNCF).

Container orchestration covers:

- Scheduling and placing containers on nodes.
- Provisioning and deploying containerized applications.
- High availability and automatic restart or replacement.
- Application configuration inside containers.
- Scaling workloads across the available infrastructure.
- Allocating CPU, memory, and other resources.
- Load balancing, traffic routing, and service discovery.
- Health monitoring and self-healing.
- Securing communication between workloads.

Common container orchestrators and managed platforms include Kubernetes, Docker Swarm, Apache Mesos, Nomad, Cloud Foundry, and the managed Kubernetes services offered by cloud providers.

## 2. Architecture

A Kubernetes cluster has a control plane and one or more worker nodes.

```text
                         +---------------------------+
                         |       Control plane       |
                         |                           |
  kubectl / API clients  |  kube-apiserver           |
  ---------------------->|  controller-manager       |
                         |  scheduler                |
                         |  etcd                     |
                         +------------+--------------+
                                      |
                    +-----------------+-----------------+
                    |                                   |
             +------+-------+                    +------+-------+
             | Worker node  |                    | Worker node  |
             |              |                    |              |
             | kubelet      |                    | kubelet      |
             | kube-proxy   |                    | kube-proxy   |
             | runtime      |                    | runtime      |
             | Pods         |                    | Pods         |
             +--------------+                    +--------------+
```

Multiple control-plane nodes can be used for high availability. Production clusters should use an odd number of etcd members and a supported topology.

### Control-plane components

| Component | Responsibility |
| --- | --- |
| `kube-apiserver` | Front end of the control plane. Receives `kubectl` and API requests, validates them, and coordinates cluster operations. |
| `etcd` | Consistent key/value store for cluster state, objects, and configuration. Back it up regularly. |
| `kube-scheduler` | Chooses a node for a new Pod based on resource requests, constraints, taints, tolerations, affinity, and other policies. |
| `kube-controller-manager` | Runs control loops that reconcile actual state with desired state. Includes controllers for nodes, ReplicaSets, endpoints, service accounts, and more. |
| `cloud-controller-manager` | Integrates with a cloud provider for load balancers, routes, and node lifecycle where applicable. |

Older material sometimes lists a "Replication Controller" or "Node Controller" as separate master components. They are controllers managed by `kube-controller-manager`.

### Worker-node components

| Component | Responsibility |
| --- | --- |
| `kubelet` | Agent on each node. Starts and monitors Pods and containers and reports node status to the API server. |
| Container runtime | Runs containers. Common runtimes include `containerd` and `CRI-O`; Docker Engine is no longer the default runtime for modern Kubernetes. |
| `kube-proxy` | Maintains network rules so traffic can reach Services. Some CNI and eBPF implementations replace or supplement parts of its role. |
| CNI plugin | Provides Pod networking. Examples include Calico, Cilium, Flannel, and Antrea. |

### Add-ons

- **CoreDNS** provides cluster DNS and service discovery.
- **Ingress controller** implements HTTP and HTTPS routing rules.
- **Metrics Server** supplies resource metrics for autoscaling and `kubectl top`.
- **Dashboard** is an optional web UI.
- **CNI, CSI, and observability agents** provide networking, storage, and monitoring.

## 3. kubectl basics

`kubectl` communicates with the API server. It reads the kubeconfig from `$HOME/.kube/config` by default. Use `KUBECONFIG` or `--kubeconfig` to select another file.

```bash
kubectl [command] [TYPE] [NAME] [flags]
```

- `command`: `get`, `describe`, `create`, `apply`, `delete`, `logs`, `exec`, and others.
- `TYPE`: resource type, such as `pod`, `pods`, `deployment`, or an abbreviation such as `po`.
- `NAME`: resource name. Names are case-sensitive.
- `flags`: optional settings such as `-n <namespace>` or `-o yaml`.

Resource types are case-insensitive and accept singular, plural, or abbreviated forms:

```bash
kubectl get pod example-pod
kubectl get pods example-pod
kubectl get po example-pod
```

Use `kubectl api-resources` to list available resource types and their API groups.

### Useful kubectl commands

```bash
kubectl version --client
kubectl cluster-info
kubectl config view
kubectl get nodes
kubectl get nodes --show-labels
kubectl get pods --all-namespaces
kubectl get pods -o wide
kubectl get pod example-pod -o yaml
kubectl describe pod example-pod
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl logs example-pod
kubectl logs -f example-pod
kubectl exec -it example-pod -- /bin/sh
kubectl apply -f manifest.yaml
kubectl delete -f manifest.yaml
```

Enable shell completion:

```bash
source <(kubectl completion bash)
echo "source <(kubectl completion bash)" >> ~/.bashrc
```

## 4. Core Kubernetes objects

### Pod

A Pod is the smallest deployable unit. It contains one or more containers that share a network namespace and can share volumes.

- Single-container Pods are the most common use case.
- Multi-container Pods are appropriate for tightly coupled helpers such as sidecars, adapters, or init containers.
- Every Pod receives an IP address and can have CPU and memory requests and limits.
- Containers in different Pods communicate using Pod IPs or Services, not container IPs.

Do not manage bare Pods for long-running applications. Use a Deployment, StatefulSet, or DaemonSet so the workload is rescheduled and scaled correctly.

### ReplicaSet

A ReplicaSet ensures that a specified number of Pod replicas are running. It uses a Pod template and selectors. In practice, manage ReplicaSets through a Deployment rather than directly.

### Deployment

A Deployment provides declarative updates for Pods and ReplicaSets. It supports:

- Creating and updating ReplicaSets.
- Scaling the application.
- Rolling updates and rollback.
- Pausing and resuming a rollout.
- Declarative image and configuration changes.

### Service

Pods are ephemeral, so their IP addresses can change. A Service provides a stable virtual IP and DNS name for a logical set of Pods selected by labels.

| Service type | Purpose |
| --- | --- |
| `ClusterIP` | Default. Exposes the Service inside the cluster only. |
| `NodePort` | Opens a port on every node and forwards traffic to the Service. Default range is usually `30000-32767`. |
| `LoadBalancer` | Requests a cloud or platform load balancer with an external address. |
| `ExternalName` | Maps a Service name to an external DNS name with a CNAME. |

### Namespace

A Namespace is a virtual cluster inside a physical cluster. Use namespaces to separate teams, environments, or applications.

- Namespaced resources must have unique names inside a namespace.
- RBAC and resource quotas can be scoped to namespaces.
- Network access across namespaces is governed by network policies, not namespace membership alone.
- Kubernetes starts with `default`, `kube-system`, and `kube-public`.

### ConfigMap

A ConfigMap stores non-sensitive configuration such as files, environment variables, command-line arguments, or ports. It separates configuration from container images.

### Secret

A Secret stores sensitive values such as passwords, tokens, SSH keys, or certificates. Secrets are base64-encoded in the API by default, which is not encryption. Use encryption at rest, RBAC, least privilege, and an external secret manager where appropriate.

### Volume, PersistentVolume, and PersistentVolumeClaim

A Volume is storage mounted into a Pod. Its lifetime can be tied to the Pod or to a separate persistent resource.

- `emptyDir` is temporary and disappears with the Pod.
- `hostPath` uses a path on the node and is not shared across nodes.
- `PersistentVolume` (PV) is cluster storage provisioned statically or dynamically.
- `PersistentVolumeClaim` (PVC) is a request for storage from a PV or StorageClass.
- Pods reference PVCs through volumes and volume mounts.

### DaemonSet

A DaemonSet ensures that a Pod runs on all or selected nodes. Common uses include log collection, node monitoring, and storage daemons.

### Labels, selectors, and annotations

- **Labels** are key/value pairs used to identify and select objects.
- **Selectors** filter objects by labels.
- **Annotations** store non-identifying metadata for tools and integrations.

```bash
kubectl label pod example-pod owner=platform-team
kubectl get pods --show-labels
kubectl get pods -l owner=platform-team
kubectl get pods -l 'environment in (test,production)'
```

### Affinity, anti-affinity, taints, and tolerations

- **nodeSelector** is a simple hard constraint based on node labels.
- **Node affinity** supports richer rules and soft preferences.
- **Pod affinity/anti-affinity** controls co-location with other Pods.
- **Taints** repel Pods from a node.
- **Tolerations** allow a Pod to run on a node with a matching taint.

```bash
kubectl taint nodes node01 dedicated=platform:NoSchedule
kubectl taint nodes node01 dedicated=platform:NoSchedule-
```

## 5. YAML and API versions

Kubernetes manifests are usually written in YAML. Every object requires four top-level fields:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: example-pod
spec:
  containers:
    - name: web
      image: nginx:stable
```

| Field | Meaning |
| --- | --- |
| `apiVersion` | API group and version used to create the object. |
| `kind` | Object type, such as Pod, Deployment, or Service. |
| `metadata` | Identity data such as name, namespace, labels, and annotations. |
| `spec` | Desired state of the object. |

Use `kubectl api-resources` and `kubectl explain <kind>` to confirm the correct API version and fields for your cluster.

### Common current API versions

| Kind | API version |
| --- | --- |
| Pod, Service, ConfigMap, Secret, Namespace, ServiceAccount, PersistentVolume, PersistentVolumeClaim | `v1` |
| Deployment, ReplicaSet, StatefulSet, DaemonSet | `apps/v1` |
| Job, CronJob | `batch/v1` |
| HorizontalPodAutoscaler | `autoscaling/v2` |
| PodDisruptionBudget | `policy/v1` |
| Ingress, NetworkPolicy | `networking.k8s.io/v1` |
| Role, RoleBinding, ClusterRole, ClusterRoleBinding | `rbac.authorization.k8s.io/v1` |
| CertificateSigningRequest | `certificates.k8s.io/v1` |

Older training material may use `extensions/v1beta1`, `apps/v1beta1`, or `networking.k8s.io/v1beta1`. Those versions are removed or deprecated in current Kubernetes releases. PodSecurityPolicy was removed in Kubernetes 1.25 and replaced by Pod Security Admission.

## 6. Pod and Deployment examples

### Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: website
  labels:
    app: website
spec:
  containers:
    - name: web-server
      image: nginx:stable
      resources:
        requests:
          memory: "64Mi"
          cpu: "100m"
        limits:
          memory: "128Mi"
          cpu: "500m"
      ports:
        - containerPort: 80
```

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: website
  labels:
    app: website
spec:
  replicas: 3
  selector:
    matchLabels:
      app: website
  template:
    metadata:
      labels:
        app: website
    spec:
      containers:
        - name: web-server
          image: nginx:stable
          ports:
            - containerPort: 80
          resources:
            requests:
              memory: "64Mi"
              cpu: "100m"
            limits:
              memory: "128Mi"
              cpu: "500m"
```

Apply and inspect the Deployment:

```bash
kubectl apply -f deployment.yaml
kubectl get deployments
kubectl rollout status deployment/website
kubectl describe deployment website
kubectl get replicasets
kubectl get pods -l app=website
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: website
spec:
  type: NodePort
  selector:
    app: website
  ports:
    - name: http
      port: 80
      targetPort: 80
      nodePort: 30080
      protocol: TCP
```

The Service selector must match the Pod labels. Access a NodePort Service with `<node-ip>:<node-port>`.

For an internal-only Service:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: website-internal
spec:
  type: ClusterIP
  selector:
    app: website
  ports:
    - name: http
      port: 80
      targetPort: 80
```

## 7. Deployments, scaling, and rollbacks

```bash
kubectl create deployment website --image=nginx:stable
kubectl scale deployment/website --replicas=5
kubectl set image deployment/website nginx=nginx:1.27
kubectl rollout status deployment/website
kubectl rollout history deployment/website
kubectl rollout undo deployment/website --to-revision=1
```

Deployment strategies:

- **Recreate** stops old Pods before starting new ones. This creates downtime.
- **RollingUpdate** gradually replaces Pods. It is the default and is suitable for highly available applications.

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

Do not modify ReplicaSets managed by a Deployment directly. Change the Deployment instead.

## 8. Namespaces and resource quotas

```bash
kubectl create namespace application
kubectl get namespaces
kubectl describe namespace application
kubectl get pods -n application
kubectl delete namespace application
```

A ResourceQuota limits the total resources a namespace can consume:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: application-quota
  namespace: application
spec:
  hard:
    pods: "10"
    requests.cpu: "4"
    requests.memory: 5Gi
    limits.cpu: "10"
    limits.memory: 10Gi
```

LimitRange can set default requests and limits for containers in a namespace.

## 9. ConfigMaps and Secrets

### ConfigMap

```bash
kubectl create configmap application-config --from-file=config.properties
kubectl get configmap application-config -o yaml
```

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: application-config
data:
  LOG_LEVEL: info
  APP_MODE: production
```

Use a ConfigMap as environment variables:

```yaml
spec:
  containers:
    - name: application
      image: example/application:1.0
      envFrom:
        - configMapRef:
            name: application-config
```

### Secret

Create a Secret from literals without putting the value in shell history where possible:

```bash
kubectl create secret generic application-secret \
  --from-literal=username=automation-user \
  --from-literal=password='<password>'
```

Use a Secret as an environment variable:

```yaml
spec:
  containers:
    - name: application
      image: example/application:1.0
      env:
        - name: APP_PASSWORD
          valueFrom:
            secretKeyRef:
              name: application-secret
              key: password
```

Secrets are not automatically secure. Restrict `get` and `list` access with RBAC, enable encryption at rest for etcd, avoid committing Secret manifests, and prefer an external secret manager for production.

## 10. Networking

Kubernetes networking has four common traffic paths:

1. **Container to container inside a Pod:** containers share the Pod network namespace and communicate over `localhost` on different ports.
2. **Pod to Pod:** each Pod has its own IP. Intra-node traffic stays local; inter-node traffic is routed by the CNI plugin.
3. **Pod to Service:** a Service provides a stable virtual IP and DNS name for selected Pods.
4. **External to Service:** traffic enters through NodePort, LoadBalancer, or an Ingress controller.

### Service type comparison

| Type | External access | Typical use |
| --- | --- | --- |
| ClusterIP | No | Internal service-to-service communication |
| NodePort | Yes, through a node IP and port | Labs, demos, temporary access |
| LoadBalancer | Yes, through a cloud or platform load balancer | Direct external exposure |
| Ingress | Yes, through an ingress controller | HTTP/HTTPS routing for multiple services |

`kubectl proxy` can access ClusterIP Services locally for debugging, but it must not be used to expose production services to the internet.

### Ingress

An Ingress is not a Service type. It defines HTTP/HTTPS routing rules and requires an ingress controller.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: website
  namespace: application
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: website.example.test
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: website
                port:
                  number: 80
```

Install and configure an ingress controller such as ingress-nginx before applying the Ingress resource. Use cert-manager or another approved process for TLS certificates.

### Network policies

A NetworkPolicy controls which Pods and endpoints can communicate. It requires a CNI plugin that supports policy enforcement.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-web-from-ingress
  namespace: application
spec:
  podSelector:
    matchLabels:
      app: website
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: ingress-nginx
      ports:
        - protocol: TCP
          port: 80
```

Start with a default-deny policy, then allow only the required traffic paths.

## 11. Storage

Kubernetes supports many volume types:

| Category | Examples |
| --- | --- |
| Local node | `emptyDir`, `hostPath`, local volumes |
| File sharing | NFS |
| Block storage | Fibre Channel, iSCSI |
| Cloud provider | EBS, Azure Disk, GCE Persistent Disk, vSphere |
| Distributed file systems | CephFS, GlusterFS |
| Special purpose | Secret, ConfigMap, CSI volumes |
| Persistent | PersistentVolume, PersistentVolumeClaim |

### PersistentVolume and PersistentVolumeClaim

A PV represents storage in the cluster. A PVC requests storage from a PV or from a StorageClass.

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: application-pv
spec:
  capacity:
    storage: 20Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: application-storage
  nfs:
    path: /srv/nfs/application
    server: 192.0.2.20
```

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: application-pvc
  namespace: application
spec:
  storageClassName: application-storage
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

Use the PVC in a Pod:

```yaml
spec:
  volumes:
    - name: application-data
      persistentVolumeClaim:
        claimName: application-pvc
  containers:
    - name: application
      image: example/application:1.0
      volumeMounts:
        - name: application-data
          mountPath: /var/lib/application
```

Access modes:

- `ReadWriteOnce`: mounted read-write by a single node.
- `ReadOnlyMany`: mounted read-only by many nodes.
- `ReadWriteMany`: mounted read-write by many nodes, if the storage supports it.

Reclaim policies in current Kubernetes are mainly `Retain` and `Delete`. The old `Recycle` policy is deprecated and should not be used in new designs.

Use a CSI driver and a StorageClass for dynamic provisioning in production. Verify the access mode and filesystem support before designing multi-node workloads.

## 12. Scheduling

### nodeSelector

```bash
kubectl label nodes node01 workload=web
```

```yaml
spec:
  nodeSelector:
    workload: web
```

### Affinity

```yaml
spec:
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 1
          preference:
            matchExpressions:
              - key: workload
                operator: In
                values:
                  - web
```

Use required affinity only when the Pod cannot run without the constraint. Soft preferences keep scheduling flexible.

### Taints and tolerations

Taints keep Pods away from nodes. Tolerations allow specific Pods to schedule onto tainted nodes.

```bash
kubectl taint nodes node02 dedicated=platform:NoSchedule
```

```yaml
spec:
  tolerations:
    - key: dedicated
      operator: Equal
      value: platform
      effect: NoSchedule
```

Use taints for dedicated nodes or nodes with special hardware.

## 13. Security

### RBAC

Role-Based Access Control connects subjects, resources, and verbs:

- **Subjects:** users, groups, or ServiceAccounts.
- **Resources:** Pods, Deployments, Services, Secrets, and other API objects.
- **Verbs:** `get`, `list`, `watch`, `create`, `update`, `patch`, `delete`, and others.

| Object | Scope |
| --- | --- |
| Role | Namespace-scoped set of permissions |
| ClusterRole | Cluster-wide permissions |
| RoleBinding | Grants a Role or ClusterRole inside a namespace |
| ClusterRoleBinding | Grants a ClusterRole across the cluster |

Example Role and RoleBinding:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployment-manager
  namespace: application
rules:
  - apiGroups: ["", "apps"]
    resources: ["deployments", "replicasets", "pods"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: deployment-manager
  namespace: application
subjects:
  - kind: User
    name: automation-user
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: deployment-manager
  apiGroup: rbac.authorization.k8s.io
```

Users and ServiceAccounts differ:

- Users are global identities managed outside the cluster, often through certificates, OIDC, or an identity provider.
- ServiceAccounts are namespaced identities used by workloads running inside Pods.

Avoid granting broad wildcard permissions. Review RoleBindings and ServiceAccount token usage regularly.

### Security context

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: application
      image: example/application:1.0
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop:
            - ALL
```

Use Pod Security Admission or a policy engine to enforce baseline security controls at the namespace level.

## 14. Installing a learning cluster with kubeadm

`kubeadm` is a bootstrap tool for creating conformant Kubernetes clusters. It prepares the control plane and joins nodes, but it does not provision machines or install every add-on.

> The original training notes used CentOS 7, Docker, old firewall ports, and legacy API versions. Those steps are not recommended for new clusters. Use a current supported Linux distribution, `containerd` or `CRI-O`, and the current kubeadm documentation.

### Common prerequisites

- A supported Linux distribution and Kubernetes version.
- Unique hostnames, correct DNS, and time synchronization.
- A container runtime installed and configured on every node.
- Swap disabled or explicitly supported through the kubelet swap configuration.
- Required kernel modules and networking settings.
- Firewall rules for the API server, etcd, kubelet, and NodePort ranges.
- A CNI plugin installed after `kubeadm init`.

### High-level workflow

```bash
# On every node: install and configure the container runtime,
# kubelet, kubeadm, and kubectl from the official repositories.

# On the first control-plane node
sudo kubeadm init --pod-network-cidr=10.244.0.0/16

# Configure kubectl for the current user
mkdir -p "$HOME/.kube"
sudo cp /etc/kubernetes/admin.conf "$HOME/.kube/config"
sudo chown "$(id -u):$(id -g)" "$HOME/.kube/config"

# Install a CNI plugin
kubectl apply -f <cni-manifest-url>

# Check the cluster
kubectl get nodes
kubectl get pods --all-namespaces
```

Join a worker node using the command printed by `kubeadm init`. Treat the join token and CA certificate hash as sensitive:

```bash
sudo kubeadm join <control-plane-endpoint>:6443 \
  --token <join-token> \
  --discovery-token-ca-cert-hash sha256:<certificate-hash>
```

If the token expires, generate a new one:

```bash
kubeadm token create --print-join-command
```

Verify that all control-plane and CNI Pods reach a healthy state before deploying applications.

### Legacy lab notes

The older lab used three CentOS nodes with a control plane and two workers, host entries, firewall ports, Docker, and `kubeadm init`. Reproducing it requires updating every step for the current Kubernetes release. In particular:

- Use `containerd` or `CRI-O` instead of the legacy Docker Engine setup where possible.
- Use current control-plane ports such as `6443`, `2379-2380`, `10250`, `10257`, and `10259`; do not copy obsolete insecure ports.
- Keep SELinux enforcing where supported rather than disabling it globally.
- Do not store real join tokens or CA hashes in notes or source control.
- Pin package versions so nodes do not drift during a build.

## 15. Logging, monitoring, and troubleshooting

Useful tools and signals:

- **Prometheus** for metrics collection and alerting.
- **Grafana** for dashboards.
- **Metrics Server** for `kubectl top` and resource autoscaling.
- **Loki, Elasticsearch, or another log backend** for centralized logs.
- **Events** for scheduling, image pull, mounting, and health failures.

Troubleshooting commands:

```bash
kubectl get nodes -o wide
kubectl get pods --all-namespaces -o wide
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous
kubectl get events -n <namespace> --sort-by=.metadata.creationTimestamp
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh
kubectl top nodes
kubectl top pods -n <namespace>
kubectl get endpoints -n <namespace>
kubectl get svc -n <namespace>
```

When debugging, check the Pod phase, events, container restarts, resource limits, image pull status, Service selectors, endpoints, network policies, and node conditions.

## 16. Quick reference

```bash
kubectl get pods
kubectl get pods --all-namespaces
kubectl get pod <pod> -o wide
kubectl get pod <pod> -o yaml
kubectl describe pod <pod>
kubectl logs <pod>
kubectl exec -it <pod> -- /bin/sh

kubectl create deployment <name> --image=<image>
kubectl scale deployment/<name> --replicas=<count>
kubectl set image deployment/<name> <container>=<image>
kubectl rollout status deployment/<name>
kubectl rollout history deployment/<name>
kubectl rollout undo deployment/<name> --to-revision=<revision>

kubectl expose deployment <name> --port=<port> --type=NodePort
kubectl get services
kubectl get ingress
kubectl get pv
kubectl get pvc
kubectl get secrets
kubectl get configmaps
kubectl get daemonsets

kubectl create namespace <namespace>
kubectl get namespaces
kubectl describe namespace <namespace>
kubectl delete namespace <namespace>
```

## 17. Further reading

- [Kubernetes documentation](https://kubernetes.io/docs/)
- [Kubernetes tutorials](https://kubernetes.io/docs/tutorials/)
- [kubectl reference](https://kubernetes.io/docs/reference/kubectl/)
- [kubeadm installation](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/)
- [Kubernetes API reference](https://kubernetes.io/docs/reference/kubernetes-api/)
- [Kubernetes by Example](https://kubernetesbyexample.com/)
- [CNCF landscape](https://landscape.cncf.io/)
