from users import GetUsers
from threads import Threads

while True:
    localUsers = GetUsers()
    localUsers.DefineUsuario()

    #users = ['Stark', 'Kako', 'Melissa', 'Pai', 'Mãe', 'Israel', 'Luma', 'Gloria', 'Olga', 'Reinaldo']
    localThreads = Threads()
    localThreads.SetThreads(localUsers.users)

    print(f'Restarting application')