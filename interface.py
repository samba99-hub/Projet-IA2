import streamlit as st
import face_recognition
import cv2
import numpy as np
import BD
import bcrypt
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

# Créer la base de données au démarrage
BD.creer_base()

st.title("🔐 Authentification avec Reconnaissance Faciale")

choix = st.selectbox("Choisissez une option", ["Inscription", "Connexion", "Connexion faciale"])

if choix == "Inscription":
    username = st.text_input("👤 Nom d'utilisateur")
    email = st.text_input("✉️ Email")
    password = st.text_input("🔑 Mot de passe", type="password")
    
    if st.button("S'inscrire"):
        with st.spinner("⏳ Vérification en cours..."):
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            if BD.ajouter_utilisateur(username, email, hashed_password):
                st.success("✅ Inscription réussie !")
            else:
                st.error("❌ Cet email est déjà utilisé. Veuillez en choisir un autre.")

# Section Connexion
elif choix == "Connexion":
    username = st.text_input("👤 Nom d'utilisateur")
    password = st.text_input("🔑 Mot de passe", type="password")

    if st.button("Se connecter"):
        with st.spinner("⏳ Vérification en cours..."):
            if BD.verifier_utilisateur(username, password):
                st.success("✅ Connexion réussie !")
            else:
                st.error("❌ Identifiants incorrects.")

# Section Connexion faciale
elif choix == "Connexion faciale":
    st.header("📸 Reconnaissance Faciale en Temps Réel")
    st.write("🔎 Regardez la caméra et laissez l’IA vous identifier")

    class FaceIDTransformer(VideoTransformerBase):
        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")

            alpha, beta = 1.8, 50
            img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            img = cv2.filter2D(img, -1, kernel)

            frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(frame_rgb)
            face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

            if face_encodings: 
                noms, signatures = BD.charger_visages()
                if signatures:
                    distances = face_recognition.face_distance(signatures, face_encodings[0])
                    if distances.any():
                        min_index = np.argmin(distances)
                        seuil = 0.6
                        if distances[min_index] < seuil:
                            st.success(f"✅ Bienvenue {noms[min_index]} !")
                        else:
                            st.error("❌ Visage non reconnu. Essayez un meilleur éclairage.")
                    else:
                        st.error("❌ Aucun visage enregistré dans la base de données.")
                else:
                    st.error("❌ La base de données est vide. Enregistrez des visages.")
            else:
                st.warning("⚠️ Aucun visage détecté. Ajustez la luminosité ou l’angle de vue.")

            return img

    # Lancer la capture vidéo avec WebRTC
    webrtc_streamer(key="facial-recognition", video_processor_factory=FaceIDTransformer)

st.divider()
st.write("🔒 **Sécurisez vos données avec une authentification robuste !**")