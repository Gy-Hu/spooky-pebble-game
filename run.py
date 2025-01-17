import os
from Convert_bench_file_to_DAG import dag
from gameSolver import spooky_solver

def check_benchmark_file(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Benchmark file not found: {filepath}")
    if os.path.getsize(filepath) == 0:
        raise ValueError(f"Benchmark file is empty: {filepath}")

try:
    benchmark_file = "benchmarks/ISCAS85XMG/c7552.bench"
    check_benchmark_file(benchmark_file)
    
    # 创建DAG对象并导入c17.bench
    DAG = dag(benchmark_file)
    
    if DAG.n == 0:
        raise ValueError(f"No vertices found in {benchmark_file}. Please check file format.")
    
    # 设置求解参数
    max_pebbles = 7  # 最大允许使用的pebbles数量 
    max_spooks = 2   # 最大允许使用的spooks数量
    Twait = 15      # 每次BMC迭代的最大等待时间
    print("Begin to solve")

    # 使用spooky_solver求解
    result = spooky_solver(DAG, "c17", max_pebbles, max_spooks, Twait)
    print(result)
    
except FileNotFoundError as e:
    print(f"Error: {str(e)}")
    print("Please ensure the benchmark file exists in the correct location.")
except ValueError as e:
    print(f"Error: {str(e)}")
    print("Please check the benchmark file format.")
except Exception as e:
    print(f"Unexpected error: {str(e)}")