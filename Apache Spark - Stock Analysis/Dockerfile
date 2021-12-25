FROM deepnote/python:3.7

# get Java
RUN sudo apt-get update && \ 
    sudo mkdir -p /usr/share/man/man1 && \
    sudo apt-get install -y openjdk-11-jdk-headless

# install hadoop
RUN cd $HOME && \
    wget https://ftp.fau.de/apache/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz && \
    tar xvzf hadoop-3.3.1.tar.gz

# set paths
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV HDFS_NAMENODE_USER=root
ENV HDFS_DATANODE_USER=root
ENV HDFS_SECONDARYNAMENODE_USER=root
ENV HADOOP_HOME=/root/hadoop-3.3.1
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
RUN echo "export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin" >> $HOME/.bashrc && \
    echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64" >> $HOME/.bashrc && \
    echo "export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop" >> $HOME/.bashrc && \
    echo "export HDFS_NAMENODE_USER=root" >> $HOME/.bashrc && \
    echo "export HDFS_DATANODE_USER=root" >> $HOME/.bashrc && \
    echo "export HDFS_SECONDARYNAMENODE_USER=root" >> $HOME/.bashrc


# get mrjob
RUN pip install mrjob
 
# set config for hadoop
RUN echo "<configuration><property><name>fs.defaultFS</name><value>hdfs://localhost:9000</value></property></configuration>" > $HADOOP_HOME/etc/hadoop/core-site.xml && \
    echo "<configuration><property><name>dfs.replication</name><value>1</value></property><property><name>dfs.namenode.name.dir</name><value>$HADOOP_HOME/namenode</value></property><property><name>dfs.datanode.data.dir</name><value>$HADOOP_HOME/datanode</value></property><property><name>dfs.client.read.shortcircuit</name><value>false</value></property></configuration>" > $HADOOP_HOME/etc/hadoop/hdfs-site.xml && \
    echo "<configuration><property><name>mapreduce.framework.name</name><value>yarn</value></property><property><name>mapreduce.application.classpath</name><value>$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/mapreduce/lib/*</value></property></configuration>" > $HADOOP_HOME/etc/hadoop/mapred-site.xml && \
    echo "<configuration><property><name>yarn.nodemanager.aux-services</name><value>mapreduce_shuffle</value></property><property><name>yarn.nodemanager.env-whitelist</name><value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value></property></configuration>" > $HADOOP_HOME/etc/hadoop/yarn-site.xml

# installing libhdfs3
RUN sudo apt install -y libxml2-dev libprotobuf-dev libkrb5-dev libgsasl7-dev libgmock-dev openssl libssl-dev libcurl4-openssl-dev protobuf-compiler libboost-dev && \
    cd /root && \
    git clone https://github.com/ContinuumIO/libhdfs3-downstream.git && \
    cd libhdfs3-downstream/libhdfs3 && mkdir build && cd build && ../bootstrap && make && make install && cd ../dist/lib/ && sudo cp -R * /usr/lib && cd

RUN pip install hdfs3

# magic line to get rid of ssh
RUN sed -i 's+ssh ${HADOOP_SSH_OPTS} ${worker} \$"\${@// /\\\\ }"+command=$"${@// /\\\\ }" ; ${command#"-- "}+g' $HADOOP_HOME/libexec/hadoop-functions.sh

# make directories for namenode and datanode data
RUN mkdir $HADOOP_HOME/datanode && \
    mkdir $HADOOP_HOME/namenode

# formatting HDFS file system
RUN $HADOOP_HOME/bin/hdfs namenode -format

# initializing home directory on HDFS file system
# done in script to get around "connection refused" issue
RUN echo "$HADOOP_HOME/sbin/start-dfs.sh" > init_home.sh && \
    echo "$HADOOP_HOME/bin/hdfs dfs -mkdir /user" >> init_home.sh && \
    echo "$HADOOP_HOME/bin/hdfs dfs -mkdir /user/root" >> init_home.sh && \
    echo "$HADOOP_HOME/sbin/stop-dfs.sh" >> init_home.sh && \
    sh init_home.sh


# installing Pig
RUN cd /root && \
    wget http://ftp.halifax.rwth-aachen.de/apache/pig/pig-0.17.0/pig-0.17.0.tar.gz && \
    tar xvzf pig-0.17.0.tar.gz && \
    rm pig-0.17.0.tar.gz
ENV PIG_HOME=/home/jovyan/pig-0.17.0
RUN echo "export PATH=$PATH:$PIG_HOME/bin" >> $HOME/.bashrc


# installing Spark
RUN cd /root && \ 
    wget https://ftp.fau.de/apache/spark/spark-3.0.3/spark-3.0.3-bin-without-hadoop.tgz && \
    tar xvzf spark-3.0.3-bin-without-hadoop.tgz && \
    rm spark-3.0.3-bin-without-hadoop.tgz
ENV SPARK_HOME=/root/spark-3.0.3-bin-without-hadoop
ENV SPARK_DIST_CLASSPATH=$HADOOP_HOME/etc/hadoop:$HADOOP_HOME/share/hadoop/common/lib/*:$HADOOP_HOME/share/hadoop/common/*:$HADOOP_HOME/share/hadoop/hdfs:$HADOOP_HOME/share/hadoop/hdfs/lib/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/yarn:$HADOOP_HOME/share/hadoop/yarn/lib/*:$HADOOP_HOME/share/hadoop/yarn/*
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PYSPARK_PYTHON=/root/venv/bin/python
RUN echo "export PATH=$PATH:$SPARK_HOME/bin" >> $HOME/.bashrc

ENV YARN_RESOURCEMANAGER_USER=root
ENV YARN_NODEMANAGER_USER=root
RUN echo "export YARN_RESOURCEMANAGER_USER=root" >> $HOME/.bashrc && \
    echo "export YARN_NODEMANAGER_USER=root" >> $HOME/.bashrc