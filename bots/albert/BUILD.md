The Albert bot is capable of advanced Diplomacy play, 
including the ability to do press up to DAIDE level 30. 

It is distributed as a set of Windows installers (as 
it is a Windows executable), but Phil Paquette packaged 
up the Albert executable inside a Singularity container 
for use on Linux HPC systems. 

This container has been exported to a Docker container using the 
following commands using the `Dockerfile` and `run.sh` files 
included in this directory.

```shell
% curl -skL -O "https://f002.backblazeb2.com/file/ppaquette-public/containers/albert_ai/albert_dumbbot-1.2.sif"
% singularity sif list albert_dumbbot-1.2.sif
% singularity sif dump 2 albert_dumbbot-1.2.sif > data.squash
% unsquashfs -dest data data.squash
% echo "data.squash" > .dockerignore
% echo "*.sif" >> .dockerignore
% docker build -t albert-ai .
```

Usage:

```shell
# Get usage
% docker run -it albert-ai
----------------------------
Trying to launch a  bot that will connect to port
----------------------------
... Launching display :99
Usage: /run.sh {albert|dumbbot} {hostname} {port_number}

# Run bot in background
% docker run -d albert-ai albert 127.0.0.1 8990
e8c74cfd91284119b513fe0cedcf82e2803a07c54d4f3368747a7880e29f7d78

# Get logs
% docker logs -f e8c74cfd91284119b513fe0cedcf82e2803a07c54d4f3368747a7880e29f7d78
----------------------------
Trying to launch a albert bot that will connect to port 8332
----------------------------
... Launching display :99
Launching bot...
+ wine /data/albert/Albert.exe -i129.114.99.77 -p8332 -h
0010:err:ole:marshal_object couldn't get IPSFactory buffer for interface {00000131-0000-0000-c000-000000000046}
0010:err:ole:marshal_object couldn't get IPSFactory buffer for interface {6d5140c1-7436-11ce-8034-00aa006009fa}
0010:err:ole:StdMarshalImpl_MarshalInterface Failed to create ifstub, hres=0x80004002
0010:err:ole:CoMarshalInterface Failed to marshal the interface {6d5140c1-7436-11ce-8034-00aa006009fa}, 80004002
0010:err:ole:get_local_server_stream Failed: 80004002

# Note that the errors beginning with 0010:err:ole are from the WINE emulator and are harmless.
```

