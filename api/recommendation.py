import json
import instructor 
from groq import Groq
from pydantic import BaseModel
from extraction import get_requirements
from filters import *
from config import *

client = Groq(api_key=GROQ_KEY)
client = instructor.from_groq(client, mode=instructor.Mode.JSON)

cpu_df = pd.read_csv(f"./{data_path}/cpu.csv")
cooler_df = pd.read_csv(f"./{data_path}/cooler.csv")
storage_df = pd.read_csv(f"./{data_path}/storage.csv")
memory_df = pd.read_csv(f"./{data_path}/memory.csv")
motherboard_df = pd.read_csv(f"./{data_path}/motherboard.csv")

class Component(BaseModel):
    index: int
    name: str 
    price: float

class ComponentChoices(BaseModel):
    cpu: Component 
    cooler: Component
    storage: Component 
    memory: Component 
    motherboard: Component

def get_filtered_csvs(message: str, limit: int):
    cpu_requirements, cooler_requirements, storage_requirements, memory_requirements, motherboard_requirements = get_requirements(message=message).values()

    cpu_filtered = filter_cpu(cpu_df.copy(), **cpu_requirements).head(limit) if cpu_requirements is not None else []
    cooler_filtered = filter_cooler(cooler_df.copy(), **cooler_requirements).head(limit) if cooler_requirements is not None else []
    storage_filtered = filter_storage(storage_df.copy(), **storage_requirements).head(limit) if storage_requirements is not None else []
    memory_filtered = filter_memory(memory_df.copy(), **memory_requirements).head(limit) if memory_requirements is not None else []
    motherboard_filtered = filter_motherboard(motherboard_df.copy(), **motherboard_requirements).head(limit) if motherboard_requirements is not None else []

    if len(cpu_filtered) == 0:
        cpu_filtered = cpu_df.copy().head(limit)
    if len(cooler_filtered) == 0:
        cooler_filtered = cooler_df.copy().head(limit)
    if len(storage_filtered) == 0:
        storage_filtered = storage_df.copy().head(limit)
    if len(memory_filtered) == 0:
        memory_filtered = memory_df.copy().head(limit)
    if len(motherboard_filtered) == 0:
        motherboard_filtered = motherboard_df.copy().head(limit)

    return cpu_filtered, cooler_filtered, storage_filtered, memory_filtered, motherboard_filtered

def get_recommendation(message: str):
    system_prompt = """You are tasked with recommending a compatible and high-performance PC setup. You are given five JSON arrays, consisting of details of CPUs, coolers, storage hard drives, memory modules, and motherboards. From the list, choose only ONE component from each array, ensuring compatibility across all components that it meets the user's expectation and preference based on their input. For each component, output the name, as well as the index number of its row. You must only select from the given options. Do not invent anything new."""

    cpu_filtered, cooler_filtered, storage_filtered, memory_filtered, motherboard_filtered = get_filtered_csvs(message=message, limit=10)

    user_prompt = f"""The user inputted: {message}

    Here are the component options:
    CPUs: {json.dumps(cpu_filtered.reset_index().to_dict(orient="records"))}
    Coolers: {json.dumps(cooler_filtered.reset_index().to_dict(orient="records"))}
    Storage: {json.dumps(storage_filtered.reset_index().to_dict(orient="records"))}
    Memory: {json.dumps(memory_filtered.reset_index().to_dict(orient="records"))}
    Motherboard: {json.dumps(motherboard_filtered.reset_index().to_dict(orient="records"))}
    """

    print("Sent request...")

    recommendation = client.chat.completions.create(
        model=MODEL,
        response_model=ComponentChoices,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    ).model_dump()

    return recommendation

if __name__ == "__main__":
    print(get_recommendation(message=TEST_MESSAGE))