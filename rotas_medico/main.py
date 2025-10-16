from flask import Flask, request, jsonify
from pydantic import BaseModel
import sqlalchemy
from sqlalchemy import create_engine, text
from datetime import datetime
import logging
from typing import Optional

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MySQL database connection
DB_HOST = "172.233.15.56"
DB_PORT = 3306
DB_USER = "prontu-ai"
DB_PASS = "tkt5a173Pg87Pq5r8Ncv6f2f"
DB_NAME = "prontu_ai"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    logger.info("Database connection successful")
except Exception as e:
    logger.error(f"Database connection failed: {str(e)}")
    raise ValueError(f"Database connection failed: {str(e)}")

# Pydantic models for request validation (mantido para validação)
class ConsultarRequest(BaseModel):
    telephone: Optional[str] = None
    data: Optional[str] = None

class ConsultarClientRequest(BaseModel):
    ids: Optional[str] = None
    data: Optional[str] = None

class LoginRequest(BaseModel):
    name: str
    email: str

@app.route("/test", methods=["GET"])
def test():
    logger.debug("Accessed /test route")
    return jsonify({"message": "Server is running"})

@app.route("/consultar", methods=["GET", "POST"])
def consultar():
    if request.method == "POST":
        data = request.get_json()
        telephone = data.get("telephone") if data else None
        data_param = data.get("data") if data else None
        logger.debug(f"POST /consultar: telephone={telephone}, data={data_param}")
    else:
        telephone = request.args.get("telephone")
        data_param = request.args.get("data")
        logger.debug(f"GET /consultar: telephone={telephone}, data={data_param}")

    if not telephone:
        logger.warning("Missing telephone parameter in /consultar")
        return jsonify({"detail": "Please provide a telephone number"}), 400

    try:
        query = "SELECT c.* FROM prontu_ai.consultas AS c JOIN prontu_ai.profissionais p ON c.profissional_id = p.id WHERE p.telefone = :telefone"
        params = {"telefone": telephone}

        if data_param:
            try:
                datetime.strptime(data_param, "%Y-%m-%d")
                query += " AND c.data = :data"
                params["data"] = data_param
            except ValueError:
                logger.warning(f"Invalid date format in /consultar: {data_param}")
                return jsonify({"detail": "Invalid date format. Use YYYY-MM-DD"}), 400

        with engine.connect() as connection:
            logger.debug(f"Executing query: {query} with params: {params}")
            result = connection.execute(text(query), params)
 
            rows = result.fetchall()
            columns = result.keys()
            results = [dict(zip(columns, row)) for row in rows]

        if not results:
            logger.info(f"No consultations found for telefone: {telephone}, data: {data_param}")
            return jsonify({"detail": "No consultations found for this telephone number and date (if provided)"}), 404

        logger.info(f"Found {len(results)} consultations for telefone: {telephone}, data: {data_param}")
        return jsonify({
            "message": "Data received",
            "telephone": telephone,
            "data": data_param,
            "results": results
        })

    except Exception as e:
        logger.error(f"Database query failed in /consultar: {str(e)}")
        return jsonify({"detail": f"Database query failed: {str(e)}"}), 500

@app.route("/consultar_client", methods=["GET", "POST"])
def consultar_client():
    if request.method == "POST":
        data = request.get_json()
        ids = data.get("ids") if data else None
        data_param = data.get("data") if data else None
        logger.debug(f"POST /consultar_client: ids={ids}, data={data_param}")
    else:
        ids = request.args.get("ids")
        data_param = request.args.get("data")
        logger.debug(f"GET /consultar_client: ids={ids}, data={data_param}")

    if not ids:
        logger.warning("Missing ids parameter in /consultar_client")
        return jsonify({"detail": "Please provide an ids parameter"}), 400

    try:
        ids = int(ids)
    except ValueError:
        logger.warning(f"Invalid ids format in /consultar_client: {ids}")
        return jsonify({"detail": "ids must be a valid integer"}), 400

    try:
        query = "SELECT c.* FROM prontu_ai.consultas AS c WHERE c.paciente_id = :ids"
        params = {"ids": ids}

        if data_param:
            try:
                datetime.strptime(data_param, "%Y-%m-%d")
                query += " AND c.data = :data"
                params["data"] = data_param
            except ValueError:
                logger.warning(f"Invalid date format in /consultar_client: {data_param}")
                return jsonify({"detail": "Invalid date format. Use YYYY-MM-DD"}), 400

        with engine.connect() as connection:
            logger.debug(f"Executing query: {query} with params: {params}")
            result = connection.execute(text(query), params)
            rows = result.fetchall()
            columns = result.keys()
            results = [dict(zip(columns, row)) for row in rows]

        if not results:
            logger.info(f"No consultations found for ids: {ids}, data: {data_param}")
            return jsonify({"detail": "No consultations found for this patient ID and date (if provided)"}), 404

        logger.info(f"Found {len(results)} consultations for ids: {ids}, data: {data_param}")
        return jsonify({
            "message": "Data received",
            "ids": ids,
            "data": data_param,
            "results": results
        })

    except Exception as e:
        logger.error(f"Database query failed in /consultar_client: {str(e)}")
        return jsonify({"detail": f"Database query failed: {str(e)}"}), 500

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"detail": "JSON body required"}), 400
        
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        logger.warning("Missing name or email in /login")
        return jsonify({"detail": "Name and email are required"}), 400

    try:
        query = "INSERT INTO users (name, email) VALUES (:name, :email)"
        with engine.connect() as connection:
            result = connection.execute(text(query), {"name": name, "email": email})
            connection.commit()
            inserted_id = result.lastrowid
            inserted_data = connection.execute(
                text("SELECT * FROM users WHERE id = :id"),
                {"id": inserted_id}
            ).fetchone()
            columns = inserted_data.keys()
            inserted_data = dict(zip(columns, inserted_data))

        logger.info(f"Inserted user: {name}, {email}")
        return jsonify({
            "message": "Data received and stored",
            "name": name,
            "email": email,
            "inserted_data": inserted_data
        })

    except Exception as e:
        logger.error(f"Database insert failed in /login: {str(e)}")
        return jsonify({"detail": f"Database insert failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)