import os
import requests
import webbrowser
from urllib.parse import urlparse
import discord
from discord.ext import commands
import asyncio
import threading
import customtkinter as ctk
import socket
from PIL import ImageGrab
import io
import subprocess

# Fonction pour afficher du texte en vert
def green_text(text):
    return f"\033[92m{text}\033[0m"

# Fonction pour capturer l'écran
def capture_ecran():
    screenshot = ImageGrab.grab()  # Capture l'écran
    img_byte_arr = io.BytesIO()  # Convertit l'image en bytes
    screenshot.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

# Fonction pour récupérer l'adresse IP publique
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        if response.status_code == 200:
            return response.json().get("ip", "Inconnue")
    except Exception as e:
        print(green_text(f"Erreur lors de la récupération de l'IP publique : {e}"))
    return "Inconnue"

# Fonction pour récupérer l'adresse IP locale
def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception as e:
        print(green_text(f"Erreur lors de la récupération de l'IP locale : {e}"))
    return "Inconnue"

# Fonction pour pinger une IP
def ip_pinger():
    while True:
        ip = input(green_text("Entrez l'IP à pinger (ou 'q' pour quitter) : "))
        if ip.lower() == 'q':
            break
            
        # Validation de l'IP
        try:
            socket.inet_aton(ip)
        except socket.error:
            print(green_text("Invalid IP"))
            continue
            
        # Demander le nombre de pings
        while True:
            try:
                count = int(input(green_text("Ping Numbers (max 10000) : ")))
                if 1 <= count <= 10000:
                    break
                else:
                    print(green_text("Le nombre doit être entre 1 et 10000"))
            except ValueError:
                print(green_text("Veuillez entrer un nombre valide"))
        
        # Exécuter le ping
        param = '-n' if os.name == 'nt' else '-c'
        command = ['ping', param, str(count), ip]
        try:
            output = subprocess.check_output(command, universal_newlines=True)
            print(green_text(output))
        except subprocess.CalledProcessError as e:
            print(green_text(f"Erreur lors du ping : {e}"))
        break

# Fonction pour afficher le menu
def afficher_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    menu_text = r"""
           ██████  ▄████▄   ██▀███   ▄▄▄       ██▓███   ██▓███  ▓█████  ██▀███  
          ▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒▒████▄    ▓██░  ██▒▓██░  ██▒▓█   ▀ ▓██ ▒ ██▒
          ░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▒██  ▀█▄  ▓██░ ██▓▒▓██░ ██▓▒▒███   ▓██ ░▄█ ▒
            ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ░██▄▄▄▄██ ▒██▄█▓▒ ▒▒██▄█▓▒ ▒▒▓█  ▄ ▒██▀▀█▄  
          ▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒ ▓█   ▓██▒▒██▒ ░  ░▒██▒ ░  ░░▒████▒░██▓ ▒██▒
          ▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░▒▓▒░ ░  ░▒▓▒░ ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░
          ░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░  ▒   ▒▒ ░░▒ ░     ░▒ ░      ░ ░  ░  ░▒ ░ ▒░
          ░  ░  ░  ░          ░░   ░   ░   ▒   ░░       ░░          ░     ░░   ░ 
                ░  ░ ░         ░           ░  ░                     ░  ░   ░     
                   ░  
                                       shd shop free tools !!!                   
    """
    options = [
        "                     ┌─  1. Webhook Spammer     5. Coordonnées   9. Owners",
        "                     ├─  2. Webhook Create      6. URL Info      10. IP Pinger",
        "                     ├─  3. Webhook Info        7. Raid          11. Discord",
        "                     └─  4. IP Lookup           8. DM All"
    ]
    print(green_text(menu_text))
    for option in options:
        print(green_text(option))

