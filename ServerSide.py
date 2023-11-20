# import socket
# import threading
# from opentelemetry import trace
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# # 初始化 TracerProvider
# trace.set_tracer_provider(TracerProvider())
# tracer = trace.get_tracer(__name__)

# # 设置一个简单的控制台Span导出器
# span_processor = BatchSpanProcessor(ConsoleSpanExporter())
# trace.get_tracer_provider().add_span_processor(span_processor)


# def handle_client(client_socket):
#     with tracer.start_as_current_span("handle_client") as span:
#         request = client_socket.recv(1024)
#         received_message = request.decode('utf-8')
#         span.set_attribute("message_received", received_message) 
#         print(f"Received: {received_message}")
#         client_socket.send(b"ACK")


# def server_loop():
#     with tracer.start_as_current_span("server_loop"):
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
#             server.bind(("0.0.0.0", 9999))
#             server.listen(5)
#             print("Listening on 0.0.0.0:9999")

#             while True:
#                 client, _ = server.accept()
#                 print("Accepted connection")
#                 client_handler = threading.Thread(target=handle_client, args=(client,))
#                 client_handler.start()

# if __name__ == "__main__":
#     server_loop()

# import socket
# import threading
# import os
# from opentelemetry import trace
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# trace.set_tracer_provider(TracerProvider())
# tracer = trace.get_tracer(__name__)
# span_processor = BatchSpanProcessor(ConsoleSpanExporter())
# trace.get_tracer_provider().add_span_processor(span_processor)

# MAX_CLIENTS = 10


# def handle_client(client_socket, address, directory):
#     with tracer.start_as_current_span("handle_client"):
#         try:
#             file_path = os.path.join(directory, f"file_from_{address[1]}.bin")
#             with open(file_path, 'wb') as file:
#                 while True:
#                     data = client_socket.recv(1024)
#                     if not data:
#                         break
#                     file.write(data)
#             print(f"Received file from {address}")
#         except Exception as e:
#             print(f"Error while handling client {address}: {e}")
#         finally:
#             client_socket.close()

# def server_loop(directory):
#     # 确保存储文件的目录存在
#     if not os.path.exists(directory):
#         os.makedirs(directory)
          
#     with tracer.start_as_current_span("server_loop"):
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
#             server.bind(("0.0.0.0", 9999))
#             server.listen(5)
#             print("Listening on 0.0.0.0:9999")
            
#             client_count = 0
            
#             while client_count < MAX_CLIENTS:
#                 client, address = server.accept()
#                 print(f"Accepted connection from {address}")
#                 client_handler = threading.Thread(target=handle_client, args=(client, address, directory))
#                 client_handler.start()
#                 client_count += 1

#                 if client_count >= MAX_CLIENTS:
#                     print("Maximum number of clients reached. Exiting server.")
#                     server.close()
#                     break

# if __name__ == "__main__":

#     server_loop("received_files")
#     print("Server has finished. Exiting.")

# import socket
# import threading
# import os
# from opentelemetry import trace
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# trace.set_tracer_provider(TracerProvider())
# tracer = trace.get_tracer(__name__)
# span_processor = BatchSpanProcessor(ConsoleSpanExporter())
# trace.get_tracer_provider().add_span_processor(span_processor)

# MAX_CLIENTS = 10
# active_threads = []  # 用于跟踪活跃的客户端线程
# server_running = True



# def handle_client(client_socket, address, directory):
#     global server_running
#     with tracer.start_as_current_span("handle_client"):
#         try:
#             file_path = os.path.join(directory, f"file_from_{address[1]}.bin")
#             with open(file_path, 'wb') as file:
#                 while True:
#                     data = client_socket.recv(1024)
#                     if not data:
#                         break
#                     if data == b"stop":  # 检查是否为停止信号
#                         server_running = False
#                         break
#                     file.write(data)
#             print(f"Received file from {address}")
#         except Exception as e:
#             print(f"Error while handling client {address}: {e}")
#         finally:
#             client_socket.close()  # 确保在 finally 块中关闭套接字


# def server_loop(directory):
#     global server_running
#     if not os.path.exists(directory):
#         os.makedirs(directory)

#     with tracer.start_as_current_span("server_loop"):
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
#             server.bind(("0.0.0.0", 9999))
#             server.listen(5)
#             print("Listening on 0.0.0.0:9999")

#             client_count = 0

