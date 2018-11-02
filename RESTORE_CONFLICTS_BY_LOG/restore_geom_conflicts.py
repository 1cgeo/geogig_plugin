import os, json, psycopg2

LOG_NAME = '20181031_22-08-54.log'

f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'logs', LOG_NAME))
data =  f.readlines()

def connectPsycopg2():
        conn = psycopg2.connect(
            u"""dbname='{0}' user='{1}' host='{2}' port='{3}' password='{4}'""".format(
                'conflitos', 
                'postgres', 
                '10.2.1.18', 
                '5432', 
                'postgres'
            )
        )
        conn.set_session(autocommit=True)
        return conn.cursor()

def export_feature(layer, data):
    values = []
    for x in data.values():
        values += ["'{0}'".format(x.decode("utf-8"))] if x else ['NULL']
    connectPsycopg2().execute(
        u"""INSERT INTO {0} ({1}) VALUES ({2});""".format(
            u"{0}.{1}".format(layer.split('/')[0], layer.split('/')[1]), 
            u",".join(data.keys()), 
            u",".join(values)
        )
    )

for line in data:
    test = line.split(':')
    if len(test) > 2 and 'layer' in test[2]:
        layer =  test[3].split(',')[0].strip()
        dat = line.split('data')[-1][2:]
        dat = dat[1:].replace('\n', '').replace("u'", "'")
        dat = dat[1:-1]
        value = u"{%s}"%(dat.replace("'", '"'))
        data = json.loads(value)
        export_feature(layer, data)