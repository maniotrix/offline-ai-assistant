from pathlib import Path

backend_dir = Path(__file__).parent.parent.absolute()
workspace_dir = backend_dir.parent
workspace_data_dir = workspace_dir / "data"

backend_data_dir = backend_dir / "data"
backend_generated_dir = backend_dir / "generated"
backend_models_dir = backend_dir / "models"
backend_inference_dir = backend_dir / "inference"
backend_migrations_dir = backend_dir / "migrations"
backend_config_dir = backend_dir / "config"
backend_database_dir = backend_dir / "database"
backend_tests_dir = backend_dir / "tests"
backend_utils_dir = backend_dir / "utils"
backend_api_dir = backend_dir / "api"
backend_services_dir = backend_dir / "services"
backend_domain_dir = backend_dir / "domain"



