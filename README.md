# 📡 Script Freebox API - Application Raddar

Ce script permet de créer et autoriser une application nommée "Raddar" sur votre Freebox pour obtenir un token d'accès à l'API.

## 🎯 Objectif

Le script vous aide à :
- Créer une application "Raddar" sur votre Freebox
- Obtenir un token d'accès valide
- Récupérer l'ID de l'application
- Sauvegarder les identifiants pour une utilisation future

## 📋 Prérequis

- Python 3.6 ou plus récent
- Une Freebox connectée au réseau
- Accès physique à votre Freebox (pour valider sur l'écran LCD)

## 🚀 Installation

### 1. Télécharger les fichiers
Assurez-vous d'avoir les fichiers suivants dans le même dossier :
- `freebox.py` (le script principal)
- `requirements.txt` (les dépendances)

### 2. Créer l'environnement virtuel
```bash
python3 -m venv venv
```

### 3. Activer l'environnement virtuel
```bash
source venv/bin/activate
```

### 4. Installer les dépendances
```bash
pip install -r requirements.txt
```

## 🎮 Utilisation

### Première utilisation (création de l'application)

1. **Lancer le script**
   ```bash
   python3 freebox.py
   ```

2. **Suivre les étapes affichées**
   - Le script se connecte automatiquement à votre Freebox
   - Il affiche les informations de votre Freebox (modèle, version API)
   - Il enregistre l'application "Raddar"

3. **Valider sur la Freebox** 🔔
   - Quand le message apparaît, allez sur l'écran LCD de votre Freebox
   - Naviguez dans les menus pour trouver la demande d'autorisation
   - Acceptez l'application "Raddar"
   - Le script attend jusqu'à 2 minutes votre validation

4. **Récupération automatique**
   - Une fois validé, le script récupère automatiquement le token
   - Les identifiants sont sauvegardés dans `freebox_credentials.json`

### Utilisations suivantes

Si vous relancez le script et qu'un fichier `freebox_credentials.json` existe :
- Le script propose d'utiliser les identifiants existants
- Tapez `N` (ou Entrée) pour utiliser les identifiants existants
- Tapez `O` pour créer une nouvelle autorisation

## 📁 Fichiers générés

### `freebox_credentials.json`
Contient vos identifiants d'accès :
```json
{
  "app_id": "raddar",
  "app_name": "Raddar",
  "app_version": "1.0.0",
  "app_token": "votre_token_ici",
  "freebox_ip": "adresse_de_votre_freebox",
  "api_version": "14.0"
}
```

## 📊 Exemple d'exécution réussie

```
🚀 Script d'enregistrement de l'application Raddar pour Freebox
============================================================

📡 Connexion à la Freebox...
✓ Version de l'API Freebox: 14.0
✓ Modèle de Freebox: Freebox v9 (r1)
✓ Domaine API: lacd3kpj.fbxos.fr

📝 Enregistrement de l'application 'Raddar'...
✓ Application enregistrée avec succès!
  - App Token: g/AdEHoXJzWwMblvl3jULCQvaEs8UfyQF9iC31tu8IoXKH6VhkjRPaNUROn4AvwK
  - Track ID: 7
  - App ID: raddar

============================================================
🔔 VALIDATION REQUISE SUR LA FREEBOX
============================================================
Veuillez vous rendre sur l'écran LCD de votre Freebox
et accepter la demande d'autorisation pour l'application 'Raddar'
============================================================

✓ Autorisation accordée avec succès!
🎉 Application autorisée avec succès!
✓ Identifiants sauvegardés dans: freebox_credentials.json

📋 RÉSUMÉ DE L'APPLICATION
========================================
App ID: raddar
App Name: Raddar
App Token: g/AdEHoXJzWwMblvl3jULCQvaEs8UfyQF9iC31tu8IoXKH6VhkjRPaNUROn4AvwK
Freebox IP: lacd3kpj.fbxos.fr
API Version: 14.0
========================================
✅ L'application Raddar est maintenant prête à être utilisée!
```

## ❓ Résolution des problèmes

### Erreur de connexion
- Vérifiez que votre Freebox est allumée et connectée
- Assurez-vous d'être sur le même réseau que la Freebox

### Timeout de validation
- Vous avez 2 minutes pour valider sur l'écran LCD
- Si le temps expire, relancez simplement le script

### Erreur SSL
- Le script désactive automatiquement la vérification SSL (normal pour les API locales)

### Application déjà existante
- Si l'application existe déjà, le script propose de la recréer
- Vous pouvez aussi utiliser les identifiants existants

## 🔧 Informations techniques

- **Langage** : Python 3
- **Dépendances** : requests, urllib3
- **API utilisée** : Freebox API v14.0
- **Protocole** : HTTPS avec certificat auto-signé

## 📞 Support

En cas de problème :
1. Vérifiez que votre Freebox est accessible
2. Relancez le script (il est conçu pour être relancé sans problème)
3. Vérifiez les messages d'erreur affichés

## 🎉 Utilisation du token

Une fois le token obtenu, vous pouvez l'utiliser pour :
- Accéder à l'API Freebox
- Contrôler votre Freebox à distance
- Développer des applications personnalisées

Le token est valide indéfiniment jusqu'à révocation manuelle.