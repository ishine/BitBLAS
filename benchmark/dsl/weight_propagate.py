# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
import bitblas
from bitblas.base.roller.policy import TensorCorePolicy, DefaultPolicy
from bitblas.base.roller.arch import CUDA
from bitblas.gpu.matmul_analysis import get_tensorized_func_and_tags
from bitblas.gpu import Matmul
from bitblas.utils import auto_detect_nvidia_target
from bitblas.base.utils import apply_and_build
from bitblas.ops.impl.matmul_impl import (
    matmul_nt,
    matmul_nt_propagate_b,
    matmul_nt_propagate_a_propagate_b,
)
from bitblas.ops.impl.matmul_dequantize_impl import (
    matmul_nt_dequantize_b,
    matmul_nt_dequantize_b_propagate_b,
)
import tvm
import time
import argparse

bitblas.set_log_level("DEBUG")
parser = argparse.ArgumentParser(description="Benchmark BitBLAS int4 on a specific target.")
parser.add_argument(
    "--target",
    type=str,
    default=auto_detect_nvidia_target(),
)
parser.add_argument(
    "--group_size",
    type=int,
    default=-1,
    help="The group size of the sequence",
)
parser.add_argument(
    "--benchmark_sets",
    nargs="+",
    default=[
        "llm_shape_fp16xint4_with_scaling_zeros_original_g128",
        "llm_shape_fp16xint4_with_scaling_zeros_rescale_g128",
        "llm_shape_fp16xint4_with_scaling_zeros_quantized_g128"
    ],
    help="List of benchmark sets, e.g., llm_int8xint1_bs4096",
)

args = parser.parse_args()
group_size = args.group_size

llm_shape_fp16xfp16 = [
    (matmul_nt, (1, 16384, 16384, "float16", "float16", "float16"), Matmul),
    (matmul_nt, (16, 16384, 16384, "float16", "float16", "float16"), Matmul),
    (matmul_nt, (32, 16384, 16384, "float16", "float16", "float16"), Matmul),
    (matmul_nt, (64, 16384, 16384, "float16", "float16", "float16"), Matmul),
    (matmul_nt, (128, 16384, 16384, "float16", "float16", "float16"), Matmul),
    (matmul_nt, (256, 16384, 16384, "float16", "float16", "float16"), Matmul),
    (matmul_nt, (512, 16384, 16384, "float16", "float16", "float16"), Matmul),
    (matmul_nt, (16384, 16384, 16384, "float16", "float16", "float16"), Matmul),
    (matmul_nt_propagate_b, (1, 16384, 16384, "float16", "float16", "float16"), Matmul),
    (matmul_nt_propagate_b, (16, 16384, 16384, "float16", "float16", "float16"), Matmul),
    (matmul_nt_propagate_b, (32, 16384, 16384, "float16", "float16", "float16"), Matmul),
    (matmul_nt_propagate_b, (64, 16384, 16384, "float16", "float16", "float16"), Matmul),
    (matmul_nt_propagate_b, (128, 16384, 16384, "float16", "float16", "float16"), Matmul),
    (matmul_nt_propagate_b, (256, 16384, 16384, "float16", "float16", "float16"), Matmul),
    (matmul_nt_propagate_b, (512, 16384, 16384, "float16", "float16", "float16"), Matmul),
    (matmul_nt_propagate_b, (16384, 16384, 16384, "float16", "float16", "float16"), Matmul),
    (matmul_nt_propagate_a_propagate_b, (16, 16384, 16384, "float16", "float16", "float16"),
     Matmul),
    (matmul_nt_propagate_a_propagate_b, (32, 16384, 16384, "float16", "float16", "float16"),
     Matmul),
    (matmul_nt_propagate_a_propagate_b, (64, 16384, 16384, "float16", "float16", "float16"),
     Matmul),
    (matmul_nt_propagate_a_propagate_b, (128, 16384, 16384, "float16", "float16", "float16"),
     Matmul),
    (matmul_nt_propagate_a_propagate_b, (256, 16384, 16384, "float16", "float16", "float16"),
     Matmul),
    (matmul_nt_propagate_a_propagate_b, (512, 16384, 16384, "float16", "float16", "float16"),
     Matmul),
    (matmul_nt_propagate_a_propagate_b, (16384, 16384, 16384, "float16", "float16", "float16"),
     Matmul),
]