# Fonction pour spammer un webhook
def webhook_spammer():
    webhook_url = input(green_text("Entrez l'URL du webhook : "))
    message = input(green_text("Entrez le message à spammer : "))
    count = int(input(green_text("Entrez le nombre de fois à spammer (max 1000) : ")))
    count = min(count, 1000)  # Limite à 1000

    for i in range(count):
        try:
            data = {"content": message}
            response = requests.post(webhook_url, json=data)
            if response.status_code == 204:
                print(green_text(f"Message {i + 1} envoyé avec succès !"))
            else:
                print(green_text(f"Échec de l'envoi du message {i + 1}."))
        except Exception as e:
            print(green_text(f"Erreur lors de l'envoi du message {i + 1} : {e}"))

# Fonction pour obtenir des informations sur un webhook
def webhook_info():
    webhook_url = input(green_text("Entrez l'URL du webhook : "))
    try:
        response = requests.get(webhook_url)
        if response.status_code == 200:
            webhook_data = response.json()
            print(green_text(f"Nom du serveur : {webhook_data.get('guild', {}).get('name', 'Inconnu')}"))
            print(green_text(f"ID du serveur : {webhook_data.get('guild_id', 'Inconnu')}"))
            print(green_text(f"ID du salon : {webhook_data.get('channel_id', 'Inconnu')}"))
            print(green_text(f"Créateur du webhook : {webhook_data.get('user', {}).get('username', 'Inconnu')}"))
        else:
            print(green_text("Impossible de récupérer les informations du webhook."))
    except Exception as e:
        print(green_text(f"Erreur lors de la récupération des informations : {e}"))

# Fonction pour créer des webhooks
def webhook_create():
    token = input(green_text("Entrez le token du bot : "))
    guild_id = input(green_text("Entrez l'ID du serveur : "))
    channel_id = input(green_text("Entrez l'ID du salon : "))
    count = int(input(green_text("Entrez le nombre de webhooks à créer : ")))
    name = input(green_text("Entrez le nom des webhooks : "))

    for i in range(count):
        try:
            url = f"https://discord.com/api/v9/channels/{channel_id}/webhooks"
            headers = {"Authorization": f"Bot {token}"}
            data = {"name": name}
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                print(green_text(f"Webhook {i + 1} créé avec succès !"))
            else:
                print(green_text(f"Échec de la création du webhook {i + 1}."))
        except Exception as e:
            print(green_text(f"Erreur lors de la création du webhook {i + 1} : {e}"))

# Fonction pour rechercher des informations sur une IP
def ip_lookup():
    ip = input(green_text("Entrez l'IP à rechercher : "))
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            ip_data = response.json()
            print(green_text(f"Pays : {ip_data.get('country', 'Inconnu')}"))
            print(green_text(f"Région : {ip_data.get('regionName', 'Inconnu')}"))
            print(green_text(f"Ville : {ip_data.get('city', 'Inconnu')}"))
            print(green_text(f"Coordonnées : {ip_data.get('lat', 'Inconnu')}, {ip_data.get('lon', 'Inconnu')}"))
            print(green_text(f"Opérateur : {ip_data.get('isp', 'Inconnu')}"))
        else:
            print(green_text("Impossible de récupérer les informations de l'IP."))
    except Exception as e:
        print(green_text(f"Erreur lors de la recherche de l'IP : {e}"))

# Fonction pour ouvrir des coordonnées sur Google Maps
def coordonnees():
    lat = input(green_text("Entrez la latitude : "))
    lon = input(green_text("Entrez la longitude : "))
    webbrowser.open(f"https://www.google.com/maps?q={lat},{lon}")

# Fonction pour obtenir des informations sur une URL
def url_info():
    url = input(green_text("Entrez l'URL : "))
    try:
        parsed_url = urlparse(url)
        print(green_text(f"Protocole : {parsed_url.scheme}"))
        print(green_text(f"Domaine : {parsed_url.netloc}"))
        print(green_text(f"Chemin : {parsed_url.path}"))
        print(green_text(f"Paramètres : {parsed_url.query}"))
    except Exception as e:
        print(green_text(f"Erreur lors de l'analyse de l'URL : {e}"))

