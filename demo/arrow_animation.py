
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import FancyArrowPatch

# Curvas paramétricas (simples e suaves) que se cruzam
t = np.linspace(-2.5, 2.5, 120)

# 1) Arco "azulado" (parábola abrindo para cima)
x1 = t + 0.3*t**3*0      # praticamente linear em x (pode ajustar a forma)
y1 = 0.8*t**2 - 0.2

# 2) Arco "avermelhado" (parábola abrindo para baixo)
x2 = t
y2 = -0.8*t**2 + 0.2

# 3) Reta "esverdeada" (quase horizontal levemente inclinada)
x3 = t
y3 = 0.1*t - 0.02

# Figura
fig, ax = plt.subplots(figsize=(5,5))
# ax.set_aspect('equal', adjustable='box')
# ax.grid(True, alpha=0.25)

# Desenho das curvas com marcadores ocos (triângulos e losangos),
# sem especificar cores (deixa o padrão do Matplotlib).
# l1, = ax.plot(x1, y1, marker="^", markevery=8, fillstyle="none", linewidth=2)
l2, = ax.plot(x2, y2, marker="v", markevery=8, fillstyle="none", linewidth=2, color = 'k')
# l3, = ax.plot(x3, y3, marker="D", markevery=8, fillstyle="none", linewidth=2)

# Limites automáticos com margem
xmin = min(x1.min(), x2.min(), x3.min()) - 0.5
xmax = max(x1.max(), x2.max(), x3.max()) + 0.5
ymin = min(y1.min(), y2.min(), y3.min()) - 0.5
ymax = max(y1.max(), y2.max(), y3.max()) + 0.5
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.axis('off')
# ax.set_title("Três curvas com setas móveis")

# Funções de ajuda para tangente (derivada numérica) e seta local
def tangent(x, y, i, h=1):
    i0 = max(i-h, 0)
    i1 = min(i+h, len(x)-1)
    dx = x[i1] - x[i0]
    dy = y[i1] - y[i0]
    return dx, dy

def make_arrow(x, y, i, scale=0.12):
    dx, dy = tangent(x, y, i)
    # normaliza e reduz o tamanho para uma “seta de direção”
    n = (dx**2 + dy**2)**0.5
    if n == 0:
        n = 1.0
    ux, uy = dx/n, dy/n
    pA = (x[i] - scale*ux, y[i] - scale*uy)
    pB = (x[i] + scale*ux, y[i] + scale*uy)
    arr = FancyArrowPatch(pA, pB, arrowstyle="-|>", mutation_scale=14, linewidth=2)
    return arr

# Seta inicial em cada curva
idx0 = 0
# arrow1 = make_arrow(x1, y1, idx0)
arrow2 = make_arrow(x2, y2, idx0)
# arrow3 = make_arrow(x3, y3, idx0)
# ax.add_patch(arrow1)
# ax.add_patch(arrow2)
ax.add_patch(arrow2)

# Pontos móveis (opcionais) na ponta da seta
# pt1, = ax.plot([x1[idx0]], [y1[idx0]], marker="o")
pt2, = ax.plot([x2[idx0]], [y2[idx0]], marker="none")
# pt3, = ax.plot([x3[idx0]], [y3[idx0]], marker="o")

# Atualização da animação
N = len(t)

def update(frame):
    i = frame % N

    # Atualiza as setas recriando os patches (mais simples que mover)
    # arrow1.set_positions(
    #     (x1[max(i-1,0)], y1[max(i-1,0)]),
    #     (x1[min(i+1,N-1)], y1[min(i+1,N-1)])
    # )
    arrow2.set_positions(
        (x2[max(i-1,0)], y2[max(i-1,0)]),
        (x2[min(i+1,N-1)], y2[min(i+1,N-1)])
    )
    # arrow3.set_positions(
    #     (x3[max(i-1,0)], y3[max(i-1,0)]),
    #     (x3[min(i+1,N-1)], y3[min(i+1,N-1)])
    # )

    # Pontos móveis
    # pt1.set_data([x1[i]], [y1[i]])
    pt2.set_data([x2[i]], [y2[i]])
    # pt3.set_data([x3[i]], [y3[i]])

    return  arrow2,  pt2 #pt1, pt2,arrow1, arrow2,

ax.set_facecolor('none')

anim = FuncAnimation(fig, update, frames=N, interval=30, blit=True)

# Exporta GIF
gif_path = "curvas_setas_animado.gif"
anim.save(gif_path, writer=PillowWriter(fps=30), savefig_kwargs={"transparent": True})

gif_path