#             while client_count < MAX_CLIENTS and server_running:
#                 client, address = server.accept()
#                 print(f"Accepted connection from {address}")
#                 client_handler = threading.Thread(target=handle_client, args=(client, address, directory))
#                 client_handler.start()
#                 active_threads.append(client_handler)  # 添加线程到列表
#                 client_count += 1

#             if client_count >= MAX_CLIENTS:
#                 print("Maximum number of clients reached. Exiting server.")
                
          

#     # 等待所有客户端线程结束
#     for thread in active_threads:
#         thread.join()

#     print("Server has finished. Exiting.")

# 174
# import socket
# import threading
# import os
# from opentelemetry import trace
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
# import random
# from opentelemetry.sdk.trace.sampling import Sampler, SamplingResult, Decision

# class CustomProbabilitySampler(Sampler):
#     def __init__(self, rate):
#         super().__init__()
#         self.rate = rate

#     def should_sample(self, context, trace_id, span_name, span_kind, parent_context, links):
#         if random.random() < self.rate:
#             return SamplingResult(Decision.RECORD_AND_SAMPLE)
#         return SamplingResult(Decision.DROP)

#     def get_description(self):
#         return f"CustomProbabilitySampler({self.rate})"

# trace.set_tracer_provider(TracerProvider())
# tracer = trace.get_tracer(__name__)
# span_processor = BatchSpanProcessor(ConsoleSpanExporter())
# trace.get_tracer_provider().add_span_processor(span_processor)

# MAX_CLIENTS = 10
# active_threads = []  
# server_running = True

# def handle_client(client_socket, address, directory):
#     global server_running
#     with tracer.start_as_current_span("handle_client"):
#         try:
#             file_path = os.path.join(directory, f"file_from_{address[1]}.bin")
#             with open(file_path, 'wb') as file:
#                 while True:
#                     data = client_socket.recv(1024)
#                     if not data:
#                         break
#                     if data == b"stop":  
#                         server_running = False
#                         break
#                     file.write(data)
#             print(f"Received file from {address}")
#         except Exception as e:
#             print(f"Error while handling client {address}: {e}")
#         finally:
#             client_socket.close() 

# def server_loop(directory):
#     global server_running
#     if not os.path.exists(directory):
#         os.makedirs(directory)

#     with tracer.start_as_current_span("server_loop"):
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
#             server.bind(("0.0.0.0", 9999))
#             server.listen(5)
#             print("Listening on 0.0.0.0:9999")

#             client_count = 0

#             while client_count < MAX_CLIENTS and server_running:
#                 client, address = server.accept()
#                 print(f"Accepted connection from {address}")
#                 client_handler = threading.Thread(target=handle_client, args=(client, address, directory))
#                 client_handler.start()
#                 active_threads.append(client_handler)  
#                 client_count += 1

#             if client_count >= MAX_CLIENTS:
#                 print("Maximum number of clients reached. Exiting server.")

#     for thread in active_threads:
#         thread.join()

#     print("Server has finished. Exiting.")

# if __name__ == "__main__":
#     server_loop("received_files")



import socket
import threading
import os
import ssl
import zlib
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.trace.sampling import Sampler, SamplingResult, Decision
import random
import time

class CustomProbabilitySampler(Sampler):
    def __init__(self, rate):
        super().__init__()
        self.rate = rate  # The probability rate for sampling

    def should_sample(self, context, trace_id, span_name, span_kind, parent_context, links):
        # Decide whether to sample the trace based on the rate
        if random.random() < self.rate:
            return SamplingResult(Decision.RECORD_AND_SAMPLE)
        else:
            return SamplingResult(Decision.DROP)

    def get_description(self):
        return f"CustomProbabilitySampler({self.rate})"
    
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)


MAX_CLIENTS = 10
active_threads = []

def handle_client(client_socket, address, directory):
    try:
        file_path = os.path.join(directory, f"file_from_{address[1]}.bin")
        with open(file_path, 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        print(f"Received file from {address}")
    except Exception as e:
        print(f"Error while handling client {address}: {e}")
    finally:
        client_socket.close()

def server_loop(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("0.0.0.0", 9999))
        server.listen(5)
        print("Listening on 0.0.0.0:9999")

        for _ in range(MAX_CLIENTS):
            client, address = server.accept()
            print(f"Accepted connection from {address}")
            client_handler = threading.Thread(target=handle_client, args=(client, address, directory))
            client_handler.start()
            active_threads.append(client_handler)

    for thread in active_threads:
        thread.join()

    print("Server has finished.")

if __name__ == "__main__":
    server_loop("received_files")
