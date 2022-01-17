__version__ = '0.0.5'


from .base_pipeline import BasePipeline
from .decorators import input_pipe, process_pipe, output_pipe
from .mappers import map_object_to_namedtuple
