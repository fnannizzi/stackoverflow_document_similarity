dependencies
```
nltk
```

usage
```
./cluster.py input-file density min-pts
  input-file:   each document to be processed should take exactly 3 lines as follows:
                  title
                  tags (space delimited)
                  body
                do not put whitespace/newlines between documents
  density:      range from 0.0-1.0 (0.0 = close, 1.0 = far)
  min-pts:      how many points are needed for a cluster to be formed
  ```
  
