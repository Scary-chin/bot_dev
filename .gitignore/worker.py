import discord
import asyncio
from discord.ext import commands


#https://www.youtube.com/watch?v=SSOrokcqpzY hébergement gratuit

L=[] #liste des [pseudos,red,archi,2,3,4]
G1=[-1,-1,-1,-1,-1]
G2=[-1,-1,-1,-1,-1]
Autres=[]




def check(s,new):
    for i in range(len(s)):
        #print(i,s[i])
        if s[i]=='2':
            new[3]=1
        if s[i]=='3':
            new[4]=1
        if s[i]=='4':
            new[5]=1
        if s[i]=='a':
            if s[i+1]=='r':
                if s[i+2]=='c':
                    new[1]=1
        if s[i]=='r':
            if s[i+1]=='e':
                new[2]=1
    return new


def clear(pseudo):
    for i in range(5):
        G1[i]=-1
        G2[i]=-1
    n=len(Autres)
    for i in range(n):
        del(Autres[0])
    for i in range(len(L)):
        if L[i][0]==pseudo:
            del(L[i])
            rempli_groupe()
            return

def rempli_groupe():
    for i in range(len(L)):
        mis=False
        for j in [4,1,0,3,2]:
            print(j,L[i][j+1])
            if not mis:
                if (G1[j]==-1 and L[i][j+1]==1):
                    G1[j]=i
                    mis=True
        for j in [4,1,0,3,2]:
            if not mis:
                if (G2[j]==-1 and L[i][j+1]==1):
                    G2[j]=i
                    mis=True
        if not mis:
            Autres.append(i)



def affiche():
    GA1=[]
    GA2=[]    
    AutresA=[]
    for i in G1:
        if i==-1:
            GA1.append('      ')
        else:
            GA1.append(L[i][0])
    for i in G2:
        if i==-1:
            GA2.append('      ')
        else:
            GA2.append(L[i][0])
    for i in Autres:
        if i==-1:
            AutresA.append('      ')
        else:
            AutresA.append(L[i][0])
    return [GA1,GA2,AutresA]



########################################



bot = commands.Bot(command_prefix='botfix', description='description here')
client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)


    if message.content.startswith('$'):
        if len(message.content)>1:
            new=['{0.author}'.format(message)+"   ",-1,-1,-1,-1,-1]
            nouveau=True
            for i in range(len(L)):
                #print(L[i][0])
                if new[0]==L[i][0]:
                    nouveau=False
        


        
            s = message.content
            new=check(s,new)
        
            if nouveau:
                L.append(new)
            else:
                await client.send_message(message.channel,"clear si tu veut modif t'es deja inscrit")
                return
        for i in range(5):
            G1[i]=-1
            G2[i]=-1
        n=len(Autres)
        for i in range(n):
            del(Autres[0])
            
        rempli_groupe()
        print("l",L,"g1",G1)
        resul=affiche()
        groupe1=''
        groupe2=''
        aut=''
        
        groupe1= ''.join(resul[0])
        groupe2= ''.join(resul[1])
        aut= ''.join(resul[2])
        
        print(resul[0])
        
        await client.send_message(message.channel,"groupe 1: " + groupe1+"\n"+"groupe 2: " +groupe2+"\n"+"autres: "+aut)



        
    if message.content.startswith('clear'):
        clear('{0.author}'.format(message)+"   ")



        await client.send_message(message.channel,"tape $")


    if message.content.startswith('$ nouvelle $ soirée laby $ omg'):
        n=len(L)
        for i in range(n):
            del(L[0])
        for i in range(5):
            G1[i]=-1
            G2[i]=-1
        n=len(Autres)
        for i in range(n):
            del(Autres[0])
            
        rempli_groupe()
        print("l",L,"g1",G1)
        resul=affiche()
        groupe1=''
        groupe2=''
        aut=''
        
        groupe1= ''.join(resul[0])
        groupe2= ''.join(resul[1])
        aut= ''.join(resul[2])
        
        print(resul[0])
        
        await client.send_message(message.channel,"groupe 1: " + groupe1+"\n"+"groupe 2: " +groupe2+"\n"+"autres: "+aut)



            

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

client.run('NDMzMzMwMzYyMzY2Njg5Mjk0.Da7Qsw.Ml4OtBAkCHSuKeD5A5730qAVb2U')





################################################################









