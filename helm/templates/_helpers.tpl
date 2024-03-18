{{/*
  Expand the name of the chart.
  */}}
{{- define "wagtail.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "wagtail.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create a fully qualified wagtail name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "wagtail.wagtail.fullname" -}}
{{- if .Values.wagtail.fullnameOverride -}}
{{- .Values.wagtail.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- printf "%s-%s" .Release.Name .Values.wagtail.name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s-%s" .Release.Name $name .Values.wagtail.name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create a fully qualified memcached name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "wagtail.memcached.fullname" -}}
{{- if .Values.memcached.fullnameOverride -}}
{{- .Values.memcached.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- printf "%s-%s" .Release.Name .Values.memcached.name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s-%s" .Release.Name $name .Values.memcached.name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "wagtail.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "wagtail.labels" -}}
helm.sh/chart: {{ include "wagtail.chart" . }}
{{ include "wagtail.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "wagtail.selectorLabels" -}}
app.kubernetes.io/name: {{ include "wagtail.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "wagtail.serviceAccountName.wagtail" -}}
{{- if .Values.serviceAccounts.wagtail.create -}}
  {{ default (include "wagtail.wagtail.fullname" .) .Values.serviceAccounts.wagtail.name }}
{{- else -}}
  {{ default "default" .Values.serviceAccounts.wagtail.name }}
{{- end -}}
{{- end }}

{{- define "wagtail.serviceAccountName.celery" -}}
{{- if .Values.serviceAccounts.celery.create -}}
  {{ default (include "wagtail.celery.fullname" .) .Values.serviceAccounts.celery.name }}
{{- else -}}
  {{ default "default" .Values.serviceAccounts.celery.name }}
{{- end -}}
{{- end }}

{{- define "wagtail.serviceAccountName.memcached" -}}
{{- if .Values.serviceAccounts.memcached.create -}}
  {{ default (include "wagtail.memcached.fullname" .) .Values.serviceAccounts.memcached.name }}
{{- else -}}
  {{ default "default" .Values.serviceAccounts.memcached.name }}
{{- end -}}
{{- end }}
