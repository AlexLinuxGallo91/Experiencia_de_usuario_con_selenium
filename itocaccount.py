class ItocAccount:

    def __init__(self,idaccount,db,server,user,password,
                 service,creation_date,modif_date,deleted):
        self.idaccount = idaccount
        self.db = db
        self.server = server
        self.user = user
        self.password = password
        self.service = service
        self.creation_date = creation_date
        self.modif_date = modif_date
        self.deleted = deleted

    def __str__(self):
        return 'idaccount : {self.idaccount}, db : {self.db}, server : {self.server},'\
               'user : {self.user}, password : {self.password}, service : {self.password}, '\
               'creation_date : {self.creation_date}, modif_date : {self.modif_date}, '\
               'deleted : {self.deleted}'.format(self=self)