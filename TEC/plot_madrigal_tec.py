import pandas as pd 

def filter_hour(row, hour = 3):
    if int(row[3]) == hour:
        return True 
    else:
        return False

def framedata(lines, out):
     cols = lines[0].split()
     
 
     df = pd.DataFrame(out, columns = cols)
     df.rename(
         columns = {'MIN':'MINUTE', 
                    'SEC': 'SECOND', 
                    'GDLAT': 'lat', 
                    'GLON': 'lon'}, 
               inplace = True
               )
     df.index =pd.to_datetime(
         df[['YEAR',
          'MONTH',
          'DAY',
          'HOUR',
          'MINUTE',
          'SECOND']])
     
     df = df.drop(columns = ['YEAR',
      'MONTH',
      'DAY',
      'HOUR',
      'MINUTE',
      'SECOND', 
      'RECNO',
      'KINDAT',
      'KINST',
      'UT1_UNIX',
      'UT2_UNIX',])
     
     return df.astype(float)



def pipe_tec(path, hour = None):
    
    lines = open(path).readlines()

    out = []
    for ln in lines[1:]:
        row = ln.split() 
        
        if hour is None:
            out.append(row)
        else:
            if filter_hour(row, hour):
                
                out.append(row)
    return framedata(lines, out)

def junksave():
    for d in [16, 18, 29]:
        fn = f'gps1512{d}g.002.hdf5.txt'
        path = "E:\\database\\"
        df = pipe_tec(path + fn, hour = 22)
        
        df.to_csv(fn)