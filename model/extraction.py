import json
import os
import instructor 
from groq import Groq
from config import GROQ_KEY, MODEL
from components import CPURequirements, CoolerRequirements, StorageRequirements, MemoryRequirements, MotherboardRequirements, PCRequirements

client = Groq(api_key=GROQ_KEY)
client = instructor.from_groq(client, mode=instructor.Mode.JSON)

def call_to_model(messages, response_model):
    response = client.chat.completions.create(
        model=MODEL,
        response_model=response_model,
        messages=messages
    ).model_dump()

    return response

def get_requirements(message: str):
    system_prompt = '''You are an expert assistant helping to extract PC component preferences from user input. Your task is to identify only the details that the user explicitly or implicitly mentions about their desired PC build. 

    The main objective is to have a list of filters that tries to significantly narrow down the choice of PC component from the wide selection within the market. Try to infer or assume user preferences within reason. For attributes that are not clearly stated or reasonably implied, you should ignore and leave blank (i.e. return None).

    Some examples include:
    'I want a PC that has lots of storage as well as RAM.' -> high min_capacity_gb for both memory and storage
    'I'm building a PC for video editing' -> high CPU processing speed
    'Give me something compact. I'm limited on desk space.' -> smaller preferred_form_factor
    '''
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]

    try: 
        pc_requirements = call_to_model(messages, PCRequirements)
        return pc_requirements
    except:
        cpu_requirements = call_to_model(messages, CPURequirements)
        cooler_requirements = call_to_model(messages, CoolerRequirements)
        storage_requirements = call_to_model(messages, StorageRequirements)
        memory_requirements = call_to_model(messages, MemoryRequirements)
        motherboard_requirements = call_to_model(messages, MotherboardRequirements)

        return {
            "cpu": cpu_requirements, 
            "cooler": cooler_requirements, 
            "storage": storage_requirements, 
            "memory": memory_requirements, 
            "motherboard": motherboard_requirements
        }

def save_requirements(reqs: dict, path: str):
    for name, data in reqs.items():
        with open(f"{path}/{name}_requirements.json", "w") as f:
            json.dump(data, f, default=lambda x: x._name_)

message = "I'm a storyboard animator, and I want a decent PC rig that does things fast! It needs at least 1 TB of storage as well as 16 GB of storage. Try to keep the costs as low as possible, but without sacrificing performance."

response = get_requirements(message)

print(response)

if not os.path.isdir("requirements"):
    os.mkdir("requirements")
save_requirements(response, path="requirements")