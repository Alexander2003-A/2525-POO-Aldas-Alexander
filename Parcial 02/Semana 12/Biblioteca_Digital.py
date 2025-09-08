# ==========================================
# SISTEMA DE GESTIÓN DE BIBLIOTECA DIGITAL
# ==========================================

from typing import List, Dict, Optional


class Libro:
    """
    Representa un libro con:
    - autor_titulo: tupla (autor, titulo) -> inmutable por diseño
    - categoria: str
    - isbn: str (clave única en la biblioteca)
    """
    def __init__(self, titulo: str, autor: str, categoria: str, isbn: str):
        self.autor_titulo = (autor, titulo)  # tupla (autor, titulo)
        self.categoria = categoria
        self.isbn = isbn

    @property
    def titulo(self) -> str:
        return self.autor_titulo[1]

    @property
    def autor(self) -> str:
        return self.autor_titulo[0]

    def __repr__(self):
        return f"Libro(ISBN={self.isbn}, '{self.titulo}' - {self.autor}, {self.categoria})"


class Usuario:
    """
    Representa un usuario de la biblioteca:
    - id_usuario: único
    - nombre
    - prestados: lista de ISBN actuales
    """
    def __init__(self, nombre: str, id_usuario: str):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.prestados: List[str] = []

    def __repr__(self):
        return f"Usuario(id={self.id_usuario}, nombre={self.nombre}, prestados={self.prestados})"


class Biblioteca:
    """
    Gestiona libros, usuarios y préstamos.
    Estructuras:
    - libros: {isbn: Libro}
    - usuarios: {id_usuario: Usuario}
    - prestamos: {isbn: id_usuario}
    - ids_usuarios: set() -> unicidad de usuarios
    - historial: lista de tuplas (accion, isbn, id_usuario) para trazabilidad
    """
    def __init__(self):
        self.libros: Dict[str, Libro] = {}
        self.usuarios: Dict[str, Usuario] = {}
        self.prestamos: Dict[str, str] = {}
        self.ids_usuarios = set()
        self.historial: List[tuple] = []

    # ---------- USUARIOS ----------
    def registrar_usuario(self, nombre: str, id_usuario: str) -> bool:
        if id_usuario in self.ids_usuarios:
            return False
        self.ids_usuarios.add(id_usuario)
        self.usuarios[id_usuario] = Usuario(nombre, id_usuario)
        self.historial.append(("ALTA_USUARIO", "-", id_usuario))
        return True

    def dar_baja_usuario(self, id_usuario: str) -> bool:
        user = self.usuarios.get(id_usuario)
        if not user:
            return False
        if user.prestados:
            # No se puede dar de baja con libros pendientes
            return False
        self.ids_usuarios.discard(id_usuario)
        del self.usuarios[id_usuario]
        self.historial.append(("BAJA_USUARIO", "-", id_usuario))
        return True

    # ---------- LIBROS ----------
    def anadir_libro(self, libro: Libro) -> bool:
        if libro.isbn in self.libros:
            return False
        self.libros[libro.isbn] = libro
        self.historial.append(("ALTA_LIBRO", libro.isbn, "-"))
        return True

    def quitar_libro(self, isbn: str) -> bool:
        if isbn in self.prestamos:  # está prestado
            return False
        if isbn not in self.libros:
            return False
        del self.libros[isbn]
        self.historial.append(("BAJA_LIBRO", isbn, "-"))
        return True

    # ---------- PRÉSTAMOS ----------
    def prestar_libro(self, isbn: str, id_usuario: str) -> bool:
        if isbn not in self.libros or id_usuario not in self.usuarios:
            return False
        if isbn in self.prestamos:
            return False  # ya prestado
        self.prestamos[isbn] = id_usuario
        self.usuarios[id_usuario].prestados.append(isbn)
        self.historial.append(("PRESTAR", isbn, id_usuario))
        return True

    def devolver_libro(self, isbn: str, id_usuario: str) -> bool:
        if self.prestamos.get(isbn) != id_usuario:
            return False
        self.prestamos.pop(isbn, None)
        user = self.usuarios[id_usuario]
        if isbn in user.prestados:
            user.prestados.remove(isbn)
        self.historial.append(("DEVOLVER", isbn, id_usuario))
        return True

    # ---------- BÚSQUEDAS ----------
    def buscar(
        self,
        titulo: Optional[str] = None,
        autor: Optional[str] = None,
        categoria: Optional[str] = None
    ) -> List[Libro]:
        """
        Retorna lista de libros que coincidan con cualquier filtro provisto.
        Coincidencia por 'contiene' e insensible a mayúsculas.
        """
        res = []
        t = titulo.lower() if titulo else None
        a = autor.lower() if autor else None
        c = categoria.lower() if categoria else None

        for libro in self.libros.values():
            ok = True
            if t and t not in libro.titulo.lower():
                ok = False
            if a and a not in libro.autor.lower():
                ok = False
            if c and c not in libro.categoria.lower():
                ok = False
            if (t or a or c) and ok:
                res.append(libro)
        return res

    # ---------- LISTADOS ----------
    def listar_prestados_usuario(self, id_usuario: str) -> List[Libro]:
        user = self.usuarios.get(id_usuario)
        if not user:
            return []
        return [self.libros[isbn] for isbn in user.prestados if isbn in self.libros]

    def listar_prestados(self) -> List[tuple]:
        """
        Lista global de préstamos (isbn, id_usuario, titulo).
        """
        salida = []
        for isbn, uid in self.prestamos.items():
            titulo = self.libros[isbn].titulo if isbn in self.libros else "?"
            salida.append((isbn, uid, titulo))
        return salida


# --------- DEMO mínima para que "salga algo" al ejecutar ---------
if __name__ == "__main__":
    b = Biblioteca()

    # Usuarios (IDs únicos con set)
    b.registrar_usuario("Ana", "U001")
    b.registrar_usuario("Luis", "U002")

    # Libros (diccionario por ISBN)
    b.anadir_libro(Libro("El Quijote", "Cervantes", "Novela", "ISBN-001"))
    b.anadir_libro(Libro("Python fácil", "Guido", "Programación", "ISBN-002"))
    b.anadir_libro(Libro("Cien años de soledad", "García Márquez", "Realismo mágico", "ISBN-003"))

    # Buscar (título / autor / categoría)
    print("Buscar 'python':", b.buscar(titulo="python"))
    print("Buscar autor 'cerv':", b.buscar(autor="cerv"))
    print("Buscar categoría 'Novela':", b.buscar(categoria="novela"))

    # Prestar / Listar / Devolver
    print("Prestar ISBN-003 a U001:", b.prestar_libro("ISBN-003", "U001"))
    print("Prestados de U001:", b.listar_prestados_usuario("U001"))
    print("Prestados global:", b.listar_prestados())
    print("Devolver ISBN-003 de U001:", b.devolver_libro("ISBN-003", "U001"))
    print("Prestados global tras devolver:", b.listar_prestados())

    # Dar de baja usuario (solo si no debe libros)
    print("Baja U001 (sin deudas):", b.dar_baja_usuario("U001"))

    # Historial (opcional,
    print("\nHistorial:")
    for mov in b.historial:
        print(mov)

