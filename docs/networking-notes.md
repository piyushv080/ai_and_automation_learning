# Networking Notes

Practical networking fundamentals for infrastructure support and automation. Examples are for learning; command availability and output vary by operating system and distribution.

## Contents

- [How a web request reaches a server](#how-a-web-request-reaches-a-server)
- [Network layers and packet flow](#network-layers-and-packet-flow)
- [Addressing and local network services](#addressing-and-local-network-services)
- [TCP, UDP, and common protocols](#tcp-udp-and-common-protocols)
- [Routing, VLANs, and firewalls](#routing-vlans-and-firewalls)
- [DNS and HTTP](#dns-and-http)
- [Proxies, load balancers, and CDNs](#proxies-load-balancers-and-cdns)
- [Troubleshooting workflow](#troubleshooting-workflow)

## How a web request reaches a server

When a user enters a web address, the browser and operating system perform a sequence of lookups and connections. Caches and connection reuse may skip some steps.

1. The client needs network configuration, often provided by DHCP: an IP address, prefix or subnet mask, default gateway, and DNS resolver.
2. The browser resolves the hostname to an address. A recursive DNS resolver can consult root, top-level-domain, and authoritative DNS servers when the answer is not cached.
3. The client chooses a route and connects to the server IP and port. TCP is used for HTTP/1.1 and HTTP/2; HTTP/3 uses QUIC over UDP.
4. For HTTPS, the client and server negotiate TLS and validate the server certificate.
5. The browser sends an HTTP request. A server, reverse proxy, or load balancer routes it to an application.
6. The server sends an HTTP response with a status code, headers, and usually a body. The browser parses the response and may request more files such as images, scripts, and stylesheets.

### HTTP status code families

| Range | Meaning | Examples |
| --- | --- | --- |
| 1xx | Informational | `100 Continue` |
| 2xx | Success | `200 OK`, `201 Created`, `204 No Content` |
| 3xx | Redirection | `301 Moved Permanently`, `302 Found`, `304 Not Modified` |
| 4xx | Client-side/request error | `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found` |
| 5xx | Server-side error | `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable` |

## Network layers and packet flow

Layer models help locate where a problem occurs. The OSI model has seven layers; the practical TCP/IP model groups them into fewer layers. Data is encapsulated as it travels down the sender's stack and decapsulated by the receiver.

| OSI layer | Examples | What it handles |
| --- | --- | --- |
| Application | HTTP, DNS, SSH, SMTP | Application requests and responses |
| Presentation | TLS, data formats | Data representation, encryption, encoding |
| Session | Session management | Dialogs between applications |
| Transport | TCP, UDP | Ports and end-to-end transport |
| Network | IPv4, IPv6, ICMP | IP addressing and routing between networks |
| Data link | Ethernet, Wi-Fi, ARP | Local link delivery using frames and link-layer addresses |
| Physical | Copper, fiber, radio | Signals and bits over a medium |

Routers forward IP packets between networks using routing tables. On a local Ethernet network, a host uses ARP for IPv4 or Neighbor Discovery for IPv6 to find the link-layer address for a next hop. Switches forward frames within a local network.

## Addressing and local network services

### IP address and subnet

An IP address identifies an interface on an IP network. A prefix length (such as `/24`) indicates how many leading bits identify the network. A subnet calculation determines which addresses are on-link and which require a router. IPv4 and IPv6 use different address sizes and rules.

### DHCP

DHCP commonly provides dynamic network configuration. The familiar IPv4 exchange is **DORA**: Discover, Offer, Request, Acknowledge. DHCP reservations and lease duration are managed by the network's DHCP service.

### ARP and Neighbor Discovery

ARP maps an IPv4 address to a link-layer address on the local network. IPv6 uses Neighbor Discovery Protocol (NDP), which is part of ICMPv6. These protocols do not route traffic across the internet; they resolve local next hops.

### VLANs

A VLAN creates a logical layer-2 network. Switch access ports commonly carry one VLAN; trunk links can carry multiple VLANs using tags. Communication between VLANs requires layer-3 routing and may be controlled by access rules.

## TCP, UDP, and common protocols

| Protocol | Key idea | Common uses |
| --- | --- | --- |
| TCP | Connection-oriented byte stream with delivery and ordering mechanisms | HTTPS, SSH, SMTP |
| UDP | Datagram transport without TCP's connection and delivery guarantees | DNS queries, real-time media, QUIC |
| ICMP | Network control and diagnostic messages | Error reporting, `ping`, path MTU discovery |

TCP's three-way handshake is **SYN → SYN-ACK → ACK**. TCP and UDP use port numbers to deliver traffic to an application on a host. A firewall or network policy must allow the relevant protocol and port in the required direction.

### Common ports

| Port | Protocol | Typical service |
| --- | --- | --- |
| 22/TCP | SSH | Secure remote shell |
| 25/TCP | SMTP | Mail transfer between servers |
| 53/UDP and TCP | DNS | Name queries and responses; TCP is also used for some responses and zone transfers |
| 80/TCP | HTTP | Unencrypted web traffic |
| 123/UDP | NTP | Time synchronization |
| 143/TCP | IMAP | Mail access |
| 443/TCP | HTTPS | HTTP over TLS (HTTP/3 uses UDP 443) |
| 445/TCP | SMB | Windows file sharing |
| 587/TCP | SMTP submission | Authenticated mail submission, commonly with TLS |
| 993/TCP | IMAPS | IMAP over TLS |
| 3389/TCP | RDP | Remote Desktop |

Port use can be customized. Confirm the actual service configuration before changing a firewall.

## Routing, VLANs, and firewalls

### Routing

Routers choose a next hop using the most specific matching route (longest-prefix match). A default route handles destinations without a more specific route. Static routes are configured manually; dynamic routing protocols exchange route information and adapt to topology changes.

### NAT

Network Address Translation (NAT) changes address information as packets cross a device. IPv4 networks commonly use source NAT/PAT to share public addresses. NAT is not a substitute for a firewall or application security.

### Firewalls and ACLs

Firewalls enforce traffic rules, often using source/destination addresses, protocol, port, connection state, and direction. An ACL may filter or classify traffic. Follow least privilege: allow only the traffic needed, in the required direction, and keep management access restricted.

Stateful firewalls track connection state and commonly allow reply traffic for permitted sessions. Stateless filters evaluate each packet against rules without maintaining that connection context.

## DNS and HTTP

DNS maps names to records such as A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail exchanger), and TXT (text). A recursive resolver performs lookups for a client; authoritative servers publish records for a zone. DNS answers may be cached according to TTL values.

```bash
dig example.com A
dig example.com MX
nslookup example.com
curl -I https://example.com
```

HTTP is an application protocol. Common methods include `GET` (retrieve), `POST` (submit/process), `PUT` (replace), `PATCH` (partially update), and `DELETE` (remove). HTTPS protects HTTP traffic with TLS in transit; it does not by itself guarantee that an application is safe or authorized.

### MTU, MSS, latency, and bandwidth

- **Bandwidth** is the capacity of a link; **throughput** is the achieved data rate.
- **Latency** is the time for data to travel; round-trip time (RTT) measures a request and reply.
- **Packet loss** means packets fail to reach their destination and can harm performance, especially for TCP.
- **MTU** is the largest layer-3 packet a link can carry without fragmentation. **MSS** is the TCP payload size negotiated for a connection.

Path MTU problems can make some connections stall while smaller requests work. Diagnose with approved network tools and avoid changing MTU without checking the full path.

## Proxies, load balancers, and CDNs

- A **forward proxy** acts on behalf of clients when they access other services.
- A **reverse proxy** accepts client requests and forwards them to backend services.
- A **load balancer** distributes connections or requests across backends. Algorithms may include round robin, least connections, or health/performance-based selection.
- A **CDN** serves cached or dynamically fetched content from distributed edge locations closer to users.

Health checks, TLS termination, client IP forwarding, timeouts, and backend capacity all affect what users experience. A successful connection to a load balancer does not prove the application is healthy.

## Troubleshooting workflow

Start with the symptom and test each hop in order. A failure at one step narrows the search; a successful `ping` does not prove that an application port is open.

1. Confirm the affected users, destination, protocol, port, and start time.
2. Check local interface configuration and routes: `ip address`, `ip route`.
3. Check name resolution: `dig name` or `getent hosts name`.
4. Check reachability where appropriate: `ping`, `tracepath`, or `traceroute`. ICMP may be filtered, so interpret results carefully.
5. Check the service port: `ss -lntup` on a Linux server; use an approved client-side port test.
6. Inspect firewall/network policy, service status, and application logs.
7. Make a controlled change, then verify end-to-end behavior.

### Linux commands

```bash
ip address                     # interface addresses
ip route                       # routing table
ss -lntup                      # listening TCP/UDP sockets
ping -c 4 192.0.2.10            # basic reachability (ICMP may be blocked)
tracepath example.com           # path and MTU hints (if installed)
dig example.com                 # DNS lookup
curl -v --connect-timeout 5 https://example.com
sudo tcpdump -ni any port 443   # packet capture; use only with authorization
```

`ifconfig`, `route`, and `netstat` are legacy utilities on many modern Linux systems; `ip` and `ss` are generally preferred. Packet captures can contain sensitive data, so limit scope and protect capture files.

## Further reading

- [RFC 9293: Transmission Control Protocol (TCP)](https://www.rfc-editor.org/rfc/rfc9293)
- [RFC 1034: Domain Names—Concepts and Facilities](https://www.rfc-editor.org/rfc/rfc1034)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
- [Cloudflare Learning Center: What is DNS?](https://www.cloudflare.com/learning/dns/what-is-dns/)
