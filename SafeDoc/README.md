# 🔒 SafeDoc - Coffre-fort Numérique Intelligent

> Application Python intelligente pour la gestion sécurisée de vos documents importants avec OCR, NLP et chiffrement AES.

## 🌟 Notre Vision

SafeDoc est une solution complète qui permet de :
- 📷 **Scanner** les documents
- 🔍 **Extraire** automatiquement le texte
- 🧠 **Classer** intelligemment les documents
- 🔐 **Sécuriser** les fichiers par chiffrement

---


## ✨ Fonctionnalités

### 🔍 Scanner Intelligent (OCR)
- Numérisation de documents papier
- Extraction de texte depuis images et PDF
- Prétraitement d'images pour meilleure qualité

### 🧠 Extraction Automatique (NLP)
- Extraction d'entités (noms, dates, montants)
- Classification automatique par type de document
- Extraction de métadonnées intelligente

### 🔐 Sécurité Maximale
- Chiffrement AES-256 de tous les documents
- Authentification utilisateur sécurisée
- Gestion de clés avec PBKDF2

### 💻 Interfaces Multiples
- **Interface Web** : Application Streamlit moderne et intuitive
- **Interface CLI** : Ligne de commande pour utilisateurs avancés

### ☁️ Stockage Cloud Premium
- Synchronisation Google Drive automatique
- Sauvegarde cloud sécurisée
- Accès depuis n'importe où

## 🚀 Installation

### Prérequis
- Python 3.9 ou supérieur
- Tesseract OCR ([Installation](https://github.com/tesseract-ocr/tesseract))

### Installation via virtualenv

```bash
# 1. Cloner le projet
cd "C:\Users\Thierno Mouctar\Desktop\Projet Python\SafeDoc"

# 2. Créer l'environnement virtuel
python -m venv venv

# 3. Activer l'environnement
# Sur Windows
.\venv\Scripts\activate
# Sur Linux/Mac
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Télécharger le modèle spaCy français
python -m spacy download fr_core_news_md

# 6. Télécharger les données NLTK
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## 📖 Utilisation

### Interface Web (Recommandée)

```bash
streamlit run src/web/app.py
```

Ouvrez votre navigateur à l'adresse : `http://localhost:8501`

### Interface CLI

```bash
# Téléverser un document
python main.py televerser chemin/vers/document.pdf

# Lister tous les documents
python main.py lister

# Rechercher un document
python main.py rechercher "facture"

# Voir un document
python main.py voir <id_document>

# Synchroniser avec le cloud (Premium)
python main.py synchroniser
```

## 📁 Structure du Projet

```
SafeDoc/
├── config/              # Configuration de l'application
├── src/
│   ├── ocr/            # Module de reconnaissance OCR
│   ├── nlp/            # Module de traitement NLP
│   ├── securite/       # Chiffrement et authentification
│   ├── stockage/       # Base de données et fichiers
│   ├── cli/            # Interface ligne de commande
│   ├── web/            # Interface web Streamlit
│   └── utils/          # Utilitaires divers
├── tests/              # Tests unitaires
├── docs/               # Documentation
└── data/               # Données (ignoré par Git)
```

## 🎓 Catégories de Documents Supportées

- 📄 Factures
- 📝 Contrats
- 🪪 Pièces d'identité
- 🏥 Documents médicaux
- 💰 Documents fiscaux
- 🎓 Documents éducatifs
- 📋 Documents administratifs
- 📊 Autres

## 💎 Version Premium

### Gratuit
- ✅ Stockage local illimité
- ✅ OCR et classification
- ✅ Chiffrement AES-256
- ⚠️ Pas de synchronisation cloud

### Premium
- ✅ Tout ce qui est gratuit
- ✅ Synchronisation Google Drive
- ✅ Sauvegarde automatique
- ✅ Accès multi-appareils
- ✅ Support prioritaire

## 🔧 Configuration

Créez un fichier `.env` à la racine du projet :

```env
# Base de données
DATABASE_URL=sqlite:///data/safedoc.db

# Clé de chiffrement principale (générez-en une unique)
MASTER_KEY=votre_cle_secrete_tres_longue_et_aleatoire

# Google Drive (optionnel, pour Premium)
GOOGLE_CLIENT_ID=votre_client_id
GOOGLE_CLIENT_SECRET=votre_client_secret

# Limites de stockage
FREE_TIER_LIMIT_MB=500
PREMIUM_TIER_LIMIT_MB=50000
```

## 🧪 Tests

```bash
# Exécuter tous les tests
pytest tests/ -v

# Tests avec couverture
pytest tests/ --cov=src --cov-report=html
```

## 📚 Documentation

- [Manuel Utilisateur](docs/manuel_utilisateur.md)
- [Documentation API](docs/documentation_api.md)
- [Guide de Contribution](docs/CONTRIBUTING.md)

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez consulter le guide de contribution.

## 📄 Licence

Ce projet est sous licence MIT.

## 👨‍💻 Auteur

Projet développé dans le cadre de l'apprentissage Python - Gestion de documents sécurisée.

## 🆘 Support

Pour toute question ou problème :
- Consultez la [Documentation](docs/)
- Ouvrez une [Issue](https://github.com/votre-repo/safedoc/issues)

---

**⚠️ Important** : Ne partagez jamais vos clés de chiffrement. Conservez-les en lieu sûr !
