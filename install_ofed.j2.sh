#!/bin/bash

set -eux
set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
{%- if params.OS == "RHEL" %}
this is for test
{%- else %}
this is for second test
{%- endif %}
