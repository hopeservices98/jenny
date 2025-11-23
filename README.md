# Jenny - Application de Chat IA Confidentielle

## Description
Jenny est une application web de chat IA thérapeutique et confidentielle, conçue pour offrir des conversations intimes et analytiques. L'IA utilise Grok de xAI via OpenRouter pour répondre de manière empathique, avec des fonctionnalités d'upload d'images et d'audios, une interface moderne, et des paramètres de sécurité ajustés.

## Fonctionnalités
- **Chat IA** : Conversations avec Jenny, IA thérapeutique utilisant Grok (xAI) via OpenRouter.
- **Uploads** : Possibilité d'uploader des images et des audios directement dans le chat.
- **Interface Moderne** : Design sombre avec Tailwind CSS, avatar de Jenny, indicateur de frappe animé.
- **Sécurité** : Paramètres de sécurité ajustés pour permettre des discussions sensibles.
- **Historique** : Sauvegarde des conversations par utilisateur dans une base de données SQLite.

## Technologies Utilisées
- **Backend** : Flask (Python), SQLAlchemy, OpenRouter API.
- **Frontend** : HTML, CSS (Tailwind), JavaScript.
- **Base de Données** : SQLite.
- **IA** : Grok (xAI) via OpenRouter.

## Installation et Configuration

### Prérequis
- Python 3.8+
- Pip
- Clé API OpenRouter

### Étapes
1. **Cloner ou télécharger le projet** :
   ```
   git clone https://github.com/hopeservices98/jenny.git
   cd jenny
   ```

2. **Installer les dépendances** :
   ```
   pip install -r requirements.txt
   ```

3. **Configurer l'API** :
   - Obtenir une clé API gratuite sur [OpenRouter](https://openrouter.ai/).
   - Définir la variable d'environnement `OPENROUTER_API_KEY` avec votre clé.
     - Exemple (Windows) : `set OPENROUTER_API_KEY=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`
     - Exemple (Linux/Mac) : `export OPENROUTER_API_KEY=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`
   - Optionnellement, ajuster `OPENROUTER_MODEL` dans `app/config.py` (défaut: x-ai/grok-4.1-fast:free).

4. **Lancer l'application** :
   ```
   python run.py
   ```
   - Accéder à http://127.0.0.1:5000/

### Déploiement sur Render
1. Connecter le repo GitHub sur [Render](https://render.com).
2. Créer un Web Service Python.
3. Ajouter les variables d'environnement :
   - `OPENROUTER_API_KEY`
   - `SECRET_KEY` (générez une clé secrète)
   - `FLASK_ENV=production`

## Structure du Projet
- `run.py` : Point d'entrée de l'application.
- `app/` : Code backend Flask.
  - `routes.py` : Routes API et logique de chat.
  - `models.py` : Modèles de base de données.
  - `config.py` : Configuration.
  - `static/` : Fichiers statiques (CSS, JS).
  - `templates/` : Templates HTML.
- `images/` : Images pour les avatars.
- `instance/` : Base de données SQLite (non versionnée).
- `requirements.txt` : Dépendances Python.
- `Procfile` : Configuration pour Render.

## Utilisation
- Ouvrir l'application dans un navigateur.
- Commencer une conversation avec Jenny.
- Uploader des images ou audios via les boutons dédiés.
- Les réponses de Jenny sont générées par l'IA avec un focus sur l'empathie et l'analyse.

## Dépannage
- **Erreur API** : Vérifier la clé API OpenRouter et les crédits disponibles.
- **Modèles non trouvés** : Vérifier la configuration du modèle dans `app/config.py`.
- **Uploads** : Le dossier `uploads/` est créé automatiquement.
- **Déploiement** : Assurer que toutes les variables d'environnement sont définies sur Render.

## Licence
Ce projet est open-source. Utilisez-le à vos risques et périls.

## Contact
Pour des questions, contacter le développeur.