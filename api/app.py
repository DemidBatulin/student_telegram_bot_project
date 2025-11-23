import os

from flask import Flask, jsonify, request

from bot import db
from bot.config import BASE_DIR


def create_app() -> Flask:
    app = Flask(__name__)

    db.init_db()

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/students")
    def get_students():
        students = db.list_students()
        return jsonify(students)

    @app.post("/students")
    def add_student():
        payload = request.get_json(force=True, silent=True) or {}
        student_id = (payload.get("id") or "").strip()
        full_name = (payload.get("full_name") or "").strip()
        group_name = (payload.get("group_name") or "").strip()

        if not student_id or not full_name:
            return jsonify({"success": False, "error": "id and full_name are required"}), 400

        db.add_student(student_id, full_name, group_name)
        return jsonify({"success": True})

    @app.get("/bindings")
    def get_bindings():
        bindings = db.list_bindings()
        return jsonify(bindings)

    return app


if __name__ == "__main__":
    from dotenv import load_dotenv

    env_path = BASE_DIR / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", "8000"))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"

    app = create_app()
    print(f"[API] Starting Flask on {host}:{port} (debug={debug})...")
    app.run(host=host, port=port, debug=debug)
