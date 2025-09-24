.PHONY: help up down build logs shell test test-api test-graph test-integration clean restart status health demo

# Default target
help:
	@echo "ECCR (Enterprise Cyber Competency Repository) - Make Commands"
	@echo "============================================================="
	@echo ""
	@echo "Docker Management:"
	@echo "  up              Start all services (Neo4j + Django API)"
	@echo "  down            Stop all services"
	@echo "  build           Rebuild and start services"
	@echo "  restart         Restart all services"
	@echo "  status          Show service status"
	@echo "  logs            Show logs from all services"
	@echo "  logs-api        Show Django API logs"
	@echo "  logs-neo4j      Show Neo4j logs"
	@echo ""
	@echo "Development:"
	@echo "  shell           Access Django shell in container"
	@echo "  shell-bash      Access bash shell in Django container"
	@echo "  migrate         Run Django migrations"
	@echo "  health          Check API and database health"
	@echo ""
	@echo "Testing:"
	@echo "  test            Run all tests"
	@echo "  test-api        Run competency API tests only"
	@echo "  test-graph      Run graph operations tests only"
	@echo "  test-integration Run integration tests only"
	@echo "  test-local      Run tests with local environment"
	@echo ""
	@echo "Demo & Utilities:"
	@echo "  demo            Run graph API demo script"
	@echo "  clean           Clean up Docker resources"
	@echo "  reset-db        Reset Neo4j database (WARNING: deletes all data)"
	@echo ""
	@echo "Local Development:"
	@echo "  dev-setup       Set up local development environment"
	@echo "  dev-run         Run Django locally (Neo4j in Docker)"
	@echo ""

# Docker Management
up:
	@echo "🚀 Starting ECCR services..."
	docker-compose up -d
	@echo "✅ Services started. API: http://localhost:8080/api/"
	@echo "   Neo4j Browser: http://localhost:7474"

down:
	@echo "🛑 Stopping ECCR services..."
	docker-compose down

build:
	@echo "🔨 Building and starting services..."
	docker-compose up -d --build
	@echo "✅ Build complete. API: http://localhost:8080/api/"

restart:
	@echo "🔄 Restarting ECCR services..."
	docker-compose restart
	@echo "✅ Services restarted."

status:
	@echo "📊 Service Status:"
	docker-compose ps

logs:
	docker-compose logs -f

logs-api:
	docker-compose logs -f eccr-backend

logs-neo4j:
	docker-compose logs -f neo4j

# Development Commands
shell:
	@echo "🐍 Opening Django shell..."
	docker-compose exec eccr-backend python manage.py shell

shell-bash:
	@echo "🐚 Opening bash shell in Django container..."
	docker-compose exec eccr-backend bash

migrate:
	@echo "🗄️  Running Django migrations..."
	docker-compose exec eccr-backend python manage.py migrate

health:
	@echo "🏥 Checking service health..."
	@echo "API Health:"
	@curl -s http://localhost:8080/api/health/ | python3 -m json.tool || echo "❌ API not responding"
	@echo ""
	@echo "Neo4j Status:"
	@docker-compose exec neo4j cypher-shell "RETURN 'Neo4j is healthy!' as status" 2>/dev/null || echo "❌ Neo4j not responding"

# Testing Commands
test:
	@echo "🧪 Running all tests..."
	cd app && NEO4J_BOLT_URI=bolt://localhost:7687 python manage.py test eccr.tests -v 2

test-api:
	@echo "🧪 Running competency API tests..."
	cd app && NEO4J_BOLT_URI=bolt://localhost:7687 python manage.py test eccr.tests.test_api -v 2

test-graph:
	@echo "🧪 Running graph operations tests..."
	cd app && NEO4J_BOLT_URI=bolt://localhost:7687 python manage.py test eccr.tests.test_graph_operations -v 2

test-integration:
	@echo "🧪 Running integration tests..."
	cd app && NEO4J_BOLT_URI=bolt://localhost:7687 python manage.py test eccr.tests.test_integration -v 2

test-local:
	@echo "🧪 Running tests with local Python environment..."
	@echo "Make sure to activate your virtual environment first!"
	cd app && python manage.py test eccr.tests -v 2

# Demo & Utilities
demo:
	@echo "🎬 Running graph API demo..."
	@echo "Make sure services are running: make up"
	NEO4J_BOLT_URI=bolt://localhost:7687 python demo_graph_api.py

clean:
	@echo "🧹 Cleaning up Docker resources..."
	docker-compose down -v --remove-orphans
	docker system prune -f
	@echo "✅ Cleanup complete."

reset-db:
	@echo "⚠️  WARNING: This will delete ALL Neo4j data!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	docker-compose stop neo4j
	docker-compose rm -f neo4j
	sudo rm -rf data/databases data/transactions
	docker-compose up -d neo4j
	@echo "🔄 Neo4j database reset complete."

# Local Development
dev-setup:
	@echo "🏗️  Setting up local development environment..."
	python3 -m venv eccr_env || echo "Virtual environment already exists"
	@echo "Activate with: source eccr_env/bin/activate"
	@echo "Install requirements: pip install -r requirements.txt"
	@echo "Start Neo4j: make up neo4j"

dev-run:
	@echo "🚀 Starting local development server..."
	@echo "Make sure Neo4j is running: docker-compose up -d neo4j"
	@echo "Make sure virtual environment is activated: source eccr_env/bin/activate"
	cd app && NEO4J_BOLT_URI=bolt://localhost:7687 python manage.py runserver

# Quick service targets
neo4j:
	@echo "🗄️  Starting Neo4j only..."
	docker-compose up -d neo4j
	@echo "✅ Neo4j started: http://localhost:7474"

api:
	@echo "🚀 Starting API only..."
	docker-compose up -d eccr-backend
	@echo "✅ API started: http://localhost:8080/api/"

# Development shortcuts
quick-test: up test-api

quick-demo: up demo

# Install target for make completion
install:
	@echo "No installation needed. Use 'make up' to start services."