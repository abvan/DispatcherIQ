DataDog_sample_alert = {
  "ddsource": "azure.synapse",
  "event_type": "synapse_pipeline_failure",
  "alert_id": "9876543210",
  "alert_title": "[Synapse] Pipeline Failed: ingest_customer_data",
  "alert_status": "Alert",
  "alert_priority": "P2",
  "alert_query": "logs(\"Azure.Synapse.* PipelineFailed\").rollup(\"count\").by(\"pipeline_name\").last(\"5m\") > 0",
  "alert_transition": "Triggered",
  "tags": [
    "env:prod",
    "team:data-engineering",
    "service:synapse",
    "workspace:prod-synapse-ws",
    "pipeline:ingest_customer_data",
    "failure_type:activity_error"
  ],
  "date": 1733553000,
  "event": {
    "pipeline_name": "ingest_customer_data",
    "run_id": "4b8427f0-ef33-49b9-a199-8fa2d50bfb1e",
    "workspace_name": "prod-synapse-ws",
    "data_factory": "synapse-managed-factory",
    "status": "Failed",
    "error": {
      "code": "DFExecutorUserError",
      "message": "Copy activity 'CopyCustomersToSQL' failed due to SQL pool timeout.",
      "details": "The dedicated SQL pool did not respond within the configured timeout.",
      "failure_type": "UserError",
      "error_time": "2025-02-07T10:43:27Z"
    },
    "activity": {
      "name": "CopyCustomersToSQL",
      "type": "Copy",
      "start_time": "2025-02-07T10:42:10Z",
      "end_time": "2025-02-07T10:43:27Z",
      "duration_in_ms": 77000
    },
    "pipeline_parameters": {
      "source_container": "customer-landing",
      "target_table": "dbo.Customers"
    }
  },
  "host": "azure-synapse",
  "message": "Synapse Pipeline **ingest_customer_data** has failed in workspace **prod-synapse-ws**. \nError: SQL pool timeout in activity CopyCustomersToSQL."
}
