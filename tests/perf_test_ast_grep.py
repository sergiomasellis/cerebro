import time
import os
from ast_grep_py import SgNode, SgRoot

def benchmark_ast_grep(file_path):
    start_time = time.perf_counter()
    
    # Read file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Parse with ast-grep
    root = SgRoot(content, "python")
    node = root.root()
    
    # Find all function definitions using kind
    # Note: 'function_definition' is the standard tree-sitter node name for Python functions
    functions = node.find_all(kind="function_definition")
    
    # Extract names to verify
    names = [f.field("name").text() for f in functions]
    print(f"DEBUG: ast-grep found: {names}")
    
    count = len(functions)
    end_time = time.perf_counter()
    
    print(f"ast-grep: Found {count} functions in {end_time - start_time:.4f}s")
    return end_time - start_time

def benchmark_raw_read(file_path):
    start_time = time.perf_counter()
    
    # Simulate current behavior: read lines and maybe some regex (simplified)
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Just counting "def " occurrences as a rough proxy for "processing"
    count = sum(1 for line in lines if line.strip().startswith("def "))
    
    end_time = time.perf_counter()
    
    print(f"Raw read: Found ~{count} functions (heuristic) in {end_time - start_time:.4f}s")
    return end_time - start_time

if __name__ == "__main__":
    target_file = "src/nodes.py"
    if not os.path.exists(target_file):
        print(f"File {target_file} not found.")
        exit(1)
        
    print(f"Benchmarking on {target_file} ({os.path.getsize(target_file)} bytes)...")
    
    # Warmup
    benchmark_raw_read(target_file)
    benchmark_ast_grep(target_file)
    
    print("-" * 20)
    
    t_raw = benchmark_raw_read(target_file)
    t_ast = benchmark_ast_grep(target_file)
    
    print("-" * 20)
    if t_ast < t_raw:
        print(f"ast-grep is {t_raw / t_ast:.2f}x faster")
    else:
        print(f"ast-grep is {t_ast / t_raw:.2f}x slower")
