# 🚀 Guide de Démarrage Rapide - SafeDoc

## ⚡ Démarrage en 3 étapes

### Étape 1: Installer Tesseract OCR

**Windows:**
1. Télécharger: https://github.com/UB-Mannheim/tesseract/wiki
2. Installer dans `C:\Program Files\Tesseract-OCR`

**Mac:**
```bash
brew install tesseract tesseract-lang
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-fra
```

### Étape 2: Lancer le script automatique

**Windows - Double-cliquez sur:**
```
demarrer.bat
```

**Mac/Linux:**
```bash
chmod +x demarrer.sh
./demarrer.sh
```

Le script va automatiquement :
- ✅ Installer toutes les dépendances
- ✅ Télécharger les modèles NLP
- ✅ Lancer l'application web

### Étape 3: Utiliser SafeDoc

1. **L'application s'ouvre automatiquement** dans votre navigateur.
2. **Accès Direct** : Vous arrivez directement sur le tableau de bord.
3. **Sécurité** : Le chiffrement est automatique.

---

## 📖 Première Utilisation

### Téléverser un document

1. Cliquez sur **"📤 Téléverser"**
2. Glissez-déposez votre fichier (PDF, image)
3. Cliquez sur **"Traiter et Sauvegarder"**
4. SafeDoc va automatiquement :
   - 🔍 Extraire le texte (OCR)
   - 🧠 Classifier le document
   - 📝 Extraire les informations clés
   - 🔐 Chiffrer le document
   - 💾 Sauvegarder en sécurité

### Voir vos documents

1. Cliquez sur **"📚 Bibliothèque"**
2. Cliquez sur **👁️** pour voir un document
3. Le fichier est déchiffré automatiquement et téléchargé.

---

## 💡 Conseils

### ✅ Bonnes Pratiques

- 📝 Notez votre mot de passe de chiffrement dans un lieu sûr
- 🔍 Scannez vos documents en haute qualité (300 DPI minimum)
- 🏷️ Vérifiez la catégorie automatique et corrigez si besoin
- 💾 Surveillez votre quota de stockage
- 🚪 Déconnectez-vous après utilisation

### ⚠️ À Éviter

- ❌ Ne partagez jamais vos mots de passe
- ❌ Ne perdez pas votre mot de passe de chiffrement
- ❌ N'uploadez pas de documents non scannés de mauvaise qualité
- ❌ Ne dépassez pas 50 MB par fichier

---

## 🆘 Besoin d'aide ?

### Documentation Complète
📖 Consultez le [Manuel Utilisateur](docs/manuel_utilisateur.md)

### Problèmes Courants

**"Tesseract non trouvé"**
→ Installez Tesseract OCR (voir Étape 1)

**"Modèle spaCy non trouvé"**
→ Exécutez: `python -m spacy download fr_core_news_md`

**"Quota dépassé"**
→ Supprimez des documents ou passez Premium

---

## 🎯 Fonctionnalités Principales

| Fonctionnalité | Description |
|----------------|-------------|
| 🔍 **OCR** | Extraction automatique de texte |
| 🧠 **Classification** | Détection automatique du type de document |
| 📝 **Extraction** | Dates, montants, emails, téléphones, etc. |
| 🔐 **Chiffrement** | AES-256 de niveau militaire |
| 🔍 **Recherche** | Par nom, contenu ou catégorie |
| 💾 **Stockage** | Local sécurisé (ou cloud Premium) |

---

## ⭐ Gratuit vs Premium

| | 🆓 Gratuit | ⭐ Premium |
|---|---|---|
| **Stockage** | 500 MB | 50 GB |
| **OCR** | ✅ | ✅ |
| **Classification** | ✅ | ✅ |
| **Chiffrement** | ✅ | ✅ |
| **Cloud** | ❌ | ✅ Google Drive |
| **Support** | Standard | Prioritaire |

---

**🔒 SafeDoc - Vos documents, en sécurité, pour toujours.**

*Prêt en 3 minutes ⚡*
