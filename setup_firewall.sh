#!/usr/bin/env bash

PUBLIC_IF=wlp61s0
PROXY_IP=127.0.0.1
PROXY_PORT=5555
TRAFFIC_PORT=5555

echo "Please ensure net.ipv4.ip_forward=1"

# Delete all rules
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X

# Setting default filter policy
iptables -P INPUT DROP
iptables -P OUTPUT ACCEPT

# Unlimited access to loop back
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

iptables -A INPUT -i ${PUBLIC_IF} -j ACCEPT
iptables -A OUTPUT -o ${PUBLIC_IF} -j ACCEPT


# if it is same system
iptables -t nat -A PREROUTING -i ${PUBLIC_IF} -p tcp --dport ${TRAFFIC_PORT} -j REDIRECT --to-port ${PROXY_PORT}
iptables -t nat -A POSTROUTING -o ${PUBLIC_IF} -j MASQUERADE


# DROP everything and Log it
iptables -A INPUT -j LOG
#iptables -A INPUT -j DROP
