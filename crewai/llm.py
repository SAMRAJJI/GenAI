from crewai import LLM

ollama_llm = LLM(
    model="ollama/qwen3-vl:2b",
    base_url="http://localhost:11434",
    temperature=0.2
)