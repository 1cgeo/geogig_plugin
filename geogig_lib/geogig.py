# -*- coding: utf-8 -*-
import re
import tempfile
import datetime
import subprocess
import os
import psycopg2

class Repository:
    def __init__(self,host,port,database,schema,repository,user,password, geogigPath, logger=False):
        self.logger = logger
        self.geogigPath = geogigPath 
        self.repoUrl = u"postgresql://{}:{}/{}/{}/{}?user={}&password={}".format(host,port,database,schema,repository,user,password)
        self.branches = {}
        try:
            command = u'{0} --repo "{1}" branch'.format(self.geogigPath, self.repoUrl)
            result = subprocess.check_output(command,shell=True)
            branch_names = [x.strip().replace(u'* ', u'') for x in result.split('\n')][:-1 ]
            for name in branch_names:
                self.branches[name] = Branch(name,self.geogigPath,self.repoUrl, self.logger)
        except subprocess.CalledProcessError as e:
            self.logger.error(e.output) if self.logger else ''
 
    def config(self,username,email):
        try:
            command = u'{0} --repo "{1}" config --global user.name {2}'.format(self.geogigPath, self.repoUrl, username)
            subprocess.check_output(command,shell=True)
            command = u'{0} --repo "{1}" config --global user.email {2}'.format(self.geogigPath, self.repoUrl, email)
            subprocess.check_output(command,shell=True)
            self.logger.debug(u"CONFIG REPOSITORY") if self.logger else '' 
        except subprocess.CalledProcessError as e:
            self.logger.error(e.output) if self.logger else ''
            
    def init(self):
        try:
            command = u'{0} --repo "{1}" init'.format(self.geogigPath, self.repoUrl)
            result = subprocess.check_output(command,shell=True)
            self.branches[u'master'] = Branch(u'master',self.geogigPath,self.repoUrl)
            return result
        except subprocess.CalledProcessError as e:
            self.logger.error(e.output) if self.logger else ''

    def clone(self,host,port,database,schema,repository,user,password,branchName):
        try:
            dest = u"postgresql://{}:{}/{}/{}/{}?user={}&password={}".format(host,port,database,schema,repository,user,password)
            command = u'{0} clone "{1}" "{2}" --branch {3}'.format(self.geogigPath, self.repoUrl, dest, branchName)
            result = subprocess.check_output(command,shell=True,universal_newlines=True)
            self.logger.debug(u"Clone - repository_origin : {0}, repository_dest : {1}".format(self.repoUrl, dest)) if self.logger else ''
            return result
        except subprocess.CalledProcessError as e:
            self.logger.error(e.output) if self.logger else ''

    def compara_schema(self,host,port,database,schema,user,password):
        layers = []
        try:
            command = u'{0} --repo "{1}" ls {2}'.format(self.geogigPath, self.repoUrl, schema)
            result = subprocess.check_output(command,shell=True)
            layers = [x.replace('/', '').strip() for x in result.split('\n') if x.strip() != ''][1:]
            strCon = u"dbname={0} user={1} password={2} host={3} port={4}".format(database, user, password, host, port)
            query=u"select array_agg(table_name::text || '/' || column_name::text) from INFORMATION_SCHEMA.COLUMNS where table_schema = 'edgv' and table_name in ('{0}')".format(u"','".join(layers))
            con = psycopg2.connect(strCon)
            con.autocommit=True
            cur = con.cursor()
            cur.execute(query)
            db_list=cur.fetchall()
            con.close()
            geogig_list = []
            for layer in layers:
                commandIn = u'{0} --repo "{1}" show HEAD:{2}/{3}'.format(self.geogigPath, self.repoUrl, schema, layer)
                result = subprocess.check_output(commandIn,shell=True)
                geogig_list =  geogig_list + [layer+'/'+x.split(':')[0] for x in result.split('\n\n')[1].split('\n')[1:]]
            return set(db_list[0][0]).difference(geogig_list)
        except subprocess.CalledProcessError as e:
            self.logger.error(e.output) if self.logger else ''

    def add_branch(self,branchName,force=False):
        try:
            if(force):
                command = u'{0} --repo "{1}" branch {2} --force'.format(self.geogigPath, self.repoUrl, branchName)
            else:
                command = u'{0} --repo "{1}" branch {2}'.format(self.geogigPath, self.repoUrl, branchName)
            result = subprocess.check_output(command,shell=True,universal_newlines=True)
            msg = subprocess.STDOUT
            self.branches[branchName] = Branch(branchName,self.geogigPath,self.repoUrl)
            self.logger.debug(u"Add branch - branch_name : {0}, message : {1}".format(branchName, msg)) if self.logger else ''
            return msg
        except subprocess.CalledProcessError as e:
            self.logger.error(e.output) if self.logger else ''        

    def del_branch(self,branchName):
        try:
            command = u'{0} --repo "{1}" branch --delete {2}'.format(self.geogigPath, self.repoUrl, branchName)
            result = subprocess.check_output(command,shell=True,universal_newlines=True)
            del self.branches[branchName]
            self.logger.debug(u"Delete branch - branch_name : {0}".format(branchName)) if self.logger else ''
        except subprocess.CalledProcessError as e:
            self.logger.error(e.output) if self.logger else ''   

    def getConfigRepository(self):
        config = {}
        command = u'{0} --repo "{1}" config --list'.format(self.geogigPath, self.repoUrl)
        result = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
        for item in [x for x in result.split('\n') if x.strip()!= '']:
            key = item.split('=')[0]
            value = item.split('=')[1]
            config[key]=value
        if(config['user.email']!=''):
            self.logger.error(u'Repository not configured') if self.logger else ''
    
    def merge_abort(self):
        try:
            abort_merge = u'{0} --repo "{1}" merge --abort'.format(self.geogigPath, self.repoUrl)
            abort_merge_run = subprocess.check_output(abort_merge,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
            self.logger.debug(u"Merge abort") if self.logger else ''
        except subprocess.CalledProcessError as e:
            self.logger.error(e.output) if self.logger else ''

    def clean_staging_area(self):
        try:
            command = u'{0} --repo "{1}" reset --hard'.format(self.geogigPath, self.repoUrl)
            result = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
            self.logger.debug(u"Clean staging area") if self.logger else ''
        except subprocess.CalledProcessError as e:
            self.logger.error(e.output) if self.logger else ''   
        
    def show_resume_commit_by_tag(self, tag):
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
        self.logger.debug(u"Resume {0} : \n{1}".format(tag, resume)) if self.logger else ''       

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

    def add(self,layer=None):
        self.__checkout()
        if layer == None:
            try:
                command = u'{0}  --repo "{1}" add'.format(self.geogigPath, self.repoUrl)
                result =  subprocess.check_output(command,shell=True,universal_newlines=True)
                self.logger.debug(u"Add - repository : {0}".format(self.repoUrl)) if self.logger else ''
                return result
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
                    values[layer[idx]] = line.split("\t")[1]
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
        attributes = [attribute.split(":")[0] for attribute in attribute_list.split("\n")[1:]]
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
                        conflict_parts = conflict_parts.strip()
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
        self.logger.debug(u"Init import - database : {0}, user : {1}".format(database, user)) if self.logger else ''
        for layer in layers:
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
                self.logger.debug(u"Import - database : {0}, layer: {1}, user : {2}".format(database, layer, user)) if self.logger else ''
            except subprocess.CalledProcessError as e:
                self.logger.error(e.output) if self.logger else ''
        self.logger.debug(u"Finished import - database : {0}, user : {1}".format(database, user)) if self.logger else ''

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
            for layer in layers:
                commandIn = u'{0}  --repo "{1}" pg export --schema {3} --host {4} --port {5} --database {6}  --user {7} --password {8} HEAD:{3}/{2} {2} --overwrite'.format(
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
                self.logger.debug(u"Export - database : {0}, layer: {1}, user : {2}".format(database, layer, user)) if self.logger else ''
            self.logger.debug(u"Finished export - database : {0}, user : {1}".format(database, user)) if self.logger else ''
            strCon = u"dbname={0} user={1} password={2} host={3} port={4}".format(database, user, password, host, port)
            con = psycopg2.connect(strCon)
            con.autocommit=True
            cur = con.cursor()
            emptyLayers = set(layersInDb).difference(layers)
            for layer in emptyLayers:
                self.logger.info(u"excluindo os registros de {0}".format(layer)) if self.logger else ''
                cur.execute(u"DELETE FROM {}.{};".format(schema,layer))
            cur.close()
            con.close()
        except subprocess.CalledProcessError as e:
            self.logger.error(e.output) if self.logger else ''
            return e
    
    def status(self):
        self.__checkout()
        command = u'{0}  --repo "{1}" status'.format(self.geogigPath, self.repoUrl)
        result =  subprocess.check_output(command,shell=True)
        self.logger.debug(u"Status : {0}".format(result)) if self.logger else ''
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
    