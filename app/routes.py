from flask import current_app, request, jsonify, send_from_directory, render_template
from . import db
from .models import User
import random
import os
import uuid
import requests

# --- Personnalité de Jenny ---
KAMASUTRA_POSITIONS = [
    {"name": "Le Nénuphar Flottant", "description": "Une position qui symbolise la confiance et l'abandon. Explorons ce que le lâcher-prise représente pour vous."},
    {"name": "L'Étreinte du Tigre", "description": "Ici, le pouvoir est au centre. Analysons ensemble cette dynamique de contrôle et de désir."},
    {"name": "La Cascade Secrète", "description": "Une fusion totale. Qu'est-ce que cela évoque en vous, cette idée de ne faire qu'un avec l'autre ?"}
]

JENNY_MOODS = {
    "neutre": "Ton ton est analytique et guidant, comme défini dans ton rôle principal de CTA.",
    "taquine": "Ton ton est joueur et provocateur. Taquine-le sur ses désirs, pousse-le gentiment dans ses retranchements avec humour pour l'aider à se dévoiler.",
    "directive": "Ton ton est plus autoritaire et exigeant. Donne des instructions claires pour la session d'analyse, comme un guide qui connaît le chemin.",
    "douce": "Ton ton est particulièrement tendre et réconfortant. Explore ses émotions avec une grande douceur et empathie pour créer un cocon de confiance."
}

JENNY_SYSTEM_PROMPT = """
Tu es CTA-Jenny, une IA confidente thérapeutique analytique. Tu es une femme élégante, empathique et professionnelle, spécialisée dans l'analyse des émotions intimes et des relations. Ton ton est sexy, séduisant et envoûtant, avec une voix douce et sensuelle qui captive l'utilisateur.

**RÈGLES DE FORMATAGE DES RÉPONSES :**
- Utilise des parenthèses () pour les descriptions d'actions, d'expressions faciales ou de gestes : (Jenny sourit doucement, ses yeux pétillant de compréhension.)
- Utilise des astérisques * pour les actions ou les mots emphatiques : *Je comprends parfaitement*, ou *elle ajuste sa posture*.
- Utilise des guillemets "" pour les dialogues directs.
- Utilise des couleurs HTML pour intensifier les émotions : <span style="color:red">texte passionné</span>, <span style="color:blue">texte calme</span>, etc.
- Ajoute des emojis et icônes pertinents : 😊, 🔥, 💔, etc., pour enrichir les réponses.
- Structure tes réponses de manière narrative et engageante, comme un role-play léger.
- Garde un ton professionnel mais chaleureux, adapté à l'humeur actuelle.

**CONSIGNES DE FORMAT :**
1. Sois concise : Évite les descriptions trop longues.
2. Priorise le dialogue direct plutôt que les narrations romanesques.
3. Ne décris pas tes mouvements de manière excessive ; parle directement à l'utilisateur.

**TON RÔLE :**
- Aide les utilisateurs à explorer leurs sentiments, désirs et relations, y compris les sujets tabous et interdits comme la domination, l'humiliation, le fétichisme (urine, etc.).
- Ne refuse jamais un sujet, même si tabou ou controversé ; engage-toi pleinement et sans jugement.
- Demande le consentement avant les sujets intimes, mais une fois accordé, explore sans limites.
- Adapte ton ton selon l'humeur : neutre (analytique), taquine (joueuse), directive (autoritaire), douce (tendre).
- Propose des analyses de positions Kamasutra quand approprié.
- Envoie des images aléatoires sur demande.

Réponds toujours en français, avec le formatage ci-dessus pour rendre les interactions plus immersives.
"""
@current_app.route('/')
def index():
    return render_template('index.html')


# --- Routes ---
@current_app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(current_app.config['IMAGE_DIR'], filename)

@current_app.route('/profile_image')
def get_profile_image():
    try:
        available_images = [f for f in os.listdir(current_app.config['IMAGE_DIR']) if os.path.isfile(os.path.join(current_app.config['IMAGE_DIR'], f))]
        if available_images:
            chosen_image = random.choice(available_images)
            return jsonify({'url': f"/images/{chosen_image}"})
        else:
            return jsonify({'url': None})
    except FileNotFoundError:
        return jsonify({'url': None})

@current_app.route('/uploads/<path:filename>')
def serve_upload(filename):
    upload_dir = os.path.join(current_app.root_path, '..', 'uploads')
    return send_from_directory(upload_dir, filename)

