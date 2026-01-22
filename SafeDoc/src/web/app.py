"""
Application Web SafeDoc
Interface Streamlit moderne et sécurisée
"""
import sys
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
from datetime import datetime
from loguru import logger

from config.config import STREAMLIT_CONFIG, USER_TIERS, MESSAGES
from src.stockage.base_de_donnees import gestionnaire_bdd
from src.securite.authentification import gestionnaire_auth, Utilisateur
from src.utils.journalisation import configurer_logs
from src.utils.gestionnaire_documents import gestionnaire_documents

# Configuration de la page
st.set_page_config(**STREAMLIT_CONFIG)

# CSS personnalisé pour un design ULTRA-PREMIUM
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* ===== PALETTE PROFESSIONNELLE (CORPORATE TECH) ===== */
    :root {
        --primary-blue: #3B82F6;
        --primary-dark: #2563EB;
        --dark-slate: #0F172A;
        --medium-slate: #1E293B;
        --light-slate: #94A3B8;
        --accent-emerald: #10B981;
        --border-color: rgba(148, 163, 184, 0.1);
        --glass-bg: rgba(30, 41, 59, 0.7);
    }
    
    /* ===== FOND & TYPO ===== */
    .stApp {
        background: var(--dark-slate);
        font-family: 'Inter', sans-serif;
        color: #F8FAFC;
    }
    
    /* ===== TITRES ===== */
    h1 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em;
    }
    
    h2 {
        color: #CBD5E1 !important;
        font-weight: 600 !important;
    }
    
    h3 {
        color: var(--primary-blue) !important;
        font-weight: 500 !important;
    }
    
    /* ===== CARTES & CONTENEURS ===== */
    .glass-card {
        background: var(--medium-slate);
        border-radius: 12px;
        padding: 24px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(59, 130, 246, 0.4);
        transform: translateY(-2px);
    }
    
    /* ===== BOUTONS ===== */
    .stButton > button {
        background: var(--primary-blue);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: var(--primary-dark);
        border-color: transparent;
        color: white;
        transform: translateY(-1px);
    }
    
    .stButton > button[kind="primary"] {
        background: var(--accent-emerald);
        color: white;
    }
    
    /* ===== INPUTS ===== */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        background: rgba(15, 23, 42, 0.8) !important;
        color: white !important;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        padding: 10px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-blue);
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: var(--medium-slate);
        border-right: 1px solid var(--border-color);
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: transparent;
        border: 1px solid transparent;
        color: #CBD5E1;
        text-align: left;
        justify-content: flex-start;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255, 255, 255, 0.05);
        color: white;
    }
    
    /* ===== MÉTRIQUES ===== */
    [data-testid="stMetricValue"] {
        color: var(--primary-blue) !important;
        font-weight: 700 !important;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--light-slate);
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)


def initialiser_session():
    """Initialise les variables de session avec un utilisateur par défaut (bypass connexion)"""
    if 'utilisateur' not in st.session_state or st.session_state.utilisateur is None:
        # Obtenir ou créer l'utilisateur par défaut
        nom_defaut = "Utilisateur"
        utilisateur_db = gestionnaire_bdd.obtenir_utilisateur_par_nom(nom_defaut)
        
        if not utilisateur_db:
            # Créer un mot de passe bidon (pas utilisé car connexion bypassée)
            hash_mdp = gestionnaire_auth.hacher_mot_de_passe("SafeDoc123!")
            utilisateur_db = gestionnaire_bdd.creer_utilisateur(nom_defaut, hash_mdp, 'premium')
        
        # Créer l'objet utilisateur pour la session
        st.session_state.utilisateur = Utilisateur(
            id=utilisateur_db.id,
            nom_utilisateur=utilisateur_db.nom_utilisateur,
            hash_mot_de_passe=utilisateur_db.hash_mot_de_passe,
            niveau=utilisateur_db.niveau,
            stockage_utilise=utilisateur_db.stockage_utilise,
            date_creation=utilisateur_db.date_creation
        )
        
    if 'page' not in st.session_state or st.session_state.page == 'connexion':
        st.session_state.page = 'dashboard'
        
    if 'mot_de_passe_chiffrement' not in st.session_state or st.session_state.mot_de_passe_chiffrement is None:
        # Utiliser une clé par défaut sécurisée définie dans le code ou l'env
        from config.config import MASTER_KEY
        st.session_state.mot_de_passe_chiffrement = MASTER_KEY


