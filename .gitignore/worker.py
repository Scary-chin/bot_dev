import discord
import asyncio
from discord.ext import commands
import marshal
import os
import psycopg2
import dropbox
import random
import time

dbx = dropbox.Dropbox('MQIZTGpkwHAAAAAAAAAAEmpsp3tCRkmkjf5eegH1ezz_lk_1BXWNoyfLV2fzISRS')

file_from='save_l'
file_to='/save_l'




def upload_file(file_from, file_to):
    #dbx = dropbox.Dropbox(access_token)
    f = open(file_from, 'rb')
    dbx.files_upload(f.read(),file_to)
    f.close()

def del_t(file_to):
    dbx.files_delete(file_to)

def download():
    f = open(file_from, 'wb')
    metadata, res = dbx.files_download(path="/save_l")
    f.write(res.content)
    f.close()

    
download()


#https://www.youtube.com/watch?v=SSOrokcqpzY hébergement gratuit

L=marshal.load(open("save_l", "rb")) #liste des [pseudos,red,archi,2,3,4,retard]

G1=[-1,-1,-1,-1,-1]
G2=[-1,-1,-1,-1,-1]
Autres=[]
roles=['archi','red','2','3','4']
retard=[]

bot = commands.Bot(command_prefix='botfix')
client = discord.Client()


def save():
    marshal.dump(L,open('save_l','wb'))
    del_t(file_to)
    upload_file(file_from, file_to)

    
def auteur(message):
    if message.author.nick == None:
        pseudo=message.author.name

    else : pseudo=message.author.nick
    return pseudo
    


def check(s,new):
    for i in range(len(s)):
        #print(i,s[i])
        if s[i]=='2':
            new[3]=1
        if s[i]=='3':
            new[4]=1
        if s[i]=='4':
            new[5]=1
        if s[i]=='a' or s[i]=='A':
            if s[i+1]=='r' or s[i+1]=='R':
                if s[i+2]=='c' or s[i+2]=='C':
                    new[1]=1
        if s[i]=='r' or s[i]=='R':
            if s[i+1]=='e':
                new[2]=1
    return new


def clear(pseudo):


    for i in range(len(L)):
        if L[i][0]==pseudo:
            del(L[i])
            rempli_groupe()
            return


def rempli_groupe():
    
    save()
    random.shuffle(L)
    print(L)
    
    n=len(retard)
    for i in range(n):
        del(retard[0])
        
        
    
    for i in range(5):
        G1[i]=-1
        G2[i]=-1
        
    n=len(Autres)
    for i in range(n):
        del(Autres[0])

        
    for i in range(len(L)):
        if L[i][-1]:
            mis=False
            for j in [4,1,0,3,2]:
                #print(j,L[i][j+1])
                if not mis:
                    if (G1[j]==-1 and L[i][j+1]==1):
                        G1[j]=i
                        mis=True
            
                if not mis:
                    if(G2[j]==-1 and L[i][j+1]==1):
                        G2[j]=i
                        mis=True
            if not mis:
                Autres.append(i)
        else:
            retard.append([L[i][0],L[i][-2]])
            #print(retard)



def affiche():
    GA1=[]
    GA2=[]    
    AutresA=[]
    reta=[]
    for i in range(5):
        GA1.append(roles[i]+": ")       
        if G1[i]==-1:
            1
        else:
            GA1.append(L[G1[i]][0]+" (")
            for j in range(5):
                if L[G1[i]][j+1]==1:
                    GA1.append(roles[j]+" ")
            GA1.append(")")
        GA1.append("\n")
        
    for i in range(5):
        GA2.append(roles[i]+": ")       
        if G2[i]==-1:
            1
        else:
            GA2.append(L[G2[i]][0]+" (")
            for j in range(5):
                if L[G2[i]][j+1]==1:
                    GA2.append(roles[j]+" ")
            GA2.append(")")
        GA2.append("\n")
        
    for i in range(len(Autres)):
        AutresA.append(L[Autres[i]][0]+" (")
        for j in range(5):
                if L[Autres[i]][j+1]==1:
                    AutresA.append(roles[j]+" ")
        AutresA.append(")\n")
    for i in range(len(retard)):
        print(retard[i][1])
        reta.append(retard[i][0]+" ("+retard[i][1]+")\n")
    return [GA1,GA2,AutresA,reta]

########################################

def aff_recap():
    "le bot affiche ou on en est"
    resul=affiche()        
    groupe1= ''.join(resul[0])
    groupe2= ''.join(resul[1])
    aut= ''.join(resul[2])
    ret=''.join(resul[3])
    s= "groupe 1: " +"\n"+ groupe1 +"\n"+"groupe 2: "+"\n" +groupe2+"\n"+"autres: "+"\n"+aut+"\n"+"retard: \n"+ret
    return s




@client.event
async def on_message(message):
    await client.change_presence(game=discord.Game(name="""!help pour aficher l'aide"""))
    
    
    
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
        await client.send_message(message.channel,
"""(prévenir Scary-chin si problèmes)
bot pour inscription laby: 
inscriptions avant 21h
commandes:
-inscription: $ roles
roles disponible: archi/ red/ 2/ 3/ 4

-Pour se désinscrire:
clear (pas de dollar au début)
-pour changer les rôles: se désincrire puis se réinscrire
-afficher les gens inscrits: $
- si vous êttes en retard écrivez: retard suivi de votre heure d'arrivée et de votre role
-a la fin de la soirée laby:
$ nouvelle $ soirée laby $ omg
-aide:
!help""" )


    if message.content.startswith('$'):
        "inscription"
        if len(message.content)>1:
            "si que $ c'est pas une inscription"
            new=[auteur(message),-1,-1,-1,-1,-1,True,True]
            "on va voir si il est inscrit"
            nouveau=True
            for i in range(len(L)):
                if new[0]==L[i][0]:
                    nouveau=False
                    
            s = message.content
            new=check(s,new)
        
            if nouveau:
                L.append(new)
                await client.send_message(message.channel,'inscription validée')
                save()
                
            else:
                await client.send_message(message.channel,"clear si tu veut modif t'es deja inscrit FRAIrrRE ")
                

                
        else:
            rempli_groupe()
            time.sleep(5)
            await client.send_message(message.channel,aff_recap())


    elif message.content.startswith('retard') or message.content.startswith('Retard') :
        
        s=list(message.content)
        
        for i in range(6):
            del(s[0])
        s=''.join(s)
        L.append([auteur(message) ,-1,-1,-1,-1,-1,s,False])
        save()
        time.sleep(5)
        await client.send_message(message.channel,'inscription retard validé')
        

        
    elif message.content.startswith('clear') or message.content.startswith('Clear'):
        "se désincrire"
        clear(auteur(message))
        time.sleep(5)
        await client.send_message(message.channel,"tape $")


    if message.content.startswith('$ nouvelle $ soirée laby $ omg'):
        marshal.dump([],open('save_l','wb'))
        n=len(L)
        for i in range(n):
            del(L[0])            
        rempli_groupe()
        save()
        time.sleep(5)
        await client.send_message(message.channel,aff_recap())



            

"""@bot.command(pass_context=True)
async def joined_at(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    print("aaaa",ctx)

    await bot.say('{0} joined at {0.joined_at}'.format(member))"""


    



        

@client.event
async def on_ready():
    
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name="""!help pour accficher l'aide""")) 

client.run('NDMzMzMwMzYyMzY2Njg5Mjk0.DbeliQ.cxmbkn0kyjEyijKjQmdz1EI-1zs')



    



################################################################









