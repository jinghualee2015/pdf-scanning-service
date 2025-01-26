## Pdf-Ocr-Service

解析文档服务，从文件系统获取待解析的PDF文档处理解析然后存储到具体的文件系统中并通过RPC形式告知上游应用
## 打包
### 开发环境
docker build -t pdf-ocr-service:dev --build-arg PROFILE=dev -f ./deploy/Dockerfile .
## 测试环境
### 存活探针
celery  -A pdf_ocr_service  inspect  ping --destination celery@pdf-ocr-service
## 集群模式
启动1个job进程
celery multi start job -A pdf_ocr_service
### 查看状态
celery -A pdf_ocr_service status
