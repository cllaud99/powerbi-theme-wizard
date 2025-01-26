import streamlit as st
from PIL import Image
import sys
import os



# Adiciona o caminho do projeto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))

from colors.color_extraction import extract_main_colors


def rgb_to_hex(rgb):
    """Converte uma cor RGB para formato hexadecimal."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


def load_default_colors():
    """Retorna as cores fixas iniciais."""
    return [
        (255, 0, 0),  # Vermelho
        (0, 255, 0),  # Verde
        (0, 0, 255),  # Azul
        (255, 255, 0),  # Amarelo
        (0, 255, 255),  # Ciano
        (255, 0, 255),  # Magenta
        (192, 192, 192),  # Cinza claro
        (0, 0, 0)  # Preto
    ]


def display_colors(colors):
    """Exibe os widgets de seleção de cor com base nas cores armazenadas em session_state."""
    for i, color_hex in enumerate(colors):
        # Cria as colunas com tamanhos iguais
        col1, col2, col3 = st.columns([1, 3, 2])  # Define o tamanho relativo das colunas

        # Na primeira coluna, exibe "Cor X"
        with col1:
            st.markdown(f"<div style='line-height: 3;'>Cor {i+1}</div>", unsafe_allow_html=True)

        # Na segunda coluna, exibe o código da cor como "bash"
        with col2:
            st.code(f"{color_hex}", language="bash")

        # Na terceira coluna, exibe o color_picker para edição de cor
        with col3:
            new_color = st.color_picker(
                label=f"{color_hex}", value=color_hex, key=f"color_picker_{i}",
                label_visibility="collapsed"
            )

            # Atualiza a cor no session_state
            colors[i] = new_color

def extract_and_update_colors(uploaded_file):
    """Extrai as cores principais da imagem carregada e retorna as novas cores."""
    # Salva a imagem temporariamente para análise
    with open("temp_image.png", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extrai as cores principais da imagem
    colors = extract_main_colors("temp_image.png", num_colors=9)

    # Limpa o arquivo temporário (opcional)
    os.remove("temp_image.png")

    return [rgb_to_hex(color) for color in colors]


def main():
    """Função principal para configurar a interface e processar a imagem."""
    # Título do app
    st.title("Gerador de Temas a partir de Imagens")

    # Inicializa as cores se ainda não estiverem no session_state
    if 'colors' not in st.session_state:
        default_colors = load_default_colors()
        st.session_state.colors = [rgb_to_hex(color) for color in default_colors]

    # Coloca todo o conteúdo dentro da sidebar (área dedicada à esquerda)
    with st.sidebar:
        # Upload da imagem
        uploaded_file = st.file_uploader("Faça upload de uma imagem", type=["jpg", "jpeg", "png"])

        # Verifica se uma imagem foi carregada
        if uploaded_file:
            # Exibe a imagem carregada
            image = Image.open(uploaded_file)
            st.image(image, caption="Imagem Carregada", use_container_width=True)

            # Extrai e atualiza as cores com base na imagem carregada
            new_colors = extract_and_update_colors(uploaded_file)

            # Atualiza as cores no session_state
            st.session_state.colors = new_colors

            # Exibe as novas cores com base na imagem
            st.subheader("Cores extraídas da imagem:")
            display_colors(st.session_state.colors)
        
        else:
            # Exibe as cores fixas se nenhuma imagem for carregada
            st.subheader("Cores Principais (configuração inicial)")
            display_colors(st.session_state.colors)


if __name__ == "__main__":
    main()
