#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour créer et autoriser une application Freebox nommée "raddar"
Ce script permet de récupérer un token valide et l'ID de l'application
après validation sur l'écran LCD de la Freebox.
"""

import requests
import json
import time
import sys
from typing import Dict, Optional, Tuple
import urllib3

# Désactiver les avertissements SSL pour les connexions locales Freebox
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class FreeboxAPI:
    def __init__(self, freebox_ip: str = "mafreebox.freebox.fr"):
        """
        Initialise la connexion à l'API Freebox
        
        Args:
            freebox_ip: Adresse IP ou nom d'hôte de la Freebox (par défaut: mafreebox.freebox.fr)
        """
        self.freebox_ip = freebox_ip
        self.base_url = f"http://{freebox_ip}/api"
        self.api_version = None
        self.app_token = None
        self.app_id = None
        self.session_token = None
        
        # Informations de l'application
        self.app_info = {
            "app_id": "raddar",
            "app_name": "Raddar",
            "app_version": "1.0.0",
            "device_name": "Python Script"
        }
    
    def get_api_version(self) -> Optional[str]:
        """
        Récupère la version de l'API Freebox
        
        Returns:
            Version de l'API ou None en cas d'erreur
        """
        try:
            response = requests.get(f"{self.base_url}/v1/api_version", timeout=10, verify=False)
            response.raise_for_status()
            data = response.json()
            
            # La réponse de l'API version ne contient pas de champ "success"
            # mais directement les informations
            if "api_version" in data:
                self.api_version = data["api_version"]
                print(f"✓ Version de l'API Freebox: {self.api_version}")
                print(f"✓ Modèle de Freebox: {data.get('box_model_name', 'Inconnu')}")
                print(f"✓ Domaine API: {data.get('api_domain', 'mafreebox.freebox.fr')}")
                
                # Mettre à jour l'URL de base avec le domaine API si disponible
                if data.get('api_domain'):
                    self.freebox_ip = data['api_domain']
                    api_base_url = data.get('api_base_url', '/api/')
                    self.base_url = f"https://{self.freebox_ip}:{data.get('https_port', 443)}{api_base_url.rstrip('/')}"
                
                return self.api_version
            else:
                print(f"✗ Erreur lors de la récupération de la version API: {data}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Erreur de connexion à la Freebox: {e}")
            return None
    
    def register_app(self) -> Optional[Tuple[str, str]]:
        """
        Enregistre l'application auprès de la Freebox
        
        Returns:
            Tuple (app_token, track_id) ou None en cas d'erreur
        """
        if not self.api_version:
            print("✗ Version API non disponible")
            return None
        
        # Utiliser seulement la version majeure de l'API
        api_major_version = self.api_version.split('.')[0]
        url = f"{self.base_url}/v{api_major_version}/login/authorize/"
        
        try:
            response = requests.post(url, json=self.app_info, timeout=10, verify=False)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success"):
                app_token = data["result"]["app_token"]
                track_id = data["result"]["track_id"]
                
                print(f"✓ Application enregistrée avec succès!")
                print(f"  - App Token: {app_token}")
                print(f"  - Track ID: {track_id}")
                print(f"  - App ID: {self.app_info['app_id']}")
                
                self.app_token = app_token
                return app_token, track_id
            else:
                print(f"✗ Erreur lors de l'enregistrement: {data}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Erreur lors de l'enregistrement: {e}")
            return None
    
    def check_authorization_status(self, track_id: str) -> str:
        """
        Vérifie le statut d'autorisation de l'application
        
        Args:
            track_id: ID de suivi de la demande d'autorisation
            
        Returns:
            Statut de l'autorisation ('unknown', 'pending', 'timeout', 'granted', 'denied')
        """
        if not self.api_version:
            return "unknown"
        
        # Utiliser seulement la version majeure de l'API
        api_major_version = self.api_version.split('.')[0]
        url = f"{self.base_url}/v{api_major_version}/login/authorize/{track_id}"
        
        try:
            response = requests.get(url, timeout=10, verify=False)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success"):
                status = data["result"]["status"]
                challenge = data["result"].get("challenge", "")
                
                if status == "granted":
                    print(f"✓ Autorisation accordée! Challenge: {challenge}")
                
                return status
            else:
                print(f"✗ Erreur lors de la vérification du statut: {data}")
                return "unknown"
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Erreur lors de la vérification: {e}")
            return "unknown"
    
    def wait_for_authorization(self, track_id: str, timeout: int = 120) -> bool:
        """
        Attend l'autorisation de l'utilisateur sur l'écran LCD
        
        Args:
            track_id: ID de suivi de la demande
            timeout: Timeout en secondes (par défaut: 120s)
            
        Returns:
            True si autorisé, False sinon
        """
        print("\n" + "="*60)
        print("🔔 VALIDATION REQUISE SUR LA FREEBOX")
        print("="*60)
        print("Veuillez vous rendre sur l'écran LCD de votre Freebox")
        print("et accepter la demande d'autorisation pour l'application 'Raddar'")
        print("="*60)
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.check_authorization_status(track_id)
            
            if status == "granted":
                print("\n✓ Autorisation accordée avec succès!")
                return True
            elif status == "denied":
                print("\n✗ Autorisation refusée par l'utilisateur")
                return False
            elif status == "timeout":
                print("\n✗ Timeout de la demande d'autorisation")
                return False
            elif status == "pending":
                remaining = int(timeout - (time.time() - start_time))
                print(f"\r⏳ En attente de validation... ({remaining}s restantes)", end="", flush=True)
                time.sleep(2)
            else:
                print(f"\n⚠️  Statut inconnu: {status}")
                time.sleep(2)
        
        print(f"\n✗ Timeout après {timeout} secondes")
        return False
    
    def save_credentials(self, filename: str = "freebox_credentials.json") -> bool:
        """
        Sauvegarde les identifiants dans un fichier JSON
        
        Args:
            filename: Nom du fichier de sauvegarde
            
        Returns:
            True si sauvegardé avec succès, False sinon
        """
        if not self.app_token:
            print("✗ Aucun token à sauvegarder")
            return False
        
        credentials = {
            "app_id": self.app_info["app_id"],
            "app_name": self.app_info["app_name"],
            "app_version": self.app_info["app_version"],
            "app_token": self.app_token,
            "freebox_ip": self.freebox_ip,
            "api_version": self.api_version
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(credentials, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Identifiants sauvegardés dans: {filename}")
            return True
            
        except Exception as e:
            print(f"✗ Erreur lors de la sauvegarde: {e}")
            return False
    
    def load_credentials(self, filename: str = "freebox_credentials.json") -> bool:
        """
        Charge les identifiants depuis un fichier JSON
        
        Args:
            filename: Nom du fichier à charger
            
        Returns:
            True si chargé avec succès, False sinon
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                credentials = json.load(f)
            
            self.app_token = credentials.get("app_token")
            self.api_version = credentials.get("api_version")
            self.freebox_ip = credentials.get("freebox_ip", self.freebox_ip)
            
            print(f"✓ Identifiants chargés depuis: {filename}")
            return True
            
        except FileNotFoundError:
            print(f"⚠️  Fichier non trouvé: {filename}")
            return False
        except Exception as e:
            print(f"✗ Erreur lors du chargement: {e}")
            return False


