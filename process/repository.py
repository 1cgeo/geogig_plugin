# -*- coding: utf-8 -*-
import subprocess, psycopg2, os, datetime, sys, re, tempfile
from branch import Branch

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

    def get_commits(self):
        output = subprocess.check_output([self.geogigPath, '--repo', self.repoUrl, 'log', '--oneline'])
        commits = []
        for line in output.split('\n'):
            commit = line.split(' ')[0]
            commits.append(commit)
        return commits


    def reset_commit(self, position):
        commits = self.get_commits()
        command = u'{0} --repo "{1}" reset {2}'.format(self.geogigPath, self.repoUrl, commits[position])
        subprocess.check_output(command,shell=True)
        self.logger.debug(u"Reset commit to --> {}".format(commits[position])) if self.logger else ''
            
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
            self.branches[branchName] = Branch(branchName,self.geogigPath,self.repoUrl)
            self.logger.debug(u"Add branch - branch_name : {0}".format(branchName)) if self.logger else ''
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