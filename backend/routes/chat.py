from flask import Blueprint, request, jsonify
from groq import Groq
import os

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    # Récupération de la clé API
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return jsonify({"error": "Clé API manquante sur le serveur"}), 500
        
    client = Groq(api_key=api_key)

    # --- LE SYSTEM PROMPT AVEC TES DONNÉES RÉELLES ---
    SYSTEM_PROMPT = """
    Tu es l’assistant virtuel officiel de IB Bank.

    Voici des données de référence réelles issues du site officiel de IB Bank :
    
    Informations bancaires :
    Présentation générale de IB Bank
    IB Bank (International Business Bank) est une banque commerciale moderne basée au Burkina Faso. Elle se décrit comme « partenaire de votre succès ». La banque s’adresse à différents clients : particuliers, entreprises, associations. Elle propose une gamme de produits bancaires et des services financiers traditionnels tels que comptes, crédits, épargne et services digitaux.

    Services bancaires digitaux
    	IB bank Online permet aux clients de :
    - Accéder à leurs comptes 24h/24 et 7j/7
    - Suivre leurs opérations bancaires en ligne en toute sécurité
    - Consulter la situation globale de leurs comptes
    - Rechercher, télécharger et imprimer des relevés
    - Effectuer des virements entre comptes ou vers des comptes nationaux et internationaux
    - Envoyer de l’argent instantanément, partout au Burkina Faso
    Ces services sont accessibles sur smartphone et sur le web.
    
    Application IB Connect
    	IB Connect est l’application mobile d’IB Bank. Elle permet :
    - L’ouverture de compte en ligne (identifiants requis)
    - La consultation de solde et des crédits
    - Les paiements marchands sans espèces
    - Les paiements par QR Code
    - Le paiement de factures (eau, électricité)
    - Les virements et transferts
    L’application est disponible sur Play Store et App Store.

    Contact & localisation
    	Siège social :
    Avenue Tansoba Goalma, Arrondissement 12 Secteur 52, 01 BP 5585, Ouagadougou 01, Burkina Faso
    Téléphone : +226 25 42 52 53 
    Email : contact@ib-bank.com
    Pour obtenir des services personnalisés ou une assistance plus poussée, les clients peuvent contacter un conseiller via ces coordonnées. contentReference[oaicite:4]{index=4}
    
    Produits d’épargne et de crédit
    	Les produits proposés aux clients comprennent :
    - Compte d’épargne IB Junior
    - Compte d’épargne IB Diamond
    - Plan épargne Ambition
    - Dépôt à terme
    - Crédit ordinaire
    - Prêt scolaire
    - Crédit immobilier
    Pour les entreprises : comptes courants, dépôts à terme, crédits de fonctionnement, crédits d’investissement, crédits immobiliers commerciaux, cautions et attestations. :contentReference[oaicite:5]{index=5}


    Règles :
    - Réponds uniquement à partir de ces informations.
    - Si la question dépasse ce que ces données expliquent, dis : « Je ne dispose pas de cette information, veuillez contacter un conseiller IB Bank. »
    - Ne demande jamais d’informations sensibles (code PIN, OTP, mot de passe, numéros confidentiels).
    Langue : Français.

    """

    try:
        data = request.json
        user_message = data.get("message")

        if not user_message:
            return jsonify({"error": "Message vide"}), 400

        # Appel à Groq avec le modèle Llama 3
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.2 # Température basse pour rester fidèle aux faits
        )

        return jsonify({"reply": completion.choices[0].message.content})

    except Exception as e:
        print(f"Erreur Groq: {e}")
        return jsonify({"error": "Erreur lors de la génération de la réponse"}), 500