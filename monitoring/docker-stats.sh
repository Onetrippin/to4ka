#!/bin/bash
STATS_FILE="/var/lib/node_exporter/docker.prom.new"

echo "# HELP docker_container_cpu_usage_seconds_total CPU usage %"
echo "# TYPE docker_container_cpu_usage_seconds_total gauge"
echo "# HELP docker_container_memory_usage_bytes Memory bytes"

docker stats --no-stream --no-trunc --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" | tail -n +2 | while read CONTAINER CPU MEM NET; do
  CONTAINER_NAME=$(echo $CONTAINER | sed 's/.*\/\(.*\)/\1/')
  CPU_PCT=$(echo $CPU | sed 's/%//')
  MEM_BYTES=$(echo $MEM | sed 's/[^0-9]*\([0-9.]*\).*/\1/ ; s/\./* 1000000/')
  echo "docker_container_cpu_usage_seconds_total{container=\"$CONTAINER_NAME\"} $CPU_PCT"
  echo "docker_container_memory_usage_bytes{container=\"$CONTAINER_NAME\"} $MEM_BYTES"
done > $STATS_FILE

mv $STATS_FILE /var/lib/node_exporter/docker.prom