def main():
    """
    Fonction principale pour créer et autoriser l'application Raddar
    """
    print("🚀 Script d'enregistrement de l'application Raddar pour Freebox")
    print("=" * 60)
    
    # Initialisation de l'API Freebox
    freebox = FreeboxAPI()
    
    # Étape 1: Récupération de la version API
    print("\n📡 Connexion à la Freebox...")
    if not freebox.get_api_version():
        print("✗ Impossible de se connecter à la Freebox")
        sys.exit(1)
    
    # Étape 2: Vérification si des identifiants existent déjà
    if freebox.load_credentials():
        print("✓ Identifiants existants trouvés")
        print(f"  - App ID: {freebox.app_info['app_id']}")
        print(f"  - App Token: {freebox.app_token}")
        
        choice = input("\nVoulez-vous créer une nouvelle autorisation ? (o/N): ").lower()
        if choice not in ['o', 'oui', 'y', 'yes']:
            print("✓ Utilisation des identifiants existants")
            return
    
    # Étape 3: Enregistrement de l'application
    print(f"\n📝 Enregistrement de l'application '{freebox.app_info['app_name']}'...")
    result = freebox.register_app()
    
    if not result:
        print("✗ Échec de l'enregistrement de l'application")
        sys.exit(1)
    
    app_token, track_id = result
    
    # Étape 4: Attente de l'autorisation
    if freebox.wait_for_authorization(track_id):
        print("\n🎉 Application autorisée avec succès!")
        
        # Étape 5: Sauvegarde des identifiants
        if freebox.save_credentials():
            print("\n📋 RÉSUMÉ DE L'APPLICATION")
            print("=" * 40)
            print(f"App ID: {freebox.app_info['app_id']}")
            print(f"App Name: {freebox.app_info['app_name']}")
            print(f"App Token: {app_token}")
            print(f"Freebox IP: {freebox.freebox_ip}")
            print(f"API Version: {freebox.api_version}")
            print("=" * 40)
            print("✅ L'application Raddar est maintenant prête à être utilisée!")
        else:
            print("⚠️  Application autorisée mais erreur de sauvegarde")
    else:
        print("\n❌ Échec de l'autorisation de l'application")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Script interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")
        sys.exit(1)