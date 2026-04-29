# 单Agent抱闸器磨损监测系统

## 启动步骤:
1. AI Service:
   - cd ai-service
   - pip install fastapi uvicorn langchain langchain-openai pydantic
   - export OPENAI_API_KEY='your-key'
   - python main.py
   
2. Backend:
   - Spring Boot 项目中引入 RestTemplate 配置
   - 运行项目 (默认 8080 端口)

3. Frontend:
   - Vue 3 项目安装 axios
   - 运行 npm run dev