group_size = 128
with_scaling = False
with_zeros = False
zeros_mode = "original"
# fmt:off
llm_shape_fp16xint4 = [
    (matmul_nt_dequantize_b, (1, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (16, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (32, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (64, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (128, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (256, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (512, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b,
     (16384, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
]

group_size = 128
with_scaling = True
with_zeros = False
zeros_mode = "original"
# fmt:off
llm_shape_fp16xint4_with_scaling = [
    (matmul_nt_dequantize_b, (1, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (16, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (32, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (64, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (128, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (256, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (512, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b,
     (16384, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
]

group_size = -1
with_scaling = True
with_zeros = True
zeros_mode = "original"
# fmt:off
llm_shape_fp16xint4_with_scaling_zeros_original = [
    (matmul_nt_dequantize_b, (1, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (16, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (32, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (64, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (128, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (256, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (512, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b,
     (16384, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
]

group_size = -1
with_scaling = True
with_zeros = True
zeros_mode = "rescale"
# fmt:off
llm_shape_fp16xint4_with_scaling_zeros_rescale = [
    (matmul_nt_dequantize_b, (1, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (16, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (32, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (64, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (128, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (256, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (512, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b,
     (16384, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
]

group_size = -1
with_scaling = True
with_zeros = True
zeros_mode = "quantized"
# fmt:off
llm_shape_fp16xint4_with_scaling_zeros_quantized = [
    (matmul_nt_dequantize_b, (1, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (16, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (32, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (64, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (128, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (256, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (512, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b,
     (16384, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
]

group_size = 128
with_scaling = True
with_zeros = True
zeros_mode = "original"
# fmt:off
llm_shape_fp16xint4_with_scaling_zeros_original_g128 = [
    (matmul_nt_dequantize_b, (1, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (16, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (32, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (64, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (128, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (256, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (512, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b,
     (16384, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
]

group_size = 128
with_scaling = True
with_zeros = True
zeros_mode = "rescale"
# fmt:off
llm_shape_fp16xint4_with_scaling_zeros_rescale_g128 = [
    (matmul_nt_dequantize_b, (1, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (16, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (32, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (64, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (128, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (256, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (512, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b,
     (16384, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
]

group_size = 128
with_scaling = True
with_zeros = True
zeros_mode = "quantized"
# fmt:off
llm_shape_fp16xint4_with_scaling_zeros_quantized_g128 = [
    (matmul_nt_dequantize_b, (1, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (16, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (32, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (64, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (128, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (256, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (512, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b,
     (16384, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
]

group_size = 128
with_scaling = True
with_zeros = True
zeros_mode = "original"
# fmt:off
llm_shape_fp16xint4_with_scaling_zeros = [
    (matmul_nt_dequantize_b, (1, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (16, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (32, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (64, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (128, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (256, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b, (512, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
                              with_scaling, with_zeros, group_size, True, False, zeros_mode),
     Matmul),
    (matmul_nt_dequantize_b,
     (16384, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
]

group_size = 128
with_scaling = False
with_zeros = False
zeros_mode = "original"
llm_shape_fp16xint4_propagate_b = [
    # (matmul_nt_dequantize_b_propagate_b, (1, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
    #                           with_scaling, with_zeros, group_size, True, False, zeros_mode), Matmul),
    (matmul_nt_dequantize_b_propagate_b,
     (16, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
    # (matmul_nt_dequantize_b_propagate_b, (32, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
    #                           with_scaling, with_zeros, group_size, True, False, zeros_mode), Matmul),
    # (matmul_nt_dequantize_b_propagate_b, (64, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
    #                           with_scaling, with_zeros, group_size, True, False, zeros_mode), Matmul),
    # (matmul_nt_dequantize_b_propagate_b, (128, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
    #                           with_scaling, with_zeros, group_size, True, False, zeros_mode), Matmul),
    # (matmul_nt_dequantize_b_propagate_b, (256, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
    #                           with_scaling, with_zeros, group_size, True, False, zeros_mode), Matmul),
    # (matmul_nt_dequantize_b_propagate_b, (512, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
    #                           with_scaling, with_zeros, group_size, True, False, zeros_mode), Matmul),
    # (matmul_nt_dequantize_b_propagate_b, (16384, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint",
    #                           with_scaling, with_zeros, group_size, True, False, zeros_mode), Matmul),
]

group_size = 128
with_scaling = True
with_zeros = False
zeros_mode = "original"
llm_shape_fp16xint4_propagate_b_with_scaling = [
    (matmul_nt_dequantize_b_propagate_b,
     (1, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling, with_zeros,
      group_size, True, False, zeros_mode), Matmul),
    (matmul_nt_dequantize_b_propagate_b,
     (16, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
    (matmul_nt_dequantize_b_propagate_b,
     (32, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
    (matmul_nt_dequantize_b_propagate_b,
     (64, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
    (matmul_nt_dequantize_b_propagate_b,
     (128, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
    (matmul_nt_dequantize_b_propagate_b,
     (256, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
    (matmul_nt_dequantize_b_propagate_b,
     (512, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
    (matmul_nt_dequantize_b_propagate_b,
     (16384, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
]

group_size = 128
with_scaling = True
with_zeros = True
zeros_mode = "original"
llm_shape_fp16xint4_propagate_b_with_scaling_zeros = [
    (matmul_nt_dequantize_b_propagate_b,
     (1, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling, with_zeros,
      group_size, True, False, zeros_mode), Matmul),
    (matmul_nt_dequantize_b_propagate_b,
     (16, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
    (matmul_nt_dequantize_b_propagate_b,
     (32, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
    (matmul_nt_dequantize_b_propagate_b,
     (64, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
    (matmul_nt_dequantize_b_propagate_b,
     (128, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
    (matmul_nt_dequantize_b_propagate_b,
     (256, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
    (matmul_nt_dequantize_b_propagate_b,
     (512, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
    (matmul_nt_dequantize_b_propagate_b,
     (16384, 16384, 16384, "float16", "float16", "float16", 4, "int8", "uint", with_scaling,
      with_zeros, group_size, True, False, zeros_mode), Matmul),
]

# fmt:on

target = tvm.target.Target(args.target)
benchmark_sets = []
for benchmark_set in args.benchmark_sets:
    benchmark_sets.extend(eval(benchmark_set))
benchmark_results = {}

for get_prim_func, input_args, d_schedule in benchmark_sets:
    ir_module = get_prim_func(*input_args)
    func = ir_module["main"]
    arch = CUDA(target)
    policy = DefaultPolicy(func=func, arch=arch)
    try:
        tensorized_func, tags = get_tensorized_func_and_tags(func, arch.target)
    except Exception:
        tags = None
    if tags:
        policy = TensorCorePolicy(func=tensorized_func, arch=arch, tags=tags)

    configs = policy.emit_config(20)
    tune_start = time.time()
    cpresults, best = apply_and_build(func, configs, arch, parallel_build=True)
    fast_tune_time = time.time() - tune_start
    print(best.code)
    print("[BitBLAS] The best latency of top 1 is {:.3f} ms".format(cpresults[0].latency))
    print("[BitBLAS] The best latency of top 20 is {:.3f} ms".format(best.latency))

    # evaluate the performance of the default schedule

    rule = d_schedule()
    default_tune_start = time.time()
    with arch.target:
        mod = bitblas.ApplyDefaultSchedule(  # pylint: disable=not-callable
            bitblas.gpu.Matmul(),
            bitblas.gpu.GEMV(),
            bitblas.gpu.Reduction(),
            bitblas.gpu.GeneralReduction(),
            bitblas.gpu.Fallback(),
        )(
            ir_module)
    try:
        with tvm.transform.PassContext(config={"tir.use_async_copy": True}):
            mod_default = tvm.build(mod, target="cuda")
    except Exception:
        mod_default = None

    default_tune_time = time.time() - default_tune_start

    args = func.buffer_map.values()

    profile_tensors = best.profile_tensors
    if mod_default is not None:
        timer_cuda_mod = mod_default.time_evaluator(mod_default.entry_name, arch.device, number=5)
        t = timer_cuda_mod(*profile_tensors).mean
    else:
        t = 1e4 - 1

    print("Time cost of BitBLAS default schedule: {:.3f} ms".format(t * 1e3))

    profile_config = {
        f"{get_prim_func.__name__}-{'-'.join([str(i) for i in input_args])}": {
            "fast_bitblas_top20_tune_time": fast_tune_time,
            "fast_bitblas_top1_latency": cpresults[0].latency,
            "fast_bitblas_top20_latency": best.latency,
            "default_bitblas_tune_time": default_tune_time,
            "default_bitblas_latency": t * 1e3 if t is not None else "Failed",
        }
    }

    benchmark_results.update(profile_config)

headers = [
    "PrimFunc",
    "Input Arguments",
    "BitBLAS Top20 Tune Time",
    "BitBLAS Top1 Latency",
    "BitBLAS Top20 Latency",
    "DefaultDLight Tune Time",
    "DefaultDLight Latency",
]

col_width = (max(len(word) for row in [headers] + list(profile_config.values()) for word in row) + 2
            )  # padding

print("".join(word.ljust(col_width) for word in headers))

print("-" * col_width * len(headers))

for config, values in benchmark_results.items():
    args = config.split("-")
    func_name = args[0]
    input_args = "-".join(args[1:])
    row = [
        func_name,
        input_args,
        f" {str(values['fast_bitblas_top20_tune_time'])} s",
        f"{values['fast_bitblas_top1_latency']:.3f} ms",
        f"{values['fast_bitblas_top20_latency']:.3f} ms",
        str(values["default_bitblas_tune_time"]),
        f"{values['default_bitblas_latency']:.3e} ms",
    ]
    print("".join(word.ljust(col_width) for word in row))
