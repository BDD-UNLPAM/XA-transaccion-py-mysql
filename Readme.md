# Flask XA Bank Transfer

Este proyecto implementa una **API REST con Flask** y renderizado de plantillas HTML que permite realizar **transferencias bancarias entre dos bancos** (Banco A y Banco B), cada uno con su propia base de datos MySQL independiente.  
El sistema utiliza **transacciones distribuidas XA (Two-Phase Commit)** para garantizar la consistencia entre ambos bancos.

---

## 🚀 Características principales

- API REST + interfaz web con Flask.
- Dos servidores MySQL separados (uno por banco).
- Transacciones distribuidas XA (`XA START`, `XA END`, `XA PREPARE`, `XA COMMIT` / `ROLLBACK`).
- Docker Compose para levantar toda la infraestructura.
- Scripts de inicialización con cuentas de ejemplo.
- Logs de transacciones y manejo de errores.
- Endpoint `/xa/status` para revisar transacciones XA preparadas.

---

## 🧱 Estructura del proyecto

```
flask_xa_bank_transfer_project/
├── app/
│   ├── main.py                # App Flask principal
│   ├── db.py                  # Conexión y manejo XA con ambos MySQL
│   ├── templates/
│   │   ├── index.html         # Formulario web de transferencias
│   │   └── result.html        # Página de resultado
│   ├── static/                # CSS/JS opcional
│   └── utils.py               # Funciones auxiliares
│
├── mysql-init/
│   ├── init_bank_a.sql        # Script inicial para Banco A
│   └── init_bank_b.sql        # Script inicial para Banco B
│
├── Dockerfile                 # Imagen Flask
├── docker-compose.yml         # Orquestación completa
├── requirements.txt           # Dependencias Python
└── README.md                  # Este archivo
```

---

## ⚙️ Requisitos

- Docker y Docker Compose instalados.
- Puerto `5000` disponible (para Flask).

---

## 🧩 Instalación y ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/<tu-usuario>/flask-xa-bank-transfer.git
   cd flask-xa-bank-transfer
   ```

2. **Levantar los contenedores:**
   ```bash
   docker compose up --build
   ```

3. **Acceder a la aplicación:**
   - Interfaz web: [http://localhost:5000](http://localhost:5000)
   - Endpoint API: `POST /transfer`

4. **Detener la aplicación:**
   ```bash
   docker compose down
   ```

---

## 🔁 Ejemplo de uso (API)

**Request:**
```bash
curl -X POST http://localhost:5000/transfer \
  -H 'Content-Type: application/json' \
  -d '{
    "from_account": 1,
    "to_account": 2,
    "amount": 100.0
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Transferencia completada correctamente"
}
```

---

## 🧪 Datos de ejemplo

| Banco | Cuenta | Titular  | Saldo inicial |
|--------|---------|----------|----------------|
| A | 1 | Juan Pérez | 1000.00 |
| B | 2 | María Gómez | 500.00 |

Podés transferir fondos entre estas cuentas mediante la interfaz web o la API.

---

## 🛠️ Variables de entorno (opcional)

Podés configurar credenciales personalizadas en un archivo `.env`:
```
MYSQL_A_USER=root
MYSQL_A_PASSWORD=rootpass
MYSQL_B_USER=root
MYSQL_B_PASSWORD=rootpass2
```

---

## 📘 Endpoints principales

| Método | Ruta | Descripción |
|--------|------|--------------|
| `GET` | `/` | Página principal con formulario de transferencia |
| `POST` | `/transfer` | Ejecuta la transferencia XA |
| `GET` | `/xa/status` | Lista las transacciones XA preparadas |

---

## 🧩 Tecnologías

- **Python 3.11**
- **Flask**
- **MySQL 8.0**
- **Docker & Docker Compose**

---

## 📄 Licencia

Este proyecto se distribuye bajo licencia MIT. Podés usarlo, modificarlo y redistribuirlo libremente.

---

## 👨‍💻 Autor

Desarrollado por [Tu Nombre](https://github.com/<tu-usuario>) — inspirado en prácticas de integridad transaccional distribuidas.

