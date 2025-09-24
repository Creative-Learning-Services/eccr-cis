# ECCR Makefile

This Makefile provides convenient commands for managing the ECCR (Enterprise Cyber Competency Repository) system.

## Quick Reference

```bash
make help           # Show all available commands
make up             # Start all services
make down           # Stop all services
make test           # Run all tests
make health         # Check service health
make clean          # Clean up Docker resources
```

## Command Categories

### Docker Management

- `make up` - Start all services (Neo4j + Django API)
- `make down` - Stop all services
- `make build` - Rebuild and start services
- `make restart` - Restart all services
- `make status` - Show service status
- `make logs` - Show logs from all services

### Testing

- `make test` - Run all tests
- `make test-api` - Run competency API tests only
- `make test-graph` - Run graph operations tests only
- `make test-integration` - Run integration tests only

### Development

- `make shell` - Access Django shell in container
- `make health` - Check API and database health
- `make demo` - Run graph API demo script

### Utilities

- `make clean` - Clean up Docker resources
- `make reset-db` - Reset Neo4j database (WARNING: deletes all data)

## Prerequisites

- Docker and Docker Compose installed
- Make utility (available by default on macOS and Linux)
- Python 3.x for local development commands

## Usage Examples

```bash
# Start development environment
make up

# Check everything is working
make health

# Run tests to verify functionality
make test

# View API logs if something goes wrong
make logs-api

# Clean up when done
make down
```

For more details, see the main README.md file.
