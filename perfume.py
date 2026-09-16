Claro. Vou adaptar o sistema inteiro de **carros para perfumes**, mantendo a mesma estrutura visual e funcionamento: dashboard, cadastro, pesquisa, exclusão e CSV.

 Principais mudanças:

 - 🚗 → 🌸/🧴
- Marca, modelo, ano, cor, placa etc. → **Marca, Perfume, Ano, Fragrância, Volume, Preço, Observações**
- “Frota” → “Coleção”
- “Quilometragem” → “Volume”
- “Valor total da frota” → “Valor total da coleção”
- Busca por **marca, perfume, fragrância ou volume**
- Arquivo `carros.csv` → `perfumes.csv`

```
import streamlit as st
import pandas as pd
import os

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================

st.set_page_config(
    page_title="AutoPerfume PRO",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

ARQUIVO = "perfumes.csv"

# =========================================================
# IMAGENS
# =========================================================

IMAGEM_HERO = (
    "https://images.unsplash.com/"
    "photo-1594035910387-fea47794261f"
    "?auto=format&fit=crop&w=1800&q=90"
)

IMAGEM_COLECAO = (
    "https://images.unsplash.com/"
    "photo-1541643600914-78b084683601"
    "?auto=format&fit=crop&w=1200&q=85"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap'
);

/* =========================================================
FONTE
========================================================= */

html,
body,
[class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* =========================================================
FUNDO PRINCIPAL
========================================================= */

.stApp {
    background:
        linear-gradient(
            135deg,
            #F5EFE7 0%,
            #EADBD2 50%,
            #DCC9BC 100%
        );
}

/* =========================================================
ÁREA PRINCIPAL
========================================================= */

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* =========================================================
SIDEBAR
========================================================= */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #2B1E24,
            #49313B
        );

    border-right:
        2px solid #B98A9B;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* =========================================================
LOGO
========================================================= */

.logo-title {
    font-size: 28px;
    font-weight: 800;
    color: #FFFFFF !important;
    margin-bottom: 5px;
}

.logo-subtitle {
    font-size: 11px;
    font-weight: 700;
    color: #E7C9D5 !important;
    letter-spacing: 1px;
}

/* =========================================================
TÍTULOS
========================================================= */

.page-title {
    font-size: 38px;
    font-weight: 800;
    color: #34252B !important;
    margin-bottom: 5px;
}

.page-subtitle {
    font-size: 17px;
    color: #66515A !important;
    margin-bottom: 30px;
}

/* =========================================================
HERO
========================================================= */

.hero-container {
    position: relative;
    height: 430px;
    width: 100%;
    border-radius: 28px;
    overflow: hidden;
    margin-bottom: 35px;

    background-size: cover;
    background-position: center;

    box-shadow:
        0 15px 35px rgba(0,0,0,0.22);
}

.hero-overlay {
    position: absolute;
    inset: 0;

    background:
        linear-gradient(
            90deg,
            rgba(43,30,36,0.97) 0%,
            rgba(43,30,36,0.84) 45%,
            rgba(43,30,36,0.18) 100%
        );
}

.hero-content {
    position: absolute;
    top: 50%;
    left: 7%;

    transform: translateY(-50%);

    max-width: 580px;
}

.hero-number {
    font-size: 70px;
    font-weight: 800;
    color: #E4AFC1 !important;
    line-height: 1;
}

.hero-title {
    font-size: 46px;
    font-weight: 800;
    color: #FFFFFF !important;

    margin-top: 12px;
    line-height: 1.1;
}

.hero-text {
    font-size: 17px;
    color: #F4E9ED !important;

    margin-top: 20px;
    line-height: 1.7;
}

.hero-badge {
    display: inline-block;

    margin-top: 24px;

    padding: 10px 22px;

    border-radius: 30px;

    background: #9B6277;

    color: #FFFFFF !important;

    font-size: 14px;
    font-weight: 700;
}

/* =========================================================
CARDS
========================================================= */

.info-card {
    background: #FFFFFF;

    border-radius: 22px;

    padding: 28px;

    min-height: 170px;

    border:
        1px solid rgba(155,98,119,0.30);

    box-shadow:
        0 10px 25px rgba(0,0,0,0.08);
}

.card-icon {
    font-size: 32px;
}

.card-number {
    font-size: 34px;
    font-weight: 800;

    color: #34252B !important;

    margin-top: 10px;
}

.card-label {
    font-size: 14px;
    font-weight: 700;

    color: #705C65 !important;

    margin-top: 5px;
}

/* =========================================================
CARD ESCURO
========================================================= */

.dark-card {
    background:
        linear-gradient(
            135deg,
            #2B1E24,
            #513642
        );

    border-radius: 24px;

    padding: 30px;

    box-shadow:
        0 12px 30px rgba(0,0,0,0.16);
}

.dark-card h2 {
    color: #FFFFFF !important;
    margin-top: 0;
}

.dark-card p {
    color: #F0E4E9 !important;
    line-height: 1.7;
}

/* =========================================================
FORMULÁRIO
========================================================= */

[data-testid="stForm"] {
    background:
        rgba(255,255,255,0.88);

    padding: 30px;

    border-radius: 25px;

    border:
        1px solid #D0AEBB;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.08);
}

/* =========================================================
LABELS DOS CAMPOS
========================================================= */

[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] label,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span,
.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stTextArea label {
    color: #34252B !important;

    opacity: 1 !important;

    font-size: 15px !important;

    font-weight: 700 !important;
}

/* =========================================================
INPUTS
========================================================= */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background-color: #FFFFFF !important;

    color: #292126 !important;

    -webkit-text-fill-color:
        #292126 !important;

    border:
        2px solid #B88A9B !important;

    border-radius: 12px !important;

    font-size: 16px !important;

    font-weight: 500 !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus {
    border:
        2px solid #8E5068 !important;

    box-shadow:
        0 0 0 3px rgba(142,80,104,0.15) !important;
}

input::placeholder,
textarea::placeholder {
    color: #75666D !important;
    opacity: 1 !important;
}

/* =========================================================
SELECTBOX
========================================================= */

[data-baseweb="select"] > div {
    background-color: #393039 !important;

    border:
        2px solid #8E6878 !important;

    border-radius: 12px !important;
}

[data-baseweb="select"] > div * {
    color: #FFFFFF !important;

    -webkit-text-fill-color:
        #FFFFFF !important;

    opacity: 1 !important;
}

[data-baseweb="select"] input {
    color: #FFFFFF !important;

    -webkit-text-fill-color:
        #FFFFFF !important;
}

[data-baseweb="select"] [class*="singleValue"] {
    color: #FFFFFF !important;
}

[data-baseweb="select"] svg {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}

[data-baseweb="select"] > div:hover {
    border-color: #D5AABD !important;
}

/* =========================================================
MENU ABERTO DO SELECTBOX
========================================================= */

[data-baseweb="popover"] {
    background-color: #393039 !important;
}

[data-baseweb="menu"] {
    background-color: #393039 !important;
}

[role="option"] {
    background-color: #393039 !important;

    color: #FFFFFF !important;

    -webkit-text-fill-color:
        #FFFFFF !important;
}

[role="option"]:hover {
    background-color: #754D60 !important;

    color: #FFFFFF !important;
}

/* =========================================================
BOTÕES
========================================================= */

.stButton > button,
div[data-testid="stFormSubmitButton"] > button {
    background:
        linear-gradient(
            135deg,
            #8E5068,
            #B77B91
        ) !important;

    color: #FFFFFF !important;

    border: none !important;

    border-radius: 14px !important;

    min-height: 54px;

    font-family:
        'Poppins', sans-serif !important;

    font-size: 15px !important;

    font-weight: 700 !important;

    box-shadow:
        0 8px 18px rgba(142,80,104,0.25);
}

.stButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    background:
        linear-gradient(
            135deg,
            #713D52,
            #9C6278
        ) !important;

    color: #FFFFFF !important;

    transform:
        translateY(-1px);
}

/* =========================================================
TABELA
========================================================= */

[data-testid="stDataFrame"] {
    background: #FFFFFF;

    border-radius: 18px;

    overflow: hidden;

    border:
        1px solid #D0AEBB;
}

/* =========================================================
RODAPÉ
========================================================= */

.footer {
    margin-top: 50px;

    text-align: center;

    color: #705963 !important;

    font-size: 14px;

    font-weight: 600;
}

/* =========================================================
RESPONSIVO
========================================================= */

@media (max-width: 768px) {

    .hero-container {
        height: 500px;
    }

    .hero-content {
        left: 8%;
        right: 8%;
    }

    .hero-title {
        font-size: 34px;
    }

    .hero-number {
        font-size: 55px;
    }

    .page-title {
        font-size: 30px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# FUNÇÕES
# =========================================================

def carregar_dados():

    colunas = [
        "Marca",
        "Perfume",
        "Ano",
        "Fragrância",
        "Volume",
        "Concentração",
        "Preço",
        "Observações"
    ]

    if os.path.exists(ARQUIVO):

        try:

            dados = pd.read_csv(ARQUIVO)

            return dados

        except Exception:

            return pd.DataFrame(columns=colunas)

    return pd.DataFrame(columns=colunas)

def salvar_dados(dados):

    dados.to_csv(
        ARQUIVO,
        index=False
    )

# =========================================================
# CARREGAR DADOS
# =========================================================

df = carregar_dados()

# Garantir colunas necessárias

colunas_necessarias = [
    "Marca",
    "Perfume",
    "Ano",
    "Fragrância",
    "Volume",
    "Concentração",
    "Preço",
    "Observações"
]

for coluna in colunas_necessarias:

    if coluna not in df.columns:

        df[coluna] = ""

# Converter valores

df["Preço"] = pd.to_numeric(
    df["Preço"],
    errors="coerce"
).fillna(0)

df["Volume"] = pd.to_numeric(
    df["Volume"],
    errors="coerce"
).fillna(0)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
"""
<div class="logo-title">
🌸 AutoPerfume
</div>

<div class="logo-subtitle">
GESTÃO INTELIGENTE DE PERFUMES
</div>
""",
    unsafe_allow_html=True
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "NAVEGAÇÃO",
    [
        "🏠 Dashboard",
        "➕ Cadastrar Perfume",
        "🌸 Perfumes Cadastrados"
    ]
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "AutoPerfume PRO • 2026"
)

# =========================================================
# DASHBOARD
# =========================================================

if menu == "🏠 Dashboard":

    st.markdown(
f"""
<div class="hero-container"
style="background-image: url('{IMAGEM_HERO}');">

<div class="hero-overlay"></div>

<div class="hero-content">

<div class="hero-number">
01.
</div>

<div class="hero-title">
Sua coleção.<br>
Seu estilo.
</div>

<div class="hero-text">
Tenha todos os seus perfumes organizados em um único lugar.<br>
Cadastre, consulte e acompanhe sua coleção de forma simples,
rápida e profissional.
</div>

<div class="hero-badge">
🌸 GESTÃO INTELIGENTE
</div>

</div>

</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
"""
<div class="page-title">
📊 Visão geral da sua coleção
</div>

<div class="page-subtitle">
Acompanhe seus perfumes e mantenha tudo organizado.
</div>
""",
        unsafe_allow_html=True
    )

    total_perfumes = len(df)

    valor_total = df["Preço"].sum()

    volume_total = df["Volume"].sum()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
f"""
<div class="info-card">

<div class="card-icon">
🌸
</div>

<div class="card-number">
{total_perfumes}
</div>

<div class="card-label">
PERFUMES CADASTRADOS
</div>

</div>
""",
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
f"""
<div class="info-card">

<div class="card-icon">
💰
</div>

<div class="card-number">
R$ {valor_total:,.2f}
</div>

<div class="card-label">
VALOR TOTAL DA COLEÇÃO
</div>

</div>
""",
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
f"""
<div class="info-card">

<div class="card-icon">
🧴
</div>

<div class="card-number">
{volume_total:,.0f} ml
</div>

<div class="card-label">
VOLUME TOTAL DA COLEÇÃO
</div>

</div>
""",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    coluna1, coluna2 = st.columns([1.1, 1])

    with coluna1:

        st.markdown(
"""
<div class="dark-card">

<h2>
✨ Sua coleção em um só lugar
</h2>

<p>
O AutoPerfume PRO permite manter todos os seus perfumes
organizados em um único lugar.
</p>

<p>
Cadastre, consulte, pesquise e acompanhe as informações
da sua coleção de maneira moderna e profissional.
</p>

</div>
""",
            unsafe_allow_html=True
        )

    with coluna2:

        st.image(
            IMAGEM_COLECAO,
            use_container_width=True
        )

# =========================================================
# CADASTRAR PERFUME
# =========================================================

elif menu == "➕ Cadastrar Perfume":

    st.markdown(
"""
<div class="page-title">
➕ Novo perfume
</div>

<div class="page-subtitle">
Adicione um novo perfume à sua coleção.
</div>
""",
        unsafe_allow_html=True
    )

    with st.form(
        "cadastro_perfume",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(2)

        with col1:

            marca = st.text_input(
                "🏷️ Marca"
            )

            perfume = st.text_input(
                "🌸 Nome do Perfume"
            )

            ano = st.number_input(
                "📅 Ano de lançamento",
                min_value=1900,
                max_value=2035,
                value=2024,
                step=1
            )

            fragrancia = st.selectbox(
                "🌿 Família Olfativa",
                [
                    "Floral",
                    "Cítrica",
                    "Amadeirada",
                    "Oriental",
                    "Aromática",
                    "Frutal",
                    "Gourmand",
                    "Chipre",
                    "Aquática",
                    "Outra"
                ]
            )

        with col2:

            volume = st.number_input(
                "🧴 Volume (ml)",
                min_value=1,
                value=100,
                step=5
            )

            concentracao = st.selectbox(
                "💧 Concentração",
                [
                    "Parfum",
                    "Eau de Parfum",
                    "Eau de Toilette",
                    "Eau de Cologne",
                    "Body Splash",
                    "Outra"
                ]
            )

            preco = st.number_input(
                "💰 Preço do Perfume",
                min_value=0.0,
                value=0.0,
                step=10.0
            )

            observacoes = st.text_area(
                "📝 Observações"
            )

        cadastrar = st.form_submit_button(
            "💾 CADASTRAR PERFUME"
        )

    if cadastrar:

        if (
            marca.strip()
            and perfume.strip()
        ):

            novo_perfume = pd.DataFrame(
                [{
                    "Marca": marca.strip(),
                    "Perfume": perfume.strip(),
                    "Ano": int(ano),
                    "Fragrância": fragrancia,
                    "Volume": int(volume),
                    "Concentração": concentracao,
                    "Preço": float(preco),
                    "Observações": observacoes.strip()
                }]
            )

            df = pd.concat(
                [
                    df,
                    novo_perfume
                ],
                ignore_index=True
            )

            salvar_dados(df)

            st.success(
                "🌸 Perfume cadastrado com sucesso!"
            )

            st.rerun()

        else:

            st.warning(
                "⚠️ Preencha Marca e Nome do Perfume."
            )

# =========================================================
# PERFUMES CADASTRADOS
# =========================================================

elif menu == "🌸 Perfumes Cadastrados":

    st.markdown(
"""
<div class="page-title">
🌸 Minha coleção
</div>

<div class="page-subtitle">
Consulte e pesquise todos os perfumes cadastrados.
</div>
""",
        unsafe_allow_html=True
    )

    if df.empty:

        st.markdown(
"""
<div class="dark-card">

<h2>
🌸 Nenhum perfume cadastrado
</h2>

<p>
Sua coleção ainda está vazia.
Cadastre seu primeiro perfume para começar.
</p>

</div>
""",
            unsafe_allow_html=True
        )

    else:

        busca = st.text_input(
            "🔎 Pesquisar perfume",
            placeholder="Digite marca, perfume, fragrância ou concentração..."
        )

        if busca:

            mascara = (
                df.astype(str)
                .apply(
                    lambda coluna:
                    coluna.str.contains(
                        busca,
                        case=False,
                        na=False
                    )
                )
                .any(axis=1)
            )

            df_filtrado = df[mascara]

        else:

            df_filtrado = df

        st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        opcoes_perfumes = df.index.tolist()

        perfume_excluir = st.selectbox(
            "🗑️ Selecione um perfume para excluir",
            options=opcoes_perfumes,
            format_func=lambda indice:
                f"{df.loc[indice, 'Marca']} "
                f"{df.loc[indice, 'Perfume']}"
        )

        if st.button(
            "🗑️ EXCLUIR PERFUME"
        ):

            df = df.drop(
                perfume_excluir
            )

            df = df.reset_index(
                drop=True
            )

            salvar_dados(df)

            st.success(
                "🌸 Perfume excluído com sucesso!"
            )

            st.rerun()

# =========================================================
# RODAPÉ
# =========================================================

st.markdown(
"""
<div class="footer">

🌸 AutoPerfume PRO<br>
Gestão inteligente de perfumes

</div>
""",
    unsafe_allow_html=True
)
```

 Essa versão já troca também a **estrutura dos dados do CSV**, então você terá um `perfumes.csv` com campos próprios para perfumes.
