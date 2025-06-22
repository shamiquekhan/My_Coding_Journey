class user:
    def __init__(self,username,name,email) : 
        self.username = username
        self.name = name
        self.email = email
        self.users = []
        
        print("user created... ")
    def intro(self, guestname) :
        self.guestname = guestname
        print("hi {}, I am {} ! Contact me at {} ." .format(guestname,self.name,self.email) )
    def __repr__(self):
        return "User(username='{}', name='{}', email='{}')".format(self.username, self.name, self.email)
    def __str__(self):
        return self.__repr__()
    def insert(self,user):
        i=0
        while i< len(self.users):
            if self.users[i].username>=user.username :
                break
            i+=1
        self.users.insert(i,user)
    def find(self,username):
        for user in self.users :
            if user.username==username:
                return user
    def update(self,user):
        target=self.find(user.username)
        target.name,target.email=user.name,user.email

    def list_all(self):
        return self.users        
shamique=user("shami_que","shamique","shamique@gamil.com")   
sam=user("s_am","sam","sam@gamil.com")
sham=user("sham_","sham","sham@gamil.com")
sohail=user("sohail_","sohail","sohail@gamil.com")
shami=user("shami_","shami","shami@gamil.com")
shaameel=user("shameel_","shameel","shameel@gamil.com")
user.list_all()
