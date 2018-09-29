from socket import *

def handleclient(connfd):
    request=connfd.recv(4096)
    # print(request)
    #将request请求按行分隔
    request_lines=request.splitlines()
    for line in request_lines:
        print(line.decode())
    try:
        f=open('index.html')
    except IOError:
        response='HTTP/1.1 404 not found\r\n'
        response+='\r\n'#空行
        response+='******sorry not found******'
    else:
        response='HTTP/1.1 200 OK\r\n'
        response+='\r\n'#空行
        response+=f.read()
    finally:
        #发送给浏览器
        connfd.send(response.encode())
#创建套接字
def main():
    sockfd=socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(('0.0.0.0',6566))
    sockfd.listen(5)
    print('listen to the port 6566')
    while True:
        connfd,addr=sockfd.accept()
        #处理请求
        handleclient(connfd)
        connfd.close()

if __name__=='__main__':
    main()