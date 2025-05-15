import streamlit as st

# Dicionário com os caracteres invisíveis mais comuns e suas descrições
invisible_chars = {
    "\u200B": "Zero Width Space (U+200B)",
    "\u200C": "Zero Width Non-Joiner (U+200C)",
    "\u200D": "Zero Width Joiner (U+200D)",
    "\u00A0": "Non-breaking Space (U+00A0)",
    "\u200E": "Left-to-Right Mark (U+200E)",
    "\u200F": "Right-to-Left Mark (U+200F)",
    "\u034F": "Combining Grapheme Joiner (U+034F)",
    "\u061C": "Arabic Letter Mark (U+061C)",
    "\uFE0E": "Variation Selector-15 (U+FE0E)",
    "\uFE0F": "Variation Selector-16 (U+FE0F)",
    "\uFEFF": "Byte Order Mark (U+FEFF)",
    "\u00AD": "Soft Hyphen (U+00AD)"
}

st.title("🔍 Verificador de Caracteres Invisíveis (Unicode)")

texto = st.text_area("Cole seu texto aqui:", height=250)

if st.button("Verificar"):
    resultados = []
    for i, c in enumerate(texto):
        if c in invisible_chars:
            resultados.append({
                "Posição": i,
                "Unicode": f"U+{ord(c):04X}",
                "Descrição": invisible_chars[c]
            })

    if resultados:
        st.success(f"Foram encontrados {len(resultados)} caractere(s) invisível(is).")
        st.table(resultados)
    else:
        st.info("Nenhum caractere invisível foi encontrado.")

st.markdown("---")
st.caption("Ferramenta criada por Synap Digital com suporte a unicode invisível comum em textos de IA.")
