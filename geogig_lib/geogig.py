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
        self.repoUrl = "postgresql://{}:{}/{}/{}/{}?user={}&password={}".format(host,port,database,schema,repository,user,password)
        self.branches = {}
        try:
            command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"' + ' branch'
            
            result = subprocess.check_output(command,shell=True)
            
            branch_names = [x.strip().replace('* ', '') for x in result.split('\n')][:-1 ]
            for name in branch_names:
                self.branches[name] = Branch(name,self.geogigPath,self.repoUrl, self.logger)
        except Exception as e:
            self.logger.error(e) if self.logger else ''
 
    def config(self,username,email):
        try:
            command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"' +' config --global user.name ' + username
            subprocess.check_output(command,shell=True)
            command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"' +' config --global user.email ' + email
            subprocess.check_output(command,shell=True)
            result = 'Atualizações realizadas com sucesso!'
            
        except Exception as e:
            return e
            
    def init(self):
        try:
            command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"' +' init'
            result = subprocess.check_output(command,shell=True)
            self.branches['master'] = Branch('master',self.geogigPath,self.repoUrl)
            return result
        except Exception as e:
            return e

    def clone(self,host,port,database,schema,repository,user,password,branchName):
        try:
            dest = "postgresql://{}:{}/{}/{}/{}?user={}&password={}".format(host,port,database,schema,repository,user,password)
            command = self.geogigPath + ' clone ' +'"'+ self.repoUrl+'"' +' "'+ dest+'" --branch '+ branchName
            result = subprocess.check_output(command,shell=True,universal_newlines=True)
            return result
        except Exception as e:
            self.logger.error(e) if self.logger else ''

    def compara_schema(self,host,port,database,schema,user,password):
        #metodo para comparar os atributos das tabelas entre a arvore do repositorio
        
        layers = []
        try:
            #lista a arvore do repositorio
            command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' ls '+schema 
            result = subprocess.check_output(command,shell=True)
            layers = [x.replace('/', '').strip() for x in result.split('\n') if x.strip() != ''][1:]

            #lista os atributos das tabelas existentes na base de dados
            strCon = 'dbname='+database+' user='+user+' password='+password+' host='+host+' port='+port
            query="select array_agg(table_name::text || '/' || column_name::text) from INFORMATION_SCHEMA.COLUMNS where table_schema = 'edgv' and table_name in ('{0}')".format("','".join(layers))
            con = psycopg2.connect(strCon)
            con.autocommit=True
            cur = con.cursor()
            cur.execute(query)
            db_list=cur.fetchall()
            con.close()

            geogig_list = []
            for layer in layers:
                commandIn = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' show '+' HEAD:'+schema+'/'+layer
                result = subprocess.check_output(commandIn,shell=True)
                geogig_list =  geogig_list + [layer+'/'+x.split(':')[0] for x in result.split('\n\n')[1].split('\n')[1:]]
            return set(db_list[0][0]).difference(geogig_list)
        except subprocess.CalledProcessError as e:
            return e



    def add_branch(self,branchName,force=False):
        try:
            if(force):
                command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' branch '+ branchName+' --force'
            else:
                command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' branch '+ branchName

            result = subprocess.check_output(command,shell=True,universal_newlines=True)
            msg = subprocess.STDOUT
            self.branches[branchName] = Branch(branchName,self.geogigPath,self.repoUrl)
            return msg

        except Exception as e:
            return e
        

    def del_branch(self,branchName):
        try:
            command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' branch --delete '+branchName
            result = subprocess.check_output(command,shell=True,universal_newlines=True)
            self.branches[branchName]
        except Exception as e:
            return e
    def getConfigRepository(self):
        config = {}
        command = '{0} --repo "{1}" config --list'.format(self.geogigPath, self.repoUrl)
        result = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
        for item in [x for x in result.split('\n') if x.strip()!= '']:
            key = item.split('=')[0]
            value = item.split('=')[1]
            config[key]=value
        if(config['user.email']!=''):
            self.logger.error(u'Repository not configured') if self.logger else ''
        else:
            pass
    
    def merge_abort(self):
        abort_merge = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' merge --abort'
        abort_merge_run = subprocess.check_output(abort_merge,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
        self.logger.error(exc) if self.logger else ''
        return exc

class Branch(object):
    def __init__(self,branchName, geogigPath, repoUrl, logger=False):
        self.logger = logger
        self.name = branchName
        self.geogigPath = geogigPath
        self.repoUrl = repoUrl
        self.conflicts = []

    def __checkout(self):
        command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' status'
        result =  subprocess.check_output(command,shell=True).split('\n')[0]
        active_branch = result.replace('# On branch ','')
        if active_branch != self.name:
            try:
                commandIn=self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' checkout '+self.name
                subprocess.call(commandIn,shell=True)
            except Exception as e:
                return e

    def add(self,layer=None):
        self.__checkout()
        if layer == None:
            command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' add'
            result =  subprocess.check_output(command,shell=True,universal_newlines=True)
        return result

    def push(self,branchName):
        self.__checkout()
        try:
            command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' push origin '+branchName
            result=subprocess.check_output(command,shell=True)
            return result
        except Exception as e:
            return e
    
    def pull(self,branchName):
        self.__checkout()
        try:
            command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' pull origin '+branchName
            result = subprocess.check_output(command,shell=True)
            return result
        except Exception as e:
            self.logger.error(e) if self.logger else ''
            return e

    def log(self,param=None):
        self.__checkout()
        if(param):
            #TODO
            pass
            
        else:
            command = self.geogigPath+ ' --repo ' +'"'+self.repoUrl+'"' +' log'
        result = subprocess.check_output(command,shell=True)
        logs = []
        aux = {}
        for line in [x for x in result.split('\n') if x.strip()!= '']:
            if line.find('Commit') > -1:
                if 'commit' in aux:
                    logs.append(aux)
                    aux = {}
                aux['commit'] = line.split(':')[1].strip()

            if line.find('Author') > -1:
                    aux['author'] = line.split(':')[1].strip()
            if line.find('Subject') > -1:
                    aux['subject'] = line.split(':')[1].strip()
            if line.find('Date') > -1:
                    aux['date'] = ':'.join(line.split(':')[1:]).strip()
            if line.find('Merge') > -1:
                    aux['Merge'] = line.split(':')[1].strip()

        logs.append(aux)
        return logs
        
    def parse_feature(self, feature, layer):
        values = {}
        if "FEATURE" in feature:
            value_part = feature.split("FEATURE")[1]
            for idx, line in enumerate(value_part.split("\n")[1:]):
                if len(line.split("\t")) > 1:
                    values[layer[idx]] = line.split("\t")[1]
                else:
                    self.logger.error(u"Error parse feature {0} {1}".format(idx, line)) if self.logger else ''
        else:
            for att in layer:
                values[att]= "DELETADO"
        return values

    def getFeatureType(self, layer):
        command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' show '+layer
        result = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)

        attribute_list = result.split("\n\n")[1]
        attributes = [attribute.split(":")[0] for attribute in attribute_list.split("\n")[1:]]
        return attributes

    def conflicts_list(self):
        
        try:
            command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' conflicts'
            result = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
            self.conflicts =  result.split('\n\n')
            if(self.conflicts):
                conflicts = []
                aux = {}
                feature_type = {}
                current_feature = ""
                for idx, conflict_parts in enumerate(self.conflicts):
                    if(idx%4 == 0):
                        conflict_parts = conflict_parts.strip()
                        current_feature = "/".join(conflict_parts.split("/")[0:2])
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

        except subprocess.CalledProcessError as exc:
            abort_merge = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' merge --abort'
            abort_merge_run = subprocess.check_output(abort_merge,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
            self.logger.error(exc) if self.logger else ''
            return exc

    def merge(self,branchName):
        self.__checkout()
        try:
            command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' merge '+branchName
            result = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
        except subprocess.CalledProcessError as exc:
            if ("CONFLICT" in exc.output):
                conflicts = self.conflicts_list()
                return conflicts
            elif "The branch has already been merged." in exc.output:
                return 'Success'
            else:
                self.logger.error(exc) if self.logger else ''
                return exc
        else:
            return 'Success'
            

    def pg_import_schema(self,host,port,database,schema,user,password):
        self.__checkout()
        command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' pg list --host '+host+' --port '+port+' --database '+database+' --schema '+schema+' --user '+user+' --password '+password
        result = subprocess.check_output(command,shell=True)
        layers = [x.replace('-', '').strip() for x in result.split('\n') if x.strip() != ''][1:]
        for layer in layers:
            try:
                commandIn = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' pg import --table '+layer+' -d '+schema+'/'+layer+' --schema '+schema+' --host '+host+' --port '+port+' --database '+database+' --user '+user+' --password '+password+' --force-featuretype' 
                result = subprocess.check_output(commandIn,shell=True)
                self.logger.info(u"Database : {0} layer: {1} {2}".format(database, layer, " ok!")) if self.logger else ''
            except subprocess.CalledProcessError as e:
                self.logger.error(e.output) if self.logger else ''
        self.logger.info(u"Database : {0} import finished".format(database)) if self.logger else ''

    def pg_export_schema(self,host,port,database,schema,user,password):
        self.__checkout()
        layers = []
        try:
            #lista as tabelas existentes na base de dados
            listLayersInDb = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' pg list --host '+host+' --port '+port+' --database '+database+' --schema '+schema+' --user '+user+' --password '+password
            result = subprocess.check_output(listLayersInDb,shell=True)
            layersInDb = [x.replace('-', '').strip() for x in result.split('\n') if x.strip() != ''][1:]
            #lista a arvore do repositorio
            command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' ls '+schema 
            result = subprocess.check_output(command,shell=True)
            layers = [x.replace('/', '').strip() for x in result.split('\n') if x.strip() != ''][1:]
            for layer in layers:
                commandIn = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' pg export --host '+host+' --port '+port+' --database '+database+' --user '+user+' --password '+password+' --schema ' + schema +' HEAD:'+schema+'/'+layer+' '+layer+' --overwrite'
                result = subprocess.check_output(commandIn,shell=True)
                self.logger.info(u"Database : {0} layer: {1} {2}".format(database, layer, " ok!")) if self.logger else ''
            self.logger.info("Database : {0} export finished".format(database)) if self.logger else ''
            #exclusão dos registros no banco de dados que nao estao na arvore
            strCon = 'dbname='+database+' user='+user+' password='+password+' host='+host+' port='+port
            con = psycopg2.connect(strCon)
            con.autocommit=True
            cur = con.cursor()
            emptyLayers = set(layersInDb).difference(layers)
            for layer in emptyLayers:
                self.logger.info(u"excluindo os registros de {0}".format(layer)) if self.logger else ''
                cur.execute("DELETE FROM {}.{};".format(schema,layer))
            cur.close()
            con.close()

        except subprocess.CalledProcessError as e:
            self.logger.error(e) if self.logger else ''
            return e
    
    def status(self):
        self.__checkout()
        command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' status'
        result =  subprocess.check_output(command,shell=True)
        self.logger.info(result) if self.logger else ''
        return result
    
    def commit(self,msg):
        self.__checkout()
        command = self.geogigPath + ' --repo ' +'"'+ self.repoUrl+'"'+' commit -m "'+msg + '"' 
        try:
            result = subprocess.check_output(command,shell=True)
        except subprocess.CalledProcessError as exc:
            if ("Nothing to commit" in exc.output):
                result = "Nothing to commit"
                
        
        return result

    def merge_features(self, decisionDict):
        for feat, decision in decisionDict.iteritems():
            command = '{0} --repo "{1}" checkout --path {2} --{3}'.format(self.geogigPath, self.repoUrl, feat, decision)
            result = subprocess.check_output(command,shell=True)
            addCommand = '{0} --repo "{1}" add {2}'.format(self.geogigPath, self.repoUrl, feat)
            result = subprocess.check_output(addCommand,shell=True)
        self.commit('merge concluido')
            
    