import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import random

st.set_page_config(
    page_title="Componentes conexas de un grafo",
    layout="wide"
)

if "grafo_generado" not in st.session_state:
    st.session_state.grafo_generado = False
    st.session_state.num_nodos = 6
    st.session_state.grafo = nx.Graph()
    st.session_state.posiciones = None
    st.session_state.aristas_manuales = []
    st.session_state.componentes = []
    st.session_state.analisis_realizado = False


def inicializar_grafo(n):
    st.session_state.num_nodos = n
    st.session_state.grafo = nx.Graph()
    st.session_state.grafo.add_nodes_from(range(n))
    st.session_state.componentes = []
    st.session_state.analisis_realizado = False


def generar_posiciones():
    st.session_state.posiciones = nx.spring_layout(
        st.session_state.grafo,
        seed=42,
        k=1.15
    )
    st.session_state.grafo_generado = True


def dfs(grafo, nodo_inicio, visitados):
    pila = [nodo_inicio]
    componente = []

    while pila:
        nodo_actual = pila.pop()

        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            componente.append(nodo_actual)

            vecinos = sorted(
                grafo.neighbors(nodo_actual),
                reverse=True
            )

            for vecino in vecinos:
                if vecino not in visitados:
                    pila.append(vecino)

    return componente


def encontrar_componentes(grafo):
    visitados = set()
    componentes = []

    for nodo in sorted(grafo.nodes()):
        if nodo not in visitados:
            componente = dfs(
                grafo,
                nodo,
                visitados
            )
            componentes.append(
                sorted(componente)
            )

    return componentes


def reiniciar():
    st.session_state.grafo_generado = False
    st.session_state.num_nodos = 6
    st.session_state.grafo = nx.Graph()
    st.session_state.posiciones = None
    st.session_state.aristas_manuales = []
    st.session_state.componentes = []
    st.session_state.analisis_realizado = False


st.title("Componentes conexas de un grafo")
st.markdown(
    "**Avance del 50 % — Matemática Computacional**  \n"
    "En esta primera versión se construye el grafo, se muestra "
    "su matriz de adyacencia y se ejecuta una versión básica "
    "del algoritmo DFS para identificar sus componentes conexas."
)

st.subheader("1. Construye el grafo")

with st.container(border=True):
    col_config, col_creacion = st.columns([1, 2])

    with col_config:
        n_nodos = st.number_input(
            "Número de nodos (4 a 12):",
            min_value=4,
            max_value=12,
            value=st.session_state.num_nodos
        )

        if n_nodos != st.session_state.num_nodos:
            st.session_state.num_nodos = n_nodos
            st.session_state.grafo_generado = False
            st.session_state.aristas_manuales = []
            st.session_state.componentes = []
            st.session_state.analisis_realizado = False

        modo = st.radio(
            "Modo de creación:",
            ["Aleatorio", "Manual"]
        )

    with col_creacion:
        if modo == "Aleatorio":
            st.info(
                "El programa crea las conexiones automáticamente. "
                "Cada posible arista tiene una probabilidad del 30 % "
                "de generarse."
            )

            if st.button(
                "🎲 Generar grafo aleatorio",
                type="primary",
                use_container_width=True
            ):
                inicializar_grafo(n_nodos)

                for i in range(n_nodos):
                    for j in range(i + 1, n_nodos):
                        if random.random() < 0.30:
                            st.session_state.grafo.add_edge(i, j)

                generar_posiciones()
                st.rerun()

        else:
            st.markdown("**Agrega las conexiones del grafo**")

            col_u, col_v, col_boton = st.columns([2, 2, 3])

            with col_u:
                u = st.selectbox(
                    "Nodo inicial",
                    range(n_nodos),
                    key="nodo_inicial"
                )

            with col_v:
                v = st.selectbox(
                    "Nodo final",
                    range(n_nodos),
                    key="nodo_final"
                )

            with col_boton:
                st.write("")

                if st.button(
                    "➕ Agregar conexión",
                    use_container_width=True
                ):
                    if u == v:
                        st.error(
                            "Un nodo no puede conectarse consigo mismo."
                        )
                    else:
                        arista = tuple(sorted((u, v)))

                        if arista not in st.session_state.aristas_manuales:
                            st.session_state.aristas_manuales.append(arista)
                            st.rerun()
                        else:
                            st.warning(
                                "Esa conexión ya fue agregada."
                            )

            if st.session_state.aristas_manuales:
                st.caption("Conexiones agregadas:")

                for indice, (nu, nv) in enumerate(
                    st.session_state.aristas_manuales
                ):
                    col_texto, col_eliminar = st.columns([5, 1])

                    col_texto.write(
                        f"Nodo {nu} — Nodo {nv}"
                    )

                    if col_eliminar.button(
                        "Eliminar",
                        key=f"eliminar_{indice}"
                    ):
                        st.session_state.aristas_manuales.pop(indice)
                        st.rerun()
            else:
                st.caption(
                    "Todavía no se han agregado conexiones."
                )

            if st.button(
                "🛠 Construir grafo",
                type="primary",
                use_container_width=True
            ):
                inicializar_grafo(n_nodos)

                for nu, nv in st.session_state.aristas_manuales:
                    st.session_state.grafo.add_edge(nu, nv)

                generar_posiciones()
                st.rerun()


