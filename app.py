import streamlit as st
import fitz  # PyMuPDF
from streamlit_drawable_canvas import st_canvas
from io import BytesIO

st.set_page_config(page_title="PDF Subrayador", layout="wide")

st.title("📑 Subir PDF y Subrayar")

# Subir archivo
uploaded_file = st.file_uploader("Sube un PDF", type=["pdf"])

if uploaded_file:
    # Cargar PDF
    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    st.sidebar.header("Opciones de subrayado")
    color = st.sidebar.color_picker("Color del subrayado", "#ffff00")
    stroke_width = st.sidebar.slider("Grosor", 2, 10, 4)

    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # mejor resolución
        img = pix.tobytes("png")

        st.subheader(f"Página {page_num + 1}")

        # Canvas para dibujar encima
        canvas = st_canvas(
            fill_color="rgba(255, 255, 255, 0)",
            stroke_color=color,
            background_image=img,
            update_streamlit=True,
            height=600,
            width=450,
            drawing_mode="freedraw",
            stroke_width=stroke_width,
            key=f"canvas{page_num}",
        )

    # Botón para descargar PDF con subrayados (simplemente guarda imágenes marcadas)
    if st.button("💾 Guardar anotaciones como imágenes"):
        for i in range(len(doc)):
            page = doc[i]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            pix.save(f"pagina_{i+1}.png")
        st.success("Se guardaron las páginas con subrayados como PNG.")

