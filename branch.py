# -*- coding: utf-8 -*-
from osgeo import ogr
import subprocess, psycopg2, os, datetime, sys, re, tempfile, time
from utils import progressbar
import multiprocessing
from multiprocessing import Queue, Manager

class Branch(object):
    def __init__(self,branchName, geogigPath, repoUrl, logger=False):
        self.logger = logger
        self.name = branchName
        self.geogigPath = geogigPath
        self.repoUrl = repoUrl
        self.conflicts = []

    def __checkout(self):
        command = u'{0}  --repo "{1}" status'.format(self.geogigPath, self.repoUrl)
        result =  subprocess.check_output(command,shell=True).split('\n')[0]
        active_branch = result.replace(u'# On branch ',u'')
        if active_branch != self.name:
            try:
                commandIn = u'{0}  --repo "{1}" checkout {2}'.format(self.geogigPath, self.repoUrl, self.name)
                subprocess.call(commandIn,shell=True)
                self.logger.debug(u"Checkout - username : {0}".format(self.name)) if self.logger else ''
            except subprocess.CalledProcessError as e:
                self.logger.error(e.output) if self.logger else ''

    def add(self, layers_table=False):
        self.__checkout()
        if layers_table:
            for layer_path in layers_table:
                command = u'{0}  --repo "{1}" add {2}'.format(self.geogigPath, self.repoUrl, layer_path)
                msg = u"Added on repository - layer path : {0}".format(layer_path)
                try:
                    result =  subprocess.check_output(command,shell=True,universal_newlines=True)
                    self.logger.debug(msg) if self.logger else ''
                except subprocess.CalledProcessError as e:
                        self.logger.error(e.output) if self.logger else ''
        else:
            command = u'{0}  --repo "{1}" add'.format(self.geogigPath, self.repoUrl)
            try:
                result =  subprocess.check_output(command,shell=True,universal_newlines=True)
                self.logger.debug(u"All layer added on repository") if self.logger else ''
            except subprocess.CalledProcessError as e:
                    self.logger.error(e.output) if self.logger else ''            

    def push(self,branchName):
        self.__checkout()
        try:
            command = u'{0}  --repo "{1}" push origin {2}'.format(self.geogigPath, self.repoUrl, branchName)
            result=subprocess.check_output(command,shell=True)
            self.logger.debug(u"Push - repository : {0}, origin : {1}".format(self.repoUrl, branchName)) if self.logger else ''
            return result
        except subprocess.CalledProcessError as e:
                self.logger.error(e.output) if self.logger else ''
    
    def pull(self,branchName):
        self.__checkout()
        try:
            command = u'{0}  --repo "{1}" pull origin {2}'.format(self.geogigPath, self.repoUrl, branchName)
            result = subprocess.check_output(command,shell=True)
            self.logger.debug(u"Pull - repository : {0}, origin : {1}".format(self.repoUrl, branchName)) if self.logger else ''
            return result
        except subprocess.CalledProcessError as e:
            self.logger.error(e.output) if self.logger else ''
            return e

    def log(self,param=None):
        self.__checkout()
        if not(param):
            command = u'{0}  --repo "{1}" log'.format(self.geogigPath, self.repoUrl)
            self.logger.debug(u"Log - repository : {0}".format(self.repoUrl)) if self.logger else ''
        try:
            result = subprocess.check_output(command,shell=True)
        except subprocess.CalledProcessError as e:
            self.logger.error(e.output) if self.logger else ''
            return
        logs = []
        aux = {}
        for line in [x for x in result.split('\n') if x.strip()!= '']:
            if line.find(u'Commit') > -1:
                if u'commit' in aux:
                    logs.append(aux)
                    aux = {}
                aux[u'commit'] = line.split(':')[1].strip()

            if line.find(u'Author') > -1:
                    aux[u'author'] = line.split(':')[1].strip()
            if line.find(u'Subject') > -1:
                    aux[u'subject'] = line.split(':')[1].strip()
            if line.find(u'Date') > -1:
                    aux[u'date'] = ':'.join(line.split(':')[1:]).strip()
            if line.find(u'Merge') > -1:
                    aux[u'Merge'] = line.split(':')[1].strip()
        logs.append(aux)
        return logs
        
    def parse_feature(self, feature, layer):
        values = {}
        if u"FEATURE" in feature:
            value_part = feature.split(u"FEATURE")[1]
            for idx, line in enumerate(value_part.split("\n")[1:]):
                if len(line.split("\t")) > 1:
                    values[layer[idx]] = line.split("\t")[1].decode('utf-8')
                else:
                    self.logger.error(u"Error parse feature {0} {1}".format(idx, line)) if self.logger else ''
        else:
            for att in layer:
                values[att]= u"DELETADO"
        return values

    def getFeatureType(self, layer):
        command = u'{0}  --repo "{1}" show {2}'.format(self.geogigPath, self.repoUrl, layer)
        result = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
        attribute_list = result.split("\n\n")[1]
        attributes = [attribute.split(":")[0].decode(u'utf-8') for attribute in attribute_list.split("\n")[1:]]
        return attributes

    def conflicts_list(self):
        try:
            command = u'{0}  --repo "{1}" conflicts'.format(self.geogigPath, self.repoUrl)
            result = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
            self.logger.debug(u"Conflicts - repository : {0}".format(self.repoUrl)) if self.logger else ''
            self.conflicts =  result.split('\n\n')
            if(self.conflicts):
                conflicts = []
                aux = {}
                feature_type = {}
                current_feature = ""
                for idx, conflict_parts in enumerate(self.conflicts):
                    if(idx%4 == 0):
                        conflict_parts = conflict_parts.strip().decode('utf-8')
                        current_feature = u"/".join(conflict_parts.split("/")[0:2])
                        if current_feature not in feature_type and current_feature != '':
                            feature_type[current_feature] = self.getFeatureType(current_feature)
                        aux["camada"] = conflict_parts.strip()
                    elif(idx%4 == 1):
                        aux["ancestor"] = self.parse_feature(conflict_parts, feature_type[current_feature])
                    elif(idx%4 == 2):
                        aux["ours"] = self.parse_feature(conflict_parts, feature_type[current_feature])
                    elif(idx%4 == 3):
                        aux["theirs"] = self.parse_feature(conflict_parts, feature_type[current_feature])
                        conflicts.append(aux)
                        aux = {}
            return conflicts
        except subprocess.CalledProcessError as e:
            abort_merge = u'{0}  --repo "{1}"  merge --abort'.format(self.geogigPath, self.repoUrl)
            abort_merge_run = subprocess.check_output(abort_merge,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
            self.logger.debug(u"Merge abort") if self.logger else ''
            self.logger.error(e.output) if self.logger else ''
            return

    def merge(self,branchName):
        self.__checkout()
        try:
            command = u'{0}  --repo "{1}" merge {2}'.format(self.geogigPath, self.repoUrl, branchName)
            result = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
            self.logger.debug(u"Merge - repository : {0}, branch : {1}".format(self.repoUrl, branchName)) if self.logger else ''
        except subprocess.CalledProcessError as e:
            if (u"CONFLICT" in e.output):
                conflicts = self.conflicts_list()
                return conflicts
            elif u"The branch has already been merged." in e.output:
                return u"Success"
            else:
                self.logger.error(e.output) if self.logger else ''
                return e
        else:
            return u"Success"
    
    def clean_staging_area(self):
        self.__checkout()
        try:
            command = u'{0} --repo "{1}" reset --hard'.format(self.geogigPath, self.repoUrl)
            result = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
            self.logger.debug(u"Clean staging area") if self.logger else ''
        except subprocess.CalledProcessError as e:
            self.logger.error(e.output) if self.logger else ''  
    
    def show_resume_commit_by_tag(self, tag):
        self.__checkout()
        cmd = u'{0}  --repo "{1}" log'.format(self.geogigPath, self.repoUrl)
        result = subprocess.check_output(cmd,shell=True,stderr=subprocess.STDOUT)
        date_line = u""
        subject_line = u""
        resume = u""
        count = 1
        for line in result.split('\n'):
            if u'date' in line.lower():
                date_line = line
            if u'subject'.lower() in line.lower() and tag.lower() in line.lower():
                subject_line = line
            if subject_line and date_line:
                resume += u"#{0:5} -- {1:30} -- {2:30}\n".format(count, date_line, subject_line)
                count +=1
                data_line = subject_line = ''
        resume = u'\n'.join(resume.split('\n')[:10])
        self.logger.debug(u"**RESUME {0} : \n{1}".format(tag.upper(), resume.upper())) if self.logger else ''
        
    def get_pg_cursor(self, host,port,database,user,password):
        conn = psycopg2.connect(
            u"""dbname='{0}' user='{1}' host='{2}' port='{3}' password='{4}'""".format(
                database, 
                user, 
                host, 
                port, 
                password
            )
        )
        return conn.cursor()
    
    def get_first_uuid(self):
        try:
            command = u'{0} --repo "{1}" log --oneline'.format(self.geogigPath, self.repoUrl)
            result = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
            head_uuid = result.split(' ')[0]
            return head_uuid
        except subprocess.CalledProcessError as e:
            self.logger.debug(u"Erro on get first uuid!") if self.logger else ''
            self.logger.error(e.output) if self.logger else ''


    def isEqualHEADs(self, host,port,database,user,password):
        #self.__checkout()
        #head_uuid = self.get_first_uuid()
        #pg_cursor = self.get_pg_cursor(host,port,database,user,password)
        #pg_cursor.execute(u"select commit_uuid from aux_geogig ;")
        #db_uuid = pg_cursor.fetchall()[0][0].strip()
        #pg_cursor.close()
        #return head_uuid == db_uuid
        return True
    
    def insert_uuid_on_db(self, host,port,database,user,password, op_type):
        self.__checkout()
        self.clean_table_on_db()
        head_uuid = self.get_first_uuid()
        pg_cursor = self.get_pg_cursor(host,port,database,user,password)
        pg_cursor.execute(u"INSERT INTO public.aux_geogig VALUES('{0}', '{1}');".format(op_type, head_uuid))
        pg_cursor.close()
        self.logger.debug(u"Inserting UUID on database!") if self.logger else ''

    def clean_table_on_db(self):
        pg_cursor = self.get_pg_cursor(host,port,database,user,password)
        pg_cursor.execute(u'DELETE FROM public.aux_geogig;')
        pg_cursor.close()
        self.logger.debug(u"Clean UUID on database!") if self.logger else ''

    def pg_import_layer(self, layer, schema, host, port, database, user, password):
        try:
            commandIn = u'{0}  --repo "{1}" pg import --table {2} -d {3}/{2} --schema {3} --host {4} --port {5} --database {6}  --user {7} --password {8} --force-featuretype'.format(
                self.geogigPath, 
                self.repoUrl, 
                layer, 
                schema, 
                host, 
                port, 
                database, 
                user, 
                password
            ) 
            result = subprocess.check_output(commandIn,shell=True)    
            self.logger.debug(u"Import - database : {0}, layer: {1}, user : {2}".format(database, layer, self.name)) if self.logger else ''
        except subprocess.CalledProcessError as e:
            self.logger.debug(u"REPLAY - Import - database : {0}, layer: {1}, user : {2}".format(database, layer, self.name)) if self.logger else ''
            self.pg_import_layer(layer, schema, host, port, database, user, password)

    def pg_import_schema(self,host,port,database,schema,user,password):
        self.__checkout()
        command = u'{0}  --repo "{1}" pg list --host {2} --port {3} --database {4} --schema {5} --user {6} --password {7}'.format(
            self.geogigPath, 
            self.repoUrl, 
            host, 
            port, 
            database, 
            schema, 
            user, 
            password
        )
        result = subprocess.check_output(command,shell=True)
        layers = [x.replace(u'-', u'').strip() for x in result.split('\n') if x.strip() != ''][1:]
        self.logger.debug(u"Init import - database : {0}, user : {1}".format(database, self.name)) if self.logger else ''
        list_data = []
        for layer in layers:
            self.pg_import_layer(layer, schema, host, port, database, user, password)
        self.logger.debug(u"Finished import - database : {0}, user : {1}".format(database, self.name)) if self.logger else ''
    
    def clean_records(self, host,port,database,user,password,schema,layersInDb,layers):
        cursor = self.get_pg_cursor(host,port,database,user,password)
        emptyLayers = set(layersInDb).difference(layers)
        for layer in emptyLayers:
            cursor.execute(u"DELETE FROM {}.{};".format(schema,layer))
            self.logger.info(u"REGISTRATION EXCLUDED : {0}".format(layer)) if self.logger else ''
        cursor.close()

    def pg_export_layer(self, layer, schema, host, port, database, user, password):
        try:
            cmd = u'{0}  --repo "{1}" pg export --schema {3} --host {4} --port {5} --database {6}  --user {7} --password {8} HEAD:{3}/{2} {2} --overwrite'.format(
                self.geogigPath, 
                self.repoUrl, 
                layer, 
                schema, 
                host, 
                port, 
                database, 
                user, 
                password
            )  
            result = subprocess.check_output(cmd,shell=True)    
            self.logger.debug(u"Exported - database : {0}, layer: {1}, user : {2}".format(database, layer, self.name)) if self.logger else ''
        except subprocess.CalledProcessError as e:
            self.logger.error(e.output) if self.logger else ''

    def pg_export_schema(self,host,port,database,schema,user,password):
        self.__checkout()
        layers = []
        try:
            listLayersInDb = u'{0}  --repo "{1}" pg list --host {2} --port {3} --database {4} --schema {5} --user {6} --password {7}'.format(
                self.geogigPath, 
                self.repoUrl, 
                host, 
                port, 
                database, 
                schema, 
                user, 
                password
            )
            result = subprocess.check_output(listLayersInDb,shell=True)
            layersInDb = [x.replace('-', '').strip() for x in result.split('\n') if x.strip() != ''][1:]
            command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' ls '+schema 
            result = subprocess.check_output(command,shell=True)
            layers = [x.replace('/', '').strip() for x in result.split('\n') if x.strip() != ''][1:]
            self.logger.debug(u"Init export - database : {0}, user : {1}".format(database, user)) if self.logger else ''
            list_data = []
            for layer in layers:
                self.pg_export_layer(layer, schema, host, port, database, user, password)
            self.logger.debug(u"Finished export - database : {0}, user : {1}".format(database, user)) if self.logger else ''
            self.clean_records(host,port,database,user,password,schema,layersInDb,layers)
        except subprocess.CalledProcessError as e:
            self.logger.error(e.output) if self.logger else ''
            return e
    
    def status(self):
        self.__checkout()
        command = u'{0}  --repo "{1}" status'.format(self.geogigPath, self.repoUrl)
        result =  subprocess.check_output(command,shell=True)
        return result
    
    def commit(self,msg):
        self.__checkout()
        command = u'{0}  --repo "{1}" commit -m "{2}"'.format(self.geogigPath, self.repoUrl, msg)
        try:
            result = subprocess.check_output(command,shell=True)
        except subprocess.CalledProcessError as exc:
            if ("Nothing to commit" in exc.output):
                result = "Nothing to commit"
            else:
                self.logger.error(exc.output) if self.logger else ''
        self.logger.debug(u"Commit : {0}".format(result)) if self.logger else ''
        return result

    def merge_features(self, decisionDict):
        for feat, decision in decisionDict.iteritems():
            command = u'{0} --repo "{1}" checkout --path {2} --{3}'.format(self.geogigPath, self.repoUrl, feat, decision)
            result = subprocess.check_output(command,shell=True)
            self.logger.debug(u"Checkout - feature : {0}, decision : {1}".format(feat, decision)) if self.logger else ''
            addCommand = u'{0} --repo "{1}" add {2}'.format(self.geogigPath, self.repoUrl, feat)
            result = subprocess.check_output(addCommand,shell=True)
            self.logger.debug(u"Add - repository : {0}, feature : {1}".format(self.repoUrl, feat)) if self.logger else ''

    def show_resume_spatial_test(self, approved_layers_paths , repproved_layers_paths):
        self.logger.debug(u"***RESULT TEST SPATIAL***") if self.logger else ''
        print_approved = u"\n".join([ u"{} - {}".format(row[0], row[1]) for row in approved_layers_paths])
        print_repproved = u"\n".join([ u"{} - {}".format(row[0], row[1]) for row in repproved_layers_paths])
        self.logger.debug(u'LAYERS APPROVED BRANCH : {0} : \n{1}'.format(self.name, print_approved)) if self.logger and print_approved else ''
        self.logger.debug(u'LAYERS REPPROVED BRANCH : {0} : \n{1}'.format(self.name, print_repproved)) if self.logger and print_repproved else ''

    def get_frames(self, host,port,database,user,password):
        pg_cursor = self.get_pg_cursor(host,port,database,user,password)
        pg_cursor.execute('select mi, st_asewkt(geom) from edgv.aux_moldura_a;')
        workspaces = { data[0].strip() : data[1].split(';')[1].strip() for data in pg_cursor.fetchall() }
        pg_cursor.close()
        return  [ ogr.CreateGeometryFromWkt(workspaces[key]) for key in workspaces if self.name in key.lower()]

    def spatial_test(self, host,port,database,user,password):
        self.__checkout()
        self.logger.debug(u"Loading data to spatial test...") if self.logger else ''
        frames = self.get_frames(host,port,database,user,password)
        table_without_wkt = self.get_all_data_staging_work()
        self.logger.debug(u"Data loaded!") if self.logger else ''
        self.logger.debug(u"Initiating space test ...") if self.logger else ''
        approved_layers_paths = []
        repproved_layers_paths = []
        all_lyrs = len(table_without_wkt)
        for i, row in enumerate(table_without_wkt):
            wkt = self.get_wkt(row[-2], row[-1])
            is_approved = False
            for frame in frames:
                if frame.Intersects(ogr.CreateGeometryFromWkt(wkt)):
                    approved_layers_paths.append([row[0], row[3]])
                    is_approved = True
            if not(is_approved):
                repproved_layers_paths.append([row[0], row[3]])
            msg = u"{2}# Geometry : {0} , status : {1}".format(row[3], u"APPROVED" if is_approved else u"REPPROVED", i)
            self.logger.debug(msg) if self.logger else ''
        msg = u"Completed spatial test - result - Approved : {0}, Reproved : {1}, Total : {2}".format(
                len(approved_layers_paths), 
                len(repproved_layers_paths), 
                len(table_without_wkt)
            )
        self.logger.debug(msg) if self.logger else ''
        self.show_resume_spatial_test(approved_layers_paths , repproved_layers_paths)
        return approved_layers_paths , repproved_layers_paths 

    def get_wkt(self, layer_path, locate):
        cmd = '{0} --repo "{1}" show {2}{3}'.format(self.geogigPath, self.repoUrl, locate, layer_path)
        result = subprocess.check_output(cmd, shell=True)
        for line in result.split('\n'):
            if 'geom' in line:
                wkt = line.split(':')[-1].strip()
                return wkt

    def get_all_data_staging_work(self):
        cmd = '{0} --repo "{1}" status  --limit 10000000'.format(self.geogigPath, self.repoUrl)
        result = subprocess.check_output(cmd, shell=True)
        data_table = []
        data_input = result.split('\n')
        for i, line in enumerate(data_input):
            if len(line.split(' ')[-1].split('/')) >= 3:
                status =  line.split(' ')[-3]
                layer_name =  line.split(' ')[-1].strip().split('/')[1]
                fid =  line.split(' ')[-1].strip().split('/')[-1]
                layer_path =  line.split(' ')[-1].strip()
                locate = 'HEAD:' if status == 'removed' else ''
                data_table.append([status, layer_name, fid, layer_path, locate])
        self.logger.debug(u"Amount : {0}".format(len(data_table))) if self.logger else ''
        return data_table