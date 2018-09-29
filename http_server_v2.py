#coding=utf-8
'''
http server v2.0
1.多线程并发
2.可以请求简单数据
3.能进行简单请求解析
4.结构使用类进程封装
'''
from socket import * 
from threading import Thread
import sys
import traceback

#httpserver类，封装具体的服务器功能
class httpserver(object):
    def __init__(self,server_addr,static_dir):
        #增添服务器对象属性
        self.server_address = server_addr
        self.static_dir = static_dir
        self.ip = server_addr[0]
        self.port = server_addr[1]
        #创建套接字
        self.create_socket()

    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.sockfd.bind(self.server_address)

    #设置监听等待客户端连接
    def serve_forever(self):
        self.sockfd.listen(5)
        print('listen the port %d'%self.port)
        while True:
            try:
                connfd,addr = self.sockfd.accept()
            except KeyboardInterrupt:
                self.sockfd.close()
                sys.exit('服务器退出')
            except Exception:
                trackback.print_exc()#更详细的打印异常信息
                continue
            #创建新的线程处理请求
            clientThread = Thread(target = self.handleRequest,args=(connfd,))
            clientThread.setDaemon(True)
            clientThread.start()
    #客户端请求函数
    def handleRequest(self,connfd):
        #接收客户端请求
        request = connfd.recv(4096)
        #解析请求内容
        requestHeaders = request.splitlines()
        print(connfd.getpeername(),':',requestHeaders[0])
        #获取具体请求内容
        getRequest = str(requestHeaders[0]).split(' ')[1]

        if getRequest == '/' or getRequest[-5:] == '.html':
            self.get_html(connfd,getRequest)
        else:
            self.get_data(connfd,getRequest)

        connfd.close()

    def get_html(self,connfd,getRequest):
        if getRequest == '/':
            filename = self.static_dir + '/index.html'
        else:
            filename = self.static_dir + getRequest
        try:
            f = open(filename)
        except IOError:
            response = 'HTTP/1.1 404 not found\r\n'
            response += '\r\n'
            response += '=======sorry not found======='
        else:
            response = 'HTTP/1.1 200 OK\r\n'
            response += '\r\n'
            response += f.read()
        finally:
            connfd.send(response.encode())

    def get_data(self,connfd,getRequest):
        urls = ['/time','/tedu','/python']
        if getRequest in urls:
            response = 'HTTP/1.1 200 OK\r\n'
            response += '\r\n'
            if getRequest == '/time':
                import time
                response += time.ctime()
            elif getRequest == '/tedu':
                response += 'welcome to tarena'
            elif getRequest == '/python':
                response += '人生苦短我用python'
        else:
            response = 'HTTP/1.1 404 not found\r\n'
            response += '\r\n'
            response += '=======sorry not found the data======='
        connfd.send(response.encode())

if __name__=='__main__':
    #服务器IP
    server_addr = ('0.0.0.0',5000)
    #静态文件夹存储目录
    static_dir = ('./static')

    #生成对象
    httpd = httpserver(server_addr,static_dir)
    #启动服务器
    httpd.serve_forever()