# Fonction pour afficher les informations des créateurs
def creators_profil():
    print(green_text("╔═════════════════════════════════════╗"))
    print(green_text("║ Author = Shadow                     ║"))
    print(green_text("║ Discord: shd Shop                   ║"))
    print(green_text("║ this is the paid version !          ║"))
    print(green_text("║═════════════════════════════════════║"))
    print(green_text("║               0. Back               ║"))
    print(green_text("╚═════════════════════════════════════╝"))
    input(green_text("Appuyez sur Entrée pour continuer..."))

# Fonction pour ouvrir le lien Discord
def join_discord():
    webbrowser.open("https://discord.gg/Wgz8NUAD")

# Fonction pour l'interface graphique DM All
def dm_tool_interface():
    # Configuration de CustomTkinter
    ctk.set_appearance_mode("dark")  # Thème sombre
    ctk.set_default_color_theme("blue")  # Thème de couleur de base

    # Variables globales
    global client, is_running
    client = None
    is_running = False

    # Fonction pour démarrer le bot
    def start_bot():
        global client, is_running

        token = token_entry.get()
        if not token:
            log_message("Veuillez entrer un token valide.")
            return

        if is_running:
            log_message("Le bot est déjà en cours d'exécution.")
            return

        # Initialisation du bot
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        client = commands.Bot(command_prefix="!", intents=intents)

        @client.event
        async def on_ready():
            log_message(f"Bot connecté en tant que {client.user}")
            log_message("Prêt à envoyer des messages.")

        # Démarrer le bot dans un thread séparé
        def run_bot():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(client.start(token))

        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        is_running = True

    # Fonction pour envoyer des messages privés
    def send_dm():
        global client

        if not client or not client.is_ready():
            log_message("Le bot n'est pas encore connecté.")
            return

        message = message_text.get("1.0", "end-1c")  # Récupère le message de la zone de texte
        if not message:
            log_message("Veuillez entrer un message.")
            return

        # Envoyer le message à tous les membres de tous les serveurs
        async def send_messages():
            success = 0
            failed = 0
            for guild in client.guilds:
                for member in guild.members:
                    try:
                        if not member.bot:  # Ne pas envoyer de message aux bots
                            await member.send(message)
                            success += 1
                            log_message(f"Message envoyé à {member.name}")
                            await asyncio.sleep(1)  # Délai pour éviter le spam
                    except discord.Forbidden:
                        log_message(f"Impossible d'envoyer un message à {member.name} (DM désactivés).")
                        failed += 1
                    except Exception as e:
                        log_message(f"Erreur avec {member.name} : {e}")
                        failed += 1
            log_message(f"Opération terminée : {success} messages envoyés, {failed} échecs.")

        # Planifier la coroutine dans la boucle d'événements du bot
        asyncio.run_coroutine_threadsafe(send_messages(), client.loop)

    # Fonction pour afficher des messages dans la console
    def log_message(message):
        console_text.configure(state="normal")
        console_text.insert("end", message + "\n")
        console_text.configure(state="disabled")
        console_text.see("end")

    # Interface graphique
    app = ctk.CTk()
    app.title("shadow DmAll")
    app.geometry("700x600")  # Taille de la fenêtre

    # Style des boutons
    button_style = {
        "fg_color": "#2E2E2E",  # Gris foncé
        "hover_color": "#404040",  # Gris un peu plus clair au survol
        "text_color": "white",  # Texte blanc
        "font": ("Arial", 14),  # Police moderne
        "corner_radius": 10  # Coins arrondis
    }

    # Utilisation de grid pour organiser les éléments
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=1)

    # Token du bot
    token_label = ctk.CTkLabel(app, text="Token du bot :", font=("Arial", 14))
    token_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
    token_entry = ctk.CTkEntry(app, width=500, font=("Arial", 12))
    token_entry.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

    # Bouton pour démarrer le bot
    start_button = ctk.CTkButton(app, text="Démarrer le bot", **button_style, command=start_bot)
    start_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    # Zone de texte pour le message
    message_label = ctk.CTkLabel(app, text="Message à envoyer :", font=("Arial", 14))
    message_label.grid(row=3, column=0, padx=20, pady=(10, 5), sticky="w")
    message_text = ctk.CTkTextbox(app, width=650, height=100, font=("Arial", 12))
    message_text.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")

    # Bouton pour envoyer les messages
    send_button = ctk.CTkButton(app, text="Envoyer les messages", **button_style, command=send_dm)
    send_button.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

    # Console de logs
    console_label = ctk.CTkLabel(app, text="Console :", font=("Arial", 14))
    console_label.grid(row=6, column=0, padx=20, pady=(10, 5), sticky="w")
    console_text = ctk.CTkTextbox(app, width=650, height=150, font=("Arial", 12), state="disabled")
    console_text.grid(row=7, column=0, padx=20, pady=(0, 10), sticky="nsew")

    # Crédit "shadow DEV" en bas au milieu
    credit_label = ctk.CTkLabel(
        app,
        text="shadow DEV",
        font=("Arial", 12, "italic"),
        text_color="gray"
    )
    credit_label.grid(row=8, column=0, padx=20, pady=(0, 20), sticky="s")  # Placement en bas

    # Lancer l'application
    app.mainloop()