if st.session_state.grafo_generado:
    st.markdown("---")
    st.subheader("2. Visualiza el grafo")

    col_grafo, col_datos = st.columns([3, 2])

    with col_grafo:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_facecolor("#ffffff")
        fig.patch.set_facecolor("#ffffff")
        ax.axis("off")

        nx.draw_networkx_edges(
            st.session_state.grafo,
            pos=st.session_state.posiciones,
            ax=ax,
            edge_color="#7f8c8d",
            width=2
        )

        nx.draw_networkx_nodes(
            st.session_state.grafo,
            pos=st.session_state.posiciones,
            ax=ax,
            node_color="#bdc3c7",
            node_size=850,
            edgecolors="#333333",
            linewidths=1.5
        )

        nx.draw_networkx_labels(
            st.session_state.grafo,
            pos=st.session_state.posiciones,
            ax=ax,
            font_size=12,
            font_weight="bold",
            font_color="black"
        )

        st.pyplot(fig)
        plt.close(fig)

    with col_datos:
        st.markdown("### Matriz de adyacencia")
        st.caption(
            "**1 = hay una conexión directa** | "
            "**0 = no hay una conexión directa**"
        )

        matriz = nx.to_numpy_array(
            st.session_state.grafo,
            dtype=int
        )

        nombres = [
            f"Nodo {i}"
            for i in range(st.session_state.num_nodos)
        ]

        df_matriz = pd.DataFrame(
            matriz,
            index=nombres,
            columns=nombres
        )

        st.dataframe(
            df_matriz,
            use_container_width=True
        )

        st.write(
            f"**Total de nodos:** "
            f"{st.session_state.num_nodos}"
        )

        st.write(
            f"**Total de aristas:** "
            f"{st.session_state.grafo.number_of_edges()}"
        )

    st.markdown("---")
    st.subheader("3. Identifica las componentes conexas")

    st.write(
        "En este avance, el algoritmo DFS se ejecuta de manera básica. "
        "El recorrido paso a paso y el resaltado visual de cada etapa "
        "se incorporarán en la versión final."
    )

    col_analizar, col_reiniciar = st.columns([2, 1])

    with col_analizar:
        if st.button(
            "▶ Ejecutar análisis DFS",
            type="primary",
            use_container_width=True
        ):
            st.session_state.componentes = encontrar_componentes(
                st.session_state.grafo
            )
            st.session_state.analisis_realizado = True
            st.rerun()

    with col_reiniciar:
        if st.button(
            "🔄 Nuevo grafo",
            use_container_width=True
        ):
            reiniciar()
            st.rerun()

    if st.session_state.analisis_realizado:
        cantidad = len(
            st.session_state.componentes
        )

        st.success(
            f"Se encontraron {cantidad} "
            f"componente(s) conexa(s)."
        )

        for indice, componente in enumerate(
            st.session_state.componentes,
            start=1
        ):
            st.write(
                f"**Componente {indice}:** "
                f"{componente}"
            )

        if cantidad == 1:
            st.info(
                "El grafo es conexo porque todos los nodos "
                "pertenecen a una sola componente."
            )
        else:
            st.info(
                f"El grafo no es conexo porque está dividido "
                f"en {cantidad} componentes."
            )

        st.caption(
            "Para la entrega final se añadirá la ejecución interactiva "
            "del DFS paso a paso, el seguimiento de nodos visitados y "
            "el resaltado visual de las componentes."
        )

else:
    st.info(
        "Configura la cantidad de nodos y genera un grafo "
        "para comenzar."
    )
