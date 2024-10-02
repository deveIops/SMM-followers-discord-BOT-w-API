⚙️ Panel BOT Discord
📚 Description
Le Bot Discord SMM Follows est un outil conçu pour passer des commandes de followers, likes, et vues sur TikTok, Instagram, et Twitch via l'API SMMFollows. Ce bot permet aux administrateurs de gérer facilement les commandes et de suivre en temps réel leur progression, avec des notifications automatiques une fois les commandes terminées.

⭐ Fonctionnalités
🎯 Gestion des commandes TikTok : Envoyer des followers ou des likes à des comptes ou vidéos TikTok.
📸 Gestion des commandes Instagram : Commander des followers pour un profil Instagram.
🎮 Gestion des commandes Twitch : Commander des followers pour des comptes Twitch.
💵 Vérification du solde : Consulter votre solde actuel et sa conversion en EUR.
🔄 Suivi des commandes : Recevoir des mises à jour automatiques lorsque les commandes sont terminées.



🚀 Installation

🔧 Prérequis
Avant de commencer, assurez-vous d'avoir installé Git et Python 3.8+. Vous devez également disposer d'un token de bot Discord et d'une clé API SMMFollows.

```
git clone https://github.com/ton_utilisateur/smm-follows-bot.git
cd smm-follows-bot
pip install -r requirements.txt
```

⚙️ Configuration
Ajoutez un fichier .env à la racine du projet avec les informations suivantes :
```
DISCORD_TOKEN=ton_token_discord
SMMFOLLOWS_API_KEY=ta_cle_api_smmfollows
CHANNEL_ID=id_du_salon_discord_pour_notifications
```

🔄 Ajouter un ID de service
Pour ajouter un nouveau service (ex. pour TikTok, Instagram, Twitch), modifiez l'ID du service dans la commande correspondante. Par exemple, pour TikTok :

```
@bot.command()
@commands.has_permissions(administrator=True)
async def gw(ctx, amount: int, target: str):
    await ctx.message.delete()
    global client_number
    client_number += 1 
    username = extract_tiktok_username(target)
    link = f"https://www.tiktok.com/@{username}" 

    api_url = "https://smmfollows.com/api/v2"
    payload = {
        'key': SMMFOLLOWS_API_KEY,
        'action': 'add',
        'service': ID_DU_SERVICE,  # Remplacez par l'ID de service correspondant
        'link': link,
        'quantity': amount 
```
⚠️ Informations importantes

````
- Le bot utilise l'API SMMFollows pour traiter les commandes.
- Assurez-vous de garder votre token Discord et votre clé API privés, ne les partagez pas publiquement.
- Le bot nécessite des permissions d'administrateur sur le serveur Discord pour fonctionner correctement et gérer les commandes.
````

⚙️ Exemple de commandes : 

!bal pour voir la balance de votre compte smm


Le reste des commandes, le nom et leur fonction c'est à vous de les configurer, il faut un minimum de compréhension pour utiliser ce code.
