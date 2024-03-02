from glob import glob
test = '1709351507'
print(test[:7])

for fp in glob(f'events/{test[:7]}*.jpg'):
  print(fp)