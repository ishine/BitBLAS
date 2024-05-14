llama_providers = ["BS1 SEQ1", "BS32 SEQ1", "BS1 SEQ4096"]
llama_times_data = [
    ("PyTorch-Inductor", [2660, 2642, 6754]),
    ("ONNXRuntime", [2748, 2780, 16206]),
    ("TensorRT", [5140, 5148, 6260]),
    ("vLLM", [0, 0, 0]),
    ("vLLM-W$_{INT4}$A$_{FP16}$", [0, 0, 0]),
    ("Welder", [2076, 2084, 6626]),
    ("Bitter", [2064, 2070, 6580]),
    ("Bitter-W$_{INT4}$A$_{FP16}$", [840, 846, 5356]),
    ("Bitter-W$_{NF4}$A$_{FP16}$", [852, 853, 5364]),
    ("Bitter-W$_{FP8}$A$_{FP8}$", [1248, 1254, 5764]),
    ("Bitter-W$_{MXFP8}$A$_{MXFP8}$", [1361, 1370, 5877]),
    ("Bitter-W$_{INT1}$A$_{INT8}$", [534, 540, 5050]),
]

bloom_providers = ["BS1 SEQ1", "BS32 SEQ1", "BS1 SEQ4096"]
bloom_times_data = [
    ("PyTorch-Inductor", [12088, 12072, 0]),
    ("ONNXRuntime", [7356, 6844, 0]),
    ("TensorRT", [5771, 5783, 0]),
    ("vLLM", [0, 0, 0]),
    ("vLLM-W$_{INT4}$A$_{FP16}$", [0, 0, 0]),
    ("Welder", [5148, 5160, 0]),
    ("Bitter", [5136, 5156, 0]),
    ("Bitter-W$_{INT4}$A$_{FP16}$", [3372, 3392, 0]),
    ("Bitter-W$_{NF4}$A$_{FP16}$", [3382, 3384, 0]),
    ("Bitter-W$_{FP8}$A$_{FP8}$", [3960, 3980, 0]),
    ("Bitter-W$_{MXFP8}$A$_{MXFP8}$", [4654, 4755, 0]),
    ("Bitter-W$_{INT1}$A$_{INT8}$", [2931, 2951, 0]),
]