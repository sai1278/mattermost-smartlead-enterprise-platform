import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 100 },   // Warmup to 100 users
    { duration: '1m',  target: 500 },   // Ramp up to 500 users
    { duration: '1m',  target: 1000 },  // Scale to 1000 users
    { duration: '2m',  target: 5000 },  // Stress load at 5000 users
    { duration: '30s', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200', 'p(99)<500'], // 95% < 200ms, 99% < 500ms
    http_req_failed: ['rate<0.01'],               // Error rate < 1%
  },
};

const BASE_URLS = {
  commandHandler: 'http://localhost:8000',
  smartleadSync: 'http://localhost:8001',
  botService: 'http://localhost:8002',
  analyticsService: 'http://localhost:8003',
  workflowEngine: 'http://localhost:8004',
};

export default function () {
  // 1. Slash Command
  let resCmd = http.get(`${BASE_URLS.commandHandler}/health`);
  check(resCmd, { 'Command Handler health OK': (r) => r.status === 200 });

  // 2. Webhook Ingest
  let payloadWebhook = JSON.stringify({
    event: 'warmup_stat',
    account_email: 'sales@enterprise.com',
    sent: 150,
    inbox: 145,
  });
  let params = { headers: { 'Content-Type': 'application/json' } };
  let resSync = http.post(`${BASE_URLS.smartleadSync}/webhook`, payloadWebhook, params);
  check(resSync, { 'Sync Webhook status 200/202': (r) => r.status === 200 || r.status === 202 });

  // 3. Analytics Metric Ingest
  let payloadAnalytics = JSON.stringify({
    account_email: 'sales@enterprise.com',
    total_sent: 150,
    total_inbox: 145,
    total_spam: 5,
  });
  let resAnalytics = http.post(`${BASE_URLS.analyticsService}/analytics/ingest`, payloadAnalytics, params);
  check(resAnalytics, { 'Analytics Ingest 200/201': (r) => r.status === 200 || r.status === 201 });

  // 4. Workflow Start
  let payloadWorkflow = JSON.stringify({
    campaign_id: 'camp-505',
    mailbox_count: 10,
    avg_inbox_rate: 96.67,
  });
  let resWorkflow = http.post(`${BASE_URLS.workflowEngine}/workflow/start`, payloadWorkflow, params);
  check(resWorkflow, { 'Workflow Start status 200/202': (r) => r.status === 200 || r.status === 202 });

  sleep(0.5);
}
