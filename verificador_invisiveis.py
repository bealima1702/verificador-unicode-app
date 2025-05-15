import streamlit as st
import base64
from collections import Counter

# Dicionário de caracteres invisíveis (códigos Unicode e nomes técnicos)
invisible_map = {
    0x0020: "Space (U+0020)",
    0x00A0: "Non-breaking Space (U+00A0)",
    0x2000: "En Quad (U+2000)",
    0x2001: "Em Quad (U+2001)",
    0x2002: "En Space (U+2002)",
    0x2003: "Em Space (U+2003)",
    0x2004: "Three-Per-Em Space (U+2004)",
    0x2005: "Four-Per-Em Space (U+2005)",
    0x2006: "Six-Per-Em Space (U+2006)",
    0x2007: "Figure Space (U+2007)",
    0x2008: "Punctuation Space (U+2008)",
    0x2009: "Thin Space (U+2009)",
    0x200A: "Hair Space (U+200A)",
    0x202F: "Narrow No-Break Space (U+202F)",
    0x205F: "Medium Mathematical Space (U+205F)",
    0x3000: "Ideographic Space (U+3000)",
    0x200B: "Zero Width Space (U+200B)",
    0x200C: "Zero Width Non-Joiner (U+200C)",
    0x200D: "Zero Width Joiner (U+200D)",
    0x2060: "Word Joiner (U+2060)",
    0x200E: "Left-to-Right Mark (U+200E)",
    0x200F: "Right-to-Left Mark (U+200F)",
    0x202A: "Left-to-Right Embedding (U+202A)",
    0x202B: "Right-to-Left Embedding (U+202B)",
    0x202C: "Pop Directional Formatting (U+202C)",
    0x202D: "Left-to-Right Override (U+202D)",
    0x202E: "Right-to-Left Override (U+202E)",
    0x00AD: "Soft Hyphen (U+00AD)",
    0x034F: "Combining Grapheme Joiner (U+034F)",
    0x061C: "Arabic Letter Mark (U+061C)",
    0xFE0E: "Variation Selector-15 (U+FE0E)",
    0xFE0F: "Variation Selector-16 (U+FE0F)",
    0xFEFF: "Byte Order Mark (U+FEFF)",
    0xFFF9: "Interlinear Annotation Anchor (U+FFF9)",
    0xFFFA: "Interlinear Annotation Separator (U+FFFA)",
    0xFFFB: "Interlinear Annotation Terminator (U+FFFB)"
}
for code in range(0xFE00, 0xFE10):
    if code not in invisible_map:
        invisible_map[code] = f"Variation Selector (U+{code:04X})"

invisible_set = set(chr(c) for c in invisible_map.keys())

st.title("🧰 Verificador & Limpador de Caracteres Invisíveis (Unicode)")

# Estado de sessão para preservar o texto limpo após clique
delete_requested = st.session_state.get("delete_requested", False)
texto_original = st.session_state.get("texto_original", "")

texto = st.text_area("Cole seu texto aqui:", value=texto_original, height=250, key="input_area")

if st.button("Verificar texto"):
    st.session_state.texto_original = texto
    resultados = []
    codigos_detectados = []
    for i, c in enumerate(texto):
        code = ord(c)
        if code in invisible_map:
            resultados.append({
                "Posição": i,
                "Unicode": f"U+{code:04X}",
                "Descrição": invisible_map[code]
            })
            codigos_detectados.append(code)

    if resultados:
        st.success(f"Foram encontrados {len(resultados)} caractere(s) invisível(is).")

        contagem = Counter(codigos_detectados)
        st.markdown("### 📊 Estatísticas por Tipo")
        for code, count in contagem.items():
            label = f"U+{code:04X}"
            nome = invisible_map[code]
            st.markdown(f"**{count}×** <span style='background-color:#00D1B2;padding:2px 6px;border-radius:4px;color:black;'> {label} {nome.split('(')[0].strip()} </span>", unsafe_allow_html=True)

        st.markdown("### ✨ Caracteres Identificados")
        texto_anotado = ""
        for i, c in enumerate(texto):
            code = ord(c)
            if code in invisible_map:
                label = f"U+{code:04X}"
                tooltip = invisible_map[code]
                span = f'<span style="background-color:#FFE082; padding:2px; margin:1px; border-radius:4px;" title="{tooltip}">{label}</span>'
                texto_anotado += span
            else:
                safe_char = c.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                texto_anotado += safe_char

        st.markdown(
            f"<div style='font-family:monospace; line-height:1.6; padding:0.5em; background-color:#F4F4F4; border-radius:6px;'>{texto_anotado}</div>",
            unsafe_allow_html=True
        )

        if st.button("🧹 Deseja limpar os caracteres invisíveis?"):
            st.session_state.delete_requested = True

if st.session_state.get("delete_requested", False):
    texto = st.session_state.get("texto_original", "")
    texto_limpo = ''.join(c for c in texto if c not in invisible_set)
    st.success("Texto limpo com sucesso!")
    st.markdown("### ✨ Texto Limpo")
    st.code(texto_limpo, language="markdown")
    st.download_button("📄 Baixar .txt limpo", texto_limpo, file_name="texto_limpo.txt")

    st.markdown("### 🔍 Visualização com remoções destacadas")
    destaque = ""
    for i, c in enumerate(texto):
        if c in invisible_set:
            code = ord(c)
            label = f"U+{code:04X}"
            destaque += f'<span style="background-color:#EF9A9A; padding:2px; margin:1px; border-radius:4px;">{label}</span>'
        else:
            safe_char = c.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            destaque += safe_char

    st.markdown(
        f"<div style='font-family:monospace; line-height:1.6; padding:0.5em; background-color:#FAFAFA; border-radius:6px;'>{destaque}</div>",
        unsafe_allow_html=True
    )

st.markdown("---")
st.caption("Ferramenta Synap Digital para auditoria e limpeza de caracteres invisíveis Unicode.")
