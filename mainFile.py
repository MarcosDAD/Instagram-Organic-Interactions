from users import GetUsers
from threads import Threads

while True:
    localUsers = GetUsers()
    localUsers.DefineUsuario()

    localThreads = Threads()
    localThreads.SetThreads(localUsers.users)

    print(f'Restarting application')
