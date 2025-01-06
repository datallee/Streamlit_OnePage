
# pip install streamlit-authenticator

import streamlit as st
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu

import pandas as pd

# Requirements : n'écrire que la partie gauche et sans la mention "import" ou "from" dans le fichier.txt

# Fonction pour charger les données des utilisateurs depuis le fichier CSV
def load_user_data():
    return pd.read_csv('mdp.csv')

# Fonction pour vérifier les identifiants de l'utilisateur
def authenticate_user(username, password, user_data):
    user = user_data[user_data['name'] == username]
    
    if user.empty:
        return False, "Utilisateur introuvable"
    
    user = user.iloc[0]  # Prendre la première ligne qui correspond
    if user['password'] != password:
        return False, "Mot de passe incorrect"
    
    # Mettre à jour l'état de la connexion dans les données
    user_data.loc[user_data['name'] == username, 'logged_in'] = True
    user_data.to_csv('mdp.csv', index=False)  # Enregistrer les modifications dans le fichier CSV
    
    return True, user['role']

def accueil():
    st.title("Bienvenue sur ma page")    

def photos():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg")

    with col2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg")

    with col3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg")

        # Ajout d'un fond sonore
        #st.audio("vent.mp3", format="audio/mpeg")

# Fonction de déconnexion
def logout(user_data):
    username = st.session_state["username"]
    user_data.loc[user_data['name'] == username, 'logged_in'] = False
    user_data.to_csv('users.csv', index=False)  # Enregistrer les modifications dans le fichier CSV
    st.session_state.clear()  # Clear session state to log out the user
    st.success("Vous êtes maintenant déconnecté.")

# Interface utilisateur pour la connexion
def login(user_data):
    st.subheader("Se connecter")
    
    # Formulaire de connexion
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type='password')
    
    if st.button("Se connecter"):
        is_authenticated, message = authenticate_user(username, password, user_data)
        if is_authenticated:
            st.session_state["authenticated"] = True
            st.session_state["role"] = message  # Rôle de l'utilisateur (admin, utilisateur, etc.)
            st.session_state["username"] = username
            st.success(f"Bienvenue, {username}!")
        else:
            st.error(message)

def page():
    with st.sidebar:
        selection = option_menu(
                    menu_title=None,
                    options = ["Accueil", "Les Photos"]
        )

    if selection == "Accueil":
        accueil()
    elif selection == "Les Photos":
        photos()

# Fonction principale
def main():
    # Charger les données des utilisateurs depuis le CSV
    user_data = load_user_data()

    # Vérifier si l'utilisateur est déjà authentifié
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        accueil()  # Appel à la fonction d'accueil si l'utilisateur est connecté
        page()  # Affichage des pages via le menu de navigation
        if st.button("Se déconnecter"):
            logout(user_data)  # Permet à l'utilisateur de se déconnecter
    else:
        login(user_data)  # Si non authentifié, afficher le formulaire de connexion

if __name__ == '__main__':
    main()
