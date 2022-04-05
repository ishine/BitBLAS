import tvm
from tvm import te
from .scope import get_scope
import numpy as np

@tvm.tir.transform.prim_func_pass(opt_level=0)
def debug_pass(f, mod, ctx):
    def printer(op):
        print(op, type(op))
        print("-----------------------------------------")

    tvm.tir.stmt_functor.post_order_visit(f.body, printer)
    return f

@tvm.tir.transform.prim_func_pass(opt_level=0)
def get_kernel_info_pass(f, mod, ctx):
    def process(op):
        nonlocal offset
        if isinstance(op, tvm.tir.stmt.Allocate):
            name = op.buffer_var.name
            if not name.endswith("shared"):
                return
            num_elements = np.prod(op.extents)
            num_bytes = num_elements * (int(tvm.DataType(op.dtype).bits) // 8)
            normalized_name = name.replace(".", "_")

            if normalized_name in smem_inputs_name:
                get_scope().exteral_shared_memroy_size[name[:-len(".shared")]] = num_bytes
            else:
                get_scope().interal_shared_memory_offset[normalized_name] = offset
                offset += num_bytes

    smem_inputs_name = [name + "_shared" for name in get_scope().shared_mem_inputs]
    offset = 0
    tvm.tir.stmt_functor.post_order_visit(f.body, process)
    get_scope().total_interal_shared_memory = offset
    return f
