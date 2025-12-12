from fastapi import FastAPI
from database import Base, engine
from routers import admin, usuario, categoria, producto, carrito, comentario, pedido, detalle_pedido, direccion_envio, visitas

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lindeza API", version="1.0")

app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(usuario.router, prefix="/usuario", tags=["Usuarios"])
app.include_router(categoria.router, prefix="/categoria", tags=["Categorias"])
app.include_router(producto.router, prefix="/producto", tags=["Productos"])
app.include_router(carrito.router, prefix="/carrito", tags=["Carrito"])
app.include_router(comentario.router, prefix="/comentario", tags=["Comentarios"])
app.include_router(pedido.router, prefix="/pedido", tags=["Pedidos"])
app.include_router(detalle_pedido.router, prefix="/detalle_pedido", tags=["DetallePedido"])
app.include_router(direccion_envio.router, prefix="/direccion_envio", tags=["DireccionesEnvio"])
app.include_router(visitas.router, prefix="/visitas", tags=["Visitas"])
