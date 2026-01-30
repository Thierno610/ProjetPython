"""
SafeDoc Flask Application - Version Optimisée & Corrigée
"""

import sys
from pathlib import Path
from datetime import datetime
import os

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify, send_from_directory

app = Flask(__name__)
app.secret_key = 'safedoc-optimized-2024'

# Configuration
try:
    from config.config import (
        MAX_UPLOAD_SIZE_BYTES, 
        ALLOWED_EXTENSIONS as CONFIG_ALLOWED,
        FREE_TIER_LIMIT_MB,
        PREMIUM_TIER_LIMIT_MB
    )
    ALLOWED_EXTENSIONS = set(CONFIG_ALLOWED)
    MAX_CONTENT_LENGTH = MAX_UPLOAD_SIZE_BYTES
except ImportError:
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    FREE_TIER_LIMIT_MB = 500
    PREMIUM_TIER_LIMIT_MB = 50000

app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = 'temp'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Import des modules avec gestion d'erreur
try:
    from src.stockage.base_de_donnees import gestionnaire_bdd
    BDD_AVAILABLE = True
except ImportError:
    print("⚠️ Base de données non disponible - Mode démonstration")
    BDD_AVAILABLE = False

try:
    from src.securite.authentification import gestionnaire_auth, Utilisateur
    AUTH_AVAILABLE = True
except ImportError:
    print("⚠️ Authentification non disponible - Mode démonstration")
    AUTH_AVAILABLE = False

try:
    from src.utils.gestionnaire_documents import gestionnaire_documents
    DOCS_AVAILABLE = True
except ImportError:
    print("⚠️ Gestionnaire de documents non disponible - Mode démonstration")
    DOCS_AVAILABLE = False

# Données de démonstration
DEMO_USER = {
    'id': 1,
    'nom_utilisateur': 'Utilisateur',
    'niveau': 'premium',
    'stockage_utilise': 1048576,
    'date_creation': datetime.now().isoformat()
}

DEMO_DOCUMENTS = [
    {
        'id': 1,
        'nom': 'facture_electricite.pdf',
        'categorie': 'Facture',
        'taille_fichier': 2048576,
        'date_upload': datetime.now(),
        'etiquettes': [{'nom': 'Urgent', 'couleur': '#FF4444'}]
    },
    {
        'id': 2,
        'nom': 'contrat_travail.pdf',
        'categorie': 'Contrat',
        'taille_fichier': 1024576,
        'date_upload': datetime.now(),
        'etiquettes': [{'nom': 'Important', 'couleur': '#4444FF'}]
    }
]

# Stockage des étiquettes en mémoire (pour la démo)
ETIQUETTES_DB = [
    {'id': 1, 'nom': 'Urgent', 'couleur': '#FF4444'},
    {'id': 2, 'nom': 'Important', 'couleur': '#4444FF'},
    {'id': 3, 'nom': 'Travail', 'couleur': '#44FF44'}
]
ETIQUETTES_ID_COUNTER = 4

class UtilisateurOptimized:
    def __init__(self, data):
        self.id = data['id']
        self.nom_utilisateur = data['nom_utilisateur']
        self.niveau = data['niveau']
        self.stockage_utilise = data.get('stockage_utilise', 0)
        self.date_creation = data.get('date_creation')
    
    def est_premium(self):
        return self.niveau == 'premium'
    
    def pourcentage_stockage(self):
        limite = self.obtenir_limite_stockage()
        return (self.stockage_utilise / limite) * 100 if limite > 0 else 0
    
    def obtenir_limite_stockage(self):
        limit_mb = PREMIUM_TIER_LIMIT_MB if self.est_premium() else FREE_TIER_LIMIT_MB
        return limit_mb * 1024 * 1024

def get_utilisateur_session():
    if 'utilisateur' not in session:
        return None
    return UtilisateurOptimized(session['utilisateur'])

