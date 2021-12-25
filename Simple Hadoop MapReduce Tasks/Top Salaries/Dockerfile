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
 
