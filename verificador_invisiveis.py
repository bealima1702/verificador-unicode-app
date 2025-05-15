import streamlit as st

# Dicionário com os códigos numéricos Unicode dos caracteres invisíveis
invisible_chars = {
    0x200B: "Zero Width Space (U+200B)",
    0x200C: "Zero Width Non-Joiner (U+200C)",
    0x200D: "Zero Width Joiner (U+200D)",
    0x00A0: "Non-breaking Space (U+00A0)",
    0x200E: "Left-to-Right Mark (U+200E)",
    0x200F: "Right-to-Left Mark (U+200F)",
    0x034F: "Combining Grapheme Joiner (U+034F)",
    0x061C: "Arabic Letter Mark (U+061C)",
    0xFE0E: "Variation Selector-15 (U+FE0E)",
    0xFE0F: "Variation Selector-16 (U+FE0F)",
    0xFEFF: "Byte Order Mark (U+FEFF)",
    0x00AD: "Soft Hyphen (U+00AD)"
}

st.title("🔍 Verificador de Caracteres Invisíveis (Unicode)")

raw_text = st.text_area("Cole seu texto aqui:", height=250)
try:
    texto = raw_text.encode().decode("unicode_escape")
except:
    texto = raw_text  # fallback se a decodificação falhar

if st.button("Verificar"):
    resultados = []
    for i, c in enumerate(texto):
        code = ord(c)
        if code in invisible_chars:
            resultados.append({
                "Posição": i,
                "Unicode": f"U+{code:04X}",
                "Descrição": invisible_chars[code]
            })

    if resultados:
        st.success(f"Foram encontrados {len(resultados)} caractere(s) invisível(is).")
        st.table(resultados)
    else:
        st.info("Nenhum caractere invisível foi encontrado.")

st.markdown("---")
st.caption("Ferramenta criada por Synap Digital com suporte a Unicode invisível comum em textos de IA.")
