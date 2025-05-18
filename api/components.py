import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from utils import create_enum_from_list, get_colours
from config import data_path

cpu_df = pd.read_csv(f"./{data_path}/cpu.csv")
cooler_df = pd.read_csv(f"./{data_path}/cooler.csv")
storage_df = pd.read_csv(f"./{data_path}/storage.csv")
memory_df = pd.read_csv(f"./{data_path}/memory.csv")
motherboard_df = pd.read_csv(f"./{data_path}/motherboard.csv")

# lists of unique values for each component's detail
CPU_MICROARCHITECTURES = sorted(cpu_df['microarchitecture'].dropna().unique().tolist())
CPU_GRAPHICS = sorted(cpu_df['integrated_graphics'].dropna().unique().tolist())
COOLER_COLOURS = sorted(cooler_df['color'].dropna().unique().tolist())
STORAGE_TYPES = sorted(storage_df['type'].dropna().unique().tolist())
STORAGE_FORM_FACTORS = sorted(storage_df['form_factor'].dropna().unique().tolist())
STORAGE_INTERFACES = sorted(storage_df['interface'].dropna().unique().tolist())
MEMORY_COLOURS = sorted(memory_df['color'].dropna().unique().tolist())
MOTHERBOARD_SOCKETS = sorted(motherboard_df['cpu_socket'].dropna().unique().tolist())
MOTHERBOARD_FORM_FACTORS = sorted(motherboard_df['form_factor'].dropna().unique().tolist())
MOTHERBOARD_COLOURS = sorted(motherboard_df['color'].dropna().unique().tolist())

COOLER_COLOURS = get_colours(COOLER_COLOURS)
MEMORY_COLOURS = get_colours(MEMORY_COLOURS)
MOTHERBOARD_COLOURS = get_colours(MOTHERBOARD_COLOURS)

Microarchitecture = create_enum_from_list("microarchitecture", CPU_MICROARCHITECTURES)
IntegratedGraphics = create_enum_from_list("IntegratedGraphics", CPU_GRAPHICS)
CoolerColour = create_enum_from_list("cooler_colour", COOLER_COLOURS)
StorageType = create_enum_from_list("storage_type", STORAGE_TYPES)
StorageFormFactor = create_enum_from_list("storage_form_factor", STORAGE_FORM_FACTORS)
StorageInterface = create_enum_from_list("storage_interface", STORAGE_INTERFACES)
MemoryColour = create_enum_from_list("memory_colour", MEMORY_COLOURS)
MotherboardSocket = create_enum_from_list("motherboard_socket", MOTHERBOARD_SOCKETS)
MotherboardFormFactor = create_enum_from_list("motherboard_form_factor", MOTHERBOARD_FORM_FACTORS)
MotherboardColour = create_enum_from_list("motherboard_clour", MOTHERBOARD_COLOURS)

# classes
class CPURequirements(BaseModel):
    min_cores: Optional[int] = Field(None, description="Minimum number of CPU cores desired")
    min_core_clock_ghz: Optional[float] = Field(None, description="Minimum core clock speed (in GHz)")
    min_boost_clock_ghz: Optional[float] = Field(None, description="Minimum boost clock speed (in GHz)")
    microarchitecture: Optional[List[Microarchitecture]] = Field(None, description="Preferred CPU microarchitecture, e.g., ['Zen 4', 'Raptor Lake'])")
    max_tdp_watts: Optional[float] = Field(None, description="Maximum thermal design power (in watts)")
    #needs_integrated_graphics: Optional[bool] = Field(None, description="Whether integrated graphics are required")
    #min_rating: Optional[float] = Field(None, description="Minimum user rating (out of 5)")
    max_price: Optional[float] = Field(None, description="Maximum budget for CPU (in USD)")

class CoolerRequirements(BaseModel):
    min_fan_rpm: Optional[float] = Field(None, description="Minimum fan RPM for cooling performance")
    max_noise_level_db: Optional[float] = Field(None, description="Desired maximum noise level in decibels")
    max_radiator_size_mm: Optional[float] = Field(None, description="Maximum radiator size in mm (e.g. 240, 360)")
    #preferred_color: Optional[List[CoolerColour]] = Field(None, description="Preferred cooler colors")
    #min_rating: Optional[float] = Field(None, description="Minimum user rating (out of 5)")
    max_price: Optional[float] = Field(None, description="Maximum budget for cooler (in USD)")

class StorageRequirements(BaseModel):
    min_capacity_gb: Optional[float] = Field(None, description="Minimum storage capacity in GB")
    preferred_type: Optional[List[StorageType]] = Field(None, description="Drive type (e.g. ['SSD', 'HDD'])")
    min_cache_gb: Optional[float] = Field(None, description="Minimum cache size in GB (e.g. 2.048, 0.512) (this should be a small number)")
    preferred_form_factor: Optional[List[StorageFormFactor]] = Field(None, description="Preferred drive form factor (e.g. ['2.5', 'M.2'])")
    preferred_interface: Optional[List[StorageInterface]] = Field(None, description="Preferred interface (e.g. ['SATA, NVMe'])")
    #min_rating: Optional[float] = Field(None, description="Minimum user rating (out of 5)")
    max_price_per_gb: Optional[float] = Field(None, description="Maximum budget for drive for each gigabyte (in USD)")

class MemoryRequirements(BaseModel):
    min_capacity_gb: Optional[float] = Field(None, description="Minimum total memory capacity in GB")
    min_speed_mhz: Optional[float] = Field(None, description="Minimum memory speed in MHz")
    max_module_count: Optional[int] = Field(None, description="Maximum number of modules (e.g. 4 for quad-channel)")
    max_cas_latency: Optional[float] = Field(None, description="Maximum acceptable CAS latency")
    #max_first_word_latency: Optional[float] = Field(None, description="Maximum acceptable first-word latency (in ns)")
    #preferred_color: Optional[List[MemoryColour]] = Field(None, description="Preferred memory colors")
    #min_rating: Optional[float] = Field(None, description="Minimum user rating (out of 5)")
    max_price: Optional[float] = Field(None, description="Maximum budget for memory (in USD)")

class MotherboardRequirements(BaseModel):
    preferred_socket: Optional[List[MotherboardSocket]] = Field(None, description="CPU socket type required (e.g. AM5, LGA1700)")
    preferred_form_factor: Optional[List[MotherboardFormFactor]] = Field(None, description="Motherboard form factor (e.g. ATX, Micro ATX)")
    min_max_memory_gb: Optional[float] = Field(None, description="Minimum supported max memory in GB")
    min_memory_slots: Optional[int] = Field(None, description="Minimum number of memory slots")
    #preferred_color: Optional[List[MotherboardColour]] = Field(None, description="Preferred motherboard color")
    #min_rating: Optional[float] = Field(None, description="Minimum user rating (out of 5)")
    max_price: Optional[float] = Field(None, description="Maximum budget for case (in USD)")

class PCRequirements(BaseModel):
    cpu: CPURequirements = Field(description="Details of preferred CPU")
    cooler: CoolerRequirements = Field(description="Details of preferred CPU")
    storage: StorageRequirements = Field(description="Details of preferred internal hard drive for storage")
    memory: MemoryRequirements = Field(description="Details of preferred memory RAM")
    motherboard: MotherboardRequirements = Field(description="Details of preferred motherboard")