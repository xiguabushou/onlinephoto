 # 建立 python3.10 环境
 FROM python:3.10
 
 # 设置 python 环境变量
 ENV PYTHONUNBUFFERED 1
 
 # 在容器内/var/www/html/下创建 mysite2 文件夹
 RUN mkdir -p /var/www/html/myweb
 
 # 设置容器内工作目录
 WORKDIR /var/www/html/myweb
 
 # 将当前目录文件拷贝一份到工作目录中（. 表示当前目录）
 COPY . /var/www/html/myweb
 
 # 利用 pip 安装依赖
 RUN pip install -r requirements.txt
 #RUN pip install uwsgi
 RUN chmod +x ./start.sh