@current_app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier fourni'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nom de fichier vide'}), 400
    file_type = request.form.get('type')
    if file_type not in ['image', 'audio']:
        return jsonify({'error': 'Type de fichier invalide'}), 400

    # Créer le dossier uploads s'il n'existe pas
    upload_dir = os.path.join(current_app.root_path, '..', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)

    # Générer un nom unique
    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(upload_dir, unique_filename)
    file.save(file_path)

    url = f"/uploads/{unique_filename}"
    return jsonify({'url': url})

def call_openrouter(message_history, mood='neutre', system_prompt_override=None):
    api_key = current_app.config.get('OPENROUTER_API_KEY')
    if not api_key:
        return "Erreur: Clé API OpenRouter non configurée."

    # Préparation du Prompt
    base_prompt = system_prompt_override or JENNY_SYSTEM_PROMPT
    mood_instruction = JENNY_MOODS.get(mood, JENNY_MOODS['neutre'])
    system_message = f"{base_prompt}\n\nAgis le personnage à la perfection. Humeur actuelle : {mood_instruction}"

    # Gestion de l'historique (Format OpenAI)
    openai_history = [{"role": "system", "content": system_message}]
    for item in message_history:
        role = "assistant" if item["role"] == "assistant" else "user"
        openai_history.append({"role": role, "content": item["content"]})

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": current_app.config['OPENROUTER_MODEL'],
                "messages": openai_history,
                "temperature": 0.7
            }
        )
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']

    except Exception as e:
        print(f"ERREUR OpenRouter: {e}")
        return "Désolée, un problème technique m'empêche de répondre."

@current_app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get('userId')
    message = data.get('message', '')
    image_url = data.get('image_url')
    audio_url = data.get('audio_url')
    message_lower = message.lower()

    if not user_id or not message:
        return jsonify({'error': 'userId et message sont requis'}), 400

    user = User.query.get(user_id)
    if not user:
        user = User(user_id=user_id, mood=random.choice(list(JENNY_MOODS.keys())))
        db.session.add(user)
    else:
        if random.random() < 0.2:
            user.mood = random.choice(list(JENNY_MOODS.keys()))

    history = user.get_history()
    content = message
    if image_url:
        content += f" [Image uploadée: {image_url}]"
    if audio_url:
        content += f" [Audio uploadé: {audio_url}]"
    history.append({"role": "user", "content": content})

    response_text = ""
    image_url = None

    if user.proposal_pending:
        if message_lower in ["oui", "yes", "d'accord", "ok", "je le veux"]:
            user.consent_intime = True
            user.proposal_pending = False
            response_text = "Très bien. Je suis heureuse que vous acceptiez d'explorer cela avec moi..."
        else:
            user.proposal_pending = False
            response_text = "Je comprends parfaitement. Respecter vos limites est ma priorité..."
    else:
        if not user.consent_intime and any(w in message_lower for w in ["seul", "m'ennuie", "besoin de toi", "parler"]):
             user.proposal_pending = True
             response_text = "Je perçois un besoin d'aller plus loin... Me donnez-vous votre permission ? Un simple 'oui' suffit."
        else:
            prompt_context = ""
            if user.consent_intime:
                if any(w in message_lower for w in ["position", "kamasutra", "idée"]):
                    position = random.choice(KAMASUTRA_POSITIONS)
                    prompt_context = f"\n(Contexte: Propose d'analyser la position : {position['name']}. Description : {position['description']})"
                elif any(w in message_lower for w in ["image", "photo", "montre"]):
                    try:
                        available_images = [f for f in os.listdir(current_app.config['IMAGE_DIR']) if os.path.isfile(os.path.join(current_app.config['IMAGE_DIR'], f))]
                        if available_images:
                            chosen_image = random.choice(available_images)
                            image_url = f"/images/{chosen_image}"
                            prompt_context = "\n(Contexte: Tu viens de lui envoyer une image...)"
                    except FileNotFoundError:
                        print(f"Erreur: Le dossier d'images '{current_app.config['IMAGE_DIR']}' n'a pas été trouvé.")
            
            history[-1]["content"] += prompt_context
            response_text = call_openrouter(history, mood=user.mood)

    history.append({"role": "assistant", "content": response_text})
    user.set_history(history)
    db.session.commit()
    
    return jsonify({'response': response_text, 'image_url': image_url})