def page_connexion():
    """Page de connexion"""
    st.markdown("<h1 style='text-align: center;'>🔒 SafeDoc</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #e0e0e0; font-size: 18px;'>Votre coffre-fort numérique intelligent</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["✨ Connexion", "🚀 Inscription"])
    
    with tab1:
        st.markdown("### Connectez-vous")
        
        nom_utilisateur = st.text_input("👤 Nom d'utilisateur", key="login_username")
        mot_de_passe = st.text_input("🔑 Mot de passe", type="password", key="login_password")
        mot_de_passe_chiffrement = st.text_input("🔐 Mot de passe de chiffrement", type="password", key="login_encryption")
        
        if st.button("🔓 Se connecter", use_container_width=True):
            if not nom_utilisateur or not mot_de_passe or not mot_de_passe_chiffrement:
                st.error("⚠️ Veuillez remplir tous les champs")
            else:
                # Authentifier
                utilisateur_db = gestionnaire_bdd.obtenir_utilisateur_par_nom(nom_utilisateur)
                
                if utilisateur_db and gestionnaire_auth.verifier_mot_de_passe(mot_de_passe, utilisateur_db.hash_mot_de_passe):
                    # Mettre à jour la dernière connexion
                    session = gestionnaire_bdd.obtenir_session()
                    utilisateur_db.derniere_connexion = datetime.now()
                    session.commit()
                    session.close()
                    
                    # Créer l'objet utilisateur
                    st.session_state.utilisateur = Utilisateur(
                        id=utilisateur_db.id,
                        nom_utilisateur=utilisateur_db.nom_utilisateur,
                        hash_mot_de_passe=utilisateur_db.hash_mot_de_passe,
                        niveau=utilisateur_db.niveau,
                        stockage_utilise=utilisateur_db.stockage_utilise,
                        date_creation=utilisateur_db.date_creation
                    )
                    st.session_state.mot_de_passe_chiffrement = mot_de_passe_chiffrement
                    st.session_state.page = 'dashboard'
                    st.rerun()
                else:
                    st.error("❌ Nom d'utilisateur ou mot de passe incorrect")
    
    with tab2:
        st.markdown("### Créez votre compte")
        
        nouveau_nom = st.text_input("👤 Nom d'utilisateur", key="register_username")
        nouveau_mdp = st.text_input("🔑 Mot de passe", type="password", key="register_password")
        confirmer_mdp = st.text_input("🔑 Confirmer le mot de passe", type="password", key="confirm_password")
        mdp_chiffrement = st.text_input("🔐 Mot de passe de chiffrement", type="password", key="register_encryption")
        
        st.info("💡 Le mot de passe de chiffrement est utilisé pour sécuriser vos documents. Ne le perdez pas !")
        
        if st.button("📝 S'inscrire", use_container_width=True):
            # Validation
            valide_nom, msg_nom = gestionnaire_auth.valider_nom_utilisateur(nouveau_nom)
            if not valide_nom:
                st.error(f"❌ {msg_nom}")
                return
            
            valide_mdp, msg_mdp = gestionnaire_auth.valider_mot_de_passe(nouveau_mdp)
            if not valide_mdp:
                st.error(f"❌ {msg_mdp}")
                return
            
            if nouveau_mdp != confirmer_mdp:
                st.error("❌ Les mots de passe ne correspondent pas")
                return
            
            if not mdp_chiffrement or len(mdp_chiffrement) < 8:
                st.error("❌ Le mot de passe de chiffrement doit contenir au moins 8 caractères")
                return
            
            # Créer l'utilisateur
            hash_mdp = gestionnaire_auth.hacher_mot_de_passe(nouveau_mdp)
            utilisateur_db = gestionnaire_bdd.creer_utilisateur(nouveau_nom, hash_mdp, 'free')
            
            if utilisateur_db:
                st.success("✅ Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
                logger.info(f"Nouvel utilisateur inscrit: {nouveau_nom}")
            else:
                st.error("❌ Ce nom d'utilisateur existe déjà")


def page_dashboard():
    """Page tableau de bord"""
    user = st.session_state.utilisateur
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"## 👤 {user.nom_utilisateur}")
        
        if user.est_premium():
            st.markdown("### ⭐ **Premium**")
        else:
            st.markdown("### 🆓 Gratuit")
        
        st.markdown("---")
        
        # Statistiques de stockage
        pourcentage = user.pourcentage_stockage()
        stockage_mb = user.stockage_utilise / (1024 * 1024)
        limite_mb = user.obtenir_limite_stockage() / (1024 * 1024)
        
        st.markdown("### 💾 Stockage")
        st.progress(min(pourcentage / 100, 1.0))
        st.markdown(f"**{stockage_mb:.1f} MB** / {limite_mb:.0f} MB")
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### 📋 Navigation")
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
        
        if st.button("📤 Téléverser", use_container_width=True):
            st.session_state.page = 'upload'
            st.rerun()
        
        if st.button("📚 Bibliothèque", use_container_width=True):
            st.session_state.page = 'bibliotheque'
            st.rerun()
        
        if not user.est_premium():
            st.markdown("---")
            if st.button("⭐ Passer Premium", use_container_width=True, type="primary"):
                st.session_state.page = 'premium'
                st.rerun()
        
        st.markdown("---")
        st.info("💡 Mode accès direct activé (sans connexion)")
    
    # Contenu principal selon la page
    if st.session_state.page == 'dashboard':
        afficher_dashboard()
    elif st.session_state.page == 'upload':
        afficher_page_upload()
    elif st.session_state.page == 'bibliotheque':
        afficher_bibliotheque()
    elif st.session_state.page == 'premium':
        afficher_page_premium()
    elif st.session_state.page == 'voir_document':
        afficher_voir_document()

def afficher_dashboard():
    """Affiche le tableau de bord avec une esthétique professionnelle"""
    st.markdown("# 🏠 Tableau de Bord")
    
    user = st.session_state.utilisateur
    
    # Vision SafeDoc (Les 4 Piliers) - Style Corporate
    st.markdown("""
    <div style='background: rgba(59, 130, 246, 0.05); padding: 15px; border-radius: 12px; border: 1px solid rgba(59, 130, 246, 0.2); margin-bottom: 25px;'>
        <h3 style='margin-top: 0; color: #3B82F6; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.05em;'>🛡️ Nos Capacités</h3>
        <div style='display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px; color: #CBD5E1;'>
            <div style='flex: 1; min-width: 120px;'>📷 <b>Scanner</b></div>
            <div style='flex: 1; min-width: 120px;'>🔍 <b>Extraire</b></div>
            <div style='flex: 1; min-width: 120px;'>🧠 <b>Classer</b></div>
            <div style='flex: 1; min-width: 120px;'>🔐 <b>Sécuriser</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Métriques
    documents = gestionnaire_bdd.obtenir_documents_utilisateur(user.id)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📄 Documents", len(documents))
    
    with col2:
        stockage_mb = user.stockage_utilise / (1024 * 1024)
        st.metric("💾 Stockage", f"{stockage_mb:.1f} MB")
    
    with col3:
        niveau_icon = "⭐" if user.est_premium() else "🆓"
        st.metric("🎯 Niveau", f"{niveau_icon} {USER_TIERS[user.niveau]['name']}")
    
    st.markdown("---")
    
    # Documents récents
    st.markdown("## 📋 Documents récents")
    
    if documents:
        documents_recents = documents[:5]
        
        for doc in documents_recents:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    categorie_icon = "📄"
                    if doc.categorie == "Facture":
                        categorie_icon = "🧾"
                    elif doc.categorie == "Contrat":
                        categorie_icon = "📝"
                    elif doc.categorie == "Pièce d'identité":
                        categorie_icon = "🪪"
                    
                    st.markdown(f"**{categorie_icon} {doc.nom}**")
                
                with col2:
                    st.markdown(f"🏷️ {doc.categorie}")
                
                with col3:
                    taille_mb = doc.taille_fichier / (1024 * 1024)
                    st.markdown(f"💾 {taille_mb:.2f} MB")
                
                with col4:
                    if st.button("👁️", key=f"view_{doc.id}"):
                        st.session_state.document_a_voir = doc.id
                        st.session_state.page = 'voir_document'
                        st.rerun()
                
                st.markdown("<hr style='margin: 10px 0; border: 0.5px solid rgba(148, 163, 184, 0.1);'>", unsafe_allow_html=True)
    else:
        st.info("💡 Aucun document. Commencez par téléverser vos premiers documents !")


def afficher_page_upload():
    """Page de téléversement"""
    st.markdown("# 📤 Téléverser un document")
    
    st.markdown("### 📁 Sélectionnez votre document")
    
    fichier = st.file_uploader(
        "Glissez-déposez ou cliquez pour sélectionner",
        type=['pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'],
        help="Formats supportés: PDF, PNG, JPG, TIFF, BMP"
    )
    
    if fichier:
        st.success(f"✅ Fichier sélectionné : {fichier.name}")
        
        # Nom personnalisé
        nom_personnalise = st.text_input("📝 Nom du document (optionnel)", value=fichier.name)
        
        if st.button("🔐 Traiter et Sauvegarder", type="primary", use_container_width=True):
            with st.spinner("⏳ Traitement en cours..."):
                # Sauvegarder temporairement
                from config.config import TEMP_PATH
                chemin_temp = TEMP_PATH / fichier.name
                with open(chemin_temp, 'wb') as f:
                    f.write(fichier.getbuffer())
                
                # Traiter
                succes, message, infos = gestionnaire_documents.traiter_document(
                    chemin_temp,
                    st.session_state.utilisateur.id,
                    st.session_state.mot_de_passe_chiffrement,
                    nom_personnalise
                )
                
                # Nettoyer
                chemin_temp.unlink(missing_ok=True)
                
                if succes:
                    st.success(message)
                    
                    # Afficher les informations extraites
                    if infos:
                        st.markdown("### 📊 Informations extraites")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("🏷️ Catégorie", infos.get('categorie', 'N/A'))
                            st.metric("📊 Confiance", f"{infos.get('confiance_categorie', 0)*100:.0f}%")
                        
                        with col2:
                            st.metric("🔍 OCR Confiance", f"{infos.get('confiance_ocr', 0):.0f}%")
                            taille_mb = infos.get('taille', 0) / (1024 * 1024)
                            st.metric("💾 Taille", f"{taille_mb:.2f} MB")
                        
                        if infos.get('texte_extrait'):
                            with st.expander("📄 Aperçu du texte extrait"):
                                st.text(infos['texte_extrait'][:500] + "...")
                    
                    # Mettre à jour le stockage
                    user_db = gestionnaire_bdd.obtenir_utilisateur_par_id(st.session_state.utilisateur.id)
                    st.session_state.utilisateur.stockage_utilise = user_db.stockage_utilise
                else:
                    st.error(message)


def afficher_bibliotheque():
    """Page bibliothèque"""
    st.markdown("# 📚 Bibliothèque de Documents")
    
    # Filtres
    col1, col2 = st.columns([3, 1])
    
    with col1:
        recherche = st.text_input("🔍 Rechercher", placeholder="Nom, catégorie...")
    
    with col2:
        from config.config import DOCUMENT_CATEGORIES
        cat_filtre = st.selectbox("🏷️ Catégorie", ["Toutes"] + DOCUMENT_CATEGORIES)
    
    # Récupérer les documents
    user_id = st.session_state.utilisateur.id
    
    if cat_filtre != "Toutes":
        documents = gestionnaire_bdd.obtenir_documents_utilisateur(user_id, categorie=cat_filtre)
    else:
        documents = gestionnaire_bdd.obtenir_documents_utilisateur(user_id)
    
    # Filtrer par recherche
    if recherche:
        documents = [d for d in documents if recherche.lower() in d.nom.lower() or recherche.lower() in d.categorie.lower()]
    
    st.markdown(f"**{len(documents)} document(s) trouvé(s)**")
    st.markdown("---")
    
    # Afficher les documents
    for doc in documents:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])
            
            with col1:
                st.markdown(f"**📄 {doc.nom}**")
            
            with col2:
                st.markdown(f"🏷️ {doc.categorie}")
            
            with col3:
                st.markdown(f"📅 {doc.date_upload.strftime('%d/%m/%Y')}")
            
            with col4:
                if st.button("👁️", key=f"voir_{doc.id}", help="Voir"):
                    st.session_state.document_id_temp = doc.id
                    afficher_modal_voir_document(doc.id)
            
            with col5:
                if st.button("🗑️", key=f"suppr_{doc.id}", help="Supprimer"):
                    if gestionnaire_bdd.supprimer_document(doc.id):
                        # Supprimer les fichiers
                        from src.stockage.gestionnaire_fichiers import gestionnaire_fichiers
                        gestionnaire_fichiers.supprimer_document(Path(doc.chemin_original), Path(doc.chemin_chiffre))
                        st.success("✅ Document supprimé")
                        st.rerun()
            
            st.markdown("<hr style='margin: 10px 0; border: 1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)


def afficher_voir_document():
    """Page de visualisation et déchiffrement d'un document"""
    doc_id = st.session_state.get('document_a_voir')
    if not doc_id:
        st.session_state.page = 'dashboard'
        st.rerun()
        
    doc = gestionnaire_bdd.obtenir_document_par_id(doc_id)
    if not doc:
        st.error("Document introuvable.")
        if st.button("⬅️ Retour"):
            st.session_state.page = 'bibliotheque'
            st.rerun()
        return
        
    st.markdown(f"# 👁️ Visualisation : {doc.nom}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Informations")
        st.markdown(f"**🏷️ Catégorie :** {doc.categorie}")
        st.markdown(f"**📅 Ajouté le :** {doc.date_ajoute.strftime('%d/%m/%Y')}")
        
        if doc.metadonnees:
            st.markdown("#### 🔍 Données extraites")
            for k, v in doc.metadonnees.items():
                st.markdown(f"- **{k} :** {v}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Accès Sécurisé")
        st.info("Ce document est chiffré. Utilisez votre clé maître pour le récupérer.")
        
        # On utilise le bypass si possible, sinon on demande
        mdp = st.session_state.get('mot_de_passe_chiffrement')
        if not mdp:
            mdp = st.text_input("Clé de chiffrement", type="password")
            
        if st.button("🔓 Déchiffrer et Télécharger", use_container_width=True, type="primary"):
            if mdp:
                with st.spinner("🔓 Déchiffrement..."):
                    succes, message, chemin = gestionnaire_documents.recuperer_document(doc_id, mdp)
                    if succes and chemin:
                        with open(chemin, 'rb') as f:
                            st.download_button(
                                "⬇️ Télécharger le fichier déchiffré",
                                f.read(),
                                file_name=f"dechiffre_{doc.nom}",
                                use_container_width=True
                            )
                        st.success("✅ Document déchiffré avec succès !")
                    else:
                        st.error(f"❌ {message}")
            else:
                st.warning("⚠️ Veuillez entrer votre clé de chiffrement.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    if st.button("🔙 Retour à la bibliothèque", use_container_width=True):
        st.session_state.page = 'bibliotheque'
        st.rerun()


def afficher_page_premium():
    """Page Premium"""
    st.markdown("# ⭐ Passez à Premium")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🆓 Gratuit")
        st.markdown("""
        - ✅ Stockage local illimité
        - ✅ OCR et classification
        - ✅ Chiffrement AES-256
        - ❌ Pas de synchronisation cloud
        - ❌ 500 MB maximum
        """)
    
    with col2:
        st.markdown("### ⭐ Premium")
        st.markdown("""
        - ✅ Tout ce qui est gratuit
        - ✅ Synchronisation Google Drive
        - ✅ Sauvegarde automatique
        - ✅ Accès multi-appareils
        - ✅ 50 GB de stockage
        - ✅ Support prioritaire
        """)
        
        st.markdown("### 💰 9.99€ / mois")
        
        if st.button("🚀 Activer Premium", type="primary", use_container_width=True):
            st.info("💡 Fonctionnalité de paiement à implémenter")


def main():
    """Point d'entrée principal"""
    # Initialiser la base de données
    gestionnaire_bdd.creer_tables()
    
    # Initialiser la session
    initialiser_session()
    
    # Router vers le tableau de bord (authentification bypassée)
    page_dashboard()


if __name__ == "__main__":
    main()
