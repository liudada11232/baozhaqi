from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
import uvicorn
import os

app = FastAPI(title="Brake AI Diagnostic Service")

# 定义输出结构
schemas = [
    ResponseSchema(name="wear_level", description="磨损百分比 (0-100)"),
    ResponseSchema(name="status", description="状态: 正常/预警/危险"),
    ResponseSchema(name="analysis", description="AI 详细分析报告"),
    ResponseSchema(name="action", description="建议采取的操作")
]
output_parser = StructuredOutputParser.from_response_schemas(schemas)
format_instructions = output_parser.get_format_instructions()

# 配置 LangChain (请设置环境变量 OPENAI_API_KEY)
# 如果使用本地模型可切换为 Ollama 或其他 LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

class SensorData(BaseModel):
    temp: float
    vib: float
    gap: float

@app.post("/analyze")
async def analyze_data(data: SensorData):
    prompt = ChatPromptTemplate.from_template(
        "你是一个工业设备监测专家。分析单Agent抱闸器传感器数据:\n"
        "温度: {temp}℃, 振动: {vib}mm/s, 抱闸间隙: {gap}mm。\n"
        "{format_instructions}"
    )
    
    messages = prompt.format_messages(
        temp=data.temp, 
        vib=data.vib, 
        gap=data.gap, 
        format_instructions=format_instructions
    )
    
    try:
        response = llm.invoke(messages)
        return output_parser.parse(response.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
