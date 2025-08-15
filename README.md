# Football Score Prediction Service

A machine learning-powered football score prediction service built with FastAPI, deployed on Kubernetes.

## Features

- 🤖 ML-powered score predictions using XGBoost
- 📊 Real-time team performance analytics
- 🌐 REST API for predictions
- 💻 Modern web interface
- 🚀 Kubernetes-ready deployment
- 📈 Auto-scaling and monitoring
- 🔒 Secure configuration management

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │   ML Service    │
│   (React/HTML)  │────│   (FastAPI)     │────│   (XGBoost)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │   Data Layer    │
                       │ (PostgreSQL +   │
                       │     Redis)      │
                       └─────────────────┘
```

## Quick Start

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd football-prediction
```

2. Create environment file:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

3. Run with Docker Compose:
```bash
docker-compose up -d
```

4. Visit http://localhost:8000

### Kubernetes Deployment

1. Apply Kubernetes manifests:
```bash
kubectl apply -f k8s/
```

2. Update secrets:
```bash
kubectl create secret generic football-prediction-secrets \
  --from-literal=FOOTBALL_API_KEY=your_key \
  --from-literal=DATABASE_URL=your_db_url \
  -n football-prediction
```

3. Access via ingress: https://football.sonneypatel.com

## API Endpoints

### Predictions
- `POST /api/v1/predict` - Get match prediction
- `GET /api/v1/predictions/recent` - Recent predictions
- `GET /api/v1/model/performance` - Model metrics

### Data
- `GET /api/v1/teams` - Available teams
- `GET /api/v1/leagues` - Available leagues
- `GET /api/v1/matches` - Historical matches
- `POST /api/v1/data/refresh` - Refresh data

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `false` |
| `DATABASE_URL` | PostgreSQL connection | Required |
| `REDIS_URL` | Redis connection | Required |
| `FOOTBALL_API_KEY` | Football API key | Required |
| `MODEL_PATH` | ML model storage | `models/` |

### Data Sources

The service integrates with:
- [Football-Data.org API](https://www.football-data.org/) for match data
- Historical databases for training data
- Real-time feeds for live updates

## ML Pipeline

### Feature Engineering
- Team performance metrics
- Head-to-head statistics
- Recent form analysis
- Home/away advantage
- Seasonal patterns

### Model Training
- XGBoost for score prediction
- Feature importance analysis
- Cross-validation
- Automated retraining

### Prediction Process
1. Extract team features
2. Calculate match context
3. Generate score predictions
4. Compute win/draw/loss probabilities
5. Provide confidence metrics

## Development

### Project Structure
```
football-prediction/
├── app/
│   ├── core/           # Configuration
│   ├── data/           # Data access layer
│   ├── ml/             # ML models
│   ├── routers/        # API endpoints
│   ├── schemas/        # Pydantic models
│   └── services/       # Business logic
├── k8s/               # Kubernetes manifests
├── static/            # Frontend assets
├── templates/         # HTML templates
└── tests/            # Test suite
```

### Running Tests
```bash
pip install pytest pytest-asyncio pytest-cov
pytest tests/ -v --cov=app
```

### Code Quality
```bash
pip install black isort flake8
black app/
isort app/
flake8 app/
```

## Monitoring

### Health Checks
- `/health` - Service health status
- Kubernetes liveness/readiness probes
- Application metrics via Prometheus

### Logging
- Structured JSON logging
- Request/response tracing
- ML model performance tracking

## Security

- API key authentication for external services
- Kubernetes secrets for sensitive data
- HTTPS/TLS termination
- Input validation and sanitization
- Rate limiting

## Scaling

### Horizontal Scaling
- Kubernetes HPA based on CPU/memory
- Auto-scaling from 2-10 replicas
- Load balancing across instances

### Performance Optimization
- Redis caching for predictions
- Model result caching
- Database query optimization
- CDN for static assets

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

- [ ] Live score integration
- [ ] Multiple league support
- [ ] Advanced ML models (LSTM, Transformers)
- [ ] Mobile app
- [ ] Betting odds integration
- [ ] Social features and predictions sharing
- [ ] Real-time model updates

## Support

- 📧 Email: support@sonneypatel.com
- 🐛 Issues: GitHub Issues
- 📖 Documentation: [Wiki](wiki-url)

---

Built with ❤️ for football prediction enthusiasts

<!-- Test deployment trigger -->