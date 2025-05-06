# 命令行

不可使用subprocess，只能使用cmd命令
所以无法通过subprocess捕获cloudflared子进程输出内容
只能使用无窗口cmd创建独立进程，然后重定向到本地文件

```dash
cloudflared tunnel --url http://localhost:port
```

# 程序输出

```cmd output
D:\Documents\程序\6muitnsa-TaskSchedule\client\util\Cloudflared>cloudflared tunnel --url http://localhost:8080
2025-05-06T13:58:28Z INF Thank you for trying Cloudflare Tunnel. Doing so, without a Cloudflare account, is a quick way to experiment and try it out. However, be aware that these account-less Tunnels have no uptime guarantee, are subject to the Cloudflare Online Services Terms of Use (https://www.cloudflare.com/website-terms/), and Cloudflare reserves the right to investigate your use of Tunnels for violations of such terms. If you intend to use Tunnels in production you should use a pre-created named tunnel by following: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps
2025-05-06T13:58:28Z INF Requesting new quick Tunnel on trycloudflare.com...
2025-05-06T13:58:33Z INF +--------------------------------------------------------------------------------------------+
2025-05-06T13:58:33Z INF |  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
2025-05-06T13:58:33Z INF |  https://reporters-heads-appeared-sc.trycloudflare.com                                     |
2025-05-06T13:58:33Z INF +--------------------------------------------------------------------------------------------+
2025-05-06T13:58:33Z INF Cannot determine default configuration path. No file [config.yml config.yaml] in [~/.cloudflared ~/.cloudflare-warp ~/cloudflare-warp]
2025-05-06T13:58:33Z INF Version 2025.2.1 (Checksum 2f51d37d18486bfbe055485012854f8c494d070b9e6f9d1e3bc2d8ea56860fbb)
2025-05-06T13:58:33Z INF GOOS: windows, GOVersion: go1.22.5-devel-cf, GoArch: 386
2025-05-06T13:58:33Z INF Settings: map[ha-connections:1 protocol:quic url:http://localhost:8080]
2025-05-06T13:58:33Z INF cloudflared will not automatically update on Windows systems.
2025-05-06T13:58:33Z INF Generated Connector ID: 3d0d79fc-6b7d-4282-ba87-0c5ae5bff0a1
2025-05-06T13:58:33Z INF Initial protocol quic
2025-05-06T13:58:33Z INF ICMP proxy will use 198.18.0.1 as source for IPv4
2025-05-06T13:58:33Z INF ICMP proxy will use fe80::29a5:e8f3:51e:5d79 in zone Mihomo as source for IPv6
2025-05-06T13:58:33Z WRN ICMP proxy feature is disabled error="cannot create ICMPv4 proxy: ICMP proxy is not implemented on windows 386 nor ICMPv6 proxy: ICMP proxy is not implemented on windows 386"
2025-05-06T13:58:33Z INF cloudflared does not support loading the system root certificate pool on Windows. Please use --origin-ca-pool <PATH> to specify the path to the certificate pool
2025-05-06T13:58:33Z INF ICMP proxy will use 198.18.0.1 as source for IPv4
2025-05-06T13:58:33Z INF Using [CurveID(4588) CurveID(25497) CurveP256] as curve preferences connIndex=0 event=0 ip=198.18.1.207
2025-05-06T13:58:33Z INF ICMP proxy will use fe80::29a5:e8f3:51e:5d79 in zone Mihomo as source for IPv6
2025-05-06T13:58:33Z INF Starting metrics server on 127.0.0.1:20241/metrics
2025-05-06T13:58:34Z INF Registered tunnel connection connIndex=0 connection=755c3825-4108-4f06-ab70-0809544f30ed event=0 ip=198.18.1.207 location=hkg11 protocol=quic
```
需要捕获的输出内容为形似此URL的URL

https://reporters-heads-appeared-sc.trycloudflare.com 

正则表达式为
```
https?:\/\/[a-z0-9-]+\.trycloudflare\.com(?=\s|$)
```
