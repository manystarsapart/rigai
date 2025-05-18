import json
import math
import pandas as pd 
from utils import convert_to_enum_name
from config import data_path

cpu_df = pd.read_csv(f"./{data_path}/cpu.csv")
cooler_df = pd.read_csv(f"./{data_path}/cooler.csv")
storage_df = pd.read_csv(f"./{data_path}/storage.csv")
memory_df = pd.read_csv(f"./{data_path}/memory.csv")
motherboard_df = pd.read_csv(f"./{data_path}/motherboard.csv")

def filter_cpu(
    df,
    min_cores=0,
    min_core_clock_ghz=0,
    min_boost_clock_ghz=0,
    microarchitecture=None,
    max_tdp_watts=math.inf,
    max_price=math.inf,
):
    if min_cores is None: 
        min_cores = 0
    if min_core_clock_ghz is None:
        min_core_clock_ghz = 0
    if min_boost_clock_ghz is None:
        min_boost_clock_ghz = 0
    if max_tdp_watts is None:
        max_tdp_watts = math.inf 
    if max_price is None:
        max_price = math.inf

    filters = [
        df["core_count"] >= min_cores,
        df["performance_core_clock"] >= min_core_clock_ghz,
        df["performance_core_boost_clock"] >= min_boost_clock_ghz,
        df["tdp"] <= max_tdp_watts,
        df["price"].astype(float) <= max_price,
    ]

    if microarchitecture:
        filters.append(df['microarchitecture'].apply(convert_to_enum_name).isin(microarchitecture))

    return df.loc[pd.concat(filters, axis=1).all(axis=1)].reset_index(drop=True)

def filter_cooler(
    df,
    min_fan_rpm=0,
    max_noise_level_db=math.inf,
    max_radiator_size_mm=math.inf,
    max_price=math.inf,
):
    if min_fan_rpm is None:
        min_fan_rpm = 0
    if max_noise_level_db is None:
        max_noise_level_db = math.inf 
    if max_radiator_size_mm is None:
        max_radiator_size_mm = math.inf 
    if max_price is None:
        max_price = math.inf 

    filters = [
        df["average_fan_rpm"] >= min_fan_rpm,
        df["average_noise_level"] <= max_noise_level_db,
        df["radiator_size"] <= max_radiator_size_mm,
        df["price"].astype(float) <= max_price,
    ]

    return df.loc[pd.concat(filters, axis=1).all(axis=1)].reset_index(drop=True)

def filter_storage(
    df,
    min_capacity_gb=0,
    preferred_type=None, 
    min_cache_gb=0,
    preferred_form_factor=None,
    preferred_interface=None,
    max_price_per_gb=math.inf
):
    if min_capacity_gb is None:
        min_capacity_gb = 0
    if min_cache_gb is None:
        min_cache_gb = 0
    if max_price_per_gb is None:
        max_price_per_gb = math.inf

    filters = [
        df["capacity_gb"].astype(float) >= min_capacity_gb,
        df["cache_gb"].astype(float) >= min_cache_gb,
        df["price_per_gb"].astype(float) <= max_price_per_gb
    ]

    if preferred_type is not None:
        filters.append(df["type"].apply(convert_to_enum_name).isin(preferred_type))

    if preferred_form_factor is not None:
        filters.append(df["form_factor"].apply(convert_to_enum_name).isin(preferred_form_factor))

    if preferred_interface is not None:
        filters.append(df["interface"].apply(convert_to_enum_name).isin(preferred_interface))

    return df.loc[pd.concat(filters, axis=1).all(axis=1)].reset_index(drop=True)

def filter_memory(
    df,
    min_capacity_gb=0,
    min_speed_mhz=None, # TODO
    max_module_count=0,
    max_cas_latency=math.inf,
    max_price=math.inf
):
    if min_capacity_gb is None:
        min_capacity_gb = 0
    if max_module_count is None:
        max_module_count = math.inf
    if max_cas_latency is None:
        max_cas_latency = math.inf 
    if max_price is None:
        max_price = math.inf
    filters = [
        df["total_ram"] >= min_capacity_gb,
        df["module_count"] <= max_module_count,
        df["cas_latency"] <= max_cas_latency,
        df["price"].astype(float) <= max_price,
    ]

    return df.loc[pd.concat(filters, axis=1).all(axis=1)].reset_index(drop=True)

def filter_motherboard(
    df,
    preferred_socket=None,
    preferred_form_factor=None, 
    min_max_memory_gb=0,
    min_memory_slots=0,
    max_price=math.inf
):
    if min_max_memory_gb is None:
        min_max_memory_gb = 0
    if min_memory_slots is None:
        min_memory_slots = 0
    if max_price is None:
        max_price = math.inf

    filters = [
        df["max_memory_gb"].astype(float) >= min_max_memory_gb,
        df["memory_slots"] >= min_memory_slots,
        df["price"] <= max_price,
    ]

    if preferred_socket:
        filters.append(df["cpu_socket"].apply(convert_to_enum_name).isin(preferred_socket))

    if preferred_form_factor:
        filters.append(df["form_factor"].apply(convert_to_enum_name).isin(preferred_form_factor))


    return df.loc[pd.concat(filters, axis=1).all(axis=1)].reset_index(drop=True)

