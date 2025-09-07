# Simulação de Vigas 2D (Apoios Simples)

Projeto em **Python** para simular vigas 2D biapoiadas (pino/rolete), com **adição de cargas concentradas e distribuídas** via interface gráfica. O objetivo é oferecer um ambiente de estudo para **Resistência dos Materiais** e servir de base para evoluir em direção a cálculos de **reações de apoio, V(x) e M(x)**.

> **Status:** Em desenvolvimento (MVP funcional de UI + desenho). Cálculos estruturais ainda como _placeholders_.

---

## ✨ Funcionalidades (atual)
- Ajuste do **comprimento da viga** (m).
- **Cargas concentradas (POINT)**: magnitude (N), posição x (m), ângulo (°).
- **Cargas distribuídas (UDL)**: intensidade w (N/m) em [x1, x2].
- Canvas com **viga, apoios e setas** das cargas.
- Lista para **adicionar/remover** cargas.

---


## ▶️ Como executar
Na **raiz do projeto** (onde está `main.py`), rode:

```bash
python main.py
