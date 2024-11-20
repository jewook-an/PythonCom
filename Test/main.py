import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from common.NumpyCm import NumpyClass

numpy_utils = NumpyClass()

print(numpy_utils.create_array([1, 2, 3, 4, 5]))