# Fonction pour l'interface graphique Raid Tool
def raid_tool_interface():
    # Configuration de CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    class DiscordBotTool(ctk.CTk):
        def __init__(self):
            super().__init__()

            self.title("Discord Bot Tool")
            self.geometry("450x700")  # Taille de la fenêtre ajustée pour inclure le défilement

            # Variables pour stocker les entrées
            self.token_var = ctk.StringVar()
            self.guild_id_var = ctk.StringVar()
            self.num_channels_var = ctk.StringVar()
            self.channel_name_var = ctk.StringVar()
            self.num_messages_var = ctk.StringVar()
            self.message_content_var = ctk.StringVar()

            # Création des widgets
            self.create_widgets()

        def create_widgets(self):
            # Texte en haut : "Scrapper Raider"
            ctk.CTkLabel(self, text="Scrapper Raider", font=("Arial", 25)).pack(pady=10)

            # Texte en rouge juste en dessous de "Scrapper Raider"
            ctk.CTkLabel(self, text="Use With VPN Or Ban Temp", font=("Arial", 11), text_color="red").pack(pady=5)

            # Token du bot
            ctk.CTkLabel(self, text="Token du bot:").pack(pady=5)
            ctk.CTkEntry(self, textvariable=self.token_var, width=400).pack(pady=5)

            # ID du serveur
            ctk.CTkLabel(self, text="ID du serveur:").pack(pady=5)
            ctk.CTkEntry(self, textvariable=self.guild_id_var, width=400).pack(pady=5)

            # Nombre de salons à créer
            ctk.CTkLabel(self, text="Nombre de salons:").pack(pady=5)
            ctk.CTkEntry(self, textvariable=self.num_channels_var, width=400).pack(pady=5)

            # Nom des salons
            ctk.CTkLabel(self, text="Nom des salons:").pack(pady=5)
            ctk.CTkEntry(self, textvariable=self.channel_name_var, width=400).pack(pady=5)

            # Nombre de messages à envoyer
            ctk.CTkLabel(self, text="Nombre de messages:").pack(pady=5)
            ctk.CTkEntry(self, textvariable=self.num_messages_var, width=400).pack(pady=5)

            # Contenu du message
            ctk.CTkLabel(self, text="Message à envoyer:").pack(pady=5)
            ctk.CTkEntry(self, textvariable=self.message_content_var, width=400).pack(pady=5)

            # Bouton pour créer les salons (gris foncé)
            ctk.CTkButton(self, text="Créer les salons", command=self.create_channels, fg_color="#333333").pack(pady=10)

            # Bouton pour envoyer les messages (gris foncé)
            ctk.CTkButton(self, text="Envoyer les messages", command=self.send_messages, fg_color="#333333").pack(pady=10)

            # Bouton pour supprimer tous les salons (gris foncé)
            ctk.CTkButton(self, text="Supprimer tous les salons", command=self.delete_channels, fg_color="#333333").pack(pady=10)

        async def run_bot(self, coro):
            """Exécute une coroutine Discord dans un événement asyncio."""
            bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

            @bot.event
            async def on_ready():
                try:
                    await coro(bot)
                except Exception as e:
                    print(f"Erreur : {e}")
                finally:
                    await bot.close()

            await bot.start(self.token_var.get())

        def create_channels(self):
            """Crée les salons dans le serveur."""
            guild_id = int(self.guild_id_var.get())
            num_channels = int(self.num_channels_var.get())
            channel_name = self.channel_name_var.get()

            async def create_channels_coro(bot):
                guild = bot.get_guild(guild_id)
                if guild:
                    # Créer les salons en parallèle
                    tasks = [guild.create_text_channel(channel_name) for _ in range(num_channels)]
                    await asyncio.gather(*tasks)
                    print(f"{num_channels} salons créés avec succès.")
                else:
                    print("Serveur introuvable.")

            asyncio.run(self.run_bot(create_channels_coro))

        def send_messages(self):
            """Envoie des messages dans tous les salons textuels du serveur."""
            guild_id = int(self.guild_id_var.get())
            num_messages = int(self.num_messages_var.get())
            message_content = self.message_content_var.get()

            async def send_messages_coro(bot):
                guild = bot.get_guild(guild_id)
                if guild:
                    # Envoyer des messages dans tous les salons textuels
                    tasks = []
                    for channel in guild.text_channels:
                        for _ in range(num_messages):
                            tasks.append(channel.send(message_content))
                    await asyncio.gather(*tasks)
                    print(f"Messages envoyés dans tous les salons.")
                else:
                    print("Serveur introuvable.")

            asyncio.run(self.run_bot(send_messages_coro))

        def delete_channels(self):
            """Supprime tous les salons textuels du serveur."""
            guild_id = int(self.guild_id_var.get())

            async def delete_channels_coro(bot):
                guild = bot.get_guild(guild_id)
                if guild:
                    # Supprimer tous les salons textuels en parallèle
                    tasks = [channel.delete() for channel in guild.text_channels]
                    await asyncio.gather(*tasks)
                    print("Tous les salons ont été supprimés.")
                else:
                    print("Serveur introuvable.")

            asyncio.run(self.run_bot(delete_channels_coro))

    # Lancer l'application
    app = DiscordBotTool()
    app.mainloop()

# Fonction principale
def main():
    while True:
        afficher_menu()
        choix = input(green_text("└───@scrapper-Tool: "))
        
        if choix.lower() == 'q':
            print(green_text("Au revoir !"))
            break
        
        try:
            choix = int(choix)
            if choix == 1:
                webhook_spammer()
            elif choix == 2:
                webhook_create()
            elif choix == 3:
                webhook_info()
            elif choix == 4:
                ip_lookup()
            elif choix == 5:
                coordonnees()
            elif choix == 6:
                url_info()
            elif choix == 7:
                raid_tool_interface()
            elif choix == 8:
                threading.Thread(target=dm_tool_interface, daemon=True).start()
            elif choix == 9:
                creators_profil()
            elif choix == 10:
                ip_pinger()
            elif choix == 11:
                join_discord()
            else:
                print(green_text("Veuillez choisir une option entre 1 et 11."))
        except ValueError:
            print(green_text("Entrée invalide. Veuillez entrer un nombre entre 1 et 11 ou 'Q' pour quitter."))

if __name__ == "__main__":
    main()