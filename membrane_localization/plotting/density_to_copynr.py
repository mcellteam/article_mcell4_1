import pandas as pd
import sys

if len(sys.argv) != 3:
    sys.exit("Expected input and output file")

df = pd.read_csv(sys.argv[1], delim_whitespace=True)


df = df.set_index('t')

area = 0.47 * 0.47 
df['MA'] = df['MA'] * area



df.to_csv(sys.argv[2], sep=' ')
