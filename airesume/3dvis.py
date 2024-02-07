import numpy as np
import plotly.express as px
import pandas as pd

z=np.array([[-4.49530104e-01,  2.91445004e-01,  3.50092946e-16],
       [-4.68583954e-01, -2.87440420e-01,  3.50092946e-16],
       [ 9.18114058e-01, -4.00458459e-03,  3.50092946e-16]])


z_df = pd.DataFrame(z, columns=['x','y','z'])

fig = px.scatter_3d(data_frame=z_df, x='x', y='y', z='z', color=['r','g','b'])

fig.show()