def get_documents_utilisateur(user_id):
    if DOCS_AVAILABLE and BDD_AVAILABLE:
        try:
            return gestionnaire_bdd.obtenir_documents_utilisateur(user_id)
        except Exception as e:
            print(f"⚠️ Erreur documents: {e}")
            return DEMO_DOCUMENTS
    return DEMO_DOCUMENTS

# --- ROUTES PRINCIPALES ---

@app.route('/static/<path:filename>')
def static_files(filename):
    """Servir les fichiers statiques"""
    return send_from_directory('static', filename)

@app.route('/')
def index():
    if 'utilisateur' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('connexion'))

@app.route('/dashboard')
def dashboard():
    user = get_utilisateur_session()
    if not user:
        return redirect(url_for('connexion'))
    
    documents = get_documents_utilisateur(user.id)
    documents_recents = documents[:5] if documents else []
    
    stockage_mb = user.stockage_utilise / (1024 * 1024)
    return render_template('dashboard.html', 
                         user=user,
                         documents=documents_recents,
                         stockage_mb=stockage_mb,
                         pourcentage_stockage=user.pourcentage_stockage(),
                         page='dashboard')

# --- AUTHENTIFICATION ---

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if 'utilisateur' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        nom_utilisateur = request.form.get('username')
        mot_de_passe = request.form.get('password')
        
        if AUTH_AVAILABLE and BDD_AVAILABLE:
            utilisateur_db = gestionnaire_bdd.obtenir_utilisateur_par_nom(nom_utilisateur)
            if utilisateur_db and gestionnaire_auth.verifier_mot_de_passe(mot_de_passe, utilisateur_db.hash_mot_de_passe):
                session['utilisateur'] = {
                    'id': utilisateur_db.id,
                    'nom_utilisateur': utilisateur_db.nom_utilisateur,
                    'niveau': utilisateur_db.niveau,
                    'stockage_utilise': utilisateur_db.stockage_utilise,
                    'date_creation': utilisateur_db.date_creation.isoformat() if utilisateur_db.date_creation else None
                }
                flash('Connexion réussie !', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Identifiants incorrects.', 'error')
        else:
            # Mode démo
            if nom_utilisateur == "Utilisateur" and mot_de_passe == "SafeDoc123!":
                session['utilisateur'] = DEMO_USER
                flash('Mode Démo: Connecté', 'success')
                return redirect(url_for('dashboard'))
            flash('Mode démo: Utilisez Utilisateur / SafeDoc123!', 'error')
                
    return render_template('login.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if 'utilisateur' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        nom_utilisateur = request.form.get('username')
        mot_de_passe = request.form.get('password')
        confirmation = request.form.get('confirm_password')
        
        if mot_de_passe != confirmation:
            flash('Mots de passe non identiques.', 'error')
            return render_template('register.html')
            
        if AUTH_AVAILABLE and BDD_AVAILABLE:
            valide, msg = gestionnaire_auth.valider_nom_utilisateur(nom_utilisateur)
            if not valide:
                flash(msg, 'error')
                return render_template('register.html')
                
            valide, msg = gestionnaire_auth.valider_mot_de_passe(mot_de_passe)
            if not valide:
                flash(msg, 'error')
                return render_template('register.html')
                
            hash_mdp = gestionnaire_auth.hacher_mot_de_passe(mot_de_passe)
            utilisateur = gestionnaire_bdd.creer_utilisateur(nom_utilisateur, hash_mdp, 'free')
            
            if utilisateur:
                flash('Compte créé ! Veuillez vous connecter.', 'success')
                return redirect(url_for('connexion'))
            flash('Nom déjà utilisé.', 'error')
        else:
            flash('Action non disponible en démo.', 'warning')
            
    return render_template('register.html')

@app.route('/mot-de-passe-oublie', methods=['GET', 'POST'])
def mot_de_passe_oublie():
    if request.method == 'POST':
        flash('Instructions envoyées par email.', 'success')
        return redirect(url_for('connexion'))
    return render_template('forgot_password.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Déconnexion effectuée.', 'success')
    return redirect(url_for('connexion'))

# --- AUTRES ROUTES ---

@app.route('/upload')
def upload():
    user = get_utilisateur_session()
    if not user: return redirect(url_for('connexion'))
    return render_template('upload.html', user=user, page='upload')

@app.route('/bibliotheque')
def bibliotheque():
    user = get_utilisateur_session()
    if not user: return redirect(url_for('connexion'))
    
    documents = get_documents_utilisateur(user.id)
    return render_template('bibliotheque.html',
                         user=user,
                         documents=documents,
                         categories=["Toutes", "Facture", "Contrat", "Identité"],
                         etiquettes=["Toutes"] + [et['nom'] for et in ETIQUETTES_DB],
                         page='bibliotheque')

@app.route('/etiquettes', methods=['GET', 'POST'])
def etiquettes():
    user = get_utilisateur_session()
    if not user: return redirect(url_for('connexion'))
    
    global ETIQUETTES_DB, ETIQUETTES_ID_COUNTER
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'creer':
            nom = request.form.get('nom', '').strip()
            if nom and not any(et['nom'].lower() == nom.lower() for et in ETIQUETTES_DB):
                ETIQUETTES_DB.append({'id': ETIQUETTES_ID_COUNTER, 'nom': nom, 'couleur': request.form.get('couleur', '#3B82F6')})
                ETIQUETTES_ID_COUNTER += 1
                flash(f'Étiquette {nom} créée', 'success')
        elif action == 'supprimer':
            et_id = int(request.form.get('etiquette_id'))
            ETIQUETTES_DB = [et for et in ETIQUETTES_DB if et['id'] != et_id]
            flash('Supprimée', 'success')
        return redirect(url_for('etiquettes'))
        
    return render_template('etiquettes.html', user=user, etiquettes=ETIQUETTES_DB, page='etiquettes')

@app.route('/statistiques')
def statistiques():
    user = get_utilisateur_session()
    if not user: return redirect(url_for('connexion'))
    
    documents = get_documents_utilisateur(user.id)
    cat_counts = {}
    for d in documents:
        cat = d.get('categorie', 'Autre')
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        
    return render_template('statistiques.html',
                         user=user,
                         documents=documents,
                         cat_counts=cat_counts,
                         poids_total=user.stockage_utilise / (1024*1024),
                         types_categories=len(cat_counts),
                         page='statistiques')

@app.route('/premium')
def premium():
    user = get_utilisateur_session()
    if not user: return redirect(url_for('connexion'))
    return render_template('premium.html', user=user, page='premium')

# --- API ---

@app.route('/api/user-data')
def api_user_data():
    """API pour récupérer les données utilisateur au format JSON"""
    user = get_utilisateur_session()
    if not user:
        return jsonify({'error': 'Non authentifié'}), 401
    
    data = {
        'id': user.id,
        'nom_utilisateur': user.nom_utilisateur,
        'niveau': user.niveau,
        'stockage_utilise': user.stockage_utilise,
        'stockage_limite': user.obtenir_limite_stockage(),
        'pourcentage': user.pourcentage_stockage(),
        'est_premium': user.est_premium()
    }
    return jsonify(data)

@app.route('/api/statistiques')
def api_statistiques():
    """API pour récupérer les statistiques au format JSON"""
    user = get_utilisateur_session()
    if not user:
        return jsonify({'error': 'Non authentifié'}), 401
    
    documents = get_documents_utilisateur(user.id)
    
    stats = {
        'total_documents': len(documents),
        'stockage_utilise': user.stockage_utilise,
        'stockage_limite': user.obtenir_limite_stockage(),
        'pourcentage_stockage': user.pourcentage_stockage(),
        'est_premium': user.est_premium()
    }
    
    return jsonify(stats)

# Initialisation
if BDD_AVAILABLE:
    try:
        gestionnaire_bdd.creer_tables()
        print("✅ BDD OK")
    except Exception as e:
        print(f"⚠️ Erreur BDD: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
