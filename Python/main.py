import numpy as np
import chunkify as chnk
x = np.array([[1, 2, 3, 1, 2, 3], [1, 2, 3, 1, 2, 3]]).T
chunks = chnk.chunkify(x)
