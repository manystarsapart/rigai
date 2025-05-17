import json
import instructor 
from groq import Groq
from pydantic import BaseModel
from filters import *
from config import *

client = Groq(api_key=GROQ_KEY)
client = instructor.from_groq(client, mode=instructor.Mode.JSON)

cpu_df = pd.read_csv(f"./{data_path}/cpu.csv")
cooler_df = pd.read_csv(f"./{data_path}/cooler.csv")
storage_df = pd.read_csv(f"./{data_path}/storage.csv")
memory_df = pd.read_csv(f"./{data_path}/memory.csv")
motherboard_df = pd.read_csv(f"./{data_path}/motherboard.csv")

cpu_requirements = json.load(open('./requirements/cpu_requirements.json', 'r'))
cooler_requirements = json.load(open('./requirements/cooler_requirements.json', 'r'))
storage_requirements = json.load(open('./requirements/storage_requirements.json', 'r'))
memory_requirements = json.load(open('./requirements/memory_requirements.json', 'r'))
motherboard_requirements = json.load(open('./requirements/motherboard_requirements.json', 'r'))

limit = 10

cpu_filtered = filter_cpu(cpu_df.copy(), **cpu_requirements).head(limit)
cooler_filtered = filter_cooler(cooler_df.copy(), **cooler_requirements).head(limit)
storage_filtered = filter_storage(storage_df.copy(), **storage_requirements).head(limit)
memory_filtered = filter_memory(memory_df.copy(), **memory_requirements).head(limit)
motherboard_filtered = filter_motherboard(motherboard_df.copy(), **motherboard_requirements).head(limit)

class Component(BaseModel):
    index: int
    name: str 
    price: int

class ComponentChoices(BaseModel):
    cpu: Component 
    cooler: Component
    storage: Component 
    memory: Component 
    motherboard: Component

def get_recommendation(message: str):
    system_prompt = """You are tasked with recommending a compatible and high-performance PC setup. You are given five JSON arrays, consisting of details of CPUs, storage hard drives, and memory modules. From the list, choose only ONE component from each array, ensuring compatibility across all components that it meets the user's expectation and preference based on their input. For each component, output the name, as well as the index number of its row. You must only select from the given options. Do not invent anything new."""

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

print(get_recommendation(message="I want a decent PC rig that does things fast and has a lot of RAM!"))