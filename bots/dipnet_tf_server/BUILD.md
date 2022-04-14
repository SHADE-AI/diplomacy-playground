# DipNetSL - tensorflow server only

Container launches the tensorflow model server for DipNetSL bot. With default settings, DipNetSLPlayer
can be instantiated in a python script that will connect to this server. 

Build:
```shell
$ wget https://f002.backblazeb2.com/file/ppaquette-public/benchmarks/neurips2019-sl_model.zip
$ mkdir bot_neurips2019-sl_model
$ unzip neurips2019-sl_model.zip -d bot_neurips2019-sl_model/
$ docker build -t dipnet_sl_tf_server .
```

Usage:
```shell
$ docker run -it dipnet_sl_tf_server
2022-04-14 16:48:13.030096: I tensorflow_serving/model_servers/server.cc:313] Running gRPC ModelServer at 0.0.0.0:9501 ...

The following environment variables are optional batching parameters for the TF server. Defaults can be overriden
with the -e flag.

ENV MAX_BATCH_SIZE=128
ENV BATCH_TIMEOUT_MICROS=250000
ENV MAX_ENQUEUED_BATCHES=1024
ENV NUM_BATCH_THREADS=8
ENV PAD_VARIABLE_LENGTH_INPUTS='true'

These variables are written to a file, batch.txt, which the TF server takes as input. 
```

