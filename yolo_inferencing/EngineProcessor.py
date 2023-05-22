import tensorrt as trt
import pycuda.autoinit
import pycuda.driver as cuda
import numpy as np

class EngineProcessor:
    def __init__(self, engine_path):
        self.engine_path = engine_path

        self.EXPLICIT_BATCH = 1 << (int)(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
        self.TRT_LOGGER = trt.Logger(trt.Logger.ERROR)

        self.batch = 1
        self.host_inputs = []
        self.cuda_inputs = []
        self.host_outputs = []
        self.cuda_outputs = []
        self.bindings = []

    def initalize(self):
        with open(self.engine_path, 'rb') as f:
            serialized_engine = f.read()

        self.runtime = trt.Runtime(self.TRT_LOGGER)
        self.engine = self.runtime.deserialize_cuda_engine(serialized_engine)

        # create buffer
        for binding in self.engine:
            size = trt.volume(self.engine.get_binding_shape(binding)) * self.batch
            host_mem = cuda.pagelocked_empty(shape=[size], dtype=np.float32)
            cuda_mem = cuda.mem_alloc(host_mem.nbytes)

            self.bindings.append(int(cuda_mem))
            if self.engine.binding_is_input(binding):
                self.host_inputs.append(host_mem)
                self.cuda_inputs.append(cuda_mem)
            else:
                self.host_outputs.append(host_mem)
                self.cuda_outputs.append(cuda_mem)

    def deinitialize(self):
        for cuda_input in self.cuda_inputs:
            cuda_input.free()

        for cuda_output in self.cuda_outputs:
            cuda_output.free()

        self.host_inputs.clear()
        self.host_outputs.clear()

        self.engine.destroy()

    def process(self, image):


        np.copyto(self.host_inputs[0], image.ravel())
        stream = cuda.Stream()
        context = self.engine.create_execution_context()


        cuda.memcpy_htod_async(self.cuda_inputs[0], self.host_inputs[0], stream)
        context.execute_v2(self.bindings)
        cuda.memcpy_dtoh_async(self.host_outputs[0], self.cuda_outputs[0], stream)
        cuda.memcpy_dtoh_async(self.host_outputs[1], self.cuda_outputs[1], stream)
        stream.synchronize()

        output = self.host_outputs
        return output[::-1]


