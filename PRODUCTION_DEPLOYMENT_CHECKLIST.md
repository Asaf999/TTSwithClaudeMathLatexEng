# Production Deployment Checklist

## Pre-Deployment

### Code Preparation
- [x] Remove all development files and demos
- [x] Remove test outputs and reports
- [x] Clean up backup files
- [x] Remove development documentation
- [ ] Update version numbers in setup.py
- [ ] Tag release in git

### Security
- [x] Input validation implemented
- [x] LaTeX command blacklisting active
- [x] Resource limits configured
- [x] Time-based execution limits set
- [ ] API rate limiting configured
- [ ] HTTPS certificates ready
- [ ] Environment variables secured

### Testing
- [x] All unit tests passing
- [x] Integration tests passing
- [x] Security tests passing
- [x] Performance benchmarks met
- [ ] Load testing completed
- [ ] Penetration testing done

## Deployment Steps

### 1. Environment Setup
```bash
# Production environment variables
export MS_ENGINE=edge
export MS_CACHE_ENABLED=true
export MS_SECURITY_ENABLED=true
export MS_LOG_LEVEL=INFO
export MS_CACHE_DIR=/var/cache/mathspeak
export MS_LOG_DIR=/var/log/mathspeak
```

### 2. Docker Deployment
```bash
# Build production image
docker build -t mathspeak:prod -f Dockerfile .

# Test the image
docker run --rm -p 8000:8000 mathspeak:prod

# Push to registry
docker tag mathspeak:prod your-registry/mathspeak:latest
docker push your-registry/mathspeak:latest
```

### 3. Kubernetes Deployment
```bash
# Apply configurations
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Verify deployment
kubectl get pods -n mathspeak
kubectl logs -n mathspeak deployment/mathspeak
```

### 4. Database/Cache Setup
```bash
# Redis for distributed caching
kubectl apply -f k8s/redis-deployment.yaml

# Persistent volume for cache
kubectl apply -f k8s/pvc.yaml
```

### 5. Monitoring Setup
```bash
# Prometheus metrics
kubectl apply -f k8s/prometheus-servicemonitor.yaml

# Grafana dashboards
kubectl apply -f k8s/grafana-dashboard.yaml

# Alerts
kubectl apply -f k8s/alerting-rules.yaml
```

## Post-Deployment

### Verification
- [ ] API endpoints responding
- [ ] Audio generation working
- [ ] Caching functioning
- [ ] Security rules enforced
- [ ] Monitoring active
- [ ] Logs collecting

### Performance Tuning
```bash
# Cache warming
ms --warm-cache /app/common_expressions.txt

# Connection pool optimization
export MS_CONNECTION_POOL_SIZE=20

# Worker scaling
kubectl scale deployment/mathspeak --replicas=3
```

### Backup Configuration
```bash
# Cache backup
kubectl exec -n mathspeak deployment/mathspeak -- \
  python -m mathspeak.utils.backup_cache

# Configuration backup
kubectl get configmap -n mathspeak -o yaml > backup/configmaps.yaml
```

## Production Configuration

### nginx.conf (already configured)
- Rate limiting: 10 req/s per IP
- Burst handling: 20 requests
- Proxy timeouts: 300s
- Gzip compression enabled

### Resource Limits
```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

### Auto-scaling
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: mathspeak-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: mathspeak
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Monitoring Checklist

### Metrics to Monitor
- [ ] API response times
- [ ] Cache hit rate
- [ ] Error rate
- [ ] CPU usage
- [ ] Memory usage
- [ ] Concurrent connections
- [ ] TTS generation time

### Alerts to Configure
- [ ] High error rate (>1%)
- [ ] Slow response time (>100ms p95)
- [ ] Low cache hit rate (<30%)
- [ ] High memory usage (>80%)
- [ ] Pod restarts
- [ ] TTS engine failures

## Rollback Plan

### Quick Rollback
```bash
# Kubernetes rollback
kubectl rollout undo deployment/mathspeak -n mathspeak

# Docker rollback
docker-compose down
docker-compose up -d --scale mathspeak=3
```

### Data Recovery
```bash
# Restore cache from backup
kubectl cp backup/cache.db mathspeak-pod:/app/cache/

# Restore configuration
kubectl apply -f backup/configmaps.yaml
```

## Security Hardening

### Network Policies
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: mathspeak-netpol
spec:
  podSelector:
    matchLabels:
      app: mathspeak
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: nginx
    ports:
    - protocol: TCP
      port: 8000
```

### Pod Security Policy
```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: mathspeak-psp
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'persistentVolumeClaim'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
```

## Final Checks

- [ ] Documentation updated
- [ ] README reflects production setup
- [ ] API keys rotated
- [ ] Backup procedures tested
- [ ] Disaster recovery plan documented
- [ ] Team trained on operations
- [ ] Support channels configured
- [ ] SLAs defined

## Support Contacts

- **On-call Engineer**: [Phone/Email]
- **DevOps Team**: [Slack Channel]
- **Security Team**: [Email]
- **Product Owner**: [Email]

---

**Deployment Date**: ___________  
**Deployed By**: ___________  
**Version**: 1.0.0